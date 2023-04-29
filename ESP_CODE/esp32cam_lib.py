import network
from umqtt.robust import MQTTClient
import camera
import time
import machine

sta_if = network.WLAN(network.STA_IF);
camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
mqtt_client = None
led = machine.Pin(4, machine.Pin.OUT)


def wifi_setup():
    global sta_if
    sta_if.active(True)
    sta_if.scan()
    sta_if.connect('SSID', 'PASSWORD')
    print("Waiting for Wifi connection")
    while not sta_if.isconnected(): time.sleep(1)
    print("Connected to WiFi")


def take_photo():
    global mqtt_client
    capture = camera.capture()
    mqtt_client.publish('image', capture, qos=0)


def mqtt_callback(topic, data_bytes):
    global led
    topic = topic.decode()
    data = data_bytes.decode()
    if topic == "command":
        if data == "take_photo":
            take_photo()
        elif data == "enable_led":
            led.value(1)
        elif data == "disable_led":
            led.value(0)


def mqtt_setup():
    global mqtt_client
    mqtt_client = MQTTClient(
        "umqtt_client",
        server='DOMAIN.cloud.shiftr.io',
        port=1883,
        user='LOGIN',
        password='PASSWORD'
    )
    mqtt_client.set_callback(mqtt_callback)
    mqtt_client.connect()
    if mqtt_client:
        mqtt_client.subscribe('command')
    print("Connected to MQTT")
    while True:
        mqtt_client.check_msg()


def run():
    wifi_setup()
    mqtt_setup()
