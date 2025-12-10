"""
Test the trained model with sample predictions
"""

import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras

MODEL_PATH = 'tomato_resnet50_model.h5'

CLASS_NAMES = [
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

def preprocess_image(image_path):
    """Preprocess image for prediction"""
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    img = img.resize((224, 224), Image.LANCZOS)
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    
    from tensorflow.keras.applications.resnet50 import preprocess_input
    img_array = preprocess_input(img_array)
    
    return img_array

def predict_image(model, image_path):
    """Make prediction on a single image"""
    img_array = preprocess_image(image_path)
    predictions = model.predict(img_array, verbose=0)
    
    predicted_idx = np.argmax(predictions[0])
    confidence = predictions[0][predicted_idx]
    predicted_class = CLASS_NAMES[predicted_idx]
    
    # Get top 3 predictions
    top_3_idx = np.argsort(predictions[0])[-3:][::-1]
    
    print(f"\n📸 Image: {os.path.basename(image_path)}")
    print(f"🎯 Prediction: {predicted_class.replace('Tomato___', '').replace('_', ' ')}")
    print(f"📊 Confidence: {confidence*100:.2f}%")
    print("\n🏆 Top 3 Predictions:")
    for i, idx in enumerate(top_3_idx, 1):
        class_name = CLASS_NAMES[idx].replace('Tomato___', '').replace('_', ' ')
        conf = predictions[0][idx] * 100
        print(f"   {i}. {class_name}: {conf:.2f}%")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Test trained model')
    parser.add_argument('--image', type=str, help='Path to image file')
    parser.add_argument('--folder', type=str, help='Path to folder with images')
    
    args = parser.parse_args()
    
    print("\n" + "🍅"*30)
    print("TOMATO DISEASE MODEL TESTING")
    print("🍅"*30 + "\n")
    
    # Load model
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Model not found: {MODEL_PATH}")
        print("   Run train.py first to create the model")
        return
    
    print(f"📥 Loading model from {MODEL_PATH}...")
    model = keras.models.load_model(MODEL_PATH)
    print(f"✅ Model loaded successfully\n")
    
    # Test single image
    if args.image:
        if os.path.exists(args.image):
            predict_image(model, args.image)
        else:
            print(f"❌ Image not found: {args.image}")
    
    # Test folder
    elif args.folder:
        if os.path.exists(args.folder):
            images = []
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
                images.extend(Path(args.folder).glob(ext))
            
            if not images:
                print(f"❌ No images found in {args.folder}")
                return
            
            print(f"Found {len(images)} images\n")
            for img_path in images:
                predict_image(model, str(img_path))
        else:
            print(f"❌ Folder not found: {args.folder}")
    
    else:
        print("Usage:")
        print("  Test single image:")
        print("    python test_model.py --image path/to/image.jpg")
        print("\n  Test folder:")
        print("    python test_model.py --folder path/to/folder")
    
    print("\n" + "🍅"*30 + "\n")

if __name__ == '__main__':
    from pathlib import Path
    main()
