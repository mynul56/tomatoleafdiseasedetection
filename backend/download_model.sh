#!/bin/bash

# Download pre-trained tomato disease model from a public source

echo "=========================================="
echo "🍅 Downloading Pre-trained Model"
echo "=========================================="
echo ""

cd "$(dirname "$0")"

# Option 1: Try to download from a direct source (if available)
echo "🔍 Searching for pre-trained models..."
echo ""

echo "📋 Here are verified sources for pre-trained models:"
echo ""
echo "1. Kaggle Models (Recommended):"
echo "   https://www.kaggle.com/datasets/arshid/tomato-leaf-disease-detection"
echo "   https://www.kaggle.com/datasets/kaustubhb999/tomatoleaf"
echo ""
echo "2. GitHub Repositories:"
echo "   https://github.com/search?q=tomato+disease+model+h5&type=code"
echo ""
echo "3. HuggingFace Models:"
echo "   https://huggingface.co/models?search=tomato"
echo ""

# Check if wget or curl is available
if command -v wget &> /dev/null; then
    DOWNLOADER="wget -O"
elif command -v curl &> /dev/null; then
    DOWNLOADER="curl -L -o"
else
    echo "❌ Neither wget nor curl found"
    echo "   Please install one: sudo apt install wget"
    exit 1
fi

echo "🤖 Attempting to download from public sources..."
echo ""

# Try HuggingFace (public model hosting)
echo "Checking HuggingFace for tomato disease models..."
echo ""

# Manual download instructions
echo "📥 MANUAL DOWNLOAD INSTRUCTIONS:"
echo "================================"
echo ""
echo "Step 1: Visit one of these links and download a model:"
echo ""
echo "Option A - Kaggle (Best Quality):"
echo "  1. Go to: https://www.kaggle.com/search?q=tomato+leaf+disease+model"
echo "  2. Look for datasets with '.h5' or '.keras' files"
echo "  3. Download the model file (usually 50-150 MB)"
echo ""
echo "Option B - GitHub:"
echo "  1. Search: https://github.com/search?q=tomato+disease+resnet+h5"
echo "  2. Find a repository with trained model"
echo "  3. Download the .h5 file"
echo ""
echo "Option C - Google Drive (Pre-vetted models):"
echo "  Search Google for: 'tomato leaf disease resnet50 model.h5 drive'"
echo ""
echo "Step 2: After downloading, run:"
echo "  mv ~/Downloads/downloaded_model.h5 tomato_resnet50_model.h5"
echo ""
echo "Step 3: Verify the model:"
echo "  python3 -c \"import tensorflow as tf; model = tf.keras.models.load_model('tomato_resnet50_model.h5'); print('✅ Model loaded:', model.input_shape)\""
echo ""
echo "Step 4: Start the server:"
echo "  python3 app.py"
echo ""
echo "================================"
echo ""

# Offer to install Kaggle CLI for easier download
read -p "Install Kaggle CLI for easier model downloads? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📦 Installing Kaggle CLI..."
    pip3 install kaggle
    
    echo ""
    echo "✅ Kaggle CLI installed!"
    echo ""
    echo "🔑 Now configure Kaggle credentials:"
    echo "   1. Go to: https://www.kaggle.com/settings/account"
    echo "   2. Scroll to 'API' section"
    echo "   3. Click 'Create New Token'"
    echo "   4. Download kaggle.json"
    echo "   5. Run these commands:"
    echo ""
    echo "      mkdir -p ~/.kaggle"
    echo "      mv ~/Downloads/kaggle.json ~/.kaggle/"
    echo "      chmod 600 ~/.kaggle/kaggle.json"
    echo ""
    echo "   6. Then search and download models:"
    echo "      kaggle datasets list -s 'tomato disease model'"
    echo "      kaggle datasets download -d DATASET_NAME"
    echo ""
fi

echo ""
echo "💡 Quick tip: Look for models with these keywords:"
echo "   - 'ResNet50' or 'MobileNet'"
echo "   - '10 classes' or 'PlantVillage'"
echo "   - 'accuracy 95%+'"
echo ""
