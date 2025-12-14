# VPS Security Recovery & Backend Redeployment Guide

## 🚨 Security Assessment & Recovery Steps

### Step 1: Assess the Damage

SSH into your VPS and run these commands:

```bash
# Check for suspicious processes
ps aux | grep -E "mining|crypto|scan|bot"

# Check network connections
netstat -tupln | grep ESTABLISHED

# Check for unauthorized users
cat /etc/passwd | grep /bin/bash

# Check recent logins
last -20
lastb -20  # Failed login attempts

# Check cron jobs for malware
crontab -l
cat /etc/crontab
ls -la /etc/cron.*

# Check running services
systemctl list-units --type=service --state=running

# Check file modifications in last 7 days
find /var/www /home -type f -mtime -7 -ls

# Check for hidden files (malware often hides)
find / -name ".*" -type f 2>/dev/null | grep -v "^/proc\|^/sys"
```

### Step 2: Immediate Security Measures

```bash
# 1. Change root password immediately
sudo passwd root

# 2. Create a new sudo user (don't use root)
sudo adduser mynul
sudo usermod -aG sudo mynul

# 3. Disable root SSH login
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
# Set: PasswordAuthentication no (after setting up SSH keys)
sudo systemctl restart sshd

# 4. Update all packages
sudo apt update
sudo apt upgrade -y
sudo apt autoremove -y

# 5. Install fail2ban (blocks brute force attacks)
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### Step 3: Clean Up Malware

```bash
# 1. Install security tools
sudo apt install clamav clamav-daemon rkhunter chkrootkit -y

# 2. Update virus definitions
sudo freshclam
sudo systemctl start clamav-daemon

# 3. Scan for malware
sudo clamscan -r -i /var /home /tmp

# 4. Check for rootkits
sudo rkhunter --check --skip-keypress
sudo chkrootkit

# 5. Remove suspicious files
# Review the scan results and delete any detected malware
# Example:
# sudo rm -f /path/to/malicious/file
```

### Step 4: Secure Firewall Configuration

```bash
# 1. Install UFW (Uncomplicated Firewall)
sudo apt install ufw -y

# 2. Set default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 3. Allow necessary ports
sudo ufw allow ssh           # Port 22
sudo ufw allow 5005/tcp      # Flask app port
sudo ufw allow 80/tcp        # HTTP (if needed)
sudo ufw allow 443/tcp       # HTTPS (if needed)

# 4. Enable firewall
sudo ufw enable
sudo ufw status verbose
```

### Step 5: Set Up SSH Key Authentication (More Secure)

**On your local machine:**

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Copy public key to VPS
ssh-copy-id mynul@206.162.244.175
```

**On VPS:**

```bash
# Disable password authentication
sudo nano /etc/ssh/sshd_config
# Set: PasswordAuthentication no
# Set: PubkeyAuthentication yes
sudo systemctl restart sshd
```

### Step 6: Remove Old Flask Application

```bash
# 1. Stop all Python processes
sudo pkill -f python
sudo pkill -f flask

# 2. Remove old application directory
cd ~
sudo rm -rf backend/
sudo rm -rf flask_app/
sudo rm -rf tomato*/

# 3. Clean up pip packages
pip3 freeze | xargs pip3 uninstall -y
```

### Step 7: Fresh Flask Backend Deployment

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Python and dependencies
sudo apt install python3 python3-pip python3-venv -y

# 3. Create application directory
mkdir -p ~/tomato-backend
cd ~/tomato-backend

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install required packages
pip install --upgrade pip
pip install flask==3.1.0
pip install tensorflow==2.18.0
pip install pillow==11.0.0
pip install flask-cors==5.0.0
pip install werkzeug==3.1.3
pip install numpy==2.2.1
pip install huggingface-hub==0.27.0
```

### Step 8: Create Secure Flask Application

Create `app.py`:

```python
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

# Download model from HuggingFace
MODEL_PATH = hf_hub_download(
    repo_id="AminHP/resnet50-10-classes",
    filename="model.h5"
)

# Load model
model = tf.keras.models.load_model(MODEL_PATH)

# Disease classes
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
```

### Step 9: Set Up Systemd Service (Auto-Start on Boot)

Create service file:

```bash
sudo nano /etc/systemd/system/tomato-backend.service
```

Add this content:

```ini
[Unit]
Description=Tomato Leaf Disease Detection Backend
After=network.target

