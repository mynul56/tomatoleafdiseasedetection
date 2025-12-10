"""
Production Backend using Pre-trained ResNet50 Model for Tomato Leaf Disease Detection
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
import io
import sys

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
RESNET_MODEL_PATH = 'ResNet50_best_model.keras'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Disease class names (matching your training dataset)
# ImageDataGenerator loads classes in alphabetical order
CLASS_NAMES = [
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___healthy',
    'Tomato___Late_blight'
]

# Try to load ResNet50 model
model = None
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.applications import ResNet50
    from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
    from tensorflow.keras.models import Model
    
    if os.path.exists(RESNET_MODEL_PATH):
        print("📥 Loading pre-trained ResNet50 model...")
        
        try:
            # Try loading as-is first (for legacy formats)
            if not os.path.isdir(RESNET_MODEL_PATH):
                model = keras.models.load_model(RESNET_MODEL_PATH)
            else:
                # For Keras 3.x directory format, rebuild the model architecture
                # and load weights manually
                print("   Detected Keras 3.x directory format, rebuilding model...")
                
                # Recreate the ResNet50 architecture (matching your training code)
                base = ResNet50(
                    weights=None,  # Don't load ImageNet weights
                    include_top=False,
                    input_shape=(299, 299, 3)
                )
                base.trainable = False
                
                x = GlobalAveragePooling2D()(base.output)
                x = Dense(1024, activation="relu")(x)
                x = Dropout(0.5)(x)
                output = Dense(len(CLASS_NAMES), activation="softmax")(x)
                
                model = Model(inputs=base.input, outputs=output)
                
                # Load weights from the .keras directory
                weights_file = os.path.join(RESNET_MODEL_PATH, 'model.weights.h5')
                if os.path.exists(weights_file):
                    print(f"   Loading weights from {weights_file}")
                    model.load_weights(weights_file)
                else:
                    print(f"   ❌ Weights file not found: {weights_file}")
                    sys.exit(1)
                    
        except Exception as load_error:
            print(f"   Error during model loading: {load_error}")
            raise
            
        print(f"✅ ResNet50 model loaded successfully")
        print(f"   Model input shape: {model.input_shape}")
        print(f"   Model output shape: {model.output_shape}")
        print(f"   Number of classes: {len(CLASS_NAMES)}")
    else:
        print(f"❌ Model file not found at: {RESNET_MODEL_PATH}")
        print("   Please ensure ResNet50_best_model.keras is in the same directory")
        sys.exit(1)
        
except ImportError as e:
    print(f"❌ TensorFlow not installed: {e}")
    print("   Install with: pip install tensorflow")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error loading ResNet50 model: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Disease information database
DISEASE_INFO = {
    'Tomato___healthy': {
        'description': 'The tomato leaf appears to be healthy with no signs of disease. The plant shows normal green coloration and no visible lesions or discoloration.',
        'treatment': [
            'Continue regular watering schedule',
            'Maintain proper fertilization',
            'Monitor plants regularly for early disease detection',
            'Ensure good air circulation around plants',
            'Remove any dead or yellowing leaves promptly'
        ]
    },
    'Tomato___Early_blight': {
        'description': 'Early blight is caused by the fungus Alternaria solani. It typically affects older leaves first, causing dark brown spots with concentric rings that resemble a target.',
        'treatment': [
            'Remove and destroy infected leaves immediately',
            'Apply copper-based fungicide every 7-10 days',
            'Improve air circulation by spacing plants properly',
            'Avoid overhead watering - water at the base of plants',
            'Use mulch to prevent soil splash onto leaves',
            'Practice crop rotation annually'
        ]
    },
    'Tomato___Late_blight': {
        'description': 'Late blight is caused by Phytophthora infestans. It spreads rapidly in cool, wet conditions and can destroy entire crops. Shows water-soaked lesions on leaves.',
        'treatment': [
            'Remove infected plants immediately to prevent spread',
            'Apply fungicide preventively in humid conditions',
            'Ensure excellent drainage in growing area',
            'Space plants properly for maximum air circulation',
            'Use resistant tomato varieties when available',
            'Destroy all infected plant material'
        ]
    },
    'Tomato___Bacterial_spot': {
        'description': 'Bacterial spot is caused by Xanthomonas bacteria. It affects leaves, stems, and fruit with small, dark, greasy-looking spots that may have a yellow halo.',
        'treatment': [
            'Use only disease-free seeds and transplants',
            'Apply copper-based bactericide',
            'Remove and destroy infected plants',
            'Avoid working with plants when wet',
            'Practice crop rotation',
            'Disinfect tools between plants'
        ]
    }
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image, target_size=(299, 299)):
    """
    Preprocess image for ResNet50 model
    - Resize to 299x299 (matching your training configuration)
    - Apply ResNet preprocessing
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize image
    image = image.resize(target_size, Image.LANCZOS)
    
    # Convert to numpy array
    img_array = np.array(image)
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    # Apply ResNet50 preprocessing (mean subtraction and scaling)
    from tensorflow.keras.applications.resnet import preprocess_input
    img_array = preprocess_input(img_array)
    
    return img_array

