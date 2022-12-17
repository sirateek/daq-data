from machine import Pin

# Output Pin
USB_PIN=25
RED_LED_PIN=2
GREEN_LED_PIN=12

# Button
S1_BUTTON=16
S2_BUTTON=14

# Input Pin
LDR_PIN=36

# Temperature Pin is a I2C
TEMPERATURE_SCL=0
TEMPERATURE_SDA=0


## Function
def init_pin_out(pin_number, initial_value=1):
    pin = Pin(pin_number, Pin.OUT)
    pin.value(initial_value)
    return pin

def init_pin_in(pin_number):
    return Pin(pin_number, Pin.IN)
    pass


def init_button(pin_number):
    return Pin(pin_number, Pin.IN, Pin.PULL_UP)

     