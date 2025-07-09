import 'package:flutter/material.dart';
import 'package:flutter_web/screens/fumehood_screen.dart';
import 'mqtt/mqtt_service.dart';
import 'mqtt/mqtt_topics.dart';
import 'screens/login_screen.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  final mqtt = MQTTService(
    broker: 'ws://146.64.54.40',
    clientId: 'flutterClient_${DateTime.now().millisecondsSinceEpoch}',
    subscribeTopics: [
      MqttTopics.loginResponse,
      MqttTopics.checkoutResponse,
      MqttTopics.fumehoodResponse,
      MqttTopics.releaseResponse,
    ],
  );

  MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'FluxiLab',
      routes: {
        '/': (context) => LoginScreen(mqtt: mqtt),
        '/fumehoods': (context) => FumehoodScreen(mqtt: mqtt),
      },
    );
  }
}
