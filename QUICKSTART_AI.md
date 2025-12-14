# Quick Start: AI Assistant

## Step 1: Get Your Groq API Key (Free)

1. **Visit Groq Console**
   - Go to: https://console.groq.com/
   - Click "Sign Up" or "Log In"

2. **Sign Up (if new user)**
   - Use your Google/GitHub account or email
   - Complete the registration

3. **Create API Key**
   - Once logged in, click on "API Keys" in the sidebar
   - Click "Create API Key" button
   - Give it a name (e.g., "Tomato Leaf App")
   - Copy the API key (starts with `gsk_...`)
   
   ⚠️ **Important**: Save this key securely - you won't be able to see it again!

## Step 2: Configure the App

1. **Open the config file**
   - Navigate to: `lib/config/api_config.dart`

2. **Paste your API key**
   ```dart
   class ApiConfig {
     static const String groqApiKey = 'gsk_YOUR_ACTUAL_KEY_HERE';
     static const String backendUrl = 'http://206.162.244.175:5005';
   }
   ```

3. **Save the file**

## Step 3: Run the App

```bash
flutter run
```

## Step 4: Test the AI Assistant

1. Open the app
2. Tap the "AI Assistant" button (blue button with brain icon)
3. Try asking:
   - "What is Early Blight?"
   - "How do I treat Bacterial Spot?"
   - "What causes Tomato Mosaic Virus?"

## Voice Features

### Using Voice Input (Speech-to-Text)
1. Tap the microphone icon (🎤) at the bottom
2. Grant microphone permission when prompted
3. Speak your question clearly
4. The app will automatically transcribe and send your message

### Using Voice Output (Text-to-Speech)
1. After receiving an AI response
2. Tap the "Listen" text with speaker icon
3. The app will read the response aloud

## Example Questions to Try

**Disease Information:**
- "Tell me about Late Blight"
- "What are the symptoms of Spider Mites?"
- "How serious is Yellow Leaf Curl Virus?"

**Treatment Advice:**
- "How do I treat Early Blight organically?"
- "What fungicide works for Septoria Leaf Spot?"
- "Can I save a plant with Mosaic Virus?"

**Prevention:**
- "How can I prevent tomato diseases?"
- "What spacing should I use to prevent disease?"
- "Should I water from above or below?"

**General Care:**
- "What nutrients do tomato plants need?"
- "When should I prune tomato plants?"
- "How much sunlight do tomatoes need?"

## Troubleshooting

### Can't get API key?
- Make sure you've verified your email with Groq
- Check if you're logged in properly
- Try using a different browser

### App shows "Failed to get response"?
- Verify your API key is copied correctly
- Check your internet connection
- Make sure the API key doesn't have extra spaces

### Voice not working?
- Grant microphone permission in device settings
- Check if microphone is working in other apps
- Try restarting the app

### Still need help?
- Check the full guide: `AI_ASSISTANT_README.md`
- Verify all permissions are granted in device settings
- Try clearing app data and relaunching

## Free Usage Limits

Groq offers generous free tier:
- High request limits
- Fast response times
- No credit card required initially

Monitor your usage at: https://console.groq.com/

---

**That's it! You're ready to use the AI Assistant! 🎉**
