#!/usr/bin/env python3
"""
ChatterboxTTS Server Client - Example usage
"""

import requests
import json
import sys
from pathlib import Path

SERVER_URL = "http://localhost:5000"


def health_check():
    """Check if server is running"""
    try:
        response = requests.get(f"{SERVER_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server is healthy")
            print(f"   • Model loaded: {data['model_loaded']}")
            print(f"   • Device: {data['device']}")
            return True
        else:
            print(f"❌ Server returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Server not reachable: {e}")
        print(f"💡 Start server with: python testing/tts_server.py")
        return False


def get_stats():
    """Get server statistics"""
    try:
        response = requests.get(f"{SERVER_URL}/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"\n📊 Server Statistics:")
            print(f"   • Model cached: {data['model_cached']}")
            print(f"   • Model cache size: {data['model_cache_size_mb']} MB")
            print(f"   • Reference cache count: {data['reference_cache_count']}")
            print(f"   • Reference cache size: {data['reference_cache_size_mb']} MB")
            print(f"   • Device: {data['device']}")
            print(f"   • torch.compile available: {data['torch_compile_available']}")
            return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to get stats: {e}")
        return False


def generate_speech(text, reference_files=None, output_file="output.wav", **kwargs):
    """
    Generate speech from text
    
    Args:
        text: Text to synthesize
        reference_files: List of reference audio file paths (optional)
        output_file: Output filename
        **kwargs: Additional parameters (temperature, exaggeration, etc.)
    """
    print(f"\n🎙️  Generating speech...")
    print(f"📝 Text: {text[:50]}{'...' if len(text) > 50 else ''}")
    
    if reference_files:
        print(f"🎤 Using {len(reference_files)} reference file(s)")
    
    payload = {
        "text": text,
        **kwargs
    }
    
    if reference_files:
        payload["reference_files"] = reference_files
    
    try:
        response = requests.post(
            f"{SERVER_URL}/generate",
            json=payload,
            timeout=120  # 2 minutes timeout
        )
        
        if response.status_code == 200:
            # Save audio file
            with open(output_file, 'wb') as f:
                f.write(response.content)
            
            file_size = Path(output_file).stat().st_size / 1024  # KB
            print(f"✅ Generated: {output_file} ({file_size:.1f} KB)")
            return True
        else:
            error = response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
            print(f"❌ Error: {error}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False


def main():
    """Example usage"""
    print("=" * 60)
    print("🎙️  ChatterboxTTS Server Client")
    print("=" * 60)
    
    # Check server health
    if not health_check():
        sys.exit(1)
    
    # Get server stats
    get_stats()
    
    # Example 1: Default voice
    print("\n" + "=" * 60)
    print("Example 1: Default Voice")
    print("=" * 60)
    
    generate_speech(
        text="Hello! This is a test of the ChatterboxTTS server.",
        output_file="server_test_default.wav",
        temperature=0.8,
        exaggeration=0.5
    )
    
    # Example 2: With reference files
    print("\n" + "=" * 60)
    print("Example 2: Voice Cloning with Multi-Reference")
    print("=" * 60)
    
    # Check if reference files exist
    ref_dir = Path("IO/AudioRef_48kHz")
    if ref_dir.exists():
        ref_files = list(ref_dir.glob("*.wav"))
        
        if ref_files:
            # Use absolute paths
            ref_paths = [str(f.absolute()) for f in ref_files[:4]]  # Limit to 4
            
            generate_speech(
                text="You know what's funny? I used to think I had everything figured out. But life doesn't really work that way, does it?",
                reference_files=ref_paths,
                output_file="server_test_cloned.wav",
                temperature=0.75,
                exaggeration=0.65,
                cfg_weight=0.5
            )
        else:
            print("⚠️  No reference files found in IO/AudioRef_48kHz")
    else:
        print("⚠️  Reference directory not found: IO/AudioRef_48kHz")
    
    # Get stats again to see if caching worked
    print("\n" + "=" * 60)
    print("Final Statistics")
    print("=" * 60)
    get_stats()
    
    print("\n✅ All tests complete!")
    print(f"💡 Generated files: server_test_default.wav, server_test_cloned.wav")


if __name__ == "__main__":
    main()
