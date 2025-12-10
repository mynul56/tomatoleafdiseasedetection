# Tomato Leaf Disease Detection Backend

Complete backend implementation using ResNet50 with transfer learning for detecting all 10 tomato leaf diseases.

## 🎯 Overview

This backend provides a REST API for detecting tomato leaf diseases using a deep learning model based on ResNet50 architecture with transfer learning from ImageNet.

### Supported Diseases (10 Classes)

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

## 📁 Project Structure

```
backend/
├── app.py                      # Flask API server (production)
├── train.py                    # Model training script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── tomato_resnet50_model.h5   # Trained model (generated after training)
├── training_history.png        # Training plots (generated after training)
├── uploads/                    # Temporary upload folder
└── data/                       # Dataset folder (see setup below)
    └── tomato_dataset/
        ├── train/
        │   ├── Tomato___Bacterial_spot/
        │   ├── Tomato___Early_blight/
        │   ├── Tomato___Late_blight/
        │   ├── Tomato___Leaf_Mold/
        │   ├── Tomato___Septoria_leaf_spot/
        │   ├── Tomato___Spider_mites Two-spotted_spider_mite/
        │   ├── Tomato___Target_Spot/
        │   ├── Tomato___Tomato_Yellow_Leaf_Curl_Virus/
        │   ├── Tomato___Tomato_mosaic_virus/
        │   └── Tomato___healthy/
        └── val/
            └── [same structure as train/]
```

## 🚀 Quick Start

### ⚡ Fastest Way (Pre-trained Model - Recommended)

**If you don't have time to train, use a pre-trained model:**

1. **Download pre-trained model from Kaggle:**
   ```bash
   # Search for: "tomato disease resnet model h5"
   # Or visit: https://www.kaggle.com/search?q=tomato+disease+h5
   ```

2. **Place model in backend folder:**
   ```bash
   # Rename downloaded file to:
   mv downloaded_model.h5 tomato_resnet50_model.h5
   ```

3. **Start server:**
   ```bash
   pip install -r requirements.txt
   python app.py
   ```

### 🤖 Automated Setup (One Command)

```bash
cd backend
bash setup_backend.sh
```

This script will:
- Install dependencies
- Check for existing model
- Offer to download dataset
- Optionally train model
- Test everything

### 🎓 Train Your Own Model (Most Accurate)

**Option A: Quick Training (30-60 minutes with GPU)**
```bash
# 1. Download dataset
python prepare_dataset.py --download

# 2. Quick train with MobileNetV2
python quick_train.py
```

**Option B: Full Training (2-4 hours, best accuracy)**
```bash
# 1. Download dataset
python prepare_dataset.py --download

# 2. Full training with ResNet50
python train.py
```

**Option C: Google Colab (FREE GPU)**
```bash
# 1. Open: https://colab.research.google.com
# 2. Upload train.py and prepare_dataset.py
# 3. Enable GPU: Runtime > Change runtime type > GPU
# 4. Run training (faster with GPU!)
# 5. Download model and place in backend/
```

## 📡 API Endpoints

### Health Check

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

### Predict Disease

```bash
POST /predict
Content-Type: multipart/form-data

Body:
  image: <image_file>
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
    {
      "disease": "Early Blight",
      "confidence": 98.45
    },
    {
      "disease": "Late Blight",
      "confidence": 1.32
    },
    {
      "disease": "Septoria Leaf Spot",
      "confidence": 0.23
    }
  ]
}
```

## 🧪 Testing the API

### Using cURL

```bash
# Health check
curl http://localhost:5005/health

# Predict disease
curl -X POST -F "image=@/path/to/tomato_leaf.jpg" http://localhost:5005/predict
```

### Using Python

```python
import requests

# Health check
response = requests.get('http://localhost:5005/health')
print(response.json())

# Predict disease
with open('tomato_leaf.jpg', 'rb') as f:
    files = {'image': f}
    response = requests.post('http://localhost:5005/predict', files=files)
    print(response.json())
```

## 🐳 Docker Deployment (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5005

CMD ["python", "app.py"]
```

```bash
docker build -t tomato-disease-api .
docker run -p 5005:5005 tomato-disease-api
```

## 🌐 VPS Deployment

### Deploy to VPS (Ubuntu)

```bash
# 1. SSH into VPS
ssh user@206.162.244.175