[Service]
Type=simple
User=mynul
WorkingDirectory=/home/mynul/tomato-backend
Environment="PATH=/home/mynul/tomato-backend/venv/bin"
ExecStart=/home/mynul/tomato-backend/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable tomato-backend
sudo systemctl start tomato-backend
sudo systemctl status tomato-backend
```

### Step 10: Set Up Nginx Reverse Proxy (Optional but Recommended)

```bash
# Install Nginx
sudo apt install nginx -y

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/tomato-backend
```

Add this:

```nginx
server {
    listen 80;
    server_name 206.162.244.175;

    location / {
        proxy_pass http://127.0.0.1:5005;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/tomato-backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 11: Monitor and Log

```bash
# View application logs
sudo journalctl -u tomato-backend -f

# View system logs
sudo tail -f /var/log/syslog

# View Nginx logs (if using)
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Monitor system resources
htop
```

### Step 12: Regular Security Maintenance

Create a maintenance script:

```bash
nano ~/security-check.sh
```

Add this:

```bash
#!/bin/bash
echo "=== Security Check ==="
echo "Date: $(date)"
echo ""

echo "Failed login attempts:"
sudo lastb | head -20
echo ""

echo "Current connections:"
sudo netstat -tupln | grep ESTABLISHED
echo ""

echo "Disk usage:"
df -h
echo ""

echo "Memory usage:"
free -h
echo ""

echo "CPU usage:"
top -bn1 | head -20
```

Make it executable:

```bash
chmod +x ~/security-check.sh
```

Run weekly:

```bash
sudo crontab -e
# Add: 0 0 * * 0 /home/mynul/security-check.sh > /home/mynul/security-report.txt
```

## 🔒 Security Best Practices

### 1. Regular Updates
```bash
# Auto-update security patches
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 2. Backup Important Data
```bash
# Backup application
tar -czf ~/backup-$(date +%Y%m%d).tar.gz ~/tomato-backend/

# Download to local machine
scp mynul@206.162.244.175:~/backup-*.tar.gz ~/Downloads/
```

### 3. Monitor System
```bash
# Install monitoring tools
sudo apt install htop iotop nethogs -y

# Check disk space regularly
df -h

# Check memory usage
free -h
```

### 4. Secure Database (if you add one later)
```bash
# If using MySQL/PostgreSQL
# - Change default password
# - Use firewall to restrict access
# - Enable SSL connections
# - Regular backups
```

### 5. Enable Automatic Security Updates
```bash
sudo nano /etc/apt/apt.conf.d/50unattended-upgrades
# Uncomment: "${distro_id}:${distro_codename}-security";
```

## 🧪 Test Your Backend

```bash
# Test health endpoint
curl http://206.162.244.175:5005/health

# Test from Flutter app
# Update lib/screens/scan_screen.dart if needed
# Change URL to: http://206.162.244.175:5005/predict
```

## ⚠️ Red Flags to Watch For

1. **High CPU/Memory usage** when app is idle
2. **Unknown processes** running
3. **Unexpected network connections**
4. **Modified system files**
5. **New user accounts** you didn't create
6. **Failed login attempts** from unknown IPs
7. **Disk space** filling up rapidly
8. **Cron jobs** you didn't create

## 📱 Update Flutter App Configuration

If you change the backend URL, update your Flutter app:

```dart
// lib/screens/scan_screen.dart
final url = Uri.parse('http://206.162.244.175:5005/predict');
```

## 🎯 Quick Command Reference

```bash
# Check backend status
sudo systemctl status tomato-backend

# Restart backend
sudo systemctl restart tomato-backend

# View logs
sudo journalctl -u tomato-backend -f

# Check firewall
sudo ufw status

# Check connections
sudo netstat -tupln

# System resources
htop
```

## 🆘 Emergency Recovery

If system is severely compromised:

1. **Take a snapshot** (if your VPS provider supports it)
2. **Backup important data**
3. **Reinstall Ubuntu** from scratch
4. Follow this guide from Step 1

---

**Remember**: Prevention is better than cure. Keep your system updated, use strong passwords, enable 2FA where possible, and monitor regularly!
