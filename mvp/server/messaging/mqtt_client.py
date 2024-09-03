import os
from datetime import datetime

import paho.mqtt.client as paho
from dotenv import load_dotenv
from paho import mqtt

from mvp.server.core.GameSession import GameSessionDTO

load_dotenv()

DEFAULT_HOST = os.environ.get("DEV_MQTT_HOST", "localhost")
MQTT_HOST = os.environ.get("MQTT_HOST", DEFAULT_HOST)
MQTT_PORT = int(os.environ.get("MQTT_PORT", 8883))
MQTT_USER = os.environ.get("MQTT_USER")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")
MQTT_TOPIC_PREFIX = os.environ.get("MQTT_TOPIC_PREFIX", "pdmgame/sessions")
MQTT_QOS = int(os.environ.get("MQTT_QOS", 0))
MQTT_HEARTBEAT_TOPIC = os.environ.get("MQTT_HEARTBEAT_TOPIC", "heartbeat")

DISABLE_MQTT = MQTT_USER is None
USE_MQTT_AUTH = MQTT_HOST != DEFAULT_HOST

print(f"{datetime.now()}: MQTT_HOST = {MQTT_HOST}")
print(f"{datetime.now()}: MQTT_USER = {MQTT_USER}")
print(f"{datetime.now()}: MQTT_HEARTBEAT_TOPIC = {MQTT_HEARTBEAT_TOPIC}")
print(f"{datetime.now()}: DISABLE_MQTT = {DISABLE_MQTT}")
print(f"{datetime.now()}: USE_MQTT_AUTH = {USE_MQTT_AUTH}")


def get_mqtt_client() -> 'MqttClientBase':
    if DISABLE_MQTT:
        yield MqttClientBase.get_instance()
    else:
        yield MqttClient.get_instance()


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"{datetime.now()}: MqttClient - connection successful")

        client.publish(
            MQTT_HEARTBEAT_TOPIC,
            payload=bytes(f"Connected on: {str(datetime.now())}", "utf-8"),
            qos=1
        )
    else:
        print(f"{datetime.now()}: MqttClient - connection failed. Code: {rc}")


class MqttClientBase:
    instance: "MqttClientBase" = None

    @staticmethod
    def get_instance() -> "MqttClientBase":
        if MqttClientBase.instance is None:
            MqttClientBase.instance = MqttClientBase()
        return MqttClientBase.instance

    def publish_session_state(self, session: GameSessionDTO):
        pass

    def publish_heartbeat(self):
        pass

    def reconnect(self):
        pass


class MqttClient(MqttClientBase):
    __client__: paho.Client = None

    @staticmethod
    def get_instance() -> "MqttClientBase":
        if MqttClient.instance is None:
            MqttClient.instance = MqttClient()
        return MqttClient.instance

    def __init__(self):
        client = paho.Client(
            protocol=paho.MQTTv311,
            callback_api_version=paho.CallbackAPIVersion.VERSION2,
            reconnect_on_failure=True,
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

    def publish_session_state(self, session: GameSessionDTO):
        self.__client__.publish(
            f"{MQTT_TOPIC_PREFIX}/{session.id}", payload=bytes(session.json(), "utf-8"),
            qos=MQTT_QOS
        )

    def publish_heartbeat(self) -> str | None:
        try:
            self.__client__.publish(
                MQTT_HEARTBEAT_TOPIC,
                payload=bytes(str(datetime.now()), "utf-8"),
                qos=1
            )
        except Exception as e:
            print(f"{datetime.now()}: Mqtt Client failed to publish heartbeat: {e}")
            self.__init__()
            return str(e)


def init_instance():
    if DISABLE_MQTT:
        MqttClientBase.get_instance()
    else:
        MqttClient.get_instance()


init_instance()
