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

    return PredictionResult(
      disease: json['disease'] ?? 'Unknown',
      confidence:
          (json['confidence'] is int
              ? (json['confidence'] as int).toDouble()
              : (json['confidence'] ?? 0.0).toDouble()) *
          100,
      description: json['description'] ?? 'No description available',
      treatment: treatmentList,
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
