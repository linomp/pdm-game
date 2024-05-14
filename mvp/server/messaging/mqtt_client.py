import os
from datetime import datetime

import paho.mqtt.client as paho
from dotenv import load_dotenv
from paho import mqtt

from mvp.server.core.game import GameSessionDTO

load_dotenv()

MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = int(os.environ.get("MQTT_PORT", 1883))
MQTT_USER = os.environ.get("MQTT_USER")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")
MQTT_TOPIC_PREFIX = os.environ.get("MQTT_TOPIC_PREFIX", "pdmgame/sessions")
MQTT_QOS = int(os.environ.get("MQTT_QOS", 0))

DISABLE_MQTT = MQTT_USER is None
USE_MQTT_AUTH = MQTT_HOST is not "localhost"


def get_mqtt_client() -> 'MqttClientBase':
    if DISABLE_MQTT:
        return MqttClientBase()
    return MqttClient()


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"{datetime.now()}: MqttClient - connection successful")
    else:
        print(f"{datetime.now()}: MqttClient - connection failed. Code: {rc}")


class MqttClientBase:
    def publish_session_state(self, client_uid: str, session: GameSessionDTO):
        pass


class MqttClient(MqttClientBase):
    __client__: paho.Client = None

    def __init__(self):
        client = paho.Client(
            protocol=paho.MQTTv311,
            callback_api_version=paho.CallbackAPIVersion.VERSION2,
            reconnect_on_failure=False,
            clean_session=True
        )
        client.on_connect = on_connect

        if USE_MQTT_AUTH:
            client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
            client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

        print(
            f"{datetime.now()}: MqttClient - attempting connection to {MQTT_HOST}:{MQTT_PORT} with user {MQTT_USER}"
        )

        client.connect(MQTT_HOST, MQTT_PORT)
        client.loop_start()

        self.__client__ = client

    def publish_session_state(self, client_uid: str, session: GameSessionDTO):
        self.__client__.publish(
            f"{MQTT_TOPIC_PREFIX}/{client_uid}", payload=bytes(session.json(), "utf-8"), qos=MQTT_QOS
        )
