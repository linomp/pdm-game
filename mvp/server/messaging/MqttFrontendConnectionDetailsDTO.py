import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_WSS_PORT = int(os.environ.get("MQTT_WSS_PORT", 8884))
MQTT_FE_USER = os.environ.get("MQTT_FE_USER")
MQTT_FE_PASSWORD = os.environ.get("MQTT_FE_PASSWORD")
MQTT_TOPIC_PREFIX = os.environ.get("MQTT_TOPIC_PREFIX", "pdmgame/clients")


class MqttFrontendConnectionDetailsDTO(BaseModel):
    host: str
    port: int
    username: str
    password: str
    base_topic: str

    def __init__(self, session_id: str):
        super().__init__(
            host=MQTT_HOST,
            port=MQTT_WSS_PORT,
            username=MQTT_FE_USER,
            password=MQTT_FE_PASSWORD,
            base_topic=f"{MQTT_TOPIC_PREFIX}/{session_id}"
        )
