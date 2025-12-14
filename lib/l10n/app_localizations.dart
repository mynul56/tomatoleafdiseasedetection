import 'package:flutter/material.dart';

class AppLocalizations {
  final Locale locale;

  AppLocalizations(this.locale);

  static AppLocalizations of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations)!;
  }

  static const LocalizationsDelegate<AppLocalizations> delegate =
      _AppLocalizationsDelegate();

  static final Map<String, Map<String, String>> _localizedValues = {
    'en': {
      // App Title
      'appTitle': 'Tomato Leaf Disease Detection',

      // Home Screen
      'homeTitle': 'Tomato Leaf Disease Detection',
      'homeSubtitle': 'AI-Powered Plant Health Analysis',
      'welcomeMessage':
          'Welcome! Detect diseases early and keep your plants healthy.',
      'captureImage': 'Capture Image',
      'captureDesc': 'Take a photo of the tomato leaf',
      'selectImage': 'Select from Gallery',
      'selectDesc': 'Choose an existing image',
      'aiAssistant': 'AI Assistant',
      'aiAssistantDesc': 'Chat with AI for plant care advice',
      'or': 'OR',

      // Camera/Gallery
      'selectImageSource': 'Select Image Source',
      'camera': 'Camera',
      'gallery': 'Gallery',
      'cancel': 'Cancel',

      // Results Screen
      'results': 'Disease Detection Results',
      'disease': 'Disease',
      'confidence': 'Confidence',
      'retry': 'Scan Another Leaf',
      'processing': 'Analyzing image...',
      'error': 'Error',
      'noImageSelected': 'No image selected',
      'analysisError': 'Error analyzing image. Please try again.',
      'networkError': 'Network error. Please check your connection.',

      // AI Assistant Screen
      'aiAssistantTitle': 'AI Assistant',
      'welcomeAI': '👋 Hello! I\'m your AI assistant for tomato plant care.',
      'demoMode': '🧪 Currently running in DEMO MODE with sample responses.',
      'askQuestion':
          'Ask me about tomato leaf diseases, treatments, or plant care!',
      'typeMessage': 'Type your question...',
      'send': 'Send',
      'listening': '🎤 Listening... Speak now!',
      'noSpeech': 'No speech detected. Please try again.',
      'voiceError': 'Voice error',
      'voiceNotAvailable':
          'Voice service not available. Grant microphone permission in Settings.',
      'micPermission': 'Microphone permission required for voice assistant',

      // Quick Actions
      'quickActions': 'Quick Actions',
      'commonDiseases': 'Common diseases',
      'prevention': 'Prevention tips',
      'treatment': 'Treatment options',
      'symptoms': 'Identify symptoms',

      // Diseases
      'earlyBlight': 'Early Blight',
      'lateBlight': 'Late Blight',
      'bacterialSpot': 'Bacterial Spot',
      'septoria': 'Septoria Leaf Spot',
      'mosaicVirus': 'Mosaic Virus',
      'targetSpot': 'Target Spot',
      'leafMold': 'Leaf Mold',
      'spiderMites': 'Spider Mites',
      'yellowLeafCurl': 'Yellow Leaf Curl',
      'healthy': 'Healthy Leaf',

      // Language
      'language': 'Language',
      'english': 'English',
      'bangla': 'বাংলা',
      'changeLanguage': 'Change Language',
    },
    'bn': {
      // App Title
      'appTitle': 'টমেটো পাতার রোগ সনাক্তকরণ',

      // Home Screen
      'homeTitle': 'টমেটো পাতার রোগ সনাক্তকরণ',
      'homeSubtitle': 'এআই-চালিত উদ্ভিদ স্বাস্থ্য বিশ্লেষণ',
      'welcomeMessage':
          'স্বাগতম! রোগ তাড়াতাড়ি শনাক্ত করুন এবং আপনার গাছ সুস্থ রাখুন।',
      'captureImage': 'ছবি তুলুন',
      'captureDesc': 'টমেটো পাতার একটি ছবি তুলুন',
      'selectImage': 'গ্যালারি থেকে নির্বাচন করুন',
      'selectDesc': 'একটি বিদ্যমান ছবি বেছে নিন',
      'aiAssistant': 'এআই সহায়ক',
      'aiAssistantDesc':
          'উদ্ভিদ পরিচর্যা পরামর্শের জন্য এআই-এর সাথে চ্যাট করুন',
      'or': 'অথবা',

      // Camera/Gallery
      'selectImageSource': 'ছবির উৎস নির্বাচন করুন',
      'camera': 'ক্যামেরা',
      'gallery': 'গ্যালারি',
      'cancel': 'বাতিল',

      // Results Screen
      'results': 'রোগ সনাক্তকরণের ফলাফল',
      'disease': 'রোগ',
      'confidence': 'আত্মবিশ্বাস',
      'retry': 'আরেকটি পাতা স্ক্যান করুন',
      'processing': 'ছবি বিশ্লেষণ করা হচ্ছে...',
      'error': 'ত্রুটি',
      'noImageSelected': 'কোনো ছবি নির্বাচন করা হয়নি',
      'analysisError': 'ছবি বিশ্লেষণে ত্রুটি। দয়া করে আবার চেষ্টা করুন।',
      'networkError': 'নেটওয়ার্ক ত্রুটি। দয়া করে আপনার সংযোগ পরীক্ষা করুন।',

      // AI Assistant Screen
      'aiAssistantTitle': 'এআই সহায়ক',
      'welcomeAI': '👋 হ্যালো! আমি টমেটো গাছের যত্নের জন্য আপনার এআই সহায়ক।',
      'demoMode': '🧪 বর্তমানে নমুনা প্রতিক্রিয়া সহ ডেমো মোডে চলছে।',
      'askQuestion':
          'টমেটো পাতার রোগ, চিকিৎসা বা উদ্ভিদ পরিচর্যা সম্পর্কে আমাকে জিজ্ঞাসা করুন!',
      'typeMessage': 'আপনার প্রশ্ন টাইপ করুন...',
      'send': 'পাঠান',
      'listening': '🎤 শুনছি... এখন বলুন!',
      'noSpeech': 'কোনো বক্তব্য সনাক্ত করা হয়নি। দয়া করে আবার চেষ্টা করুন।',
      'voiceError': 'ভয়েস ত্রুটি',
      'voiceNotAvailable':
          'ভয়েস সেবা উপলব্ধ নেই। সেটিংসে মাইক্রোফোন অনুমতি দিন।',
      'micPermission': 'ভয়েস সহায়কের জন্য মাইক্রোফোন অনুমতি প্রয়োজন',

      // Quick Actions
      'quickActions': 'দ্রুত কর্ম',
      'commonDiseases': 'সাধারণ রোগ',
      'prevention': 'প্রতিরোধের টিপস',
      'treatment': 'চিকিৎসার বিকল্প',
      'symptoms': 'লক্ষণ চিহ্নিত করুন',

      // Diseases
      'earlyBlight': 'আর্লি ব্লাইট',
      'lateBlight': 'লেট ব্লাইট',
      'bacterialSpot': 'ব্যাকটেরিয়াল স্পট',
      'septoria': 'সেপ্টোরিয়া লিফ স্পট',
      'mosaicVirus': 'মোজাইক ভাইরাস',
      'targetSpot': 'টার্গেট স্পট',
      'leafMold': 'লিফ মোল্ড',
      'spiderMites': 'স্পাইডার মাইটস',
      'yellowLeafCurl': 'হলুদ পাতা কার্ল',
      'healthy': 'সুস্থ পাতা',

      // Language
      'language': 'ভাষা',
      'english': 'English',
      'bangla': 'বাংলা',
      'changeLanguage': 'ভাষা পরিবর্তন করুন',
    },
  };

  String translate(String key) {
    return _localizedValues[locale.languageCode]?[key] ?? key;
  }

  // Convenience getters for common strings
  String get appTitle => translate('appTitle');
  String get homeTitle => translate('homeTitle');
  String get homeSubtitle => translate('homeSubtitle');
  String get welcomeMessage => translate('welcomeMessage');
  String get captureImage => translate('captureImage');
  String get captureDesc => translate('captureDesc');
  String get selectImage => translate('selectImage');
  String get selectDesc => translate('selectDesc');
  String get aiAssistant => translate('aiAssistant');
  String get aiAssistantDesc => translate('aiAssistantDesc');
  String get or => translate('or');
  String get selectImageSource => translate('selectImageSource');
  String get camera => translate('camera');
  String get gallery => translate('gallery');
  String get cancel => translate('cancel');
  String get results => translate('results');
  String get disease => translate('disease');
  String get confidence => translate('confidence');
  String get retry => translate('retry');
  String get processing => translate('processing');
  String get error => translate('error');
  String get noImageSelected => translate('noImageSelected');
  String get analysisError => translate('analysisError');
  String get networkError => translate('networkError');
  String get aiAssistantTitle => translate('aiAssistantTitle');
  String get welcomeAI => translate('welcomeAI');
  String get demoMode => translate('demoMode');
  String get askQuestion => translate('askQuestion');
  String get typeMessage => translate('typeMessage');
  String get send => translate('send');
  String get listening => translate('listening');
  String get noSpeech => translate('noSpeech');
  String get voiceError => translate('voiceError');
  String get voiceNotAvailable => translate('voiceNotAvailable');
  String get micPermission => translate('micPermission');
  String get quickActions => translate('quickActions');
  String get commonDiseases => translate('commonDiseases');
  String get prevention => translate('prevention');
  String get treatment => translate('treatment');
  String get symptoms => translate('symptoms');
  String get language => translate('language');
  String get english => translate('english');
  String get bangla => translate('bangla');
  String get changeLanguage => translate('changeLanguage');
}

class _AppLocalizationsDelegate
    extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  bool isSupported(Locale locale) {
    return ['en', 'bn'].contains(locale.languageCode);
  }

  @override
  Future<AppLocalizations> load(Locale locale) async {
    return AppLocalizations(locale);
  }

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}
