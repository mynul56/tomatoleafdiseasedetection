#!/bin/bash

echo "🚀 Setting up Tomato Disease Detection Backend on VPS..."
echo ""

# Navigate to project directory
cd /var/www/tomatoleafdiseasedetection

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo "📥 Installing Python packages..."
pip install flask flask-cors werkzeug gunicorn --quiet

# Create uploads directory if it doesn't exist
mkdir -p uploads
chmod 755 uploads

# Create systemd service file
echo "⚙️  Creating systemd service..."
cat <<'EOF' | sudo tee /etc/systemd/system/tomato-api.service > /dev/null
[Unit]
Description=Tomato Disease Detection API
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/var/www/tomatoleafdiseasedetection
Environment="PATH=/var/www/tomatoleafdiseasedetection/venv/bin"
ExecStart=/var/www/tomatoleafdiseasedetection/venv/bin/python test_backend.py
Restart=always
RestartSec=10
StandardOutput=append:/var/www/tomatoleafdiseasedetection/backend.log
StandardError=append:/var/www/tomatoleafdiseasedetection/backend.log

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
echo "🔄 Reloading systemd..."
sudo systemctl daemon-reload

# Enable and start service
echo "🚀 Starting service..."
sudo systemctl enable tomato-api
sudo systemctl start tomato-api

# Wait a moment
sleep 2

# Check status
echo ""
echo "=" * 60
echo "✅ Setup Complete!"
echo "=" * 60
echo ""
echo "📊 Service Status:"
sudo systemctl status tomato-api --no-pager -l

echo ""
echo "🔍 Testing API:"
curl -s http://localhost:5005/health | python3 -m json.tool || echo "Server starting..."

echo ""
echo "=" * 60
echo "Useful Commands:"
echo "=" * 60
echo "View logs:        sudo journalctl -u tomato-api -f"
echo "Restart:          sudo systemctl restart tomato-api"
echo "Stop:             sudo systemctl stop tomato-api"
echo "Status:           sudo systemctl status tomato-api"
echo "Test health:      curl http://localhost:5005/health"
echo ""
echo "API is running on port 5005 🎉"
echo "External access:  http://YOUR_VPS_IP:5005"
echo "=" * 60
