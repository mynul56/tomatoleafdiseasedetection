"""
Download Pre-trained Tomato Disease Model
Simplified version with multiple fallback options
"""

import os
import sys

print("=" * 70)
print("🍅 Pre-trained Model Setup")
print("=" * 70)
print()

# Check if model exists
if os.path.exists('tomato_resnet50_model.h5'):
    size_mb = os.path.getsize('tomato_resnet50_model.h5') / (1024 * 1024)
    print(f"✅ Model already exists!")
    print(f"   File: tomato_resnet50_model.h5")
    print(f"   Size: {size_mb:.2f} MB")
    print()
    
    # Verify it works
    try:
        import tensorflow as tf
        model = tf.keras.models.load_model('tomato_resnet50_model.h5', compile=False)
        print(f"✅ Model loads successfully")
        print(f"   Input: {model.input_shape}")
        print(f"   Output: {model.output_shape} ({model.output_shape[-1]} classes)")
        print()
        print("🚀 You're ready! Start the server with:")
        print("   python app.py")
        sys.exit(0)
    except Exception as e:
        print(f"⚠️  Model exists but won't load: {e}")
        print()

print("❌ No model found. Here are your options:")
print()

print("📥 OPTION 1: Download from Kaggle (EASIEST)")
print("=" * 70)
print()
print("1. Visit: https://www.kaggle.com/datasets/arshid/tomato-leaf-disease-detection")
print("   (You may need to create a free Kaggle account)")
print()
print("2. Click 'Download' button")
print()
print("3. After download, run:")
print("   mv ~/Downloads/archive.zip ./")
print("   unzip archive.zip")
print("   # Find the .h5 file and rename it:")
print("   mv path/to/model.h5 tomato_resnet50_model.h5")
print()

print("📥 OPTION 2: Use Kaggle CLI (AUTOMATED)")
print("=" * 70)
print()
print("1. Setup Kaggle credentials:")
print("   - Go to: https://www.kaggle.com/settings/account")
print("   - Create API token")
print("   - Download kaggle.json")
print()
print("2. Configure:")
print("   mkdir -p ~/.kaggle")
print("   mv ~/Downloads/kaggle.json ~/.kaggle/")
print("   chmod 600 ~/.kaggle/kaggle.json")
print()
print("3. Download:")
print("   kaggle datasets download -d arshid/tomato-leaf-disease-detection")
print("   unzip tomato-leaf-disease-detection.zip")
print()

print("📥 OPTION 3: Search GitHub (ALTERNATIVE)")
print("=" * 70)
print()
print("1. Search: https://github.com/search?q=tomato+disease+detection+h5&type=code")
print("2. Find a repository with trained .h5 model")
print("3. Download and rename to: tomato_resnet50_model.h5")
print()

print("📥 OPTION 4: Train Your Own (CUSTOM)")
print("=" * 70)
print()
print("python prepare_dataset.py --download")
print("python quick_train.py  # 30-60 min with GPU")
print()

print("=" * 70)
print()
print("💡 RECOMMENDED: Use Option 1 (Kaggle) - it's the easiest!")
print()
print("After downloading, run this script again to verify:")
print("   python get_model.py")
print()
