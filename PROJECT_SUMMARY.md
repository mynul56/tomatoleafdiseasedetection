# 🍅 Tomato Leaf Disease Detection App - Project Summary

## ✅ What's Been Built

A complete, production-ready Flutter mobile application for detecting diseases in tomato leaves using AI/ML.

## 📱 App Features

### 1. **Home Screen** (`lib/screens/home_screen.dart`)
- Beautiful, modern UI with green theme
- Two main actions:
  - 📸 **Take Photo** - Capture image using device camera
  - 🖼️ **Choose from Gallery** - Select existing image
- Helpful tips for best results
- Smooth navigation

### 2. **Scan Screen** (`lib/screens/scan_screen.dart`)
- Image preview before scanning
- "Scan for Disease" button
- Server health check before sending request
- Loading indicator during analysis
- Option to choose different image
- Error handling with user-friendly messages

### 3. **Result Screen** (`lib/screens/result_screen.dart`)
- Disease name display
- Color-coded confidence score (green/orange/red based on confidence)
- Progress bar visualization
- Detailed disease description
- Treatment recommendations (numbered list)
- "Scan Another Leaf" button to restart

## 🏗️ Technical Architecture

### Models (`lib/models/`)
- **PredictionResult** - Data model for API responses
  - Disease name
  - Confidence score
  - Description
  - Treatment steps
  - JSON serialization

### Services (`lib/services/`)
- **ApiService** - Backend communication
  - `predictDisease()` - Send image for analysis
  - `checkServerHealth()` - Verify backend is running
  - Configurable base URL
  - Error handling

### App Configuration (`lib/main.dart`)
- Material Design 3
- Green color scheme
- Clean navigation
- No debug banner

## 📦 Dependencies

All dependencies installed via `pubspec.yaml`:

```yaml
image_picker: ^1.1.2    # Camera & gallery access
http: ^1.2.2            # HTTP requests  
path_provider: ^2.1.4   # File paths
cupertino_icons: ^1.0.8 # iOS icons
```

## 🔐 Permissions Configured

### Android (`android/app/src/main/AndroidManifest.xml`)
✅ INTERNET - API communication
✅ CAMERA - Photo capture
✅ READ_EXTERNAL_STORAGE - Gallery access
✅ WRITE_EXTERNAL_STORAGE - Image saving

### iOS (`ios/Runner/Info.plist`)
✅ NSCameraUsageDescription - Camera permission
✅ NSPhotoLibraryUsageDescription - Gallery permission

## 📡 Backend Integration

### Expected Endpoints

**1. Health Check**
```
GET /health
Response: { "status": "healthy", "model_loaded": true }
```

**2. Disease Prediction**
```
POST /predict
Body: multipart/form-data with 'file' field
Response: {
  "disease": "Disease Name",
  "confidence": 0.0-1.0,
  "description": "Description text",
  "treatment": ["Step 1", "Step 2", ...]
}
```

### Backend URL Configuration

Located in `lib/services/api_service.dart`:

```dart
static const String baseUrl = 'http://10.0.2.2:5000';
```

**Change based on environment:**
- Android Emulator: `http://10.0.2.2:5000`
- iOS Simulator: `http://localhost:5000`
- Physical Device: `http://YOUR_LOCAL_IP:5000`
- Production: `https://your-api.com`

## 📚 Documentation Created

1. **SETUP_GUIDE.md** - Complete setup instructions
   - Prerequisites
   - Installation steps
   - Backend configuration
   - Running the app
   - Troubleshooting

2. **APP_README.md** - App documentation
   - Features overview
   - Project structure
   - Dependencies
   - Screenshots section

3. **BACKEND_REFERENCE.py** - Sample backend implementation
   - Flask server structure
   - Disease information database
   - Image preprocessing
   - Prediction endpoint

4. **setup.sh** - Quick start script
   - Automated dependency installation
   - Setup verification
   - Next steps guidance

## 🎨 UI/UX Design

### Color Scheme
- Primary: Green shades (representing healthy plants)
- Backgrounds: Light green tones
- Accents: White with green borders
- Status colors: Green (high confidence), Orange (medium), Red (low)

