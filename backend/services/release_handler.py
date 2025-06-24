import json
from backend.utils.jwt_utils import decode_token

class ReleaseHandler:
    def __init__(self, mqtt_client, database):
        self.mqtt_client = mqtt_client
        self.db = database

    def handle_release_request(self, payload: bytes, response_topic: str):
        try:
            data = json.loads(payload.decode())
            token = data.get("token")
            fumehood_nr = data.get("fumehoodNr")

            if not token or not fumehood_nr:
                return self._respond(response_topic, {"status": "error", "message": "Missing fields"})

            session = decode_token(token)
            if "error" in session:
                return self._respond(response_topic, {"status": "error", "message": session["error"]})

            user = self.db.getUserRow(email=session["user"])
            if not user:
                return self._respond(response_topic, {"status": "error", "message": "User not found"})

            success = self.db.release_fumehood(fumehood_nr, user["id"])
            if success:
                self.db.log_usage_action(user["id"], fumehood_nr, "release")
                return self._respond(response_topic, {"status": "success", "fumehoodNr": fumehood_nr})
            else:
                return self._respond(response_topic, {"status": "error", "message": "Permission denied or not assigned"})

        except json.JSONDecodeError:
            self._respond(response_topic, {"status": "error", "message": "Invalid JSON"})

    def _respond(self, topic, message):
        self.mqtt_client.publish(topic, json.dumps(message))
