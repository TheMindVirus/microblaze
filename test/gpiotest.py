#!/usr/bin/python3
from pynq.overlays.base import BaseOverlay
from pynq.lib.rpi import Rpi

print("[INFO]: Loading Base Overlay...")
base = BaseOverlay("base.bit")
base.select_rpi() # Switch Raspberry Pi Microblaze to use GPIO pins instead of PMOD pins

pinout = \
{
    "ip_name": base.RPI["ip_name"], # "iop_rpi/mb_bram_ctrl"
    "rst_name": base.RPI["rst_name"], # "mb_iop_rpi_reset"
    "intr_pin_name": base.RPI["intr_pin_name"], # "iop_rpi/dff_en_reset_vector_0/q"
    "intr_ack_name": base.RPI["intr_ack_name"], # "mb_iop_rpi_intr_ack"
}

program = "/home/xilinx/microblaze/dummy/dummy.elf"

pi = Rpi(pinout, program)

print(dir(pi))

#for i in range(0, 8):
#    print(hex(pi.read_mailbox(i * 4)))

print(pi.mmio)
print(pi.state)

data = ""
for i in range(0, 16384, 4):
    value = pi.mmio.read(i)
    if value != 0:
        tag = ""
        tag += chr((value >> 24) & 0xFF)
        tag += chr((value >> 16) & 0xFF)
        tag += chr((value >>  8) & 0xFF)
        tag += chr((value      ) & 0xFF)
        print("[MMIO]: 0x{:016X}: 0x{:08X} | {}".format(i, value, tag))
    if i >= 0x0100:
        break
    data += tag[::-1]
print(data)
