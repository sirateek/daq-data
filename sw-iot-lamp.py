import uasyncio as asyncio
import time
from machine import Pin
from umqtt.robust import MQTTClient

from config import (
    WIFI_SSID, WIFI_PASS,
    MQTT_BROKER, MQTT_USER, MQTT_PASS
)


light_pin = Pin(25, Pin.OUT)
switch_1_pin = Pin(16, Pin.IN, Pin.PULL_UP)

# Define MQTT Channel to listen
MQTT_TOPIC = "b6310545426/lamp/2"


# Connect to MQTT Broker
mqtt = MQTTClient(client_id="",
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)
mqtt.connect()

light_state = light_pin.value()
button_state = False

def sub_callback(topic, payload):
    # use decode instead of direct byte-array comparison
    if topic.decode() == MQTT_TOPIC:
        try:
            payload_int = int(payload)
            if payload_int not in range(0,2):
                print("Data not in range, Skipping")
                return
            light_pin.value(1 - payload_int)
            print(payload)
        except ValueError:
            print("Warning: Input value error. Skipping this process.")
    
    
    
mqtt.set_callback(sub_callback)
mqtt.subscribe(MQTT_TOPIC)

async def mqtt_main_loop():
    while True:
        mqtt.check_msg()
        await asyncio.sleep_ms(1)


async def button_press_loop():
    global button_state
    while True:
        value = switch_1_pin.value()
        if value == 0 and not button_state:
            button_state = True
            state = light_pin.value()
            mqtt.publish(MQTT_TOPIC, str(state))
            light_pin.value(1 - state)
        elif value == 1:
            button_state = False
        await asyncio.sleep_ms(60)
        


asyncio.create_task(mqtt_main_loop())
asyncio.create_task(button_press_loop())
asyncio.run_until_complete()


