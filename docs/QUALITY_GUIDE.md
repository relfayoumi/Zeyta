# ChatterboxTTS Quality Improvement Guide

## 🎯 Quick Summary
**Best Setup**: 3-6 reference clips at 48kHz, 5-8 seconds each, varied emotions, WAV forma## 🎛️ ChatterboxTTS Parameters

### Temperature (Expressiveness) 🌡️
Controls how much variation and emotion in the voice.

```python
--temperature 0.5   # Very controlled, monotone, consistent
--temperature 0.7   # Balanced (DEFAULT, RECOMMENDED)
--temperature 0.9   # More expressive, emotional
--temperature 1.2   # Very expressive (may sound unstable)
```

**When to Adjust:**
- **Audiobooks/narration**: 0.5-0.7 (consistent, clear)
- **Conversational/natural**: 0.7-0.9 (balanced emotion)
- **Dramatic/emotional**: 0.9-1.1 (intense scenes)
- **Experimental/wild**: 1.2+ (unpredictable, creative)

**Effect**: Higher = more pitch variation, energy changes, emotional range

---

### Exaggeration 🎭
Controls how dramatically emotions are expressed.

```python
--exaggeration 0.5   # Subtle, understated emotions
--exaggeration 1.0   # Natural (DEFAULT)
--exaggeration 1.5   # More dramatic, theatrical
--exaggeration 2.0   # Very exaggerated, over-the-top
```

**When to Adjust:**
- **Professional/business**: 0.7-0.9 (controlled)
- **Conversational**: 1.0-1.2 (natural)
- **Character voices**: 1.3-1.7 (animated, distinct)
- **Comedy/parody**: 1.5-2.0 (exaggerated)

**Effect**: Higher = stronger emotional peaks, more vocal variety, pronounced inflections

**⚠️ Warning**: Too high (>2.0) can sound artificial or cartoonish

---

### CFG Weight (Classifier-Free Guidance) 🎯
Controls how closely the model follows your reference audio's characteristics.

```python
--cfg-weight 1.5    # Looser adherence, more creative
--cfg-weight 3.0    # Balanced (DEFAULT)
--cfg-weight 4.5    # Stronger adherence to reference
--cfg-weight 6.0    # Very strict cloning
```

**When to Adjust:**
- **Creative freedom**: 1.5-2.5 (model has more flexibility)
- **Balanced**: 3.0-3.5 (follows reference but natural)
- **Strict cloning**: 4.0-5.0 (very close to reference)
- **Extreme precision**: 5.5-7.0 (may sound robotic)

**Effect**: Higher = closer match to reference voice, less creative freedom

**� Tip**: Use higher values (4-5) when you want exact voice matching, lower (2-3) for more natural variation

---

### Pace (Speech Speed) ⚡
Controls how fast or slow the speech is.

```python
--pace 0.5    # Half speed (very slow)
--pace 0.8    # Slower than normal
--pace 1.0    # Normal speed (DEFAULT)
--pace 1.3    # Faster than normal
--pace 2.0    # Double speed (very fast)
```

**When to Adjust:**
- **Meditation/relaxation**: 0.6-0.8 (calm, slow)
- **Narration**: 0.9-1.1 (clear, measured)
- **Conversation**: 1.0-1.2 (natural)
- **Excited/urgent**: 1.3-1.6 (energetic)
- **Time-sensitive**: 1.5-2.0 (very fast, may lose clarity)

**Effect**: Lower = more pauses, clearer pronunciation; Higher = faster delivery, less pauses

**⚠️ Warning**: 
- Below 0.7 can sound unnatural/robotic
- Above 1.5 may lose clarity and natural rhythm

---

### Parameter Combinations (Presets)

#### 📖 **Audiobook Narrator**
```bash
--temperature 0.6 --exaggeration 0.8 --cfg-weight 4.0 --pace 0.95
```
- Controlled emotion, subtle expression
- Close to reference voice
- Slightly slower for clarity

#### 💬 **Natural Conversation**
```bash
--temperature 0.8 --exaggeration 1.1 --cfg-weight 3.0 --pace 1.1
```
- Good emotional range
- Natural exaggeration
- Balanced voice matching
- Slightly faster (conversational)

#### 🎭 **Dramatic Character**
```bash
--temperature 1.0 --exaggeration 1.5 --cfg-weight 2.5 --pace 1.0
```
- High expressiveness
- Theatrical emotion
- Creative freedom
- Normal pace with dramatic pauses

