
import paho.mqtt.client as mqtt

from backend.database.mysql_db import MySQLDatabase
from backend.services.auth_handler import AuthHandler
from backend.services.fumehood_handler import FumehoodHandler
from backend.services.checkout_handler import CheckoutHandler

BROKER_ADDRESS = 'pta-smartlab.csir.co.za' #"172.30.243.138"
PORT = 1883

#Topics
FUMEHOOD_LIST_REQ = "frontend/fumehoods/request"
FUMEHOOD_LIST_RES = "backend/fumehoods/response"
LOGIN_REQUEST_TOPIC = "frontend/login/request"
LOGIN_RESPONSE_TOPIC = "backend/login/response"
CHECKOUT_REQUEST_TOPIC = "frontend/fumehoods/checkout"
CHECKOUT_RESPONSE_TOPIC = "backend/fumehoods/checkout_response"

#Maybe use global instance?
client = mqtt.Client()
db=MySQLDatabase()
authHandler = AuthHandler(
    mqtt_client=client,
    database=db
)
fumehood_handler=FumehoodHandler(client, db)
checkout_handler = CheckoutHandler(client, db)

def onConnect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code:", rc)
    client.subscribe(LOGIN_REQUEST_TOPIC)
    client.subscribe(FUMEHOOD_LIST_REQ)
    client.subscribe(CHECKOUT_REQUEST_TOPIC)

def onMessage(client, userdata, msg):
    if msg.topic == LOGIN_REQUEST_TOPIC:
        authHandler.handle_login_request(msg.payload, LOGIN_RESPONSE_TOPIC)
    elif msg.topic == FUMEHOOD_LIST_REQ:
        fumehood_handler.handle_fumehood_list_request(msg.payload, FUMEHOOD_LIST_RES)
    elif msg.topic == CHECKOUT_REQUEST_TOPIC:
        checkout_handler.handle_checkout_request(msg.payload, CHECKOUT_RESPONSE_TOPIC)


client.on_connect = onConnect
client.on_message = onMessage

client.connect(BROKER_ADDRESS, PORT, 60)
client.loop_forever()