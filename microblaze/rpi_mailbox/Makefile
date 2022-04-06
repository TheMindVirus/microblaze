all:
	/opt/microblazeel-xilinx-elf/bin/mb-gcc main.c -o rpi_mailbox.elf \
	-I /usr/local/lib/python3.6/dist-packages/pynq/lib/rpi/bsp_iop_rpi/iop_rpi_mb/include \
        -L /usr/local/lib/python3.6/dist-packages/pynq/lib/rpi/bsp_iop_rpi/iop_rpi_mb/lib/

	mb-objcopy -O binary rpi_mailbox.elf rpi_mailbox.bin