#### 😄 **Comedy/Energetic**
```bash
--temperature 1.1 --exaggeration 1.7 --cfg-weight 2.8 --pace 1.3
```
- Very expressive
- Exaggerated emotions
- Some creative freedom
- Faster, energetic delivery

#### 🧘 **Calm/Meditation**
```bash
--temperature 0.5 --exaggeration 0.6 --cfg-weight 3.5 --pace 0.75
```
- Minimal variation
- Subtle expression
- Consistent voice
- Slower, relaxing pace

#### 🎯 **Precise Voice Clone**
```bash
--temperature 0.7 --exaggeration 1.0 --cfg-weight 5.0 --pace 1.0
```
- Moderate expressiveness
- Natural exaggeration
- Strong reference adherence
- Exact reference pace

---

### Advanced Tuning Tips

**Finding Your Sweet Spot:**
1. Start with defaults: `--temperature 0.7 --exaggeration 1.0 --cfg-weight 3.0 --pace 1.0`
2. Adjust ONE parameter at a time
3. Generate, listen, compare
4. Iterate until satisfied

**Common Issues & Solutions:**

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| Sounds robotic | CFG too high, temp too low | Lower `--cfg-weight` to 2.5, raise `--temperature` to 0.9 |
| Too much variation | Temp/exag too high | Lower `--temperature` and `--exaggeration` |
| Doesn't match reference | CFG too low | Raise `--cfg-weight` to 4-5 |
| Too slow/boring | Pace too low, temp too low | Increase `--pace` to 1.2, `--temperature` to 0.8 |
| Too fast/unclear | Pace too high | Lower `--pace` to 0.9-1.0 |
| Over-the-top emotion | Exaggeration too high | Lower `--exaggeration` to 1.0-1.2 |
| Flat/monotone | Temp/exag too low | Raise both to 0.8-1.0 |

--- Sample Rate (Most Important!)

### ⭐ **48kHz - RECOMMENDED**
- **Why**: Studio standard, captures all human-audible frequencies (up to 20kHz)
- **Benefits**: 
  - Better sibilance (S, SH, T sounds)
  - Clearer breath sounds
  - More "air" and presence
  - Natural high-frequency detail
- **File size**: Moderate (2x larger than 24kHz, but worth it)

### ⚠️ 24kHz - Acceptable but Limited
- Only captures up to 12kHz
- Missing high-frequency detail (12-20kHz range)
- Sounds "muffled" or "dull" compared to 48kHz

### ❌ 96kHz - Overkill
- Files are 2x larger than 48kHz
- No audible benefit (exceeds human hearing)
- Wastes disk space and processing time

### ❌ 16kHz or Lower - Poor Quality
- Phone call quality
- Very limited frequency range
- Not recommended for voice cloning

---

## 🎙️ Reference Audio Best Practices

### Number of References
- **1 file**: ⭐⭐ Basic cloning (not recommended)
- **2 files**: ⭐⭐⭐ Good variety
- **3-4 files**: ⭐⭐⭐⭐ Very good (RECOMMENDED)
- **5-6 files**: ⭐⭐⭐⭐⭐ Excellent diversity
- **7+ files**: May have diminishing returns

### Duration per Clip
- **< 3s**: Too short, missing voice characteristics
- **3-8s**: ✅ **OPTIMAL** - enough data without bloat
- **10-15s**: Good but slower processing
- **20+ seconds**: Wasteful, split into multiple clips

### Total Combined Duration
- **15-30s**: ✅ **IDEAL** for most use cases
- **30-45s**: Very good for complex voices
- **45-60s**: Excellent but slower
- **> 60s**: Diminishing returns, very slow

---

## 🎭 Emotional Variety (Critical!)

### Mix Different Emotions
```
✅ GOOD MIX:
• angry_5s.wav (intense emotion)
• serious_9s.wav (neutral/focused)
• rejection_6s.wav (defensive/firm)
• happy_7s.wav (positive emotion)

❌ BAD MIX:
• neutral_20s.wav (single emotion, too long)
• calm_15s.wav (all similar tones)
```

### Why Variety Matters
- Each clip teaches the model different vocal characteristics
- Angry = vocal cord tension, intensity
- Serious = controlled tone, authority
- Happy = lighter voice, higher pitch inflections
- Sad = breathier, lower energy

### Recommended Mix
1. **1-2 intense clips** (angry, excited, scared)
2. **1-2 neutral clips** (serious, focused, explanatory)
3. **1-2 varied clips** (happy, sad, sarcastic)

---

## 🔊 Audio Codec & Format

### ✅ Best: WAV (PCM)
- **Pros**: Uncompressed, lossless, perfect quality
- **Cons**: Large file size
- **Use when**: Quality is priority

