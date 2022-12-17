import json
import kidbright as kb
from umqtt.robust import MQTTClient
import time
from machine import ADC
import math

from config import (
    MQTT_BROKER, MQTT_USER, MQTT_PASS
)

MQTT_PUBLISH_TOPIC = "b6310545426/sensors"

kb.init()

# ldrPin
ldr_pin = Pin(36)
ldr_input = ADC(ldr_pin)

def calculate_input_voltage(value):
    return (value * 1.1) / 4095

def calculate_ldr_resistant(measured_voltage):
    return (measured_voltage * 33000) / (3.3 - measured_voltage)

def calculate_lux(ldr_resistant):
    # Sensor range is only up to 10000 lux --> resistant 0.1
    if ldr_resistant * (10 ** -3) < 0.1:
        log_resistant = math.log10(0.1)
    else:
        log_resistant = math.log10(ldr_resistant * (10 ** -3))
    return 10 ** ((4*(2-log_resistant))/3)

# Connect to MQTT Broker
mqtt = MQTTClient(client_id="",
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)
mqtt.connect()

while True:
    input_voltage = calculate_input_voltage(ldr_input.read())
    ldr_resistant = calculate_ldr_resistant(input_voltage)
    
    
    data = {
        'light': calculate_lux(ldr_resistant),
        'temperature': kb.temperature()
    }
    print("Publishing: ", data)
    mqtt.publish(MQTT_PUBLISH_TOPIC,
            json.dumps(data))
    time.sleep(10)

