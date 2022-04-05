#!/usr/bin/python3
from pynq.overlays.base import BaseOverlay
from pynq.lib.rpi import Rpi
import time

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

program = "/home/xilinx/microblaze/print/print.elf"

pi = Rpi(pinout, program)
print("[INFO]: RPI MicroBlaze State: " + str(pi.state))

#try:
#    while True:
#        pass
#except:
#    raise

time.sleep(3)
