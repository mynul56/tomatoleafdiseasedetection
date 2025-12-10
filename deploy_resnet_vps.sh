#!/bin/bash

# ====================================
# Deploy ResNet50 Backend to VPS
# ====================================

echo "🚀 Deploying ResNet50 Backend to VPS..."

# Update code from git
echo "📥 Pulling latest code..."
cd /var/www/tomatoleafdiseasedetection
git pull origin main

# Activate virtual environment and install dependencies
echo "📦 Installing dependencies..."
./venv/bin/pip install numpy pillow tensorflow flask flask-cors

# Update systemd service to use resnet_backend.py
echo "⚙️  Updating systemd service..."
sudo tee /etc/systemd/system/tomato-api.service > /dev/null << 'EOF'
[Unit]
Description=Tomato Disease Detection API (ResNet50)
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/var/www/tomatoleafdiseasedetection
Environment="PATH=/var/www/tomatoleafdiseasedetection/venv/bin"
ExecStart=/var/www/tomatoleafdiseasedetection/venv/bin/python resnet_backend.py
StandardOutput=append:/var/www/tomatoleafdiseasedetection/backend.log
StandardError=append:/var/www/tomatoleafdiseasedetection/backend.log
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and restart service
echo "🔄 Restarting service..."
sudo systemctl daemon-reload
sudo systemctl restart tomato-api
sudo systemctl enable tomato-api

# Check service status
echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Service Status:"
sudo systemctl status tomato-api --no-pager

echo ""
echo "📝 Recent Logs:"
tail -n 20 /var/www/tomatoleafdiseasedetection/backend.log

echo ""
echo "🌐 API Endpoints:"
echo "   Health: http://YOUR_VPS_IP:5005/health"
echo "   Predict: POST http://YOUR_VPS_IP:5005/predict"
echo ""
echo "🔍 Monitor logs: tail -f /var/www/tomatoleafdiseasedetection/backend.log"
