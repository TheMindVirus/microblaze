#!/usr/bin/python3
from pynq.overlays.base import BaseOverlay
from pynq import MMIO
import time

print("[INFO]: Loading Base Overlay...")
base = BaseOverlay("base.bit")
base.download()
time.sleep(0.2)

mmio_base = base.ip_dict["iop_rpi/mb_bram_ctrl"]["phys_addr"]
mmio_range = base.ip_dict["iop_rpi/mb_bram_ctrl"]["addr_range"]
mmio = MMIO(mmio_base, mmio_range)

mbox_base = 0x0000B880
mbox_size = 0x00000020
for i in range(mbox_base, mbox_base + mbox_size, 4):
    print(hex(mmio.read(i)))
