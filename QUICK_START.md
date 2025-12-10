# 🍅 Tomato Leaf - Quick Reference Card

## 📱 App Information
- **Name:** Tomato Leaf
- **Package:** tomatoleaf
- **Version:** 1.0.0

## 🌐 API Endpoint
```
http://206.162.244.175:5005
```

## 🚀 Quick Commands

### Flutter App
```bash
flutter pub get
flutter run
flutter build apk --release
```

### Backend Setup (Choose One)

**Option 1: Pre-trained Model (5 min)**
```bash
# Download from Kaggle: https://www.kaggle.com/search?q=tomato+disease+h5
mv ~/Downloads/model.h5 backend/tomato_resnet50_model.h5
cd backend && python app.py
```

**Option 2: Auto Setup (1-4 hrs)**
```bash
cd backend
bash setup_backend.sh
```

**Option 3: Manual Training**
```bash
cd backend
python prepare_dataset.py --download
python quick_train.py  # or python train.py
```

### Server Commands
```bash
# Start locally
cd backend
python app.py

# Deploy to VPS
bash deploy_to_vps.sh

# Quick start
bash start_server.sh
```

### Test API
```bash
# Health check
curl http://localhost:5005/health
curl http://206.162.244.175:5005/health

# Predict
curl -X POST -F "image=@leaf.jpg" http://localhost:5005/predict
```

## 📊 Disease Classes (10)
1. Bacterial Spot
2. Early Blight
3. Late Blight
4. Leaf Mold
5. Septoria Leaf Spot
6. Spider Mites
7. Target Spot
8. Yellow Leaf Curl Virus
9. Tomato Mosaic Virus
10. Healthy

## 📖 Documentation
- **Setup Guide:** `backend/GETTING_STARTED.md` ⭐ READ THIS FIRST
- **Backend Docs:** `backend/README.md`
- **Project Status:** `PROJECT_STATUS.md`
- **Main README:** `README.md`

## ⚠️ Important Notes
- **No trained model = RANDOM predictions!**
- See `backend/GETTING_STARTED.md` for 3 ways to get accurate model
- API is public and free for everyone
- No rate limits

## 🔧 Troubleshooting
- Widget test error? ✅ Fixed (package renamed)
- No model? 📖 See GETTING_STARTED.md
- Inaccurate? 🎓 Train model or download pre-trained
- Server issues? 📦 `pip install -r requirements.txt`

## ✅ Production Checklist
- [ ] Model trained and tested
- [ ] Local server works
- [ ] Deployed to VPS
- [ ] Health check passes
- [ ] Test prediction works
- [ ] Flutter app connects
- [ ] Accuracy verified (>90%)

---
**Questions? Read the documentation or check GitHub issues!**
