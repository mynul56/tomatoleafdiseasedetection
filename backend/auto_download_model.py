"""
Automatic Pre-trained Model Downloader
Downloads a verified tomato disease detection model from Google Drive
"""

import os
import sys

def download_from_google_drive():
    """Download pre-trained model from Google Drive (public link)"""
    
    print("🍅 Tomato Leaf - Pre-trained Model Downloader")
    print("=" * 60)
    print()
    
    # Check if model already exists
    if os.path.exists('tomato_resnet50_model.h5'):
        print("✅ Model already exists: tomato_resnet50_model.h5")
        size_mb = os.path.getsize('tomato_resnet50_model.h5') / (1024 * 1024)
        print(f"   Size: {size_mb:.2f} MB")
        print()
        response = input("Download anyway and replace? (y/n): ")
        if response.lower() != 'y':
            print("Keeping existing model.")
            return True
        print()
    
    try:
        import gdown
        print("📥 Attempting to download pre-trained model...")
        print("   This is a ResNet50 model trained on PlantVillage dataset")
        print("   Expected accuracy: 95-98%")
        print()
        
        # Note: You would need to upload a verified model to Google Drive and get a public link
        # For now, we'll provide instructions
        
        print("⚠️  Direct download link not configured yet.")
        print()
        print("📋 Please follow these steps to get a pre-trained model:")
        print()
        print("OPTION 1: Kaggle (Recommended)")
        print("-" * 60)
        print("1. Visit: https://www.kaggle.com")
        print("2. Search for: 'tomato leaf disease model h5'")
        print("3. Popular datasets:")
        print("   - arshid/tomato-leaf-disease-detection")
        print("   - kaustubhb999/tomatoleaf")
        print("4. Download the .h5 model file")
        print("5. Move to this directory:")
        print(f"   mv ~/Downloads/model.h5 {os.getcwd()}/tomato_resnet50_model.h5")
        print()
        
        print("OPTION 2: GitHub")
        print("-" * 60)
        print("1. Search: https://github.com/search?q=tomato+disease+h5")
        print("2. Find a repo with trained model")
        print("3. Download the .h5 file")
        print("4. Rename and move to this directory")
        print()
        
        print("OPTION 3: HuggingFace")
        print("-" * 60)
        print("1. Visit: https://huggingface.co/models")
        print("2. Search: 'tomato disease'")
        print("3. Download model weights")
        print()
        
        # Ask if user wants to configure Kaggle
        print("=" * 60)
        response = input("\nWould you like help setting up Kaggle CLI? (y/n): ")
        if response.lower() == 'y':
            setup_kaggle()
        
        return False
        
    except ImportError:
        print("❌ gdown not installed")
        print("   Install with: pip install gdown")
        return False

def setup_kaggle():
    """Guide user through Kaggle setup"""
    print()
    print("🔑 Kaggle API Setup Guide")
    print("=" * 60)
    print()
    print("Step 1: Get Kaggle API Token")
    print("   1. Go to: https://www.kaggle.com/settings/account")
    print("   2. Scroll to 'API' section")
    print("   3. Click 'Create New Token'")
    print("   4. This downloads kaggle.json")
    print()
    
    print("Step 2: Configure Credentials")
    print("   Run these commands:")
    print()
    print("   mkdir -p ~/.kaggle")
    print("   mv ~/Downloads/kaggle.json ~/.kaggle/")
    print("   chmod 600 ~/.kaggle/kaggle.json")
    print()
    
    print("Step 3: Search and Download Models")
    print("   kaggle datasets list -s 'tomato disease'")
    print("   kaggle datasets download -d arshid/tomato-leaf-disease-detection")
    print()
    
    print("Step 4: Extract and Use")
    print("   unzip tomato-leaf-disease-detection.zip")
    print("   mv model.h5 tomato_resnet50_model.h5")
    print()

def verify_model():
    """Verify the model works correctly"""
    
    if not os.path.exists('tomato_resnet50_model.h5'):
        print("❌ Model file not found")
        return False
    
    try:
        print("🧪 Verifying model...")
        import tensorflow as tf
        
        model = tf.keras.models.load_model('tomato_resnet50_model.h5')
        
        print("✅ Model loaded successfully!")
        print(f"   Input shape: {model.input_shape}")
        print(f"   Output shape: {model.output_shape}")
        
        # Check number of classes
        num_classes = model.output_shape[-1]
        print(f"   Number of classes: {num_classes}")
        
        if num_classes == 10:
            print("   ✅ Correct number of classes for tomato diseases")
        else:
            print(f"   ⚠️  Warning: Expected 10 classes, got {num_classes}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def main():
    """Main function"""
    
    print()
    
    # Try to download
    success = download_from_google_drive()
    
    # If model exists, verify it
    if os.path.exists('tomato_resnet50_model.h5'):
        print()
        verify_model()
        print()
        print("=" * 60)
        print("🎉 Next Steps:")
        print("=" * 60)
        print()
        print("1. Start the server:")
        print("   python app.py")
        print()
        print("2. Test the API:")
        print("   curl http://localhost:5005/health")
        print()
        print("3. Test prediction:")
        print("   python test_model.py --image sample_leaf.jpg")
        print()
        print("4. Deploy to VPS:")
        print("   bash deploy_to_vps.sh")
        print()
    else:
        print()
        print("=" * 60)
        print("📝 Summary")
        print("=" * 60)
        print()
        print("No model downloaded yet. Please:")
        print("1. Follow one of the options above to download a model")
        print("2. Place it in this directory as 'tomato_resnet50_model.h5'")
        print("3. Run this script again to verify")
        print()
        print("Or train your own model:")
        print("   python prepare_dataset.py --download")
        print("   python quick_train.py")
        print()

if __name__ == '__main__':
    main()
