import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../mqtt/mqtt_service.dart';
import '../mqtt/mqtt_topics.dart';

class LoginScreen extends StatefulWidget {
  final MQTTService mqtt;

  const LoginScreen({super.key, required this.mqtt});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _storage = const FlutterSecureStorage();

  String? _statusMessage;
  bool _loading = false;

  @override
  void initState() {
    super.initState();

    // Register MQTT message handler for login responses
    widget.mqtt.onMessage = _handleMqttMessage;
    widget.mqtt.connect();
  }

  void _handleMqttMessage(String topic, Map<String, dynamic> payload) {
    if (topic == MqttTopics.loginResponse) {
      setState(() => _loading = false);
      if (payload['status'] == 'success') {
        _storage.write(key: 'jwt', value: payload['token']);
        Navigator.pushReplacementNamed(context, '/fumehoods');
      } else {
        setState(() {
          _statusMessage = payload['message'] ?? 'Login failed';
        });
      }
    }
  }

  void _submitLogin() {
    setState(() {
      _loading = true;
      _statusMessage = null;
    });

    final email = _emailController.text.trim();
    final password = _passwordController.text;

    if (email.isEmpty || password.isEmpty) {
      setState(() {
        _loading = false;
        _statusMessage = 'Please fill in all fields.';
      });
      return;
    }

    widget.mqtt.publish(MqttTopics.loginRequest, {
      'email': email,
      'password': password,
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('FluxiLab Login')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _emailController,
              decoration: const InputDecoration(labelText: 'Email or OrgID'),
            ),
            TextField(
              controller: _passwordController,
              decoration: const InputDecoration(labelText: 'Password'),
              obscureText: true,
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _loading ? null : _submitLogin,
              child:
                  _loading
                      ? const CircularProgressIndicator()
                      : const Text('Login'),
            ),
            if (_statusMessage != null) ...[
              const SizedBox(height: 16),
              Text(_statusMessage!, style: const TextStyle(color: Colors.red)),
            ],
          ],
        ),
      ),
    );
  }
}
