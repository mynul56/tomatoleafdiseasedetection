import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:image/image.dart' as img;
import '../models/prediction_result.dart';

class ApiService {
  // Change this to your backend URL
  // For Android Emulator: use 10.0.2.2
  // For iOS Simulator: use localhost or your machine's IP
  // For physical device: use your machine's local IP address (e.g., http://192.168.x.x:5005)
  // For VPS: use your VPS IP or domain (e.g., http://206.162.244.175:5005)
  static const String baseUrl = 'http://206.162.244.175:5005';

  // Validate if image has leaf-like characteristics (green colors and texture)
  Future<bool> _validateLeafImage(File imageFile) async {
    try {
      print('[Validation] Starting validation for: ${imageFile.path}');
      final bytes = await imageFile.readAsBytes();
      final image = img.decodeImage(bytes);

      if (image == null) {
        print('[Validation] Failed to decode image');
        return false;
      }

      print('[Validation] Image size: ${image.width}x${image.height}');

      // Sample pixels and check for green dominance and texture
      int greenPixels = 0;
      int leafGreenPixels = 0; // More specific leaf green
      int totalSamples = 0;
      int brightnessSum = 0;
      final step = (image.width / 20)
          .ceil(); // Sample every 20th pixel for efficiency

      for (int y = 0; y < image.height; y += step) {
        for (int x = 0; x < image.width; x += step) {
          final pixel = image.getPixel(x, y);
          final r = pixel.r.toInt();
          final g = pixel.g.toInt();
          final b = pixel.b.toInt();

          // Calculate brightness
          final brightness = (r + g + b) / 3;
          brightnessSum += brightness.toInt();

          // Check for general green (including diseased brownish leaves)
          if (g > r * 0.85 || (g > 70 && g > b * 0.85)) {
            greenPixels++;
          }

          // Check for leaf-specific green (healthy leaf color)
          // Leaves typically: green dominant, not too bright/dark, balanced ratios
          if (g > r &&
              g > b && // Green dominant
              g >= 40 &&
              g <= 220 && // Reasonable green range
              r >= 20 &&
              r <= 180 && // Not pure colors
              brightness > 40 &&
              brightness < 230) {
            // Not too dark/bright
            leafGreenPixels++;
          }
          totalSamples++;
        }
      }

      // Calculate ratios
      final greenRatio = greenPixels / totalSamples;
      final leafGreenRatio = leafGreenPixels / totalSamples;
      final avgBrightness = brightnessSum / totalSamples;

      print(
        '[Validation] Green ratio: ${(greenRatio * 100).toStringAsFixed(1)}%',
      );
      print(
        '[Validation] Leaf green ratio: ${(leafGreenRatio * 100).toStringAsFixed(1)}%',
      );
      print('[Validation] Avg brightness: ${avgBrightness.toStringAsFixed(1)}');

      // Stricter validation: require both general green AND leaf-specific green
      // At least 30% general green AND 20% leaf-specific green
      // Also check brightness isn't too extreme (avoid pure artificial colors)
      final isValid =
          greenRatio >= 0.30 &&
          leafGreenRatio >= 0.20 &&
          avgBrightness > 40 &&
          avgBrightness < 200;

      print('[Validation] Result: ${isValid ? "PASS" : "FAIL"}');
      return isValid;
    } catch (e) {
      // On error, reject the image (fail-safe)
      print('[Validation] ERROR: $e');
      return false;
    }
  }

  Future<PredictionResult> predictDisease(File imageFile) async {
    try {
      // First validate if image looks like a leaf
      final isLeafLike = await _validateLeafImage(imageFile);

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
        final result = PredictionResult.fromJson(jsonData);

        // Override isValid with our client-side validation
        return PredictionResult(
          disease: result.disease,
          confidence: result.confidence,
          description: result.description,
          treatment: result.treatment,
          isValid: isLeafLike,
        );
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
