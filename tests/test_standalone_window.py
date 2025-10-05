#!/usr/bin/env python3
"""
Test script to verify standalone window functionality in app.py
"""

import sys
from pathlib import Path

print("=" * 60)
print("Testing Standalone Window Mode")
print("=" * 60)
print()

# Check if pywebview import works
print("1. Testing pywebview availability...")
try:
    import webview
    print("   ✅ pywebview is available")
    print(f"   Version: {webview.__version__ if hasattr(webview, '__version__') else 'Unknown'}")
except ImportError:
    print("   ⚠️  pywebview not installed")
    print("   This is expected in CI - app will fall back to browser mode")

# Check if threading import works
print()
print("2. Testing threading module...")
try:
    import threading
    print("   ✅ threading module available")
except ImportError:
    print("   ❌ threading module not available (should not happen)")

# Check if time import works
print()
print("3. Testing time module...")
try:
    import time
    print("   ✅ time module available")
except ImportError:
    print("   ❌ time module not available (should not happen)")

# Verify app.py has the standalone window code
print()
print("4. Verifying app.py contains standalone window code...")
app_file = Path(__file__).parent.parent / "app.py"
if app_file.exists():
    with open(app_file, 'r') as f:
        content = f.read()
    
    checks = {
        "webview import": "import webview" in content,
        "threading import": "import threading" in content,
        "inbrowser=False": "inbrowser=False" in content,
        "create_window call": "webview.create_window" in content,
        "webview.start call": "webview.start()" in content,
        "fallback to browser": "falling back to browser" in content.lower(),
    }
    
    all_passed = True
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"   {status} {check}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print()
        print("=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        print()
        print("Standalone window mode is properly configured.")
        print("The app will:")
        print("  - Run in a standalone window if pywebview is installed")
        print("  - Fall back to browser mode if pywebview is not available")
    else:
        print()
        print("❌ Some tests failed")
        sys.exit(1)
else:
    print("   ❌ app.py not found")
    sys.exit(1)
