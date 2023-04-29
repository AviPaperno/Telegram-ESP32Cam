import paho.mqtt.client as mqtt

from config import MQTT_LOGIN, MQTT_KEEPALIVE, MQTT_PORT, MQTT_HOST, MQTT_PASSWORD


def on_connect(client, userdata, flags, rc):
    client.subscribe("image")


def on_message(client, userdata, msg):
    if msg.topic == "image":
        if msg.payload != b'None':
            with open(f"images/photo.jpeg", "wb") as file:
                file.write(msg.payload)


client = mqtt.Client(client_id="TelegramBot", clean_session=True)

client.username_pw_set(MQTT_LOGIN, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE)
