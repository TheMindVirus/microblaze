#!/usr/bin/python3
from pynq.overlays.base import BaseOverlay
from pynq.lib.rpi import Rpi

print("[INFO]: Loading Base Overlay...")
base = BaseOverlay("base.bit")
base.select_rpi() # Switch Raspberry Pi Microblaze to use GPIO pins instead of PMOD pins

pi = Rpi(base.RPI, "/home/xilinx/microblaze/rpi_mailbox/rpi_mailbox.bin")
print(pi.state)

data = ""
addresses = [0xFFF8, 0xFF00, 0xFFFC]
for i in addresses:
    value = pi.mmio.read(i)
    tag = ""
    tag += chr((value >> 24) & 0xFF)
    tag += chr((value >> 16) & 0xFF)
    tag += chr((value >>  8) & 0xFF)
    tag += chr((value      ) & 0xFF)
    data += tag[::-1]
    print("[MMIO]: 0x{:016X}: 0x{:08X} | {}".format(i, value, tag))
print(data)
