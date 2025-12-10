#!/bin/bash

# One-click demo script - starts server with or without model

echo "=========================================="
echo "🍅 Tomato Leaf - Quick Start Demo"
echo "=========================================="
echo ""

cd "$(dirname "$0")"

# Check if model exists
if [ -f "tomato_resnet50_model.h5" ]; then
    echo "✅ Model found!"
    echo "   Starting server with trained model..."
    echo ""
else
    echo "⚠️  No trained model found!"
    echo ""
    echo "Server will start but predictions will be INACCURATE."
    echo ""
    echo "For accurate predictions:"
    echo "  1. Read: GETTING_STARTED.md"
    echo "  2. Or run: bash setup_backend.sh"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Exiting. Run './setup_backend.sh' to get started properly."
        exit 1
    fi
fi

# Install dependencies if needed
if ! python -c "import flask" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -q -r requirements.txt
fi

echo "🚀 Starting Tomato Leaf API Server..."
echo ""
echo "Server will be available at:"
echo "  • Local: http://localhost:5005"
echo "  • Network: http://0.0.0.0:5005"
echo ""
echo "Endpoints:"
echo "  • Health: GET  /health"
echo "  • Predict: POST /predict"
echo ""
echo "Press Ctrl+C to stop"
echo "=========================================="
echo ""

python app.py
