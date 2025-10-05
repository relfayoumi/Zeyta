import logging
from config import STT_MODEL_SIZE, STT_COMPUTE_TYPE

# Globals
stt_model = None
_torch = None
_sd = None
_WhisperModel = None


def initialize_stt():
    """Blocking load of faster-whisper model (no background threads, no silero)."""
    global stt_model, _torch, _WhisperModel
    if stt_model is not None:
        return
    try:
        import torch as torch_lib
        _torch = torch_lib  # retained if future GPU logic needed
        try:
            from faster_whisper import WhisperModel as _WM
        except ModuleNotFoundError:
            logging.error(
                "STT backend 'faster_whisper' is not installed. Install with: pip install faster-whisper"
            )
            stt_model = None
            return
        except Exception as e:
            logging.error(f"Unexpected error importing faster_whisper: {e}")
            stt_model = None
            return
        _WhisperModel = _WM
        try:
            stt_model = _WM(STT_MODEL_SIZE, device="auto", compute_type=STT_COMPUTE_TYPE)
        except Exception as e:
            logging.error(f"Failed to construct WhisperModel: {e}")
            stt_model = None
            return
    except Exception as e:
        # suppress verbose stack in runtime; concise message only
        logging.error(f"Failed to initialize STT models: {e}")
        stt_model = None


def listen_and_transcribe(timeout: float | None = None):
    """Listen and transcribe. Returns tuple (text, audio_array).

    `text` is lowercased transcript or empty string. `audio_array` is the
    concatenated numpy float32 waveform (or None on failure).

    Optional `timeout` (seconds) will stop listening after that period with no result.
    """
    global stt_model, _torch, _sd

    # Lazy import sounddevice and numpy to avoid startup hit
    if _sd is None:
        import sounddevice as sd
        _sd = sd
    import numpy as np
    if stt_model is None:
        initialize_stt()  # blocking (we load everything up front in main anyway)
        if stt_model is None:
            return ("", None)

    samplerate = 16000
    chunk_size = 512
    speaking = False
    # Use lists of frames to avoid repeated np.concatenate in the hot loop
    buffer_frames = []  # will store numpy arrays (float32)
    # Prebuffer to keep a short pre-roll so the first word isn't clipped.
    from collections import deque
    prebuffer = deque()
    prebuffer_samples = int(0.3 * samplerate)  # keep ~300ms
    prebuffer_total = 0

    try:
        import webrtcvad

        vad = webrtcvad.Vad(2)  # aggressiveness 0-3; 2 is moderate

        # webrtcvad requires frames of 10/20/30 ms. We'll use 20 ms frames.
        frame_ms = 20
        frame_size = int(samplerate * frame_ms / 1000)  # samples per frame

        # local bindings for speed
        local_stt_model = stt_model
        local_WhisperModel = _WhisperModel

        with _sd.InputStream(samplerate=samplerate, channels=1, dtype="float32") as stream:
            # Stay quiet until speech actually detected
            elapsed = 0.0
            # small state machine counters to avoid flip-flopping
            speech_frames = 0
            silence_frames = 0
            required_speech_frames = int(0.15 / (frame_ms / 1000.0))  # require 150ms of speech to start
            # require ~1.618 seconds of silence to end (golden ratio pause)
            required_silence_seconds = 1.618
            required_silence_frames = int(required_silence_seconds / (frame_ms / 1000.0))

            # accumulator for partial frames (use list for efficient appends)
            acc_list = []
            acc_len = 0

            while True:
                chunk, _ = stream.read(chunk_size)
                chunk = chunk.flatten()

                # Maintain prebuffer (store copies of raw chunks)
                prebuffer.append(chunk.copy())
                prebuffer_total += chunk.size
                while prebuffer_total > prebuffer_samples:
                    left = prebuffer.popleft()
                    prebuffer_total -= left.size

                # accumulate into acc_list until we have enough samples
                acc_list.append(chunk)
                acc_len += chunk.size
                # process full frames from the accumulated list
                while acc_len >= frame_size:
                    # build a frame by possibly slicing the first arrays
                    needed = frame_size
                    parts = []
                    while needed > 0:
                        part = acc_list.pop(0)
                        if part.size <= needed:
                            parts.append(part)
                            needed -= part.size
                        else:
                            parts.append(part[:needed])
                            # put back the remainder
                            acc_list.insert(0, part[needed:])
                            needed = 0
                    # recalc acc_len
                    acc_len -= frame_size

                    frame = np.concatenate(parts)

                    # convert float32 -1..1 to 16-bit PCM bytes
                    ints = (frame * 32767).astype('int16')
                    frame_bytes = ints.tobytes()

                    is_speech_frame = vad.is_speech(frame_bytes, sample_rate=samplerate)

                    if is_speech_frame:
                        speech_frames += 1
                        silence_frames = 0
                    else:
                        silence_frames += 1
                        speech_frames = 0

                    # Start speech once we have enough consecutive speech frames
                    if speech_frames >= required_speech_frames and not speaking:
                        speaking = True
                        # prepend prebuffer to the buffer to avoid cutting first word
                        if prebuffer_total > 0:
                            try:
                                pre_audio = np.concatenate(list(prebuffer))
                                buffer_frames.append(pre_audio)
                            except Exception:
                                pass
                            prebuffer.clear()
                            prebuffer_total = 0

                    if speaking:
                        # append this frame to buffer_frames (store numpy arrays)
                        buffer_frames.append(frame)

                    # If we've seen enough silence while speaking, end utterance
                    if speaking and silence_frames >= required_silence_frames:
                        # finalize and transcribe
                        total_samples = sum(f.size for f in buffer_frames)
                        if total_samples > int(0.3 * samplerate):
                            try:
                                # refresh local model references if needed
                                if local_stt_model is None and local_WhisperModel is not None:
                                    globals()['stt_model'] = local_WhisperModel(STT_MODEL_SIZE, device="cuda", compute_type=STT_COMPUTE_TYPE)
                                    local_stt_model = globals()['stt_model']
                                if globals().get('stt_model') is None:
                                    return ("", None)
                                audio = np.concatenate(buffer_frames)

                                # First attempt using Whisper's internal VAD filter (fast, removes non-speech)
                                try:
                                    segments, _ = globals()['stt_model'].transcribe(audio, beam_size=3, language="en", vad_filter=True)
                                    text = "".join(seg.text for seg in segments).strip()
                                except Exception:
                                    text = ""

                                # If the VAD-filtered result is empty (e.g. noisy background removed everything),
                                # retry without Whisper's VAD to give the model a chance to transcribe short/quiet speech.
                                if not text:
                                    try:
                                        segments, _ = globals()['stt_model'].transcribe(audio, beam_size=3, language="en", vad_filter=False)
                                        text = "".join(seg.text for seg in segments).strip()
                                    except Exception:
                                        text = ""

                                audio_out = audio
                                return (text.lower() if text else "", audio_out)
                            except Exception:
                                return ("", None)
                        # else treat as noise without logging
                        # reset state for next utterance
                        buffer_frames = []
                        speaking = False
                        speech_frames = 0
                        silence_frames = 0

                if timeout is not None:
                    elapsed += chunk_size / samplerate
                    if elapsed >= timeout:
                        return ("", None)

    except Exception:
        # Silent failure
        return ("", None)
    

