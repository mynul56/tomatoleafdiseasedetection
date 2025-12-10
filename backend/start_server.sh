#!/bin/bash

echo "========================================="
echo "Tomato Leaf Backend - Quick Start"
echo "========================================="
echo ""

cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

echo "✅ Virtual environment found"

# Check if model exists
if [ ! -d "hf_model" ]; then
    echo "❌ Model directory not found!"
    exit 1
fi

echo "✅ Model directory found"

# Activate virtual environment and start server
echo ""
echo "Starting server on http://0.0.0.0:5005"
echo "Press Ctrl+C to stop"
echo ""

source venv/bin/activate
python app.py
