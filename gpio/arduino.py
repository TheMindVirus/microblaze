#!/usr/bin/python3
from pynq.overlays.base import BaseOverlay
from pynq.lib.arduino import arduino_io

print("[INFO]: Loading Base Overlay...")
base = BaseOverlay("base.bit")
print("[INFO]: Loading Complete")

A0 = arduino_io.Arduino_IO(base.iop_arduino.mb_info, 14, "out")
A1 = arduino_io.Arduino_IO(base.iop_arduino.mb_info, 15, "out")
A2 = arduino_io.Arduino_IO(base.iop_arduino.mb_info, 16, "out")
A3 = arduino_io.Arduino_IO(base.iop_arduino.mb_info, 17, "out")
A4 = arduino_io.Arduino_IO(base.iop_arduino.mb_info, 18, "out")
A5 = arduino_io.Arduino_IO(base.iop_arduino.mb_info, 19, "out")
AnalogPins = [A0, A1, A2, A3, A4, A5]

for pin in AnalogPins:
    pin.write(1)

