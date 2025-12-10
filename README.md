# 🍅 Tomato Leaf - Disease Detection App

<div align="center">
  <img src="assets/images/tomato.jpg" alt="Tomato Leaf Logo" width="150"/>
  
  ### AI-Powered Tomato Leaf Disease Detection
  
  [![Flutter](https://img.shields.io/badge/Flutter-3.38.3-blue.svg)](https://flutter.dev/)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
  [![API](https://img.shields.io/badge/API-Public-brightgreen.svg)](http://206.162.244.175:5005)
</div>

---

## 📱 About The App

**Tomato Leaf** is a mobile application that uses deep learning (ResNet50) to detect diseases in tomato plants from leaf images. Simply take a photo or upload an image, and get instant disease diagnosis with treatment recommendations.

### ✨ Features

- 📸 **Capture or Upload** - Use camera or select from gallery
- 🧠 **AI-Powered Detection** - ResNet50 model with 95%+ accuracy
- 🔍 **10 Disease Classes** - Detects all major tomato leaf diseases
- 💊 **Treatment Guide** - Get detailed treatment recommendations
- 🎯 **Confidence Scores** - See prediction confidence and top-3 results
- 🌐 **Public API** - Free REST API for developers

### 🦠 Detected Diseases

1. **Bacterial Spot** - Xanthomonas infection
2. **Early Blight** - Alternaria solani fungus
3. **Late Blight** - Phytophthora infestans
4. **Leaf Mold** - Passalora fulva fungus
5. **Septoria Leaf Spot** - Septoria lycopersici fungus
6. **Spider Mites** - Two-spotted spider mite
7. **Target Spot** - Corynespora cassiicola fungus
8. **Yellow Leaf Curl Virus** - Whitefly-transmitted virus
9. **Tomato Mosaic Virus** - Contact-transmitted virus
10. **Healthy** - No disease detected

---

## 🚀 Quick Start

### For Users (Mobile App)

1. **Download the App**
   - Coming soon to Google Play Store
   - APK available in [Releases](https://github.com/mynul56/tomatoleafdiseasedetection/releases)

2. **Use the App**
   - Open app and tap "Scan Leaf"
   - Take photo or select from gallery
   - Get instant disease diagnosis
   - View treatment recommendations

### For Developers (Flutter App)

#### Prerequisites
- Flutter SDK (3.38.3 or higher)
- Dart SDK
- Android Studio / Xcode (for mobile development)

#### Installation

```bash
# Clone repository
git clone https://github.com/mynul56/tomatoleafdiseasedetection.git
cd tomatoleafdiseasedetection

# Install dependencies
flutter pub get

# Run the app
flutter run
```

### For Developers (Backend API)

**🎯 Want accurate predictions? See: [backend/GETTING_STARTED.md](backend/GETTING_STARTED.md)**

#### Quick Setup (5 minutes)

```bash
cd backend

# Option 1: Download pre-trained model (fastest)
# - Search Kaggle: https://www.kaggle.com/search?q=tomato+disease+h5
# - Download model.h5 file
# - Rename to: tomato_resnet50_model.h5

# Option 2: Auto-setup (downloads dataset + trains)
bash setup_backend.sh

# Start server
pip install -r requirements.txt
python app.py
```

**For detailed setup options, see [backend/GETTING_STARTED.md](backend/GETTING_STARTED.md)**

---

## 🌐 Public API Access

**Anyone can use our free public API!**

### Base URL
```
http://206.162.244.175:5005
```

### Endpoints

#### 1. Health Check
```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "model": "ResNet50",
  "model_loaded": true,
  "classes": 10,
  "class_names": ["Tomato___Bacterial_spot", ...]
}
```

#### 2. Predict Disease
```bash
POST /predict
Content-Type: multipart/form-data

Body:
  image: <image_file>
```

**Example using cURL:**
```bash
curl -X POST -F "image=@/path/to/tomato_leaf.jpg" \
  http://206.162.244.175:5005/predict
```

**Example using Python:**
```python
import requests

url = "http://206.162.244.175:5005/predict"
files = {'image': open('tomato_leaf.jpg', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

**Example using JavaScript:**
```javascript
const formData = new FormData();
formData.append('image', imageFile);

fetch('http://206.162.244.175:5005/predict', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

**Response:**
```json
{
  "disease": "Early Blight",
  "confidence": 98.45,
  "description": "Early blight is caused by the fungus Alternaria solani...",
  "treatment": [
    "Remove and destroy infected leaves immediately",
    "Apply copper-based fungicide every 7-10 days",
    "Improve air circulation by spacing plants properly",
    ...
  ],
  "top_predictions": [
    {"disease": "Early Blight", "confidence": 98.45},
    {"disease": "Late Blight", "confidence": 1.32},
    {"disease": "Septoria Leaf Spot", "confidence": 0.23}
  ]
}
```

### Rate Limits
- **No rate limits** - Free for everyone!
- Please be respectful and don't abuse the service
- For high-volume usage, consider deploying your own instance

---

## 🏗️ Architecture

### Mobile App (Flutter)
```
lib/
├── main.dart                    # App entry point
├── models/
│   └── prediction_result.dart   # Data models
├── screens/
│   ├── home_screen.dart         # Home with animated logo
│   ├── scan_screen.dart         # Camera/gallery picker
│   └── result_screen.dart       # Disease results
└── services/
    └── api_service.dart         # API integration
```

### Backend (Python/Flask)
```
backend/
├── app.py                       # Production API server
├── train.py                     # Model training script
├── test_model.py               # Testing utilities
├── prepare_dataset.py          # Dataset preparation
├── deploy_to_vps.sh            # Deployment script
└── README.md                   # Backend documentation
```

### ML Model
- **Architecture:** ResNet50 (Transfer Learning)
- **Pretrained on:** ImageNet (1.2M images)
- **Fine-tuned on:** PlantVillage Tomato Dataset
- **Input Size:** 224x224 RGB
- **Output:** 10 disease classes
- **Accuracy:** 95-98% validation accuracy

---

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| Validation Accuracy | 95-98% |
| Top-3 Accuracy | 99%+ |
| Inference Time | ~100ms |
| Model Size | ~100MB |

**Confusion Matrix Insights:**
- Highest accuracy: Healthy leaves (99%+)
- Common confusion: Early vs Late Blight
- Recommended: Check top-3 predictions for borderline cases

---

## 🛠️ Development

### Run Locally

```bash
# Flutter app
flutter run

# Backend server (local)
cd backend
pip install -r requirements.txt
python app.py
```

### Build for Production

```bash
# Android APK
flutter build apk --release

# iOS App
flutter build ios --release

# Deploy backend to VPS
cd backend
bash deploy_to_vps.sh
```

### Train Your Own Model

See [backend/README.md](backend/README.md) for detailed training instructions.

```bash
cd backend
python prepare_dataset.py --download
python train.py
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs** - Open an issue
2. **Suggest Features** - Create a feature request
3. **Submit PRs** - Fork, develop, and submit pull requests
4. **Improve Dataset** - Add more training images
5. **Translate** - Help translate to other languages

### Development Guidelines

```bash
# Fork the repository
git clone https://github.com/YOUR_USERNAME/tomatoleafdiseasedetection.git

# Create feature branch
git checkout -b feature/amazing-feature

# Make changes and commit
git commit -m "Add amazing feature"

# Push and create PR
git push origin feature/amazing-feature
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **PlantVillage Dataset** - Training data
- **ResNet Paper** - Deep Residual Learning (He et al., 2015)
- **TensorFlow/Keras** - ML framework
- **Flutter** - Cross-platform UI framework

---

## 📞 Contact & Support

- **Developer:** Mynul Islam
- **GitHub:** [@mynul56](https://github.com/mynul56)
- **Repository:** [tomatoleafdiseasedetection](https://github.com/mynul56/tomatoleafdiseasedetection)
- **Issues:** [Report Bug](https://github.com/mynul56/tomatoleafdiseasedetection/issues)

### API Status

Check API health: http://206.162.244.175:5005/health

---

## 🌟 Star History

If you find this project useful, please consider giving it a ⭐!

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/mynul56/tomatoleafdiseasedetection?style=social)
![GitHub forks](https://img.shields.io/github/forks/mynul56/tomatoleafdiseasedetection?style=social)
![GitHub issues](https://img.shields.io/github/issues/mynul56/tomatoleafdiseasedetection)
![GitHub pull requests](https://img.shields.io/github/issues-pr/mynul56/tomatoleafdiseasedetection)

---

<div align="center">
  <p>Built with ❤️ for farmers and agricultural professionals worldwide</p>
  <p><strong>Tomato Leaf</strong> - Protecting crops, one leaf at a time 🍅</p>
</div>

