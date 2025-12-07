#!/bin/bash

# Quick Backend Start Script

echo "🍅 Starting Tomato Disease Detection Backend"
echo "==========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r backend_requirements.txt --user

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🚀 Starting backend server..."
echo ""

# Start the server
python3 test_backend.py