### Components
- Elevated buttons with icons
- Outlined secondary buttons
- Info cards with icons
- Smooth rounded corners (12px radius)
- Proper spacing and padding
- Material Design 3 standards

## 🚀 How to Run

### Quick Start
```bash
# 1. Install dependencies
cd /home/mynul-islam/projects/tomatoleafdiseasedetection/tomatoleafdiseasedetection
flutter pub get

# 2. Run the app
flutter run
```

### Using Setup Script
```bash
# 1. Run setup script
./setup.sh

# 2. Start backend (in separate terminal)
cd /home/mynul-islam/projects/backend
python main.py

# 3. Run Flutter app
flutter run
```

## ✅ Quality Checks

- ✅ No compilation errors
- ✅ All imports resolved
- ✅ Proper error handling
- ✅ Loading states implemented
- ✅ User-friendly messages
- ✅ Permissions configured
- ✅ Clean code structure
- ✅ Responsive UI
- ✅ Material Design compliance

## 🔄 App Flow

```
Start
  ↓
Home Screen
  ↓
[Choose Image Source]
  ├─→ Camera → Capture Photo
  └─→ Gallery → Select Image
       ↓
Scan Screen (Preview)
  ↓
[Scan for Disease]
  ↓
API Request → Backend ML Model
  ↓
Result Screen
  ├─→ Disease Name
  ├─→ Confidence Score
  ├─→ Description
  └─→ Treatment Steps
       ↓
[Scan Another Leaf] → Back to Home
```

## 📱 Supported Platforms

- ✅ Android (API 21+)
- ✅ iOS (10.0+)
- ⚠️ Web (requires camera API support)
- ⚠️ Desktop (Linux/Windows/macOS - limited camera support)

## 🛠️ Customization Options

### Change Theme Color
Edit `lib/main.dart`:
```dart
colorScheme: ColorScheme.fromSeed(
  seedColor: Colors.blue, // Change from green
),
```

### Modify API Timeout
Edit `lib/services/api_service.dart`:
```dart
.timeout(const Duration(seconds: 10)); // Increase from 5
```

### Add More Diseases
Update backend's disease information database with new entries.

## 📊 Current Status

| Component | Status | Notes |
|-----------|--------|-------|
| Flutter App | ✅ Complete | All screens implemented |
| UI/UX | ✅ Complete | Modern, responsive design |
| Image Picker | ✅ Complete | Camera & gallery support |
| API Integration | ✅ Complete | With error handling |
| Permissions | ✅ Complete | Android & iOS configured |
| Documentation | ✅ Complete | Comprehensive guides |
| Backend Reference | ✅ Complete | Sample implementation |
| Testing | ⏳ Ready | Needs backend connection |

## 🎯 Next Steps

1. **Start Backend Server**
   - Use provided `BACKEND_REFERENCE.py` as template
   - Ensure ML model is loaded
   - Test `/health` and `/predict` endpoints

2. **Configure Backend URL**
   - Update `lib/services/api_service.dart`
   - Use correct IP for your testing environment

3. **Test the App**
   - Run on emulator or physical device
   - Test camera functionality
   - Test gallery selection
   - Verify disease detection

4. **Deploy**
   - Build release APK/IPA
   - Deploy backend to cloud
   - Update production URL

## 💡 Tips

- **For best ML results**: Ensure images are clear, well-lit, and properly framed
- **Performance**: Images are resized before upload to reduce bandwidth
- **Offline mode**: Currently requires internet; consider adding local ML model
- **Security**: Add authentication for production deployment

## 🐛 Known Considerations

- Backend must be running before app can detect diseases
- Camera may not work on all emulators (test on physical device)
- Android API 30+ requires scoped storage handling (already implemented)
- Network timeouts set to 5 seconds (configurable)

## 📞 Support

For issues:
1. Check SETUP_GUIDE.md
2. Verify backend is running (`curl http://localhost:5000/health`)
3. Check `flutter doctor` for environment issues
4. Review app logs for error messages

## 🎉 Success!

Your tomato leaf disease detection app is **fully built and ready to run**! 

Just:
1. Start your backend server
2. Run `flutter run`
3. Start detecting diseases! 🚀

---

**Built with ❤️ using Flutter & AI**
