all:
	/opt/microblazeel-xilinx-elf/bin/mb-gcc -Wl,-gc-sections -Wl,-T -Wl,./lscript.ld \
	-I /usr/local/lib/python3.6/dist-packages/pynq/lib/arduino/bsp_iop_arduino/iop_arduino_mb/include \
        -L /usr/local/lib/python3.6/dist-packages/pynq/lib/arduino/bsp_iop_arduino/iop_arduino_mb/lib/ \
        -Wl,--start-group,-lxil,-lgcc,-lc,--end-group arduino_mailbox.c -o arduino_mailbox.elf

	/opt/microblazeel-xilinx-elf/bin/mb-size arduino_mailbox.elf | tee "arduino_mailbox.elf.size"

	mb-objcopy -O binary arduino_mailbox.elf arduino_mailbox.bin
