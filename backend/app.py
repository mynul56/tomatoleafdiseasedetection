"""
Production Backend for Tomato Leaf Disease Detection
Using HuggingFace ResNet50 Model - 10 Disease Classes
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import TFResNetForImageClassification, AutoImageProcessor
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os
import json

app = Flask(__name__)
CORS(app)

# Configuration
MODEL_PATH = './hf_model'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Load the model
try:
    print(f"Loading model from {MODEL_PATH}...")
    model = TFResNetForImageClassification.from_pretrained(MODEL_PATH, from_pt=True)
    processor = AutoImageProcessor.from_pretrained(MODEL_PATH)
    
    # Load class labels from config
    with open(os.path.join(MODEL_PATH, 'config.json'), 'r') as f:
        config = json.load(f)
        id2label = config['id2label']
    
    print(f"✓ Model loaded successfully!")
    print(f"✓ Model supports {len(id2label)} classes")
except Exception as e:
    print(f"✗ Error loading model: {str(e)}")
    model = None
    processor = None
    id2label = {}

# Disease information with treatments
DISEASE_TREATMENTS = {
    "A healthy tomato leaf": {
        "short_name": "Healthy",
        "description": "Your tomato leaf is healthy! No disease detected.",
        "treatment": "Continue regular care: adequate watering, proper fertilization, and monitoring for pests."
    },
    "A tomato leaf with Bacterial Spot": {
        "short_name": "Bacterial Spot",
        "description": "Bacterial spot causes dark, greasy-looking spots on leaves and fruit.",
        "treatment": "Remove infected leaves, avoid overhead watering, apply copper-based bactericides, and use disease-resistant varieties."
    },
    "A tomato leaf with Early Blight": {
        "short_name": "Early Blight",
        "description": "Early blight creates concentric rings (target spots) on lower leaves first.",
        "treatment": "Remove infected leaves, improve air circulation, mulch to prevent soil splash, and apply fungicides containing chlorothalonil or copper."
    },
    "A tomato leaf with Late Blight": {
        "short_name": "Late Blight",
        "description": "Late blight causes water-soaked spots that quickly turn brown and can destroy entire plants.",
        "treatment": "Remove and destroy infected plants immediately, apply fungicides preventively in wet weather, and ensure proper spacing for air circulation."
    },
    "A tomato leaf with Leaf Mold": {
        "short_name": "Leaf Mold",
        "description": "Leaf mold appears as yellow spots on upper leaf surfaces with olive-green mold on undersides.",
        "treatment": "Improve greenhouse ventilation, reduce humidity below 85%, remove infected leaves, and apply fungicides if necessary."
    },
    "A tomato leaf with Septoria Leaf Spot": {
        "short_name": "Septoria Leaf Spot",
        "description": "Septoria leaf spot shows circular spots with dark borders and gray centers containing tiny black dots.",
        "treatment": "Remove infected leaves, avoid overhead watering, mulch around plants, rotate crops, and apply fungicides containing copper or chlorothalonil."
    },
    "A tomato leaf with Spider Mites Two-spotted Spider Mite": {
        "short_name": "Spider Mites",
        "description": "Spider mites cause stippling and yellowing of leaves, with fine webbing in severe cases.",
        "treatment": "Spray plants with strong water jets, introduce predatory mites, apply insecticidal soap or neem oil, and maintain adequate humidity."
    },
    "A tomato leaf with Target Spot": {
        "short_name": "Target Spot",
        "description": "Target spot creates concentric rings similar to early blight but with distinct tan-colored centers.",
        "treatment": "Remove infected leaves, improve air circulation, avoid overhead irrigation, and apply fungicides containing azoxystrobin or chlorothalonil."
    },
    "A tomato leaf with Tomato Mosaic Virus": {
        "short_name": "Tomato Mosaic Virus",
        "description": "Mosaic virus causes mottled light and dark green patterns on leaves and stunted growth.",
        "treatment": "No cure available. Remove and destroy infected plants, disinfect tools, wash hands before handling plants, and use virus-resistant varieties."
    },
    "A tomato leaf with Tomato Yellow Leaf Curl Virus": {
        "short_name": "Yellow Leaf Curl Virus",
        "description": "This virus causes severe leaf curling, yellowing, and stunted plant growth.",
        "treatment": "No cure available. Remove infected plants, control whitefly populations (the virus vector), use reflective mulches, and plant resistant varieties."
    }
}

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'num_classes': len(id2label) if id2label else 0
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Predict disease from uploaded image"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    # Check if image is present
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        # Read and process image
        img_bytes = file.read()
        image = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        
        # Preprocess with the processor
        inputs = processor(images=image, return_tensors="tf")
        
        # Make prediction
        outputs = model(**inputs)
        logits = outputs.logits
        
        # Get probabilities
        probabilities = tf.nn.softmax(logits, axis=-1).numpy()[0]
        
        # Get top prediction
        predicted_class_idx = int(np.argmax(probabilities))
        confidence = float(probabilities[predicted_class_idx])
        
        # Get label
        predicted_label = id2label[str(predicted_class_idx)]
        
        # Get disease info
        disease_info = DISEASE_TREATMENTS.get(predicted_label, {
            "short_name": "Unknown",
            "description": predicted_label,
            "treatment": "Unable to provide treatment information."
        })
        
        # Get top 3 predictions
        top_3_indices = np.argsort(probabilities)[-3:][::-1]
        top_3_predictions = [
            {
                'disease': DISEASE_TREATMENTS.get(id2label[str(idx)], {}).get('short_name', id2label[str(idx)]),
                'confidence': float(probabilities[idx]),
                'full_label': id2label[str(idx)]
            }
            for idx in top_3_indices
        ]
        
        return jsonify({
            'success': True,
            'disease': disease_info['short_name'],
            'confidence': confidence,
            'description': disease_info['description'],
            'treatment': disease_info['treatment'],
            'full_label': predicted_label,
            'top_predictions': top_3_predictions
        })
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

@app.route('/', methods=['GET'])
def index():
    """API documentation"""
    return jsonify({
        'name': 'Tomato Leaf Disease Detection API',
        'version': '1.0',
        'model': 'HuggingFace ResNet50',
        'classes': list(id2label.values()) if id2label else [],
        'endpoints': {
            '/': 'API documentation (this page)',
            '/health': 'Health check',
            '/predict': 'POST image for disease prediction'
        },
        'usage': {
            'method': 'POST',
            'endpoint': '/predict',
            'content_type': 'multipart/form-data',
            'parameters': {
                'image': 'Image file (jpg, jpeg, png)'
            }
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5005))
    app.run(host='0.0.0.0', port=port, debug=False)
