#!/usr/bin/python3
from pynq.overlays.base import BaseOverlay
import pynq.lib.rpi as rpi
#import time

print("[INFO]: Loading Base Overlay...")
base = BaseOverlay("base.bit")
base.select_rpi()
pi = rpi.Rpi(base.RPI, "/home/xilinx/microblaze/rpi_mailbox/rpi_mailbox.elf")
print("[INFO]: RPi MicroBlaze State: " + str(pi.state))

ADDRESS = rpi.MAILBOX_OFFSET + rpi.MAILBOX_PY2IOP_ADDR_OFFSET
RPIDATA = rpi.MAILBOX_OFFSET + rpi.MAILBOX_PY2IOP_DATA_OFFSET
COMMAND = rpi.MAILBOX_OFFSET + rpi.MAILBOX_PY2IOP_CMD_OFFSET

def pi_get(address):
    pi.write(ADDRESS, address)
    pi.write(COMMAND, rpi.READ_CMD)
    return pi.read(RPIDATA)

def pi_set(address, data):
    pi.write(ADDRESS, address)
    pi.write(RPIDATA, data)
    pi.write(COMMAND, rpi.WRITE_CMD)

gpio_base = rpi.RPI_DIO_BASEADDR
gpio_size = 0x1C

pi_set(gpio_base + 0x8, 0xFFFFFFFF)

for offset in range(0, gpio_size, 4):
    address = gpio_base + offset
    data = pi_get(address)
    print("[MBOX]: {:016X}: {:08X}".format(address, data))

#value = pi_get(gpio_base)
#value |= (1 << 29)
#pi_set(gpio_base, value)

#time.sleep(5)

#value = pi.read(gpio_base)
#value &= 0xffffffff ^ (1 << 29)
#pi.write(gpio_base, value)


"""
GPIO5  = rpi_io.RPI_IO(base.iop_rpi.mb_info,  5, "out")
GPIO6  = rpi_io.RPI_IO(base.iop_rpi.mb_info,  6, "out")
GPIO13 = rpi_io.RPI_IO(base.iop_rpi.mb_info, 13, "out")
GPIO19 = rpi_io.RPI_IO(base.iop_rpi.mb_info, 19, "out")
GPIO26 = rpi_io.RPI_IO(base.iop_rpi.mb_info, 26, "out")
DigitalPins = [GPIO5, GPIO6, GPIO13, GPIO19, GPIO26]

for pin in DigitalPins:
    pin.write(1)

"""
