"""
Sample Flask Backend for Tomato Leaf Disease Detection
This is a reference implementation showing how to structure the backend API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow import keras
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MODEL_PATH = 'models/tomato_disease_model.h5'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Disease information database
DISEASE_INFO = {
    'Healthy': {
        'description': 'The tomato leaf appears to be healthy with no signs of disease.',
        'treatment': [
            'Continue regular watering and fertilization',
            'Monitor plants regularly for early disease detection',
            'Maintain good air circulation'
        ]
    },
    'Early Blight': {
        'description': 'Early blight is caused by the fungus Alternaria solani. It typically affects older leaves first, causing dark brown spots with concentric rings.',
        'treatment': [
            'Remove and destroy infected leaves',
            'Apply copper-based fungicide',
            'Improve air circulation around plants',
            'Avoid overhead watering',
            'Rotate crops annually'
        ]
    },
    'Late Blight': {
        'description': 'Late blight is caused by Phytophthora infestans. It spreads rapidly in cool, wet conditions and can destroy entire crops.',
        'treatment': [
            'Remove infected plants immediately',
            'Apply fungicide preventively',
            'Ensure good drainage',
            'Space plants properly for air circulation',
            'Use resistant varieties'
        ]
    },
    'Leaf Mold': {
        'description': 'Leaf mold is caused by Passalora fulva fungus. It thrives in high humidity and causes pale green to yellowish spots on upper leaf surfaces.',
        'treatment': [
            'Reduce humidity in greenhouse',
            'Improve ventilation',
            'Remove infected leaves',
            'Apply appropriate fungicide',
            'Use resistant varieties'
        ]
    },
    'Septoria Leaf Spot': {
        'description': 'Septoria leaf spot is caused by Septoria lycopersici fungus. It causes small, circular spots with gray centers and dark borders.',
        'treatment': [
            'Remove infected leaves',
            'Mulch around plants to prevent soil splash',
            'Water at base of plants',
            'Apply fungicide regularly',
            'Practice crop rotation'
        ]
    },
    'Bacterial Spot': {
        'description': 'Bacterial spot is caused by Xanthomonas bacteria. It affects leaves, stems, and fruit with small, dark spots.',
        'treatment': [
            'Use disease-free seeds and transplants',
            'Apply copper-based bactericide',
            'Remove infected plants',
            'Avoid working with wet plants',
            'Practice crop rotation'
        ]
    },
    'Yellow Leaf Curl Virus': {
        'description': 'Yellow leaf curl virus is transmitted by whiteflies. It causes yellowing, curling, and stunting of plants.',
        'treatment': [
            'Control whitefly populations',
            'Remove infected plants immediately',
            'Use resistant varieties',
            'Install insect-proof nets',
            'Apply reflective mulch'
        ]
    },
    'Mosaic Virus': {
        'description': 'Mosaic virus causes mottled yellow and green patterns on leaves and can stunt plant growth.',
        'treatment': [
            'Remove and destroy infected plants',
            'Control aphid populations',
            'Disinfect tools between plants',
            'Use virus-free seeds',
            'Plant resistant varieties'
        ]
    },
    'Target Spot': {
        'description': 'Target spot is caused by Corynespora cassiicola fungus. It produces concentric ring patterns in lesions.',
        'treatment': [
            'Remove infected plant debris',
            'Apply fungicide treatment',
            'Improve air circulation',
            'Avoid overhead irrigation',
            'Practice crop rotation'
        ]
    },
    'Spider Mites': {
        'description': 'Spider mites are tiny pests that cause yellow stippling on leaves and fine webbing on plants.',
        'treatment': [
            'Spray with water to dislodge mites',
            'Apply insecticidal soap or neem oil',
            'Introduce beneficial predatory mites',
            'Maintain adequate humidity',
            'Remove heavily infested leaves'
        ]
    }
}

# Load the trained model
try:
    model = keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_file):
    """Preprocess image for model prediction"""
    # Read image
    image = Image.open(io.BytesIO(image_file.read()))
    
    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize to model input size (adjust based on your model)
    image = image.resize((224, 224))
    
    # Convert to numpy array and normalize
    image_array = np.array(image) / 255.0
    
    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)
    
    return image_array

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    """Predict disease from uploaded image"""
    
    # Check if file is present
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    # Check if file is valid
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload an image (PNG, JPG, JPEG)'}), 400
    
    # Check if model is loaded
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Preprocess image
        with open(filepath, 'rb') as f:
            processed_image = preprocess_image(f)
        
        # Make prediction
        predictions = model.predict(processed_image)
        predicted_class_index = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_index])
        
        # Class names (adjust based on your model's classes)
        class_names = [
            'Bacterial Spot',
            'Early Blight',
            'Healthy',
            'Late Blight',
            'Leaf Mold',
            'Septoria Leaf Spot',
            'Spider Mites',
            'Target Spot',
            'Yellow Leaf Curl Virus',
            'Mosaic Virus'
        ]
        
        disease_name = class_names[predicted_class_index]
        disease_data = DISEASE_INFO.get(disease_name, {
            'description': 'Disease information not available.',
            'treatment': ['Consult with an agricultural expert']
        })
        
        # Prepare response
        result = {
            'disease': disease_name,
            'confidence': confidence,
            'description': disease_data['description'],
            'treatment': disease_data['treatment']
        }
        
        # Clean up uploaded file (optional)
        # os.remove(filepath)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

if __name__ == '__main__':
    print("Starting Tomato Disease Detection Server...")
    print(f"Model path: {MODEL_PATH}")
    print(f"Upload folder: {UPLOAD_FOLDER}")
    app.run(host='0.0.0.0', port=5000, debug=True)
