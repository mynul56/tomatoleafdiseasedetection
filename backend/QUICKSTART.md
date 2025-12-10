# 🚀 Quick Start - Get Pre-trained Model

You're in the `backend/` directory. Here's the fastest way to get accurate predictions:

## ⚡ 3 Steps to Get Started (5 minutes)

### Step 1: Download a Pre-trained Model

**Option A: Kaggle (Best Quality)**
```bash
# 1. Visit Kaggle and download a model:
#    https://www.kaggle.com/search?q=tomato+leaf+disease+model
# 
# Recommended datasets:
#    - https://www.kaggle.com/datasets/arshid/tomato-leaf-disease-detection
#    - https://www.kaggle.com/datasets/kaustubhb999/tomatoleaf

# 2. After downloading, move it here:
mv ~/Downloads/downloaded_model.h5 tomato_resnet50_model.h5
```

**Option B: Use Kaggle CLI (Automated)**
```bash
# 1. Get Kaggle credentials:
#    - Go to: https://www.kaggle.com/settings/account
#    - Click "Create New Token" under API
#    - Save kaggle.json

# 2. Configure Kaggle:
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# 3. Download model:
source venv/bin/activate
kaggle datasets download -d arshid/tomato-leaf-disease-detection
unzip tomato-leaf-disease-detection.zip
# Find and rename the .h5 file to tomato_resnet50_model.h5
```

### Step 2: Verify Model

```bash
source venv/bin/activate
python auto_download_model.py
```

### Step 3: Start Server

```bash
source venv/bin/activate
python app.py
```

## ✅ Verify It's Working

```bash
# Health check
curl http://localhost:5005/health

# Test prediction (if you have a test image)
curl -X POST -F "image=@test_leaf.jpg" http://localhost:5005/predict
```

## 🎯 What You Need

✅ **Virtual environment created** (`venv/`)  
✅ **Packages installed** (tensorflow, flask, etc.)  
⏳ **Pre-trained model** (download from links above)

## 📊 Current Status

Run this to check:
```bash
source venv/bin/activate
python auto_download_model.py
```

## 🚀 Deploy to VPS

Once working locally:
```bash
bash deploy_to_vps.sh
```

## 🆘 Troubleshooting

**"No model found"**
- Download from Kaggle links above
- Rename to exactly: `tomato_resnet50_model.h5`
- Place in this `backend/` directory

**"Model won't load"**
- Check file size (should be 50-150 MB)
- Verify it's a Keras model: `file tomato_resnet50_model.h5`

**"Dependencies missing"**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

**Need more help?** See `GETTING_STARTED.md` for detailed options.
