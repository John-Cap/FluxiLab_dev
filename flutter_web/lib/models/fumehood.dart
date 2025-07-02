class Fumehood {
  final int fumehoodNr;
  final String ipAddr;
  final String? externalPort;
  final String redirectUrl;

  Fumehood({
    required this.fumehoodNr,
    required this.ipAddr,
    required this.externalPort,
    required this.redirectUrl,
  });

  factory Fumehood.fromJson(Map<String, dynamic> json) {
    return Fumehood(
      fumehoodNr: json['fumehoodNr'],
      ipAddr: json['ipAddr'],
      externalPort: json['externalPort'],
      redirectUrl: json['redirectUrl'],
    );
  }
}
