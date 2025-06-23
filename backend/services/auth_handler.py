import json

from backend.utils.jwt_utils import generate_token

class AuthHandler:
    def __init__(self, mqtt_client, database):
        self.mqtt_client = mqtt_client
        self.db = database

    def handle_login_request(self, payload: bytes, response_topic: str):
        try:
            data = json.loads(payload.decode())

            email = data.get("username")
            password = data.get("password")

            if not email or not password:
                return self._publish_response(response_topic, {
                    "status": "error",
                    "message": "Email and password required"
                })

            user = self.db.getUserRow(email=email)

            if user and user["password"] == password:
                token = generate_token(email, "admin" if user["admin"] else "user")
                return self._publish_response(response_topic, {
                    "status": "success",
                    "role": "admin" if user["admin"] else "user",
                    "token": token
                })

            return self._publish_response(response_topic, {
                "status": "error",
                "message": "Invalid credentials"
            })

        except json.JSONDecodeError:
            self._publish_response(response_topic, {
                "status": "error",
                "message": "Invalid JSON format"
            })

    def _publish_response(self, topic: str, message: dict):
        self.mqtt_client.publish(topic, json.dumps(message))
