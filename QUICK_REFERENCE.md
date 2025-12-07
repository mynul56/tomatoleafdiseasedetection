# 🚀 Quick Reference Card

## Essential Commands

### Setup & Install
```bash
# Install dependencies
flutter pub get

# Check Flutter environment
flutter doctor

# List available devices
flutter devices
```

### Running the App
```bash
# Run on default device
flutter run

# Run on specific device
flutter run -d <device-id>

# Run on Android emulator
flutter run -d emulator-5554

# Run with hot reload enabled (default)
flutter run
# Then press 'r' for hot reload, 'R' for hot restart
```

### Building
```bash
# Build Android APK
flutter build apk --release

# Build Android App Bundle
flutter build appbundle --release

# Build iOS app
flutter build ios --release
```

### Debugging
```bash
# Clean build
flutter clean

# Analyze code
flutter analyze

# Run tests
flutter test

# View logs
flutter logs
```

## Backend URLs

| Environment | URL |
|-------------|-----|
| Android Emulator | `http://10.0.2.2:5000` |
| iOS Simulator | `http://localhost:5000` |
| Physical Device | `http://YOUR_IP:5000` |

**Find your IP:**
```bash
# Linux/Mac
hostname -I | awk '{print $1}'

# Windows
ipconfig | findstr IPv4
```

## Key Files to Edit

### Change Backend URL
📁 `lib/services/api_service.dart`
```dart
static const String baseUrl = 'http://10.0.2.2:5000';
```

### Change App Theme
📁 `lib/main.dart`
```dart
colorScheme: ColorScheme.fromSeed(seedColor: Colors.green),
```

### Adjust Image Quality
📁 `lib/screens/home_screen.dart`
```dart
maxWidth: 1024,
maxHeight: 1024,
imageQuality: 85,  // 0-100
```

## API Response Format

```json
{
  "disease": "Early Blight",
  "confidence": 0.95,
  "description": "Disease description text",
  "treatment": [
    "Treatment step 1",
    "Treatment step 2"
  ]
}
```

## Common Issues & Solutions

### "Cannot connect to server"
✅ Check backend is running
✅ Verify correct IP in api_service.dart
✅ For Android emulator, use 10.0.2.2

### "Permission denied"
✅ Grant camera/storage permissions in device settings
✅ Reinstall app if needed

### "Build failed"
```bash
flutter clean
flutter pub get
flutter run
```

### Camera not working
✅ Test on physical device (emulator cameras limited)
✅ Check permissions granted
✅ Verify AndroidManifest.xml and Info.plist

## File Structure

```
lib/
├── main.dart                   # App entry
├── models/
│   └── prediction_result.dart  # Data model
├── screens/
│   ├── home_screen.dart        # Image selection
│   ├── scan_screen.dart        # Image preview
│   └── result_screen.dart      # Results
└── services/
    └── api_service.dart        # API client
```

## App Flow

```
Home → Select Image → Scan → View Results → Home
```

## Testing Checklist

- [ ] Camera opens and captures image
- [ ] Gallery opens and selects image
- [ ] Image displays on scan screen
- [ ] Scan button shows loading
- [ ] Error message if server down
- [ ] Results display correctly
- [ ] "Scan Another Leaf" returns to home

## Backend Testing

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test prediction (with image file)
curl -X POST -F "file=@test_image.jpg" http://localhost:5000/predict
```

## Useful Flutter Commands During Development

```bash
# Hot reload (in running app terminal)
r

# Hot restart
R

# Clear screen
c

# Quit
q

# Toggle performance overlay
P

# Take screenshot
s
```

## Package Versions

```yaml
image_picker: ^1.1.2
http: ^1.2.2
path_provider: ^2.1.4
cupertino_icons: ^1.0.8
```

## Device Requirements

- **Android:** API 21+ (Android 5.0+)
- **iOS:** iOS 10.0+
- **Storage:** ~50MB for app
- **Permissions:** Camera, Storage, Internet

## Performance Tips

1. Images auto-resized to reduce upload time
2. Server health checked before requests
3. Timeouts set to 5 seconds
4. Clean loading states
5. Efficient state management

## Documentation Files

- 📘 **SETUP_GUIDE.md** - Complete setup instructions
- 📗 **PROJECT_SUMMARY.md** - Project overview
- 📙 **ARCHITECTURE.md** - Technical architecture
- 📕 **APP_README.md** - App documentation
- 🐍 **BACKEND_REFERENCE.py** - Backend template

## Support

For detailed information, see **SETUP_GUIDE.md**

---

**Quick Start:**
```bash
./setup.sh          # Run setup
flutter run         # Launch app
```

**That's it! Happy coding! 🎉**
