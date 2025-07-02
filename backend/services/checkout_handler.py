import json

from backend.utils.jwt_utils import decode_token

class CheckoutHandler:
    def __init__(self, mqtt_client, database):
        self.mqtt_client = mqtt_client
        self.db = database

    def handle_checkout_request(self, payload: bytes, response_topic: str):
        try:
            data = json.loads(payload.decode())
            token = data.get("token")
            fumehood_nr = data.get("fumehoodNr")

            if not token or not fumehood_nr:
                return self._respond(response_topic, {"status": "error", "message": "Missing fields"})

            session = decode_token(token)
            if "error" in session:
                return self._respond(response_topic, {"status": "error", "message": session["error"]})

            email = session["user"]
            user = self.db.getUserRow(email=email)
            if not user or not user["active"]:
                return self._respond(response_topic, {"status": "error", "message": "User not found"})

            success = self.db.assign_fumehood_to_user(fumehood_nr, user["id"])

            if success:
                self.db.log_usage_action(user["id"], fumehood_nr, "checkout")
                return self._respond(response_topic, {"status": "success", "fumehoodNr": fumehood_nr})
            else:
                return self._respond(response_topic, {"status": "error", "message": "Fumehood unavailable"})

        except json.JSONDecodeError:
            self._respond(response_topic, {"status": "error", "message": "Invalid JSON"})

    def _respond(self, topic, message):
        self.mqtt_client.publish(topic, json.dumps(message))
