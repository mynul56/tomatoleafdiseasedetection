"""
Simple Test Backend for Tomato Leaf Disease Detection
This is a minimal Flask backend to test the app connection
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Create upload folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Backend server is running!'
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    """Mock prediction endpoint - returns sample data"""
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Mock response - replace this with actual ML prediction
        result = {
            'disease': 'Early Blight',
            'confidence': 0.87,
            'description': 'Early blight is a common fungal disease caused by Alternaria solani. It typically affects older leaves first, causing dark brown spots with concentric rings that resemble a target.',
            'treatment': [
                'Remove and destroy infected leaves immediately',
                'Apply copper-based fungicide every 7-10 days',
                'Improve air circulation by spacing plants properly',
                'Avoid overhead watering - water at the base of plants',
                'Use mulch to prevent soil splash onto leaves',
                'Practice crop rotation annually'
            ]
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🍅 Tomato Disease Detection Backend Server")
    print("=" * 60)
    print(f"📁 Upload folder: {UPLOAD_FOLDER}")
    print("🌐 Server starting on http://0.0.0.0:5005")
    print("   • Android Emulator: http://10.0.2.2:5005")
    print("   • iOS Simulator: http://localhost:5005")
    print("   • Physical Device: http://YOUR_IP:5005")
    print("   • VPS: http://YOUR_VPS_IP:5005")
    print("=" * 60)
    print("✅ Health check: http://localhost:5005/health")
    print("🔍 Predict endpoint: POST http://localhost:5005/predict")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5005, debug=True)
