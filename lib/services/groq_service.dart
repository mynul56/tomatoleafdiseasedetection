import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';

class GroqService {
  static const String _baseUrl =
      'https://api.groq.com/openai/v1/chat/completions';
  static const bool _useDemoMode =
      true; // Set to false when you have your Groq API key

  static const String _systemPrompt =
      '''You are an AI assistant for a Tomato Leaf Disease Detection app. 
Your role is to help users with:
- Understanding tomato leaf diseases (Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Tomato Mosaic Virus, Yellow Leaf Curl Virus)
- Treatment recommendations and prevention methods
- General tomato plant care advice
- Interpreting disease detection results
- Answering questions about symptoms and disease progression

Be helpful, concise, and provide accurate agricultural information.''';

  String _getDemoResponse(String message) {
    final lowerMessage = message.toLowerCase();

    if (lowerMessage.contains('early blight')) {
      return '🍂 Early Blight (Alternaria solani)\n\nSymptoms: Dark brown spots with concentric rings (bull\'s eye pattern) on older, lower leaves.\n\nTreatment:\n• Remove and destroy infected leaves\n• Apply copper-based fungicides\n• Improve air circulation\n\nPrevention:\n• Rotate crops (3-4 years)\n• Mulch to prevent soil splash\n• Water at soil level, not overhead\n• Space plants 24-36 inches apart';
    } else if (lowerMessage.contains('late blight')) {
      return '⚠️ Late Blight (Phytophthora infestans)\n\nSymptoms: Water-soaked spots that rapidly turn brown, white fuzzy growth on undersides. Can kill plants in days!\n\nTreatment:\n• Remove infected plants IMMEDIATELY\n• Apply fungicides (chlorothalonil/mancozeb)\n• Destroy - don\'t compost!\n\nPrevention:\n• Use resistant varieties\n• Ensure good drainage\n• Monitor in cool, wet weather\n• This is the Irish Potato Famine pathogen - very serious!';
    } else if (lowerMessage.contains('bacterial spot')) {
      return '🦠 Bacterial Spot (Xanthomonas)\n\nSymptoms: Small, dark, greasy-looking spots on leaves and fruit.\n\nTreatment:\n• Remove infected plants\n• Apply copper bactericides\n• Sanitize tools between plants\n\nPrevention:\n• Use certified disease-free seeds\n• Avoid overhead watering\n• Rotate crops for 3+ years\n• Don\'t work with wet plants';
    } else if (lowerMessage.contains('mosaic virus') ||
        lowerMessage.contains('virus')) {
      return '🧬 Tomato Mosaic Virus\n\nSymptoms: Mottled, distorted leaves with yellow and green patterns. Stunted growth.\n\nTreatment:\n• NO CURE - remove infected plants immediately\n• Destroy - don\'t compost\n• Sanitize tools with 10% bleach solution\n\nPrevention:\n• Wash hands after smoking (tobacco carries virus)\n• Use resistant varieties\n• Control aphids (virus vectors)\n• Buy certified virus-free transplants';
    } else if (lowerMessage.contains('septoria')) {
      return '🔵 Septoria Leaf Spot\n\nSymptoms: Small circular spots with gray centers and dark borders on lower leaves.\n\nTreatment:\n• Remove infected leaves\n• Apply fungicides\n• Mulch around plants\n\nPrevention:\n• Good air circulation\n• Remove plant debris\n• Avoid overhead watering\n• Rotate crops';
    } else if (lowerMessage.contains('prevent') ||
        lowerMessage.contains('prevention')) {
      return '🛡️ Disease Prevention Strategies:\n\n1. **Spacing**: 24-36" apart for airflow\n2. **Watering**: Soil level only, morning is best\n3. **Mulching**: Prevents soil splash\n4. **Rotation**: 3-4 years between tomatoes\n5. **Sanitation**: Remove debris, clean tools\n6. **Resistant Varieties**: Check seed labels\n7. **Nutrition**: Healthy plants resist disease\n8. **Monitoring**: Catch problems early!';
    } else if (lowerMessage.contains('treatment') ||
        lowerMessage.contains('treat')) {
      return '💊 Treatment Options:\n\n**Fungal Diseases:**\n• Copper-based fungicides\n• Organic: Neem oil, sulfur\n• Remove infected parts\n\n**Bacterial Diseases:**\n• Copper sprays\n• Remove infected plants\n• Improve drainage\n\n**Viral Diseases:**\n• No cure - remove immediately\n• Prevent spread to other plants\n\n**Key**: Early detection is critical!';
    } else if (lowerMessage.contains('common') ||
        lowerMessage.contains('diseases') ||
        lowerMessage.contains('list')) {
      return '📋 Common Tomato Diseases:\n\n1. Early Blight - Concentric ring spots\n2. Late Blight - Rapid plant death\n3. Septoria Leaf Spot - Gray-centered spots\n4. Bacterial Spot - Dark, greasy spots\n5. Tomato Mosaic Virus - Mottled leaves\n6. Fusarium Wilt - One-sided yellowing\n7. Leaf Mold - Yellow blotches\n8. Spider Mites - Stippled leaves\n9. Target Spot - Bulls-eye lesions\n10. Yellow Leaf Curl - Curled, yellow leaves';
    } else if (lowerMessage.contains('water') ||
        lowerMessage.contains('watering')) {
      return '💧 Proper Watering:\n\n**Best Practices:**\n• Water deeply, 1-2" per week\n• Morning watering is ideal\n• Soil level only - never overhead\n• Consistent moisture prevents stress\n• Avoid wetting foliage\n\n**Signs of Problems:**\n• Wilting: Needs water or root disease\n• Yellowing: Overwatering or disease\n• Cracking fruit: Irregular watering';
    } else {
      return '👋 I\'m your tomato care expert!\n\n**Ask me about:**\n• Specific diseases ("Tell me about Early Blight")\n• Treatment options\n• Prevention strategies\n• Watering and care\n• Disease identification\n\n**Try asking:**\n• "How do I prevent tomato diseases?"\n• "What is Late Blight?"\n• "How should I water tomatoes?"\n\nWhat would you like to know? 🍅';
    }
  }

