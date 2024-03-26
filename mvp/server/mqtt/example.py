# Source: https://github.com/hivemq-cloud/paho-mqtt-client-example/blob/master/simple_example.py
import os
import time

import paho.mqtt.client as paho
from dotenv import load_dotenv
from paho import mqtt
from paho.mqtt.enums import CallbackAPIVersion


def on_connect(client, userdata, flags, rc, properties=None):
    """
        Prints the result of the connection with a reasoncode to stdout ( used as callback for connect )

        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param flags: these are response flags sent by the broker
        :param rc: stands for reasonCode, which is a code for the connection result
        :param properties: can be used in MQTTv5, but is optional
    """
    print("CONNACK received with code %s." % rc)


# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None, reasonCode=None, packetIdentifier=None):
    """
        Prints mid to stdout to reassure a successful publish ( used as callback for publish )

        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param mid: variable returned from the corresponding publish() call, to allow outgoing messages to be tracked
        :param properties: can be used in MQTTv5, but is optional
        :param reasonCode: can be used in MQTTv5, but is optional
        :param packetIdentifier: can be used in MQTTv5, but is optional
    """
    print("mid: " + str(mid))


# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    """
        Prints a reassurance for successfully subscribing

        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param mid: variable returned from the corresponding publish() call, to allow outgoing messages to be tracked
        :param granted_qos: this is the qos that you declare when subscribing, use the same one for publishing
        :param properties: can be used in MQTTv5, but is optional
    """
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    """
        Prints a mqtt message to stdout ( used as callback for subscribe )

        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param msg: the message with topic and payload
    """
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


if __name__ == "__main__":
    load_dotenv()

    MQTT_HOST = os.environ.get("MQTT_HOST", "test.mosquitto.org")
    MQTT_PORT = int(os.environ.get("MQTT_PORT", 1883))
    MQTT_USER = os.environ.get("MQTT_USER")
    MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")
    MQTT_TOPIC_PREFIX = os.environ.get("MQTT_TOPIC_PREFIX", "pdmgame/clients")

    topic = f"{MQTT_TOPIC_PREFIX}/test"

    print(f"Connecting to {MQTT_HOST}:{MQTT_PORT} with user {MQTT_USER} and topic {topic}")

    # using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
    # userdata is user defined data of any type, updated by user_data_set()
    # client_id is the given name of the client
    client = paho.Client(client_id="pdmgame_server_example", userdata=None, protocol=paho.MQTTv5,
                         callback_api_version=CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect

    if MQTT_USER is not None and MQTT_PASSWORD is not None:
        client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

    client.connect(MQTT_HOST, MQTT_PORT)

    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_publish = on_publish

    client.loop_start()

    i = 0
    while True:
        client.publish(topic, payload=i, qos=1)
        time.sleep(5)
        i += 1
