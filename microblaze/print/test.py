#!/usr/bin/python3
from pynq.overlays.base import BaseOverlay
from pynq.lib import MicroblazeLibrary
import time

print("[INFO]: Loading Base Overlay...")
base = BaseOverlay("base.bit")
base.select_rpi()
rpi = MicroblazeLibrary(base.RPI, ["gpio"])
#print("[INFO]: RPI MicroBlaze State: " + str(rpi.state))

pin = rpi.gpio_open(29)
rpi.gpio_set_direction(pin, rpi.GPIO_OUT)
rpi.gpio_write(pin, 255)
time.sleep(3)
rpi.gpio_close(pin)
