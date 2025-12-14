# AI Assistant Setup Guide

## Overview
The AI Assistant feature uses Groq's powerful LLM (Llama 3.3 70B) to provide intelligent responses about tomato leaf diseases, treatments, and plant care. It also includes voice input and text-to-speech capabilities.

## Features
- 💬 Chat with AI about tomato diseases
- 🎤 Voice input (speech-to-text)
- 🔊 Voice output (text-to-speech)
- 🚀 Quick action buttons for common questions
- 📱 Beautiful, user-friendly interface

## Setup Instructions

### 1. Get Groq API Key
1. Visit [https://console.groq.com/](https://console.groq.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the API key

### 2. Configure API Key
Open `lib/config/api_config.dart` and replace `YOUR_GROQ_API_KEY_HERE` with your actual Groq API key:

```dart
class ApiConfig {
  static const String groqApiKey = 'gsk_xxxxxxxxxxxxxxxxxxxx';
  static const String backendUrl = 'http://206.162.244.175:5005';
}
```

### 3. Install Dependencies
Run the following command in your project directory:

```bash
flutter pub get
```

### 4. Grant Permissions
The app requires microphone permission for voice input. On first use, the app will request permission automatically.

For iOS, ensure you have added the microphone permission to `ios/Runner/Info.plist`:
```xml
<key>NSMicrophoneUsageDescription</key>
<string>We need microphone access for voice assistant</string>
<key>NSSpeechRecognitionUsageDescription</key>
<string>We need speech recognition for voice input</string>
```

### 5. Run the App
```bash
flutter run
```

## Usage

### Text Chat
1. Open the app and tap "AI Assistant" button
2. Type your question in the text field
3. Press send or hit Enter
4. Get instant AI-powered responses

### Voice Input
1. Tap the microphone icon (🎤)
2. Speak your question clearly
3. The app will transcribe and send your message automatically

### Voice Output
1. For any AI response, tap the "Listen" button
2. The app will read the response aloud using text-to-speech

### Quick Actions
Use the quick action chips at the top for common questions:
- Common Diseases
- Prevention Tips
- Treatment Guide

## Supported Topics
The AI assistant can help with:
- Identifying tomato leaf diseases
- Understanding disease symptoms
- Treatment recommendations
- Prevention methods
- General tomato plant care
- Disease progression information
- Soil and environmental conditions
- Organic vs chemical treatments

## Models Used
- **LLM**: Llama 3.3 70B Versatile (via Groq)
- **Speech Recognition**: Platform-native (Android/iOS)
- **Text-to-Speech**: Platform-native (Android/iOS)

## Troubleshooting

### "Microphone permission required"
- Go to device Settings → Apps → Tomato Leaf → Permissions
- Enable Microphone permission

### "Voice service not available"
- Ensure microphone permission is granted
- Check if device has a working microphone
- Restart the app

### "Failed to get response"
- Check internet connection
- Verify API key is correctly configured
- Ensure you have Groq API credits

### Voice recognition not working
- Speak clearly and loudly
- Check device microphone is working
- Try in a quiet environment
- Ensure speech recognition is supported on your device

## API Limits
- Groq offers generous free tier limits
- Check your usage at [console.groq.com](https://console.groq.com/)
- Consider upgrading for production use

## Privacy & Security
- API key should NEVER be committed to public repositories
- Consider using environment variables or secure storage in production
- Voice data is processed on-device (not sent to servers)
- Only text messages are sent to Groq API

## Cost Considerations
- Groq currently offers free API access with rate limits
- Monitor your usage in the Groq console
- Consider implementing caching for common questions
- Set up usage alerts to avoid unexpected costs

## Future Enhancements
- [ ] Chat history persistence
- [ ] Disease-specific conversation context
- [ ] Image analysis integration
- [ ] Offline mode with cached responses
- [ ] Multi-language support
- [ ] Custom voice settings