  Future<String> sendMessage(String message) async {
    // DEMO MODE: Works without API key for testing
    if (_useDemoMode) {
      // Simulate realistic API delay
      await Future.delayed(const Duration(milliseconds: 1000));
      return _getDemoResponse(message);
    }

    // Check if API key is configured
    if (ApiConfig.groqApiKey == 'YOUR_GROQ_API_KEY_HERE' ||
        ApiConfig.groqApiKey.isEmpty) {
      throw Exception(
        '⚠️ Groq API key not configured!\n\n'
        'Please follow these steps:\n\n'
        '1. Get free API key from:\n   https://console.groq.com/\n\n'
        '2. Open: lib/config/api_config.dart\n\n'
        '3. Replace YOUR_GROQ_API_KEY_HERE\n   with your actual API key\n\n'
        '4. Restart the app\n\n'
        'See QUICKSTART_AI.md for detailed instructions.',
      );
    }

    try {
      final response = await http.post(
        Uri.parse(_baseUrl),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ${ApiConfig.groqApiKey}',
        },
        body: jsonEncode({
          'model': 'llama-3.3-70b-versatile',
          'messages': [
            {'role': 'system', 'content': _systemPrompt},
            {'role': 'user', 'content': message},
          ],
          'temperature': 0.7,
          'max_tokens': 1024,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['choices'][0]['message']['content'];
      } else {
        throw Exception('Failed to get response: ${response.statusCode}');
      }
    } catch (e) {
      if (e.toString().contains('API key not configured')) {
        rethrow;
      }
      throw Exception('Error: $e');
    }
  }

  Future<String> askAboutDisease(String diseaseName) async {
    final message =
        'Tell me about $diseaseName in tomato plants, including symptoms, treatment, and prevention.';
    return await sendMessage(message);
  }
}
