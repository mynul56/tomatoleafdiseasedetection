# Tomato Leaf Disease Detection App

A Flutter mobile application that detects diseases in tomato leaves using machine learning. Users can capture or import images of tomato leaves, and the app will identify potential diseases with confidence scores and treatment recommendations.

## Features

- 📸 **Capture Images**: Take photos directly with your device camera
- 🖼️ **Import Images**: Select images from your gallery
- 🔍 **Disease Detection**: AI-powered disease identification
- 📊 **Confidence Scores**: View prediction confidence levels
- 💊 **Treatment Info**: Get disease descriptions and treatment recommendations
- 🎨 **Modern UI**: Clean, intuitive interface with Material Design

## Prerequisites

- Flutter SDK (3.10.1 or higher)
- Dart SDK
- Android Studio / Xcode (for iOS)
- Python backend server running (see backend setup below)

## Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd tomatoleafdiseasedetection
```

### 2. Install Dependencies

```bash
flutter pub get
```

### 3. Configure Backend URL

Edit `lib/services/api_service.dart` and update the `baseUrl`:

```dart
// For Android Emulator
static const String baseUrl = 'http://10.0.2.2:5000';

// For iOS Simulator
static const String baseUrl = 'http://localhost:5000';

// For Physical Device (use your computer's local IP)
static const String baseUrl = 'http://192.168.x.x:5000';
```

### 4. Run the App

```bash
# For Android
flutter run

# For iOS
flutter run -d ios

# For specific device
flutter devices  # List available devices
flutter run -d <device-id>
```

## Backend Setup

The app requires a Flask backend server for disease detection.

### Backend Structure

The backend should have:
- Flask server with `/predict` endpoint
- TensorFlow/Keras model for disease detection
- `/health` endpoint for server status

### Example Backend Response Format

```json
{
  "disease": "Early Blight",
  "confidence": 0.95,
  "description": "Early blight is a common fungal disease...",
  "treatment": [
    "Remove infected leaves",
    "Apply fungicide",
    "Improve air circulation"
  ]
}
```

### Starting the Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

The server should run on `http://localhost:5000`

## Project Structure

```
lib/
├── main.dart                 # App entry point
├── models/
│   └── prediction_result.dart # Data model for API response
├── screens/
│   ├── home_screen.dart      # Home screen with image selection
│   ├── scan_screen.dart      # Image preview and scanning
│   └── result_screen.dart    # Detection results display
└── services/
    └── api_service.dart      # Backend API communication
```

## Permissions

### Android
The following permissions are automatically configured:
- `INTERNET` - For API communication
- `CAMERA` - For capturing photos
- `READ_EXTERNAL_STORAGE` - For gallery access

### iOS
Required permissions in Info.plist:
- `NSCameraUsageDescription` - Camera access
- `NSPhotoLibraryUsageDescription` - Photo library access

## Dependencies

- `image_picker: ^1.1.2` - Image capture and selection
- `http: ^1.2.2` - HTTP requests to backend
- `path_provider: ^2.1.4` - File system paths

## Troubleshooting

### Cannot Connect to Server

1. Ensure the backend server is running
2. Check the correct IP address is configured in `api_service.dart`
3. For Android emulator, use `10.0.2.2` instead of `localhost`
4. For physical devices, ensure your phone and computer are on the same network

### Camera Not Working

1. Check permissions are granted in device settings
2. For Android, ensure manifest permissions are correct
3. For iOS, check Info.plist has usage descriptions

### Build Errors

```bash
# Clean build
flutter clean
flutter pub get
flutter run
```

## Screenshots

[Add screenshots of your app here]

## Future Enhancements

- [ ] Offline mode with local ML model
- [ ] History of scanned leaves
- [ ] Multiple language support
- [ ] Share results feature
- [ ] Disease prevention tips

## License

[Your License Here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
