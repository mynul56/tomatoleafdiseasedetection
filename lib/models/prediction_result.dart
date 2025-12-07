class PredictionResult {
  final String disease;
  final double confidence;
  final String description;
  final List<String> treatment;

  PredictionResult({
    required this.disease,
    required this.confidence,
    required this.description,
    required this.treatment,
  });

  factory PredictionResult.fromJson(Map<String, dynamic> json) {
    return PredictionResult(
      disease: json['disease'] ?? 'Unknown',
      confidence: (json['confidence'] ?? 0.0).toDouble(),
      description: json['description'] ?? 'No description available',
      treatment: List<String>.from(json['treatment'] ?? []),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'disease': disease,
      'confidence': confidence,
      'description': description,
      'treatment': treatment,
    };
  }
}
