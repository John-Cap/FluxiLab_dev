
import json

class AuthHandler:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
        # Mock data
        self.user_store = {
            "user1": {"password": "userpass", "role": "user"},
            "admin1": {"password": "adminpass", "role": "admin"},
        }

    def handleLoginRequest(self, payload: bytes, response_topic: str):
        try:
            data = json.loads(payload.decode())

            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return self._publishResponse(response_topic, {
                    "status": "error",
                    "message": "Username and password required"
                })

            user = self.user_store.get(username)

            if user and user["password"] == password:
                return self._publishResponse(response_topic, {
                    "status": "success",
                    "role": user["role"],
                    "token": f"mock-token-{username}"
                })

            return self._publishResponse(response_topic, {
                "status": "error",
                "message": "Invalid credentials"
            })

        except json.JSONDecodeError:
            self._publishResponse(response_topic, {
                "status": "error",
                "message": "Invalid JSON payload"
            })

    def _publishResponse(self, topic: str, message: dict):
        payload = json.dumps(message)
        self.mqtt_client.publish(topic, payload)
