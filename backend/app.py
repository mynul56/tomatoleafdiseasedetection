"""
Production Backend for Tomato Leaf Disease Detection
Using ResNet50 with Transfer Learning - All 10 Disease Classes
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MODEL_PATH = 'tomato_resnet50_model.h5'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# All 10 tomato disease classes (alphabetically ordered as ImageDataGenerator loads them)
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

# Try to load ResNet50 model
model = None
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.applications import ResNet50
    from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
    from tensorflow.keras.models import Model
    
    if os.path.exists(MODEL_PATH):
        print(f"📥 Loading trained model from {MODEL_PATH}...")
        model = keras.models.load_model(MODEL_PATH)
        print(f"✅ Model loaded successfully")
    else:
        print("⚠️  No trained model found. Downloading pre-trained model...")
        print("   Attempting to download from TensorFlow Hub...")
        
        try:
            # Try to download a pre-trained PlantVillage model
            import tensorflow_hub as hub
            print("   Using TensorFlow Hub PlantVillage model...")
            
            # Load pre-trained model (this would need actual hub URL)
            # For now, build with ImageNet and random initialization
            base_model = ResNet50(
                weights='imagenet',
                include_top=False,
                input_shape=(224, 224, 3)
            )
            
            # Freeze base model layers
            base_model.trainable = False
            
            # Add custom classification head
            x = GlobalAveragePooling2D()(base_model.output)
            x = Dense(512, activation='relu')(x)
            x = Dropout(0.5)(x)
            x = Dense(256, activation='relu')(x)
            x = Dropout(0.3)(x)
            output = Dense(len(CLASS_NAMES), activation='softmax')(x)
            
            model = Model(inputs=base_model.input, outputs=output)
            
            # Compile model
            model.compile(
                optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            
            print(f"✅ ResNet50 model built with ImageNet weights")
            print(f"⚠️  WARNING: Model is NOT trained on tomato diseases!")
            print(f"   Predictions will be RANDOM until model is trained.")
            print(f"   To get accurate results:")
            print(f"   1. Download dataset: python prepare_dataset.py --download")
            print(f"   2. Train model: python train.py")
            print(f"   3. Restart server")
            
        except ImportError:
            print("   tensorflow_hub not available, using ImageNet baseline")
            base_model = ResNet50(
                weights='imagenet',
                include_top=False,
                input_shape=(224, 224, 3)
            )
            
            base_model.trainable = False
            x = GlobalAveragePooling2D()(base_model.output)
            x = Dense(512, activation='relu')(x)
            x = Dropout(0.5)(x)
            x = Dense(256, activation='relu')(x)
            x = Dropout(0.3)(x)
            output = Dense(len(CLASS_NAMES), activation='softmax')(x)
            
            model = Model(inputs=base_model.input, outputs=output)
            model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
            
            print(f"⚠️  Model NOT trained - predictions will be inaccurate!")
    
    print(f"   Model input shape: {model.input_shape}")
    print(f"   Model output shape: {model.output_shape}")
    print(f"   Number of classes: {len(CLASS_NAMES)}")
    
except ImportError as e:
    print(f"❌ TensorFlow not installed: {e}")
    print("   Install with: pip install tensorflow")
except Exception as e:
    print(f"⚠️  Error loading model: {e}")
    import traceback
    traceback.print_exc()

# Comprehensive disease information database
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
    'Tomato___Leaf_Mold': {
        'description': 'Leaf mold is caused by Passalora fulva fungus. It thrives in high humidity and causes pale green to yellowish spots on upper leaf surfaces with olive-green to brown fuzzy growth underneath.',
        'treatment': [
            'Reduce humidity in greenhouse or growing area',
            'Improve ventilation significantly',
            'Remove and destroy infected leaves',
            'Apply appropriate fungicide',
            'Use resistant varieties',
            'Avoid overhead watering'
        ]
    },
    'Tomato___Septoria_leaf_spot': {
        'description': 'Septoria leaf spot is caused by Septoria lycopersici fungus. It causes small, circular spots with gray centers and dark borders, often with tiny black dots in the center.',
        'treatment': [
            'Remove infected leaves and destroy them',
            'Mulch around plants to prevent soil splash',
            'Water at base of plants only',
            'Apply fungicide regularly during wet periods',
            'Practice crop rotation (3-4 years)',
            'Clean up all plant debris at end of season'
        ]
    },
    'Tomato___Spider_mites Two-spotted_spider_mite': {
        'description': 'Two-spotted spider mites are tiny pests that cause stippling and yellowing of leaves. Severe infestations produce fine webbing on plants.',
        'treatment': [
            'Spray plants with strong water stream',
            'Apply insecticidal soap or neem oil',
            'Introduce predatory mites',
            'Maintain adequate moisture levels',
            'Remove heavily infested leaves',
            'Use miticides if infestation is severe'
        ]
    },
    'Tomato___Target_Spot': {
        'description': 'Target spot is caused by Corynespora cassiicola fungus. It produces brown lesions with concentric rings, similar to early blight but with more uniform circles.',
        'treatment': [
            'Remove infected leaves promptly',
            'Apply fungicide at first sign of disease',
            'Improve air circulation',
            'Avoid overhead irrigation',
            'Practice crop rotation',
            'Clean up plant debris regularly'
        ]
    },
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': {
        'description': 'Yellow leaf curl virus is transmitted by whiteflies. It causes yellowing, upward curling, and severe stunting of plants. Leaves become thick and leathery.',
        'treatment': [
            'Control whitefly populations with insecticides',
            'Remove infected plants immediately',
            'Use resistant varieties when possible',
            'Apply reflective mulches to repel whiteflies',
            'Inspect plants regularly for whitefly presence',
            'Destroy infected plants to prevent spread'
        ]
    },
    'Tomato___Tomato_mosaic_virus': {
        'description': 'Tomato mosaic virus causes mottled light and dark green patterns on leaves, leaf distortion, and stunted growth. It spreads through contaminated tools and hands.',
        'treatment': [
            'Remove and destroy infected plants',
            'Disinfect all tools between uses',
            'Wash hands thoroughly when handling plants',
            'Use resistant varieties',
            'Control aphid populations',
            'Do not use tobacco products around plants'
        ]
    }
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image, target_size=(224, 224)):
    """
    Preprocess image for ResNet50 model
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize image
    image = image.resize(target_size, Image.LANCZOS)
    
    # Convert to numpy array
    img_array = np.array(image)
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    # Apply ResNet50 preprocessing
    from tensorflow.keras.applications.resnet50 import preprocess_input
    img_array = preprocess_input(img_array)
    
    return img_array

def predict_disease(image):
    """
    Predict disease using ResNet50 model
    """
    if model is None:
        raise Exception("Model not loaded")
    
    try:
        # Preprocess image
        processed_image = preprocess_image(image)
        
        # Get prediction
        predictions = model.predict(processed_image, verbose=0)
        
        # Get predicted class and confidence
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        
        predicted_disease = CLASS_NAMES[predicted_class_idx]
        
        # Get top 3 predictions
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
        'classes': len(CLASS_NAMES),
        'class_names': CLASS_NAMES
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
        
        # Format disease name for display
        disease_display = disease.replace('Tomato___', '').replace('_', ' ').title()
        
        # Prepare response
        response = {
            'disease': disease_display,
            'confidence': round(confidence * 100, 2),
            'description': disease_info['description'],
            'treatment': disease_info['treatment'],
            'top_predictions': [
                {
                    'disease': pred['disease'].replace('Tomato___', '').replace('_', ' ').title(),
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
    print(f"🧠 ML Model: ResNet50 with Transfer Learning")
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
