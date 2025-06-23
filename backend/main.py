
import paho.mqtt.client as mqtt
from services.auth_handler import AuthHandler

BROKER_ADDRESS = "146.64.54.40" #"172.30.243.138"
PORT = 1883
LOGIN_REQUEST_TOPIC = "frontend/login/request"
LOGIN_RESPONSE_TOPIC = "backend/login/response"

#Maybe use global instance
client = mqtt.Client()
auth_handler = AuthHandler(client)

def onConnect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code:", rc)
    client.subscribe(LOGIN_REQUEST_TOPIC)

def onMessage(client, userdata, msg):
    if msg.topic == LOGIN_REQUEST_TOPIC:
        auth_handler.handleLoginRequest(msg.payload, LOGIN_RESPONSE_TOPIC)
    else:
        print(f"Ignored message on {msg.topic}")


client.on_connect = onConnect
client.on_message = onMessage

client.connect(BROKER_ADDRESS, PORT, 60)
client.loop_forever()