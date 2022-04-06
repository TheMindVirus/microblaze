#!/usr/bin/python3
from pynq.overlays.base import BaseOverlay
import pynq.lib.arduino as arduino
#from pynq.lib.arduino import arduino_io
import time

print("[INFO]: Loading Base Overlay...")
base = BaseOverlay("base.bit")

#program = "/home/xilinx/pynq/lib/arduino/arduino_mailbox.bin"
#program = "/home/xilinx/microblaze/arduino_mailbox/arduino_mailbox.elf"
program = "/home/xilinx/microblaze/arduino_mailbox/arduino_mailbox.bin"

MBOX_ADDR = arduino.MAILBOX_OFFSET + arduino.MAILBOX_PY2IOP_ADDR_OFFSET
MBOX_DATA = arduino.MAILBOX_OFFSET + arduino.MAILBOX_PY2IOP_DATA_OFFSET
MBOX_CMD = arduino.MAILBOX_OFFSET + arduino.MAILBOX_PY2IOP_CMD_OFFSET

TRI_OFFSET = arduino.ARDUINO_DIO_BASEADDR + arduino.ARDUINO_DIO_TRI_OFFSET
DAT_OFFSET = arduino.ARDUINO_DIO_BASEADDR + arduino.ARDUINO_DIO_DATA_OFFSET

ino = arduino.Arduino(base.ARDUINO, program)
print(ino.state)

def idlecheck():
    global ino
    countdown = 10
    while (((ino.read(MBOX_CMD) & 0x1) != 0) and (countdown > 0)):
        time.sleep(0.001)
        countdown -= 1
    return countdown

def ino_get(address):
    ino.write(MBOX_ADDR, address)
    ino.write(MBOX_CMD, 0x10f)
    idlecheck()
    return ino.read(MBOX_DATA)

def ino_set(address, data):
    ino.write(MBOX_ADDR, address)
    ino.write(MBOX_DATA, data)
    ino.write(MBOX_CMD, 0x107)
    return idlecheck()

tmp = ino_get(TRI_OFFSET)
tmp &= ~(1 << 13)
ino_set(TRI_OFFSET, tmp)

tmp = ino_get(DAT_OFFSET)
tmp |= (1 << 13)
ino_set(DAT_OFFSET, tmp)

#tmp = ino_get(DAT_OFFSET)
#tmp &= ~(1 << 13)
#ino_set(DAT_OFFSET, tmp)

#pin = arduino_io.Arduino_IO(base.ARDUINO, 13, "out")
#pin.write(0)

"""
data = ""
addresses = [0xFFF8, 0xFF00, 0xFFFC]
for i in addresses:
    value = arduino.mmio.read(i)
    tag = ""
    tag += chr((value >> 24) & 0xFF)
    tag += chr((value >> 16) & 0xFF)
    tag += chr((value >>  8) & 0xFF)
    tag += chr((value      ) & 0xFF)
    data += tag[::-1]
    print("[MMIO]: 0x{:016X}: 0x{:08X} | {}".format(i, value, tag))
print(data)
"""
