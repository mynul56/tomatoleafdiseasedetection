#!/bin/bash

# Deployment script for VPS
# Usage: bash deploy_to_vps.sh

set -e

echo "======================================"
echo "🍅 Tomato Disease Detection Backend"
echo "      VPS Deployment Script"
echo "======================================"
echo ""

# Configuration
VPS_IP="206.162.244.175"
VPS_USER="root"
VPS_PORT="22"
REMOTE_DIR="/root/tomatoleafdiseasedetection/tomatoleafdiseasedetection/backend"
MODEL_FILE="tomato_resnet50_model.h5"

echo "📋 Configuration:"
echo "  VPS IP: $VPS_IP"
echo "  User: $VPS_USER"
echo "  Remote Directory: $REMOTE_DIR"
echo ""

# Check if model exists
if [ ! -f "$MODEL_FILE" ]; then
    echo "❌ Model file not found: $MODEL_FILE"
    echo "   Please train the model first:"
    echo "   python train.py"
    exit 1
fi

echo "✅ Model file found: $MODEL_FILE"
MODEL_SIZE=$(du -h "$MODEL_FILE" | cut -f1)
echo "   Size: $MODEL_SIZE"
echo ""

# Step 1: Push code to Git
echo "📤 Step 1/5: Pushing code to Git..."
git add .
git commit -m "Update backend with ResNet50 all diseases" || echo "No changes to commit"
git push origin main
echo "✅ Code pushed to Git"
echo ""

# Step 2: Transfer model file to VPS
echo "📤 Step 2/5: Transferring model to VPS..."
echo "   This may take a few minutes..."
scp -P $VPS_PORT "$MODEL_FILE" "$VPS_USER@$VPS_IP:$REMOTE_DIR/" || {
    echo "❌ Failed to transfer model"
    exit 1
}
echo "✅ Model transferred successfully"
echo ""

# Step 3: Pull latest code on VPS
echo "📥 Step 3/5: Pulling latest code on VPS..."
ssh -p $VPS_PORT "$VPS_USER@$VPS_IP" "cd $REMOTE_DIR/.. && git pull origin main"
echo "✅ Code pulled on VPS"
echo ""

# Step 4: Install dependencies on VPS
echo "📦 Step 4/5: Installing dependencies on VPS..."
ssh -p $VPS_PORT "$VPS_USER@$VPS_IP" << 'EOF'
cd /root/tomatoleafdiseasedetection/tomatoleafdiseasedetection/backend
source ../venv/bin/activate || python3 -m venv ../venv && source ../venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
EOF
echo "✅ Dependencies installed"
echo ""

# Step 5: Restart service
echo "🔄 Step 5/5: Restarting API service..."
ssh -p $VPS_PORT "$VPS_USER@$VPS_IP" << 'EOF'
# Update systemd service to use new app.py
sudo systemctl stop tomato-api

# Update service file if needed
sudo tee /etc/systemd/system/tomato-api.service > /dev/null << 'SERVICE'
[Unit]
Description=Tomato Disease Detection API
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/tomatoleafdiseasedetection/tomatoleafdiseasedetection/backend
Environment="PATH=/root/tomatoleafdiseasedetection/tomatoleafdiseasedetection/venv/bin"
ExecStart=/root/tomatoleafdiseasedetection/tomatoleafdiseasedetection/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

sudo systemctl daemon-reload
sudo systemctl start tomato-api
sudo systemctl enable tomato-api
sleep 3
sudo systemctl status tomato-api --no-pager -l
EOF
echo "✅ Service restarted"
echo ""

# Test the API
echo "🧪 Testing API..."
sleep 5
HEALTH_RESPONSE=$(curl -s "http://$VPS_IP:5005/health")

if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    echo "✅ API is healthy!"
    echo ""
    echo "$HEALTH_RESPONSE" | python3 -m json.tool
else
    echo "⚠️  Warning: API health check failed"
    echo "Response: $HEALTH_RESPONSE"
fi

echo ""
echo "======================================"
echo "✅ Deployment Complete!"
echo "======================================"
echo ""
echo "🌐 API Endpoints:"
echo "  Health: http://$VPS_IP:5005/health"
echo "  Predict: http://$VPS_IP:5005/predict"
echo ""
echo "📝 Next Steps:"
echo "  1. Test API with: curl http://$VPS_IP:5005/health"
echo "  2. Update Flutter app baseUrl to: http://$VPS_IP:5005"
echo "  3. Test prediction from mobile app"
echo ""
echo "📊 View logs:"
echo "  ssh $VPS_USER@$VPS_IP"
echo "  sudo journalctl -u tomato-api -f"
echo ""
