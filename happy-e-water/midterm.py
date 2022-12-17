from time import ticks_ms
from machine import Pin
from umqtt.robust import MQTTClient
import uasyncio as asyncio


from config import (
    MQTT_BROKER, MQTT_USER, MQTT_PASS
)

# Define PIN
GREEN_LED_PIN=12
RED_LED_PIN=2

mqtt_status_pin = Pin(GREEN_LED_PIN, Pin.OUT)
blinking_status_pin = Pin(RED_LED_PIN, Pin.OUT)


# Define MQTT Channel to listen and publusg
MQTT_SUBSCTIBE_TOPIC = "b6310545426/midterm/blink"
MQTT_PUBLISH_TOPIC = "b6310545426/midterm/uptime"

# Connect to MQTT Broker
mqtt = MQTTClient(client_id="",
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)
mqtt.connect()

# (Fix when restart the code and the RED Led goes off)
# At this point, It is obvious that wifi is already connected. Otherwise, The mqtt.connect()
# would throw out and error.
blinking_status_pin.value(0)
# Turn on the mqtt status pin.
mqtt_status_pin.value(0)

is_running_blinking = False

def sub_callback(topic, payload):
    global is_running_blinking
    print("Incomming Payload: ",payload)
    # use decode instead of direct byte-array comparison
    if topic.decode() == MQTT_SUBSCTIBE_TOPIC:
        try:
            payload_int = int(payload)
            if payload_int not in range(1, 11):
                print("Data not in range, Skipping")
                return
            if is_running_blinking:
                print("Task is currently running. Skipping this command.")
                return
            is_running_blinking = True
            # Call for coroutine to run.
            asyncio.create_task(run_blinking_task(payload_int))
            
            
        except ValueError:
            print("Warning: Input value error. Skipping this process.")

mqtt.set_callback(sub_callback)
mqtt.subscribe(MQTT_SUBSCTIBE_TOPIC)

async def run_blinking_task(count):
    global blinking_status_pin,is_running_blinking
    # We don't see the effect of the last time blinking. So add one to make it more obvious.
    for i in range(count+1):
        # Turn LED Off
        blinking_status_pin.value(1)
        await asyncio.sleep_ms(850)
        # Turn LED On
        blinking_status_pin.value(0)
        await asyncio.sleep_ms(150)
        print("Blink ", i)
    # Set the state back to the normal
    blinking_status_pin.value(0)
    is_running_blinking = False
    print("Done the task")

async def mqtt_main_loop():
    while True:
        mqtt.check_msg()
        await asyncio.sleep_ms(1)


async def publish_device_uptime():
    global MQTT_PUBLISH_TOPIC
    while True:
        ticks_in_sec = ticks_ms()/1000
        mqtt.publish(MQTT_PUBLISH_TOPIC, str(ticks_in_sec))
        await asyncio.sleep_ms(1000)

asyncio.create_task(mqtt_main_loop())
asyncio.create_task(publish_device_uptime())
asyncio.run_until_complete()








