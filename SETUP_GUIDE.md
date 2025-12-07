# 🍅 Tomato Leaf Disease Detection - Complete Setup Guide

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Quick Start](#quick-start)
3. [Detailed Setup](#detailed-setup)
4. [Running the Application](#running-the-application)
5. [Backend Configuration](#backend-configuration)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

This is a complete Flutter mobile application for detecting diseases in tomato leaves using AI/ML. The app allows users to:
- 📸 Capture photos of tomato leaves using the camera
- 🖼️ Import images from the gallery
- 🔍 Analyze leaves for disease detection
- 📊 View confidence scores and treatment recommendations

**Technology Stack:**
- **Frontend:** Flutter/Dart
- **Backend:** Flask (Python)
- **ML Model:** TensorFlow/Keras

---

## ⚡ Quick Start

### Prerequisites
- Flutter SDK 3.10.1+
- Android Studio / Xcode (for mobile deployment)
- Python 3.8+ (for backend)

### Install Dependencies
\`\`\`bash
# Navigate to project directory
cd /home/mynul-islam/projects/tomatoleafdiseasedetection/tomatoleafdiseasedetection

# Install Flutter packages
flutter pub get
\`\`\`

---

## 🔧 Detailed Setup

### Step 1: Flutter Application Setup

#### 1.1 Project Structure
\`\`\`
lib/
├── main.dart                      # App entry point
├── models/
│   └── prediction_result.dart     # Response data model
├── screens/
│   ├── home_screen.dart           # Image selection screen
│   ├── scan_screen.dart           # Image preview & scanning
│   └── result_screen.dart         # Results display
└── services/
    └── api_service.dart           # Backend API client
\`\`\`

#### 1.2 Dependencies (Already Added)
\`\`\`yaml
dependencies:
  image_picker: ^1.1.2      # Camera & gallery access
  http: ^1.2.2              # HTTP requests
  path_provider: ^2.1.4     # File system paths
\`\`\`

#### 1.3 Permissions (Already Configured)

**Android** (`android/app/src/main/AndroidManifest.xml`):
- ✅ INTERNET
- ✅ CAMERA
- ✅ READ_EXTERNAL_STORAGE
- ✅ WRITE_EXTERNAL_STORAGE

**iOS** (`ios/Runner/Info.plist`):
- ✅ NSCameraUsageDescription
- ✅ NSPhotoLibraryUsageDescription

### Step 2: Backend Configuration

#### 2.1 Update Backend URL

Edit \`lib/services/api_service.dart\` and set the correct backend URL:

\`\`\`dart
static const String baseUrl = 'YOUR_BACKEND_URL';
\`\`\`

**Configuration Options:**

| Environment | URL | Use Case |
|-------------|-----|----------|
| Android Emulator | \`http://10.0.2.2:5000\` | Testing on Android emulator |
| iOS Simulator | \`http://localhost:5000\` | Testing on iOS simulator |
| Physical Device | \`http://192.168.x.x:5000\` | Testing on real device (same WiFi) |
| Production | \`https://your-api.com\` | Production deployment |

**Find Your Local IP (for physical devices):**
\`\`\`bash
# Linux/Mac
hostname -I

# Windows
ipconfig
\`\`\`

#### 2.2 Backend Setup

Your backend should implement these endpoints:

**1. Health Check Endpoint**
\`\`\`
GET /health
Response: { "status": "healthy", "model_loaded": true }
\`\`\`

**2. Prediction Endpoint**
\`\`\`
POST /predict
Content-Type: multipart/form-data
Body: file (image file)

Response: {
  "disease": "Early Blight",
  "confidence": 0.95,
  "description": "Disease description...",
  "treatment": ["Step 1", "Step 2", ...]
}
\`\`\`

See \`BACKEND_REFERENCE.py\` for a complete Flask implementation example.

---

## 🚀 Running the Application

### Option 1: Run on Android Emulator

\`\`\`bash
# Start Android emulator (if not running)
# Then run:
flutter run
\`\`\`

### Option 2: Run on Physical Device

\`\`\`bash
# Enable USB debugging on your Android device
# Connect via USB
# Then run:
flutter run
\`\`\`

### Option 3: Run on iOS Simulator (macOS only)

\`\`\`bash
# Open iOS simulator
open -a Simulator

# Run app
flutter run -d ios
\`\`\`

### List Available Devices

\`\`\`bash
flutter devices
\`\`\`

### Run on Specific Device

\`\`\`bash
flutter run -d <device-id>
\`\`\`

---

## 🔌 Backend Configuration

### Starting the Backend Server

If you have a backend in \`/home/mynul-islam/projects/backend\`:

\`\`\`bash
cd /home/mynul-islam/projects/backend

# Install dependencies (first time only)
pip install flask flask-cors tensorflow pillow numpy werkzeug

# Run server
python main.py
\`\`\`

The server should start on \`http://0.0.0.0:5000\`

### Backend Requirements

Your backend needs:
- Flask web server
- ML model (TensorFlow/Keras)
- Image preprocessing
- Disease classification logic

### Test Backend Connection

\`\`\`bash
# Test health endpoint
curl http://localhost:5000/health

# Expected response:
# {"status":"healthy","model_loaded":true}
\`\`\`

---

## 🐛 Troubleshooting

### Issue: "Cannot connect to server"

**Solutions:**
1. Ensure backend server is running
2. Check firewall isn't blocking port 5000
3. Verify correct IP address in \`api_service.dart\`
4. For Android emulator: Use \`10.0.2.2\` instead of \`localhost\`
5. For physical device: Ensure device and computer are on same WiFi

**Debug Steps:**
\`\`\`bash
# Check if server is running
curl http://localhost:5000/health

# Test from your device IP
curl http://YOUR_IP:5000/health
\`\`\`

### Issue: "Camera permission denied"

**Solutions:**
1. Go to device Settings > Apps > Your App > Permissions
2. Enable Camera and Storage permissions
3. Reinstall the app if needed

### Issue: "Build failed"

**Solutions:**
\`\`\`bash
# Clean build artifacts
flutter clean

# Get dependencies again
flutter pub get

# Try running again
flutter run
\`\`\`

### Issue: "Image picker not working"

**Solutions:**
1. Check Android/iOS permissions are configured
2. For Android API 30+, ensure proper storage permissions
3. Try on a physical device instead of emulator

### Issue: "Model prediction errors"

**Solutions:**
1. Verify ML model is loaded correctly in backend
2. Check image preprocessing matches model requirements
3. Ensure model input size matches preprocessed image size
4. Verify class names match model output

---

## 📝 App Flow

1. **Home Screen**
   - User selects "Take Photo" or "Choose from Gallery"
   - Image picker opens camera or gallery
   
2. **Scan Screen**
   - Selected image is displayed
   - User taps "Scan for Disease"
   - Image is sent to backend API
   - Loading indicator shows during processing
   
3. **Result Screen**
   - Disease name displayed
   - Confidence score shown with color-coded progress bar
   - Disease description provided
   - Treatment recommendations listed
   - User can scan another leaf

---

## 🎨 Customization

### Change App Theme

Edit \`lib/main.dart\`:

\`\`\`dart
theme: ThemeData(
  colorScheme: ColorScheme.fromSeed(
    seedColor: Colors.green, // Change this color
  ),
),
\`\`\`

### Add More Disease Info

Update backend's \`DISEASE_INFO\` dictionary with additional diseases and treatments.

### Modify UI Colors

All screens use consistent green theme. To change:
- Search for \`Colors.green.shade700\`
- Replace with your preferred color

---

## 📱 Testing

### Test Image Capture
1. Open app on device/emulator
2. Tap "Take Photo"
3. Verify camera opens
4. Capture image
5. Verify image appears on scan screen

### Test Gallery Selection
1. Open app
2. Tap "Choose from Gallery"
3. Select an image
4. Verify image appears on scan screen

### Test Disease Detection
1. Select a tomato leaf image
2. Tap "Scan for Disease"
3. Verify loading indicator appears
4. Check results are displayed correctly

---

## 🚢 Deployment

### Android APK

\`\`\`bash
flutter build apk --release
\`\`\`

APK location: \`build/app/outputs/flutter-apk/app-release.apk\`

### iOS App

\`\`\`bash
flutter build ios --release
\`\`\`

### Backend Deployment

Deploy Flask backend to:
- Heroku
- AWS EC2
- Google Cloud Platform
- DigitalOcean
- Railway

Update \`api_service.dart\` with production URL.

---

## 📞 Support

For issues or questions:
1. Check this documentation
2. Review error messages in console
3. Run \`flutter doctor\` to check environment
4. Check backend logs for API errors

---

## ✅ Checklist

Before running the app:

- [ ] Flutter SDK installed (\`flutter doctor\`)
- [ ] Dependencies installed (\`flutter pub get\`)
- [ ] Backend server running
- [ ] Backend URL configured in \`api_service.dart\`
- [ ] Device/emulator ready
- [ ] Permissions granted on device
- [ ] Backend health endpoint responding

---

## 🎉 You're Ready!

Your tomato leaf disease detection app is now ready to use. Run \`flutter run\` and start detecting diseases!

For any updates or improvements, feel free to modify the code. The app is built with clean architecture and is easy to extend.

Happy coding! 🚀
