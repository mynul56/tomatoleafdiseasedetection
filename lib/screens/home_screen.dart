import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'scan_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  Future<void> _pickImage(BuildContext context, ImageSource source) async {
    final picker = ImagePicker();
    try {
      final XFile? pickedFile = await picker.pickImage(
        source: source,
        maxWidth: 1024,
        maxHeight: 1024,
        imageQuality: 85,
      );

      if (pickedFile != null && context.mounted) {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => ScanScreen(imageFile: File(pickedFile.path)),
          ),
        );
      }
    } catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('Error picking image: $e')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.green.shade50,
      appBar: AppBar(
        title: const Text(
          'TOMATO LEAF DISEASE DETECTOR',
          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
        ),
        backgroundColor: Colors.green.shade700,
        foregroundColor: Colors.white,
        elevation: 0,
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // App Logo/Icon
              ClipRRect(
                borderRadius: BorderRadius.circular(20),
                child: Image.asset(
                  'assets/unnamed.jpg',
                  width: 200,
                  height: 200,
                  fit: BoxFit.cover,
                ),
              ),
              const SizedBox(height: 24),

              // Title
              Text(
                'Detect Tomato Diseases',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: Colors.green.shade900,
                ),
              ),
              const SizedBox(height: 12),

              // Description
              Text(
                'Take a photo or select an image of a tomato leaf to identify diseases',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 16, color: Colors.grey.shade700),
              ),
              const SizedBox(height: 48),

              // Camera Button
              ElevatedButton.icon(
                onPressed: () => _pickImage(context, ImageSource.camera),
                icon: const Icon(Icons.camera_alt, size: 28),
                label: const Text(
                  'Take Photo',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.green.shade700,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
              const SizedBox(height: 16),

              // Gallery Button
              OutlinedButton.icon(
                onPressed: () => _pickImage(context, ImageSource.gallery),
                icon: const Icon(Icons.photo_library, size: 28),
                label: const Text(
                  'Choose from Gallery',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
                ),
                style: OutlinedButton.styleFrom(
                  foregroundColor: Colors.green.shade700,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  side: BorderSide(color: Colors.green.shade700, width: 2),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
              const SizedBox(height: 48),

              // Info Card
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.green.shade100,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.green.shade300),
                ),
                child: Row(
                  children: [
                    Icon(Icons.info_outline, color: Colors.green.shade900),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        'For best results, take a clear photo with good lighting',
                        style: TextStyle(
                          color: Colors.green.shade900,
                          fontSize: 14,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
