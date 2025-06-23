import json

class AuthHandler:
    def __init__(self, mqttClient, database):
        self.mqttClient = mqttClient
        self.db = database

    def handleLoginRequest(self, payload: bytes, responseTopic: str):
        try:
            data = json.loads(payload.decode())

            email = data.get("username")  # or "email" if preferred
            password = data.get("password")

            if not email or not password:
                return self._publishResponse(responseTopic, {
                    "status": "error",
                    "message": "Email and password required"
                })

            user = self.db.get_user_by_email(email)
            if user and user["password"] == password:
                return self._publishResponse(responseTopic, {
                    "status": "success",
                    "role": "admin" if user["admin"] else "user",
                    "token": f"mock-token-{email}"
                })

            return self._publishResponse(responseTopic, {
                "status": "error",
                "message": "Invalid credentials"
            })

        except json.JSONDecodeError:
            self._publishResponse(responseTopic, {
                "status": "error",
                "message": "Invalid JSON format"
            })

    def _publishResponse(self, topic: str, message: dict):
        self.mqttClient.publish(topic, json.dumps(message))
