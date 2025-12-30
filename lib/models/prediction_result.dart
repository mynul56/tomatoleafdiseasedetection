class PredictionResult {
  final String disease;
  final double confidence;
  final String description;
  final List<String> treatment;
  final bool isValid; // True if image appears to be a tomato leaf

  PredictionResult({
    required this.disease,
    required this.confidence,
    required this.description,
    required this.treatment,
    this.isValid = true,
  });

  factory PredictionResult.fromJson(Map<String, dynamic> json) {
    // Handle treatment - can be either String or List
    List<String> treatmentList;
    final treatmentData = json['treatment'];

    if (treatmentData is String) {
      // If it's a string, split by sentences or newlines, or wrap in a list
      treatmentList = [treatmentData];
    } else if (treatmentData is List) {
      treatmentList = List<String>.from(treatmentData);
    } else {
      treatmentList = [];
    }

    // Backend returns confidence as decimal (0.0-1.0), convert to percentage
    final rawConfidence = (json['confidence'] is int
        ? (json['confidence'] as int).toDouble()
        : (json['confidence'] ?? 0.0).toDouble());

    // If confidence is <= 1.0, it's a decimal - multiply by 100
    // If it's > 1.0, it's already a percentage
    final confidenceValue = rawConfidence <= 1.0
        ? rawConfidence * 100
        : rawConfidence;

    return PredictionResult(
      disease: json['disease'] ?? 'Unknown',
      confidence: confidenceValue,
      description: json['description'] ?? 'No description available',
      treatment: treatmentList,
      isValid: true, // Client-side will override this
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'disease': disease,
      'confidence': confidence,
      'description': description,
      'treatment': treatment,
      'isValid': isValid,
    };
  }
}
