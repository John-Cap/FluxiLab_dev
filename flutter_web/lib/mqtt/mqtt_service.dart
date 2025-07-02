import 'dart:convert';
import 'package:mqtt_client/mqtt_browser_client.dart';
import 'package:mqtt_client/mqtt_client.dart';

typedef MessageCallback =
    void Function(String topic, Map<String, dynamic> payload);

class MQTTService {
  final String broker;
  final String clientId;
  final List<String> subscribeTopics;
  final String statusTopic;

  late MessageCallback onMessage = (topic, payload) {};
  late MqttBrowserClient _client;

  MQTTService({
    required this.broker,
    required this.clientId,
    required this.subscribeTopics,
    required this.statusTopic,
  });

  Future<void> connect() async {
    _client = MqttBrowserClient(broker, clientId);
    _client.onConnected = onConnect;
    _client.port = 9001;
    _client.logging(on: false);
    _client.keepAlivePeriod = 20;
    _client.onDisconnected = _onDisconnected;
    // _client.useWebSocket = true;

    final connMessage = MqttConnectMessage()
        .withClientIdentifier(clientId)
        .startClean()
        .withWillQos(MqttQos.atMostOnce);
    _client.connectionMessage = connMessage;

    try {
      await _client.connect();
    } catch (e) {
      print('MQTT connection failed: $e');
      _client.disconnect();
    }

    _client.updates!.listen((List<MqttReceivedMessage<MqttMessage>> messages) {
      final recMsg = messages[0].payload as MqttPublishMessage;
      final payload = MqttPublishPayload.bytesToStringAsString(
        recMsg.payload.message,
      );

      try {
        final data = json.decode(payload);
        onMessage(messages[0].topic, data);
      } catch (_) {
        print('Invalid JSON received');
      }
    });

    // Subscribe to topics
    for (final topic in subscribeTopics) {
      _client.subscribe(topic, MqttQos.atMostOnce);
    }
  }

  void publish(String topic, Map<String, dynamic> message) {
    final builder = MqttClientPayloadBuilder();
    builder.addString(json.encode(message));
    _client.publishMessage(topic, MqttQos.atMostOnce, builder.payload!);
  }

  void _onDisconnected() {
    print('Disconnected from MQTT broker');
  }

  void disconnect() {
    _client.disconnect();
  }

  void onConnect() {
    final builder = MqttClientPayloadBuilder();
    builder.addString(json.encode({"statusPing": "MQTT_CONNECTED_UI_SIDE"}));
    _client.publishMessage(statusTopic, MqttQos.atMostOnce, builder.payload!);
    print("MQTT service connected!");
  }
}
