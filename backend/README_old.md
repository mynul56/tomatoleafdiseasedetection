# Tomato Leaf Disease Detection Backend

## Overview
This backend uses a pre-trained **ResNet50** model from HuggingFace to detect 10 different tomato leaf diseases with high accuracy.

## Model Information
- **Model**: wellCh4n/tomato-leaf-disease-classification-resnet50
- **Source**: HuggingFace Transformers
- **Architecture**: ResNet50
- **Classes**: 10 disease types

## Supported Diseases
1. Healthy
2. Bacterial Spot
3. Early Blight
4. Late Blight
5. Leaf Mold
6. Septoria Leaf Spot
7. Spider Mites (Two-spotted Spider Mite)
8. Target Spot
9. Tomato Mosaic Virus
10. Tomato Yellow Leaf Curl Virus

## Setup

### Local Development

1. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server**:
   ```bash
   python app.py
   ```

   The server will start on `http://0.0.0.0:5005`

## API Endpoints

### GET /
API documentation and usage information

### GET /health
Health check endpoint

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "num_classes": 10
}
```

### POST /predict
Predict disease from uploaded image

**Request**:
- Method: POST
- Content-Type: multipart/form-data
- Body: image file with key "image"

**Example using curl**:
```bash
curl -X POST \
  -F "image=@/path/to/tomato_leaf.jpg" \
  http://localhost:5005/predict
```

**Response**:
```json
{
  "success": true,
  "disease": "Early Blight",
  "confidence": 0.95,
  "description": "Early blight creates concentric rings (target spots) on lower leaves first.",
  "treatment": "Remove infected leaves, improve air circulation, mulch to prevent soil splash, and apply fungicides containing chlorothalonil or copper.",
  "full_label": "A tomato leaf with Early Blight",
  "top_predictions": [
    {
      "disease": "Early Blight",
      "confidence": 0.95,
      "full_label": "A tomato leaf with Early Blight"
    },
    {
      "disease": "Target Spot",
      "confidence": 0.03,
      "full_label": "A tomato leaf with Target Spot"
    },
    {
      "disease": "Septoria Leaf Spot",
      "confidence": 0.01,
      "full_label": "A tomato leaf with Septoria Leaf Spot"
    }
  ]
}
```

## Deployment

### Production Server
For production deployment, use a WSGI server like **gunicorn**:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5005 app:app
```

### Environment Variables
- `PORT`: Server port (default: 5005)

## Model Files
The model is downloaded from HuggingFace and stored in the `hf_model/` directory:
- `config.json`: Model configuration and class labels
- `model.safetensors`: Model weights (PyTorch format)
- `preprocessor_config.json`: Image preprocessing configuration

The model is automatically converted from PyTorch to TensorFlow when loaded for the first time.

## Development Notes

### Model Loading
The model uses HuggingFace Transformers library and is loaded with:
```python
from transformers import TFResNetForImageClassification, AutoImageProcessor

model = TFResNetForImageClassification.from_pretrained('./hf_model', from_pt=True)
processor = AutoImageProcessor.from_pretrained('./hf_model')
```

### Image Processing
Images are processed using the AutoImageProcessor which:
1. Resizes to 224x224 pixels
2. Normalizes pixel values
3. Converts to the correct tensor format

### Prediction Flow
1. Client uploads image via POST request
2. Image is read and converted to RGB
3. Processed with AutoImageProcessor
4. Model makes prediction
5. Results include top prediction + confidence + top 3 alternatives
6. Disease information and treatment recommendations returned

## Troubleshooting

### Model Loading Issues
If you get "No module named 'torch'" error:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### CUDA Warnings
CUDA warnings (GPU-related) can be ignored if running on CPU. The model will automatically use CPU.

### Port Already in Use
If port 5005 is already in use:
```bash
export PORT=5006
python app.py
```

## License
This backend uses the pre-trained model from HuggingFace. Model license: See https://huggingface.co/wellCh4n/tomato-leaf-disease-classification-resnet50
