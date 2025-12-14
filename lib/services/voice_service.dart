import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:flutter_tts/flutter_tts.dart';
import 'package:permission_handler/permission_handler.dart';
import 'dart:async';

class VoiceService {
  final stt.SpeechToText _speech = stt.SpeechToText();
  final FlutterTts _flutterTts = FlutterTts();
  bool _isInitialized = false;
  String _lastRecognizedWords = '';
  Completer<String>? _speechCompleter;
  String _currentLanguage = 'en-US'; // Default to English

  // Set language for speech recognition and TTS
  Future<void> setLanguage(String languageCode) async {
    _currentLanguage = languageCode == 'bn' ? 'bn-BD' : 'en-US';
    if (_isInitialized) {
      await _flutterTts.setLanguage(_currentLanguage);
    }
  }

  // Initialize speech recognition and text-to-speech
  Future<bool> initialize() async {
    if (_isInitialized && _speech.isAvailable) return true;

    try {
      // Request microphone permission
      final status = await Permission.microphone.request();
      if (!status.isGranted) {
        print('Microphone permission denied');
        return false;
      }

      // Stop any existing instance
      if (_speech.isListening) {
        await _speech.stop();
      }

      // Initialize speech to text
      final initialized = await _speech.initialize(
        onStatus: (status) {
          print('Speech status: $status');
          // If listening stopped, cancel any pending completer
          if (status == 'notListening' &&
              _speechCompleter != null &&
              !_speechCompleter!.isCompleted) {
            if (_lastRecognizedWords.isNotEmpty) {
              _speechCompleter!.complete(_lastRecognizedWords);
            }
          }
        },
        onError: (error) {
          print('Speech error: ${error.errorMsg}');
          if (_speechCompleter != null && !_speechCompleter!.isCompleted) {
            _speechCompleter!.completeError(
              Exception('Speech recognition error: ${error.errorMsg}'),
            );
          }
        },
      );

      if (initialized != true) {
        print('Speech recognition initialization failed');
        _isInitialized = false;
        return false;
      }

      _isInitialized = initialized;

      // Configure TTS with current language
      await _flutterTts.setLanguage(_currentLanguage);
      await _flutterTts.setSpeechRate(0.5);
      await _flutterTts.setVolume(1.0);
      await _flutterTts.setPitch(1.0);

      print(
        'Voice service initialized successfully with language: $_currentLanguage',
      );
      return _isInitialized;
    } catch (e) {
      print('Voice service initialization error: $e');
      _isInitialized = false;
      return false;
    }
  }

  // Start listening to user speech
  Future<String> listen() async {
    if (!_isInitialized) {
      throw Exception('Voice service not initialized');
    }

    // Check if speech recognition is available
    final isAvailable = _speech.isAvailable;
    if (isAvailable != true) {
      throw Exception('Speech recognition not available on this device');
    }

    // Stop any ongoing listening first
    if (_speech.isListening) {
      await _speech.stop();
      await Future.delayed(const Duration(milliseconds: 100));
    }

    _lastRecognizedWords = '';
    _speechCompleter = Completer<String>();

    try {
      // Start listening with proper callback and language
      final success = await _speech.listen(
        onResult: (result) {
          _lastRecognizedWords = result.recognizedWords;
          print(
            'Recognized: $_lastRecognizedWords (final: ${result.finalResult})',
          );

          // If this is the final result, we're done
          if (result.finalResult &&
              _speechCompleter != null &&
              !_speechCompleter!.isCompleted) {
            _speechCompleter!.complete(_lastRecognizedWords);
          }
        },
        localeId: _currentLanguage,
        listenFor: const Duration(seconds: 30),
        pauseFor: const Duration(seconds: 3),
        partialResults: true,
        onSoundLevelChange: (level) {
          print('Sound level: $level');
        },
        cancelOnError: true,
        listenMode: stt.ListenMode.confirmation,
      );

      if (success != true) {
        throw Exception(
          'Failed to start listening. Please check microphone permissions.',
        );
      }

      // Wait for either:
      // 1. Final result from speech recognition
      // 2. Timeout after 35 seconds
      final result = await _speechCompleter!.future.timeout(
        const Duration(seconds: 35),
        onTimeout: () {
          // Return whatever we have so far
          return _lastRecognizedWords;
        },
      );

      await _speech.stop();
      return result;
    } catch (e) {
      await _speech.stop();
      if (_speechCompleter != null && !_speechCompleter!.isCompleted) {
        _speechCompleter!.completeError(e);
      }
      rethrow;
    }
  }

  // Stop listening
  Future<void> stopListening() async {
    await _speech.stop();
  }

  // Speak text using TTS
  Future<void> speak(String text) async {
    await _flutterTts.speak(text);
  }

  // Stop speaking
  Future<void> stopSpeaking() async {
    await _flutterTts.stop();
  }

  // Check if currently speaking
  bool get isSpeaking => _speech.isListening;

  // Check if currently listening
  bool get isListening => _speech.isListening;

  // Dispose resources
  void dispose() {
    _speech.cancel();
    _flutterTts.stop();
  }

  // Reset for next listen session
  void reset() {
    _lastRecognizedWords = '';
    _speechCompleter = null;
  }
}
