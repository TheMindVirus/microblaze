#!/usr/bin/python3
from pynq.overlays.base import BaseOverlay
import pynq.lib.rpi as rpi
import time

print("[INFO]: Loading Base Overlay...")
base = BaseOverlay("base.bit")
base.select_rpi()
pi = rpi.Rpi(base.RPI, "/home/xilinx/microblaze/rpi_mailbox/rpi_mailbox.bin")
pi.reset()
pi.run()
print("[INFO]: RPi MicroBlaze State: " + str(pi.state))

READ = rpi.READ_CMD
WRITE = rpi.WRITE_CMD

ADDRESS = rpi.MAILBOX_OFFSET + rpi.MAILBOX_PY2IOP_ADDR_OFFSET
RPIDATA = rpi.MAILBOX_OFFSET + rpi.MAILBOX_PY2IOP_DATA_OFFSET
COMMAND = rpi.MAILBOX_OFFSET + rpi.MAILBOX_PY2IOP_CMD_OFFSET

def idlecheck():
    countdown = 10
    while ((pi.read(COMMAND) != 0x2) and (countdown > 0)):
        time.sleep(0.001)
        countdown -= 1
    return countdown

def pi_get(address):
    pi.write(ADDRESS, address)
    pi.write(COMMAND, READ)
    if (idlecheck() != 0):
        return pi.read(RPIDATA)
    else:
        return 0x00000000

def pi_set(address, data):
    pi.write(ADDRESS, address)
    pi.write(RPIDATA, data)
    pi.write(COMMAND, WRITE)
    return idlecheck()

gpio_base = rpi.RPI_DIO_BASEADDR + rpi.RPI_DIO_DATA_OFFSET
tri_base = rpi.RPI_DIO_BASEADDR + rpi.RPI_DIO_TRI_OFFSET
gpio_size = 0x8

addresses = [ADDRESS, RPIDATA, COMMAND]
for address in addresses:
    data = pi.mmio.read(address)
    print("[MMIO]: 0x{:016X}: 0x{:08X}".format(address, data))

for offset in range(0, gpio_size, 4):
    address = gpio_base + offset
    data = pi_get(address)
    print("[MBOX]: 0x{:016X}: 0x{:08X}".format(address, data))

#pi_set(tri_base, 0)

tmp = pi_get(tri_base)
print("[TMP1]: 0x{:08X}".format(tmp))
tmp &= 0xFFFFFFFF ^ (1 << 5)
print("[TMP2]: 0x{:08X}".format(tmp))
pi_set(tri_base, tmp)

#pi_set(gpio_base, (1 << 5))

tmp = pi_get(gpio_base)
print("[TMP1]: 0x{:08X}".format(tmp))
tmp |= (1 << 5)
print("[TMP2]: 0x{:08X}".format(tmp))
pi_set(gpio_base, tmp)

for offset in range(0, gpio_size, 4):
    address = gpio_base + offset
    data = pi_get(address)
    print("[MBOX]: 0x{:016X}: 0x{:08X}".format(address, data))

time.sleep(3)
print("[WAIT]: 3")

#pi_set(gpio_base, 0)

tmp = pi_get(gpio_base)
#tmp &= ~(1 << 5)
tmp &= 0xFFFFFFFF ^ (1 << 5)
pi_set(gpio_base, tmp)

for offset in range(0, gpio_size, 4):
    address = gpio_base + offset
    data = pi_get(address)
    print("[MBOX]: 0x{:016X}: 0x{:08X}".format(address, data))


print("0x{:08X}".format(~(1 << 5)))
print("0x{:08X}".format(0xFFFFFFFF ^ (1 << 5)))

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