def predict_disease(image):
    """
    Predict disease using ResNet50 model
    """
    try:
        # Preprocess image
        processed_image = preprocess_image(image)
        
        # Get prediction
        predictions = model.predict(processed_image, verbose=0)
        
        # Get predicted class and confidence
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        
        predicted_disease = CLASS_NAMES[predicted_class_idx]
        
        # Get top 3 predictions for additional info
        top_3_indices = np.argsort(predictions[0])[-3:][::-1]
        top_3_predictions = [
            {
                'disease': CLASS_NAMES[idx],
                'confidence': float(predictions[0][idx])
            }
            for idx in top_3_indices
        ]
        
        return {
            'disease': predicted_disease,
            'confidence': confidence,
            'top_predictions': top_3_predictions
        }
        
    except Exception as e:
        print(f"Error in prediction: {e}")
        import traceback
        traceback.print_exc()
        raise

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model': 'ResNet50',
        'model_loaded': model is not None,
        'classes': len(CLASS_NAMES)
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Predict disease from uploaded image"""
    try:
        # Check if file is present
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Use PNG, JPG, or JPEG'}), 400
        
        # Read and process image
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Predict disease
        prediction_result = predict_disease(image)
        
        disease = prediction_result['disease']
        confidence = prediction_result['confidence']
        
        # Get disease information
        disease_info = DISEASE_INFO.get(disease, {
            'description': f'Information about {disease} is not available.',
            'treatment': ['Consult with agricultural expert']
        })
        
        # Prepare response
        response = {
            'disease': disease.replace('_', ' ').title(),
            'confidence': round(confidence * 100, 2),
            'description': disease_info['description'],
            'treatment': disease_info['treatment'],
            'top_predictions': [
                {
                    'disease': pred['disease'].replace('_', ' ').title(),
                    'confidence': round(pred['confidence'] * 100, 2)
                }
                for pred in prediction_result['top_predictions']
            ]
        }
        
        print(f"✅ Prediction: {response['disease']} ({response['confidence']}%)")
        
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Error in prediction endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🍅 Tomato Disease Detection Backend Server (ResNet50)")
    print("="*60)
    print(f"📁 Upload folder: {UPLOAD_FOLDER}")
    print(f"🧠 ML Model: ResNet50 (Pre-trained)")
    print(f"📊 Classes: {len(CLASS_NAMES)}")
    print(f"🌐 Server starting on http://0.0.0.0:5005")
    print("   • Android Emulator: http://10.0.2.2:5005")
    print("   • iOS Simulator: http://localhost:5005")
    print("   • Physical Device: http://YOUR_IP:5005")
    print("   • VPS: http://YOUR_VPS_IP:5005")
    print("="*60)
    print("✅ Health check: http://localhost:5005/health")
    print("🔍 Predict endpoint: POST http://localhost:5005/predict")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5005, debug=True)
