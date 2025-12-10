import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../models/prediction_result.dart';

class ApiService {
  // Change this to your backend URL
  // For Android Emulator: use 10.0.2.2
  // For iOS Simulator: use localhost or your machine's IP
  // For physical device: use your machine's local IP address (e.g., http://192.168.x.x:5005)
  // For VPS: use your VPS IP or domain (e.g., http://206.162.244.175:5005)
  static const String baseUrl = 'http://206.162.244.175:5005';

  Future<PredictionResult> predictDisease(File imageFile) async {
    try {
      final request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/predict'),
      );

      // Add the image file to the request
      request.files.add(
        await http.MultipartFile.fromPath('image', imageFile.path),
      );

      // Send the request
      final streamedResponse = await request.send();
      final response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body);
        return PredictionResult.fromJson(jsonData);
      } else {
        throw Exception('Failed to predict disease: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error connecting to server: $e');
    }
  }

  // Check if the server is running
  Future<bool> checkServerHealth() async {
    try {
      final response = await http
          .get(Uri.parse('$baseUrl/health'))
          .timeout(const Duration(seconds: 5));
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}
