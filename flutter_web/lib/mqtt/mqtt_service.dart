import 'dart:async';
import 'dart:convert';
import 'package:flutter_web/mqtt/mqtt_topics.dart';
import 'package:mqtt_client/mqtt_browser_client.dart';
import 'package:mqtt_client/mqtt_client.dart';

typedef MessageCallback =
    void Function(String topic, Map<String, dynamic> payload);

class MQTTService {
  final String broker;
  final String clientId;
  final List<String> subscribeTopics;

  late MessageCallback onMessage = (topic, payload) {};
  late MqttBrowserClient _client;

  Timer? _heartbeatTimer;

  MQTTService({
    required this.broker,
    required this.clientId,
    required this.subscribeTopics,
  });

  Future<void> connect() async {
    _client = MqttBrowserClient(broker, clientId);
    _client.onConnected = onConnect;
    _client.port = 9001;
    _client.logging(on: false);
    _client.keepAlivePeriod = 60;
    // _client.onDisconnected = _onDisconnected;
    // _client.autoReconnect = true;
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
        print('Invalid JSON received: $payload');
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
    _client.publishMessage(topic, MqttQos.atLeastOnce, builder.payload!);
  }

  Future<void> _onDisconnected() async {
    for (var topic in subscribeTopics) {
      _client.unsubscribe(topic);
    }
    // await _client.connect();
    print('Disconnected from MQTT broker, attempting reconnect...');
  }

  void disconnect() {
    _heartbeatTimer?.cancel();
    _heartbeatTimer = null;
    // _client.disconnect();
  }

  void onConnect() {
    _heartbeatTimer = Timer.periodic(const Duration(seconds: 15), (_) {
      final builder = MqttClientPayloadBuilder();
      builder.addString(json.encode({"uiHeartbeat": "MQTT_CONNECTED_UI_SIDE"}));
      _client.publishMessage(
        MqttTopics.statusUI,
        MqttQos.atMostOnce,
        builder.payload!,
      );
    });
    print("MQTT service connected!");
  }
}