### ✅ Great: FLAC
- **Pros**: Lossless compression (smaller than WAV, same quality)
- **Cons**: Slightly slower to decode
- **Use when**: Storage space matters

### ❌ Avoid: MP3, AAC, OGG
- **Why**: Lossy compression introduces artifacts
- **Problem**: Model learns compression artifacts, not voice
- **Result**: Lower quality cloning

---

## 🎤 Recording Quality Tips

### Microphone
- **Best**: Condenser mic (Blue Yeti, AT2020, etc.)
- **Good**: Phone mic (iPhone/Android in quiet room)
- **Avoid**: Laptop built-in mics (too much noise)

### Environment
- ✅ **Quiet room** (no AC, fans, traffic)
- ✅ **Close to mic** (6-12 inches)
- ✅ **Consistent distance** across all clips
- ❌ Avoid echo-y rooms (bathrooms, empty spaces)
- ❌ No background music/TV

### Recording Settings
```
Sample Rate: 48000 Hz
Bit Depth: 16-bit (or 24-bit for mastering)
Channels: Mono or Stereo (both work)
Format: WAV (PCM)
```

### Audacity Settings (Free Software)
1. File → Export → Export Audio
2. Format: WAV (Microsoft) signed 16-bit PCM
3. Sample Rate: 48000 Hz

---

## 🎛️ Post-Processing (Optional)

### Basic Cleanup (Recommended)
1. **Normalize**: Bring peak to -3dB (prevents clipping)
2. **Noise Reduction**: Remove background hiss (gentle!)
3. **Trim Silence**: Remove dead air at start/end

### Advanced (Be Careful!)
- **EQ**: Only if you know what you're doing
- **Compression**: Can help even out volume
- **De-Esser**: Reduce harsh S sounds (use sparingly)
- ⚠️ **DON'T OVERDO IT** - natural is better than processed

### What NOT to Do
- ❌ Heavy compression (kills dynamics)
- ❌ Excessive noise reduction (robotic sound)
- ❌ Reverb or effects (model will clone them)
- ❌ Autotune (unnatural artifacts)

---

## 🔧 ChatterboxTTS Parameters

### Temperature (Expressiveness)
```python
--temperature 0.5   # Very controlled, monotone
--temperature 0.7   # Balanced (DEFAULT, RECOMMENDED)
--temperature 0.9   # More expressive, emotional
--temperature 1.2   # Very expressive (may sound unstable)
```

### When to Adjust
- **Audiobooks/narration**: 0.5-0.7
- **Conversational/natural**: 0.7-0.9
- **Dramatic/emotional**: 0.9-1.1
- **Experimental/wild**: 1.2+

---

## 📈 Upgrade Path (From Your Current Setup)

### Current Setup
```
✅ angry_5s.wav - 24kHz (good duration, good emotion)
✅ serious_9s.wav - 48kHz (excellent!)
✅ rejection_6s.wav - 24kHz (good duration, good emotion)
❌ neutral_20s.wav - Excluded (too long, single emotion)
```

### Recommended Improvements

#### 1. **Resample to 48kHz** (PRIORITY #1)
```powershell
python utils\resample_references.py IO\AudioRef --output-dir IO\AudioRef_48kHz
```
This will upgrade angry_5s.wav and rejection_6s.wav to 48kHz.

#### 2. **Add More Emotional Variety**
Record or find:
- **happy_6s.wav** (positive, upbeat tone)
- **sarcastic_7s.wav** (dry humor, dismissive)
- **concerned_5s.wav** (worried, softer)

#### 3. **Split neutral_20s.wav** (Optional)
If it has varied content:
```python
# Example: Split into 4x 5-second clips
# Use Audacity: Select 0-5s → File → Export Selected Audio
neutral_20s.wav → 
  serious_focused_5s.wav (0-5s)
  explaining_5s.wav (5-10s)
  thoughtful_5s.wav (10-15s)
  concluding_5s.wav (15-20s)
```

#### 4. **Target Setup** (5-6 clips, all 48kHz)
```
angry_5s.wav          - 48kHz, intense
serious_9s.wav        - 48kHz, focused
rejection_6s.wav      - 48kHz, defensive
happy_6s.wav          - 48kHz, positive
sarcastic_7s.wav      - 48kHz, dry humor
concerned_5s.wav      - 48kHz, soft

Total: 38 seconds, 6 clips, varied emotions
Rating: ⭐⭐⭐⭐⭐ EXCELLENT
```

---

## 🚀 Quick Quality Checklist

