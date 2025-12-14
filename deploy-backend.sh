#!/bin/bash

# Tomato Backend Fresh Deployment Script
# Run this on your VPS after security cleanup

set -e  # Exit on error

echo "=================================="
echo "Tomato Backend Deployment Script"
echo "=================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as sudo
if [ "$EUID" -eq 0 ]; then 
   echo -e "${RED}Please do not run as root. Use a regular user account.${NC}"
   exit 1
fi

echo -e "${YELLOW}Step 1: Installing system packages...${NC}"
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

echo -e "${GREEN}✓ System packages installed${NC}"
echo ""

echo -e "${YELLOW}Step 2: Creating application directory...${NC}"
cd ~
rm -rf tomato-backend
mkdir -p tomato-backend
cd tomato-backend

echo -e "${GREEN}✓ Directory created${NC}"
echo ""

echo -e "${YELLOW}Step 3: Setting up Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

echo -e "${GREEN}✓ Virtual environment created${NC}"
echo ""

echo -e "${YELLOW}Step 4: Installing Python packages...${NC}"
pip install --upgrade pip
pip install flask==3.1.0
pip install tensorflow==2.18.0
pip install pillow==11.0.0
pip install flask-cors==5.0.0
pip install werkzeug==3.1.3
pip install numpy==2.2.1
pip install huggingface-hub==0.27.0

echo -e "${GREEN}✓ Python packages installed${NC}"
echo ""

echo -e "${YELLOW}Step 5: Creating Flask application...${NC}"
cat > app.py << 'EOFPYTHON'
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import numpy as np
import io
import os
from huggingface_hub import hf_hub_download
import tensorflow as tf

app = Flask(__name__)
CORS(app)

print("Downloading model from HuggingFace...")
MODEL_PATH = hf_hub_download(
    repo_id="AminHP/resnet50-10-classes",
    filename="model.h5"
)

print("Loading model...")
model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded successfully!")

DISEASE_CLASSES = [
    "Bacterial_spot",
    "Early_blight", 
    "Late_blight",
    "Leaf_Mold",
    "Septoria_leaf_spot",
    "Spider_mites Two-spotted_spider_mite",
    "Target_Spot",
    "Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato_mosaic_virus",
    "Tomato_healthy"
]

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "model_loaded": True})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        
        file = request.files['image']
        img = Image.open(io.BytesIO(file.read()))
        img = img.convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        predictions = model.predict(img_array)
        predicted_class = DISEASE_CLASSES[np.argmax(predictions)]
        confidence = float(np.max(predictions))
        
        return jsonify({
            "disease": predicted_class,
            "confidence": confidence
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=False)
EOFPYTHON

echo -e "${GREEN}✓ Flask application created${NC}"
echo ""

echo -e "${YELLOW}Step 6: Creating systemd service...${NC}"
sudo tee /etc/systemd/system/tomato-backend.service > /dev/null << EOFSERVICE
[Unit]
Description=Tomato Leaf Disease Detection Backend
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/tomato-backend
Environment="PATH=$HOME/tomato-backend/venv/bin"
ExecStart=$HOME/tomato-backend/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOFSERVICE

echo -e "${GREEN}✓ Systemd service created${NC}"
echo ""

echo -e "${YELLOW}Step 7: Enabling and starting service...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable tomato-backend
sudo systemctl start tomato-backend

echo -e "${GREEN}✓ Service started${NC}"
echo ""

echo -e "${YELLOW}Step 8: Configuring firewall...${NC}"
sudo ufw allow 5005/tcp
sudo ufw --force enable

echo -e "${GREEN}✓ Firewall configured${NC}"
echo ""

echo "=================================="
echo -e "${GREEN}Deployment Complete!${NC}"
echo "=================================="
echo ""
echo "Backend is running on: http://$(hostname -I | awk '{print $1}'):5005"
echo ""
echo "Test with: curl http://$(hostname -I | awk '{print $1}'):5005/health"
echo ""
echo "View logs: sudo journalctl -u tomato-backend -f"
echo "Check status: sudo systemctl status tomato-backend"
echo ""
echo -e "${YELLOW}Update your Flutter app URL to:${NC}"
echo "http://$(hostname -I | awk '{print $1}'):5005/predict"
echo ""
