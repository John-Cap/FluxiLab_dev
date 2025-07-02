import json

from backend.utils.jwt_utils import decode_token

ORG_WAN_IP = "146.64.129.34"  #TODO - Move to config

class FumehoodHandler:
    def __init__(self, mqtt_client, database):
        self.mqtt_client = mqtt_client
        self.db = database

    def handle_fumehood_list_request(self, payload: bytes, response_topic: str):
        try:
            data = json.loads(payload.decode())
            token = data.get("token")

            if not token:
                print('MIssing token!')
                return self._respond(response_topic, {"status": "error", "message": "Missing token"})

            session = decode_token(token)
            if "error" in session:
                print('Session error!')
                return self._respond(response_topic, {"status": "error", "message": session["error"]})

            user_email = session.get("user")
            role = session.get("role")

            fumehoods_raw = self.db.fetch_all_fumehoods() if role == "admin" else self.db.fetch_fumehoods_by_user(user_email)
            fumehoods = self._prepare_fumehoods(fumehoods_raw)
            
            print(f'Prepared fumehoods: {fumehoods}')

            self._respond(response_topic, {
                "status": "success",
                "fumehoods": fumehoods
            })

        except json.JSONDecodeError:
            print(f'Error preparing fumehood list!')
            self._respond(response_topic, {"status": "error", "message": "Invalid JSON format"})

    def _respond(self, topic: str, message: dict):
        self.mqtt_client.publish(topic, json.dumps(message))
        
    def _prepare_fumehoods(self, records):
        return [
            {
                "fumehoodNr": row["fumehoodNr"],
                "ipAddr": row["ipAddr"],
                "externalPort": row["externalPort"],
                "redirectUrl": f"http://{ORG_WAN_IP}:{row['externalPort']}"
            }
            for row in records
        ]