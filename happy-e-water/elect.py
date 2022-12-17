from machine import Pin, ADC
from time import sleep
from umqtt.robust import MQTTClient

from config import (
    WIFI_SSID, WIFI_PASS,
    MQTT_BROKER, MQTT_USER, MQTT_PASS
)

# Define MQTT Channel to listen
MQTT_TOPIC = "b6310545426/happye/electric"
# Connect to MQTT Broker
mqtt = MQTTClient(client_id="",
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)
mqtt.connect()


# Input Pins
sensor_pin = Pin(32)
sensor_input = ADC(sensor_pin)
sensor_input.atten(ADC.ATTN_11DB)
max_value = 3126
min_value = 2960
diff = max_value - min_value


def cal_amp():
    inputValue = sensor_input.read()
    print(inputValue)
    value = (inputValue-min_value)/diff
    if value < 0:
        return 0.0
    return value

    
while True:
    amp = cal_amp()
    print("Amp ", ": ", amp, " a")
    mqtt.publish(MQTT_TOPIC, str(amp))
    sleep(1)



