import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:url_launcher/url_launcher.dart';
import '../mqtt/mqtt_service.dart';
import '../mqtt/mqtt_topics.dart';
import '../models/fumehood.dart';

class FumehoodScreen extends StatefulWidget {
  final MQTTService mqtt;

  const FumehoodScreen({super.key, required this.mqtt});

  @override
  State<FumehoodScreen> createState() => _FumehoodScreenState();
}

class _FumehoodScreenState extends State<FumehoodScreen> {
  final _storage = const FlutterSecureStorage();
  List<Fumehood> _fumehoods = [];
  bool _loading = true;
  String? _status;

  @override
  void initState() {
    super.initState();
    widget.mqtt.onMessage = _handleMqttMessage;
    _requestFumehoodList();
  }

  Future<void> _requestFumehoodList() async {
    final token = await _storage.read(key: 'jwt');
    if (token == null) {
      Navigator.pushReplacementNamed(context, '/');
      return;
    }

    widget.mqtt.publish(MqttTopics.fumehoodRequest, {'token': token});
  }

  void _releaseFumehood(Fumehood hood) async {
    final token = await _storage.read(key: 'jwt');
    if (token == null) return;

    widget.mqtt.publish(MqttTopics.releaseRequest, {
      'token': token,
      'fumehoodNr': hood.fumehoodNr,
    });

    setState(() {
      _status = 'Releasing fumehood...';
    });
  }

  void _handleMqttMessage(String topic, Map<String, dynamic> payload) {
    if (topic == MqttTopics.fumehoodResponse) {
      if (payload['status'] == 'success') {
        final List<dynamic> items = payload['fumehoods'];
        final list = items.map((json) => Fumehood.fromJson(json)).toList();
        setState(() {
          _fumehoods = list;
          _loading = false;
          _status = null;
        });
      } else {
        setState(() {
          _status = payload['message'] ?? 'Failed to fetch fumehoods';
          _loading = false;
        });
      }
      return;
    }
    if (topic == MqttTopics.releaseResponse) {
      if (payload['status'] == 'success') {
        setState(() {
          _status = 'Fumehood released.';
        });
        _requestFumehoodList(); // refresh display
      } else {
        setState(() {
          _status = payload['message'] ?? 'Release failed.';
        });
      }
      return;
    }
    if (topic == MqttTopics.checkoutResponse) {
      if (payload['status'] == 'success') {
        final redirectUrl = payload['redirectUrl'];
        launchUrl(Uri.parse(redirectUrl), mode: LaunchMode.externalApplication);
      } else {
        setState(() {
          _status = payload['message'] ?? 'Checkout failed';
        });
      }
      return;
    }
  }

  void _checkoutFumehood(Fumehood hood) async {
    final token = await _storage.read(key: 'jwt');
    if (token == null) return;

    widget.mqtt.publish(MqttTopics.checkoutRequest, {
      'token': token,
      'fumehoodNr': hood.fumehoodNr,
    });

    setState(() {
      _status = 'Attempting checkout...';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Available Fumehoods')),
      body:
          _loading
              ? const Center(child: CircularProgressIndicator())
              : ListView.builder(
                itemCount: _fumehoods.length,
                itemBuilder: (context, index) {
                  final hood = _fumehoods[index];

                  return ListTile(
                    title: Text('Fumehood #${hood.fumehoodNr}'),
                    subtitle: Text(hood.redirectUrl),
                    trailing: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        if (hood.externalPort != null)
                          ElevatedButton(
                            onPressed: () => _checkoutFumehood(hood),
                            child: const Text('Connect'),
                          ),
                        const SizedBox(width: 8),
                        ElevatedButton(
                          onPressed: () => _releaseFumehood(hood),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.grey[700],
                          ),
                          child: const Text('Release'),
                        ),
                      ],
                    ),
                  );
                },
              ),
      bottomNavigationBar:
          _status != null
              ? Padding(
                padding: const EdgeInsets.all(8),
                child: Text(
                  _status!,
                  style: const TextStyle(color: Colors.blue),
                ),
              )
              : null,
    );
  }
}
