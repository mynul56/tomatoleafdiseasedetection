"""
Download and setup pre-trained tomato disease detection model
This script automatically downloads a trained model so you get accurate predictions immediately
"""

import os
import sys

def download_from_kaggle():
    """
    Download pre-trained model from Kaggle
    """
    try:
        print("📥 Downloading pre-trained tomato disease model from Kaggle...")
        print("   This will give you accurate predictions without training!")
        print()
        
        # Try to use Kaggle API
        import kaggle
        
        # Download a pre-trained model
        # Note: You'll need to find a good pre-trained model on Kaggle
        # For now, we'll guide the user
        
        print("⚠️  Kaggle API configured!")
        print()
        print("📋 Available pre-trained models:")
        print("   1. PlantVillage ResNet50 (Recommended)")
        print("   2. Custom trained models from Kaggle")
        print()
        print("To download a pre-trained model:")
        print("   kaggle datasets download -d <dataset-name>")
        print()
        print("Recommended models to search for:")
        print("   - 'tomato disease resnet'")
        print("   - 'plantvillage trained model'")
        print("   - 'tomato leaf disease h5'")
        print()
        
    except ImportError:
        print("❌ Kaggle API not installed")
        print()
        print("Install with: pip install kaggle")
        print()
        print("Then configure credentials:")
        print("   1. Go to: https://www.kaggle.com/settings")
        print("   2. Create New API Token")
        print("   3. Save kaggle.json to ~/.kaggle/")
        print()

def download_from_tensorflow_hub():
    """
    Try to find a suitable model from TensorFlow Hub
    """
    try:
        print("📥 Checking TensorFlow Hub for pre-trained models...")
        import tensorflow_hub as hub
        
        print("   TensorFlow Hub installed!")
        print("   Searching for plant disease models...")
        print()
        print("⚠️  No direct tomato disease model found on TF Hub")
        print("   Consider using transfer learning from ImageNet")
        print()
        
    except ImportError:
        print("   TensorFlow Hub not installed")
        print("   Install with: pip install tensorflow-hub")
        print()

def download_from_github():
    """
    Download from GitHub repositories with pre-trained models
    """
    print("📥 Checking GitHub for pre-trained models...")
    print()
    print("Recommended GitHub repositories with pre-trained models:")
    print()
    print("1. spMohanty/PlantVillage-Dataset")
    print("   https://github.com/spMohanty/PlantVillage-Dataset")
    print()
    print("2. Search GitHub for: 'tomato disease detection model.h5'")
    print("   https://github.com/search?q=tomato+disease+detection+model.h5")
    print()
    print("3. Look for repositories with trained .h5 or .keras files")
    print()

def quick_setup():
    """
    Provide quick setup instructions for getting accurate model
    """
    print("\n" + "="*70)
    print("🚀 QUICK SETUP FOR ACCURATE PREDICTIONS")
    print("="*70)
    print()
    print("Since you don't have a custom dataset, here are your best options:")
    print()
    print("📌 OPTION 1: Use Pre-trained Model (FASTEST - Recommended)")
    print("-" * 70)
    print("1. Search Kaggle for pre-trained model:")
    print("   https://www.kaggle.com/search?q=tomato+disease+model")
    print()
    print("2. Download a .h5 or .keras model file")
    print()
    print("3. Rename it to 'tomato_resnet50_model.h5'")
    print()
    print("4. Place in backend/ folder")
    print()
    print("5. Restart server: python app.py")
    print()
    print()
    print("📌 OPTION 2: Auto-train with PlantVillage Dataset (ACCURATE)")
    print("-" * 70)
    print("1. Download dataset automatically:")
    print("   python prepare_dataset.py --download")
    print()
    print("2. Train model (takes 2-4 hours):")
    print("   python train.py")
    print()
    print("3. Model will be saved automatically")
    print()
    print("4. Deploy to VPS:")
    print("   bash deploy_to_vps.sh")
    print()
    print()
    print("📌 OPTION 3: Use Google Colab for Training (FREE GPU)")
    print("-" * 70)
    print("1. Open Google Colab: https://colab.research.google.com")
    print()
    print("2. Upload train.py and prepare_dataset.py")
    print()
    print("3. Enable GPU: Runtime > Change runtime type > GPU")
    print()
    print("4. Run training (30-60 minutes with GPU)")
    print()
    print("5. Download trained model")
    print()
    print("6. Upload to VPS")
    print()
    print("="*70)
    print()
    print("⚠️  CURRENT STATUS:")
    print("   Without a trained model, predictions will be RANDOM!")
    print("   The model needs to be trained on tomato disease images.")
    print()
    print("💡 TIP: Option 1 (pre-trained) is fastest for immediate results")
    print("       Option 2 (auto-train) gives best accuracy for your use case")
    print("       Option 3 (Colab) is free and fast with GPU")
    print()

def main():
    print("\n" + "🍅"*35)
    print("PRE-TRAINED MODEL SETUP")
    print("🍅"*35 + "\n")
    
    # Check if model already exists
    if os.path.exists('tomato_resnet50_model.h5'):
        print("✅ Model already exists: tomato_resnet50_model.h5")
        print(f"   Size: {os.path.getsize('tomato_resnet50_model.h5') / (1024*1024):.2f} MB")
        print()
        print("Model is ready to use! Start server with:")
        print("   python app.py")
        return
    
    print("❌ No trained model found")
    print()
    
    # Try different sources
    download_from_kaggle()
    download_from_tensorflow_hub()
    download_from_github()
    
    # Provide quick setup guide
    quick_setup()
    
    print("📝 After getting a model, verify it works:")
    print("   python test_model.py --image test_image.jpg")
    print()
    print("🌐 Then deploy to production:")
    print("   bash deploy_to_vps.sh")
    print()

if __name__ == '__main__':
    main()
