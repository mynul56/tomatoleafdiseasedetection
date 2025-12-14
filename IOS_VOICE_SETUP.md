# iOS Setup for Voice Features

If you plan to run this app on iOS, you need to add microphone and speech recognition permissions to your `Info.plist` file.

## Location
`ios/Runner/Info.plist`

## Add These Entries

Add the following entries inside the `<dict>` tag in your Info.plist file:

```xml
<key>NSMicrophoneUsageDescription</key>
<string>This app needs access to your microphone for voice assistant features</string>

<key>NSSpeechRecognitionUsageDescription</key>
<string>This app needs access to speech recognition to transcribe your voice questions</string>
```

## Complete Example

Your Info.plist should look similar to this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>Tomato Leaf</string>
    
    <!-- Other existing keys... -->
    
    <!-- ADD THESE TWO ENTRIES -->
    <key>NSMicrophoneUsageDescription</key>
    <string>This app needs access to your microphone for voice assistant features</string>
    
    <key>NSSpeechRecognitionUsageDescription</key>
    <string>This app needs access to speech recognition to transcribe your voice questions</string>
    
    <!-- Rest of your config... -->
</dict>
</plist>
```

## Testing on iOS

After adding these entries:
1. Clean build: `flutter clean`
2. Get dependencies: `flutter pub get`
3. Run on iOS: `flutter run -d ios`
4. First time you tap the mic button, iOS will show a permission dialog
5. Grant the permission to use voice features

## Note
These permissions are only required for iOS. Android permissions are already configured in the AndroidManifest.xml file.