# 2. Clone repository
git clone <your-repo-url>
cd backend

# 3. Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Copy trained model to VPS
# (from local machine)
scp tomato_resnet50_model.h5 user@206.162.244.175:~/backend/

# 5. Create systemd service
sudo nano /etc/systemd/system/tomato-api.service
```

**systemd Service Configuration:**

```ini
[Unit]
Description=Tomato Disease Detection API
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/backend
Environment="PATH=/home/your-username/backend/venv/bin"
ExecStart=/home/your-username/backend/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 6. Start service
sudo systemctl daemon-reload
sudo systemctl start tomato-api
sudo systemctl enable tomato-api
sudo systemctl status tomato-api
```

## 🔧 Model Architecture

### ResNet50 with Transfer Learning

```
Input (224x224x3)
    ↓
ResNet50 Base (ImageNet pretrained, frozen)
    ↓
Global Average Pooling
    ↓
Dense(512, ReLU) + Dropout(0.5)
    ↓
Dense(256, ReLU) + Dropout(0.3)
    ↓
Dense(10, Softmax)
    ↓
Output (10 disease classes)
```

**Key Features:**
- Pre-trained on ImageNet (1.2M images, 1000 classes)
- Transfer learning: leverages learned features
- Custom classification head for tomato diseases
- Dropout layers prevent overfitting
- Data augmentation improves generalization

## 📊 Performance Metrics

**Expected Performance:**
- Validation Accuracy: 95-98%
- Top-3 Accuracy: 99%+
- Inference Time: ~100ms per image
- Model Size: ~100MB

**Confusion Matrix Analysis:**
- Highest accuracy: Healthy leaves (99%+)
- Common confusion: Early vs Late Blight
- Recommendation: Ensemble multiple predictions

## 🛠️ Troubleshooting

### Model not loading

```bash
# Check if model file exists
ls -lh tomato_resnet50_model.h5

# If missing, train the model
python train.py
```

### Out of memory during training

```python
# Reduce batch size in train.py
BATCH_SIZE = 16  # or 8
```

### Low accuracy

1. Ensure dataset quality (clean, diverse images)
2. Increase training epochs
3. Enable fine-tuning (uncomment in train.py)
4. Add more data augmentation

### Server not accessible from mobile

```bash
# Check firewall
sudo ufw allow 5005

# Verify server is listening on 0.0.0.0
netstat -tuln | grep 5005
```

## 📝 Model Training Tips

### For Best Accuracy:

1. **Dataset Quality:**
   - Minimum 1000 images per class
   - Diverse lighting conditions
   - Different leaf angles and backgrounds
   - Balanced class distribution

2. **Data Augmentation:**
   - Rotation (40°)
   - Horizontal/vertical flips
   - Zoom (20%)
   - Width/height shifts (20%)

3. **Training Strategy:**
   - Phase 1: Train only classification head (50 epochs)
   - Phase 2: Fine-tune last 20 layers (20 epochs)
   - Use early stopping to prevent overfitting
   - Monitor validation accuracy

4. **Hyperparameter Tuning:**
   - Learning rate: 0.0001 (initial), 0.00001 (fine-tuning)
   - Batch size: 32 (adjust based on GPU memory)
   - Image size: 224x224 (ResNet50 standard)

## 🤝 Integration with Flutter App

The Flutter app should connect to this backend:

```dart
// Update baseUrl in api_service.dart
final String baseUrl = 'http://206.162.244.175:5005';  // VPS
// or
final String baseUrl = 'http://10.0.2.2:5005';  // Android Emulator
```

## 📄 License

This project uses the PlantVillage dataset which is publicly available for research purposes.

## 🙏 Acknowledgments

- PlantVillage Dataset: https://www.kaggle.com/datasets/arjuntejaswi/plant-village
- ResNet50 Architecture: Deep Residual Learning (He et al., 2015)
- TensorFlow/Keras Framework

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review training logs: `training_history.png`
3. Test with health endpoint: `GET /health`
4. Verify model file exists and is loaded correctly

---

**Built with ❤️ for accurate tomato disease detection**
