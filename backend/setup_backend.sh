#!/bin/bash

# Automated Setup Script for Tomato Leaf Backend
# This script will get you up and running with accurate predictions

set -e

echo "=========================================="
echo "🍅 Tomato Leaf Backend Auto-Setup"
echo "=========================================="
echo ""

# Check if in backend directory
if [ ! -f "app.py" ]; then
    echo "❌ Please run this script from the backend/ directory"
    exit 1
fi

# Setup virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Check if model exists
if [ -f "tomato_resnet50_model.h5" ]; then
    echo "✅ Model found: tomato_resnet50_model.h5"
    MODEL_SIZE=$(du -h tomato_resnet50_model.h5 | cut -f1)
    echo "   Size: $MODEL_SIZE"
    echo ""
    echo "Skipping training - model already exists"
    echo ""
else
    echo "❌ No trained model found"
    echo ""
    echo "📋 You have 3 options for getting a trained model:"
    echo ""
    echo "Option 1: Download pre-trained model (FASTEST)"
    echo "   - Search Kaggle: https://www.kaggle.com/search?q=tomato+disease+h5"
    echo "   - Download .h5 file"
    echo "   - Rename to: tomato_resnet50_model.h5"
    echo "   - Place in backend/ folder"
    echo ""
    echo "Option 2: Auto-train with dataset (MOST ACCURATE)"
    echo "   - Run: python prepare_dataset.py --download"
    echo "   - Then: python quick_train.py (faster) or python train.py (better)"
    echo ""
    echo "Option 3: Use Google Colab (FREE GPU)"
    echo "   - Upload train.py to Colab"
    echo "   - Enable GPU"
    echo "   - Download trained model"
    echo ""
    
    read -p "Do you want to download the dataset now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📥 Downloading PlantVillage dataset..."
        python prepare_dataset.py --download
        
        read -p "Dataset downloaded. Train now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "🏋️  Starting quick training (this will take 30-60 minutes)..."
            python quick_train.py
        else
            echo "⏭️  Skipping training. Run manually:"
            echo "   python quick_train.py  (faster, 30-60 min)"
            echo "   python train.py        (better accuracy, 2-4 hours)"
        fi
    else
        echo "⏭️  Skipping dataset download"
        echo ""
        echo "⚠️  WARNING: Running without trained model!"
        echo "   Predictions will be inaccurate until you train a model"
    fi
fi

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""

# Test the server
if [ -f "tomato_resnet50_model.h5" ]; then
    echo "🧪 Testing model..."
    python -c "
import tensorflow as tf
from tensorflow import keras
model = keras.models.load_model('tomato_resnet50_model.h5')
print('✅ Model loads successfully')
print(f'   Input shape: {model.input_shape}')
print(f'   Output shape: {model.output_shape}')
" 2>/dev/null || echo "⚠️  Could not test model"
    echo ""
fi

echo "🚀 Next Steps:"
echo ""
echo "1. Start server locally:"
echo "   python app.py"
echo ""
echo "2. Test the API:"
echo "   curl http://localhost:5005/health"
echo ""
echo "3. Deploy to VPS:"
echo "   bash deploy_to_vps.sh"
echo ""
echo "4. Update Flutter app endpoint:"
echo "   http://206.162.244.175:5005"
echo ""
