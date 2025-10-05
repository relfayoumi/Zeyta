#!/usr/bin/env python3
"""
Resample all reference audio files to 48kHz (studio standard)
for optimal ChatterboxTTS quality
"""
import os
import torchaudio
from torchaudio.transforms import Resample

def resample_to_48k(input_dir, output_dir=None, target_sr=48000):
    """
    Resample all audio files in a directory to target sample rate.
    
    Args:
        input_dir: Directory containing reference audio files
        output_dir: Output directory (if None, overwrites originals)
        target_sr: Target sample rate (default 48000Hz)
    """
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    files = [f for f in os.listdir(input_dir) if f.endswith(('.wav', '.mp3', '.flac'))]
    
    print(f"🎵 Resampling {len(files)} files to {target_sr}Hz...")
    print(f"📁 Input: {input_dir}")
    if output_dir:
        print(f"📁 Output: {output_dir}")
    else:
        print(f"⚠️  WARNING: Will overwrite original files!")
    print()
    
    for filename in files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir or input_dir, filename)
        
        # Load audio
        waveform, sr = torchaudio.load(input_path)
        
        if sr == target_sr:
            print(f"✅ {filename}: Already {target_sr}Hz - skipping")
            continue
        
        # Resample
        print(f"🔄 {filename}: {sr}Hz → {target_sr}Hz")
        resampler = Resample(sr, target_sr)
        resampled = resampler(waveform)
        
        # Save
        torchaudio.save(output_path, resampled, target_sr)
        
        # Show file size change
        old_size = os.path.getsize(input_path) / 1024
        new_size = os.path.getsize(output_path) / 1024
        print(f"   Size: {old_size:.1f}KB → {new_size:.1f}KB")
    
    print(f"\n✅ Done! All files resampled to {target_sr}Hz")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Resample audio files to 48kHz")
    parser.add_argument("input_dir", help="Directory containing audio files")
    parser.add_argument("--output-dir", help="Output directory (overwrites if not specified)")
    parser.add_argument("--sample-rate", type=int, default=48000, 
                       help="Target sample rate (default: 48000)")
    
    args = parser.parse_args()
    
    resample_to_48k(args.input_dir, args.output_dir, args.sample_rate)
