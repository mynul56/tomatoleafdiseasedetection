# Voice Service Troubleshooting Guide

## ✅ Latest Fixes Applied

### What Was Fixed:
1. **Better null safety checks** - Changed `if (!isAvailable)` to `if (isAvailable != true)`
2. **Stop before start** - Now stops any ongoing listening before starting new session
3. **Prevent concurrent sessions** - Added check to prevent multiple simultaneous listening
4. **Auto re-initialization** - Voice service will try to re-initialize if not ready
5. **Better error callbacks** - Enhanced status and error handling in initialization

## 🎤 Testing Voice Feature

### Step 1: Grant Microphone Permission
1. Open the app
2. Go to AI Assistant (এআই সহায়ক)
3. When you first tap the microphone 🎤 button
4. Android will ask for permission
5. **Tap "Allow" or "অনুমতি দিন"**

### Step 2: Check System Settings (If Still Not Working)
1. Exit the app
2. Go to Android Settings → Apps
3. Find "Tomato Leaf" app
4. Tap "Permissions" (অনুমতি)
5. Make sure "Microphone" is **ALLOWED**
6. Restart the app

### Step 3: Test Voice Input
1. Open AI Assistant
2. Tap microphone 🎤 button
3. Wait for "শুনছি... এখন বলুন!" / "🎤 Listening... Speak now!"
4. Speak clearly:
   - **English**: "What is Early Blight?"
   - **Bangla**: "আর্লি ব্লাইট কি?"
5. Wait 2-3 seconds after speaking
6. Voice input will automatically send

## 🔍 Common Issues & Solutions

### Issue 1: "Failed to start listening"
**Cause**: Microphone permission not granted
**Solution**: 
- Go to Android Settings → Apps → Tomato Leaf → Permissions
- Enable Microphone permission
- Restart app

### Issue 2: "Voice service not available"
**Cause**: Speech recognition not initialized
**Solution**:
- Close and reopen the app
- Tap microphone button - it will try to re-initialize
- If still failing, check if your device supports speech recognition

### Issue 3: No sound when tapping 🔊 Listen button
**Cause**: Device volume is muted or too low
**Solution**:
- Increase device volume
- Check if media volume is on (not just ringtone)
- Test with other audio to confirm speakers work

### Issue 4: Voice input in wrong language
**Cause**: App language doesn't match speech language
**Solution**:
- Switch app language using the 🌐 button (top-right on home screen)
- Voice input will automatically match UI language
- English mode = English speech
- Bangla mode = Bangla speech

## 🧪 Testing Checklist

Test each of these:
- [ ] Microphone permission granted
- [ ] Tap 🎤 button - shows "Listening" snackbar
- [ ] Speak question - text appears in input field
- [ ] Question auto-sends to AI
- [ ] AI responds in correct language
- [ ] Tap 🔊 on AI message - hear response
- [ ] Switch language - voice follows language
- [ ] Try both English and Bangla voice input

## 📱 Device Requirements

### Minimum Requirements:
- Android 5.0 (API 21) or higher
- Microphone hardware
- Internet connection (for Google Speech Recognition)
- 50MB free storage

### Recommended:
- Android 8.0 or higher
- Good quality microphone
- Stable WiFi or 4G connection
- Quiet environment for best recognition

## 🎯 Voice Commands That Work

### English Voice Commands:
- "What is Early Blight?"
- "How to prevent diseases?"
- "Tell me about Late Blight"
- "What are common tomato diseases?"
- "How should I water tomatoes?"
- "Treatment for Bacterial Spot"

### Bangla Voice Commands (বাংলা):
- "আর্লি ব্লাইট কি?"
- "রোগ কিভাবে প্রতিরোধ করব?"
- "লেট ব্লাইট সম্পর্কে বলুন"
- "সাধারণ টমেটো রোগ কি কি?"
- "টমেটোতে কিভাবে পানি দেব?"
- "ব্যাকটেরিয়াল স্পটের চিকিৎসা"

## 🔧 Technical Details

### Voice Service Features:
- **Speech-to-Text**: Google Speech Recognition API
- **Text-to-Speech**: Flutter TTS (works offline for common languages)
- **Supported Languages**: 
  - English (en-US)
  - Bangla (bn-BD)
- **Auto language switching**: Matches UI language
- **Timeout**: 30 seconds listening, auto-submit after 3 seconds pause

### Error Handling:
- Null safety checks on all boolean returns
- Try-catch blocks on all async operations
- Completer for managing async speech results
- Auto-cleanup on errors
- User-friendly error messages in both languages

## 💡 Pro Tips

1. **Speak naturally** - No need to speak slowly, just clearly
2. **Pause briefly** after your question - Voice input auto-submits after 3 seconds
3. **Use quiet environment** - Background noise can affect recognition
4. **Hold phone steady** - About 6-12 inches from mouth
5. **Check language** - Make sure app is in language you're speaking
6. **Try typing first** - If voice isn't working, type to test AI responses

## 📊 What Changed in Latest Update

### Files Modified:
1. `voice_service.dart`:
   - Better null checks: `if (isAvailable != true)`
   - Stop before start: `if (_speech.isListening) await _speech.stop()`
   - Enhanced error callbacks in initialize()
   - Better completer handling

2. `ai_assistant_screen.dart`:
   - Re-initialization attempt if voice not ready
   - Prevent concurrent listening sessions
   - Better error message display

### Result:
- ✅ No more "type 'Null' is not a subtype of type 'bool'" error
- ✅ No more concurrent session conflicts
- ✅ Better permission handling
- ✅ Clearer user feedback
- ✅ More reliable voice input

## 🎉 Expected Behavior

**When everything works correctly:**
1. Tap 🎤 → See "Listening..." snackbar
2. Speak → See your words in input field
3. Auto-submit → AI responds in your language
4. Tap 🔊 → Hear AI response spoken aloud
5. Switch language → Everything updates instantly

If this is what you're experiencing - **Voice is working perfectly!** 🎊
