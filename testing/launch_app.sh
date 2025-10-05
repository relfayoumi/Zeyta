#!/bin/bash
# Quick launcher script for the Integrated Testing App

echo "🚀 Zeyta Integrated Testing App"
echo "================================"
echo ""
echo "Starting the testing interface..."
echo ""

cd "$(dirname "$0")"
python integrated_app.py

echo ""
echo "Goodbye! 👋"