Before generating:
- [ ] All references are 48kHz WAV
- [ ] Each clip is 3-10 seconds
- [ ] Total duration is 15-40 seconds
- [ ] Mix of at least 3 different emotions
- [ ] No background noise
- [ ] Clean recordings (no music/effects)
- [ ] Consistent recording quality across all clips
- [ ] Using `--blend-voices --expressive` flags

---

## 🎯 Command Examples

### Basic (Good Quality)
```powershell
python testing\test_tts_clean.py --ref-dir IO\AudioRef --blend-voices
```

### Standard Expressive (Recommended)
```powershell
python testing\test_tts_clean.py --ref-dir IO\AudioRef --blend-voices --expressive
```

### High Quality with Custom Settings
```powershell
python testing\test_tts_clean.py --ref-dir IO\AudioRef --blend-voices --expressive --temperature 0.8 --exaggeration 1.2
```

### Maximum Expressiveness
```powershell
python testing\test_tts_clean.py --ref-dir IO\AudioRef --blend-voices --expressive --temperature 0.95 --exaggeration 1.5 --emotion-markup
```

### Precise Voice Clone
```powershell
python testing\test_tts_clean.py --ref-dir IO\AudioRef --blend-voices --expressive --cfg-weight 5.0 --exaggeration 0.9
```

### Fast & Energetic
```powershell
python testing\test_tts_clean.py --ref-dir IO\AudioRef --blend-voices --expressive --pace 1.3 --temperature 0.9 --exaggeration 1.3
```

### Slow & Dramatic
```powershell
python testing\test_tts_clean.py --ref-dir IO\AudioRef --blend-voices --expressive --pace 0.85 --temperature 1.0 --exaggeration 1.4
```

### Audiobook Quality
```powershell
python testing\test_tts_clean.py --ref-dir IO\AudioRef --blend-voices --expressive --temperature 0.6 --exaggeration 0.8 --cfg-weight 4.0 --pace 0.95
```

### Custom Text
```powershell
python testing\test_tts_clean.py --ref-dir IO\AudioRef --blend-voices --expressive --text "Your custom text here"
```

### All Parameters (Full Control)
```powershell
python testing\test_tts_clean.py --ref-dir IO\AudioRef --blend-voices --expressive --temperature 0.8 --exaggeration 1.2 --cfg-weight 3.5 --pace 1.1 --emotion-markup --text "Your text"
```

---

## 🔬 Testing & Comparison

### A/B Testing
1. Generate with current setup (save as `test_24khz.wav`)
2. Resample references to 48kHz
3. Generate again (save as `test_48khz.wav`)
4. Compare side-by-side

### What to Listen For
- **Clarity**: Are S, T, SH sounds crisp?
- **Presence**: Does it sound "close" or "distant"?
- **Natural**: Does emotion sound genuine?
- **Artifacts**: Any robotic or glitchy sounds?

---

## 💡 Pro Tips

1. **Consistency is Key**: Record all references in one session, same mic, same distance
2. **Natural Speech**: Don't "perform" - just talk naturally with emotion
3. **Avoid Scripts**: Improvise or speak naturally (sounds more genuine)
4. **Room Treatment**: Even a closet with clothes dampens echo
5. **Monitor Levels**: Peak around -6dB to -3dB (not maxed out)
6. **Save Originals**: Keep unprocessed versions as backup
7. **Batch Process**: Use `resample_references.py` for consistency

---

## 🆘 Troubleshooting

### "Output sounds robotic"
- ✅ Add more reference clips (need variety)
- ✅ Increase temperature (try 0.8-0.9)
- ✅ Check reference quality (no heavy processing)

### "Wrong emotion/tone"
- ✅ Add clips with desired emotion
- ✅ Remove clips with opposite emotion
- ✅ Try `--emotion-markup` flag

### "Sounds muffled"
- ✅ Upgrade to 48kHz references
- ✅ Check source audio quality
- ✅ Reduce noise reduction (if used)

### "Too slow to generate"
- ⚠️ Reduce total reference duration to 20-30s
- ⚠️ Use fewer reference files (4 instead of 6)
- ✅ Your GPU is working hard (this is normal)

---

## 📚 Additional Resources

### Free Audio Software
- **Audacity**: Recording, editing, format conversion
- **OBS Studio**: Screen recording with audio
- **VLC**: Audio playback and conversion

### Learning
- Research "audio sample rate" and "Nyquist theorem"
- Study professional voice acting techniques
- Listen to high-quality audiobooks for reference

---

**Last Updated**: Based on your current setup (3 files, mixed sample rates)
**Priority Action**: Resample all files to 48kHz for immediate quality boost! 🚀
