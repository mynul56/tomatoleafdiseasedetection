#!/bin/bash
VPS_IP="206.162.244.175"
VPS_USER="root"
REMOTE_DIR="/root/tomato-backend"

echo "Deploying to VPS..."

# Copy files
rsync -avz --exclude 'venv' --exclude '__pycache__' --exclude '*.pyc' --exclude 'tf_model' --exclude 'uploads' ./ $VPS_USER@$VPS_IP:$REMOTE_DIR/

# Setup and run
ssh $VPS_USER@$VPS_IP "cd $REMOTE_DIR && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && systemctl restart tomato-backend"

echo "Done! Backend at http://$VPS_IP:5005"
