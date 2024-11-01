EXECUTEABLE_NAME=hello.exe
AARCH64_GCC_FLAGS=-Obinary
KERNEL8_PATH=build/kernel8.img

# May need to change these if you used a different folder structure for the toolchain
BUILD_PATH=build/aarch64-rtems6-raspberrypi4b
TOOLCHAIN_PATH=~/development/rtems/6
PI4_BSP=--rtems-bsp=aarch64/raspberrypi4b
AARCH64_GCC_PATH=~/development/rtems/6/aarch64-rtems6/bin

# Change this to your media path
SD_CARD_PATH=/media/sjaemin/bootfs

# For UART communication
UART_PORT=/dev/ttyUSB0
# Use 8-N-1 config with baud rate (b) of 115200
# 8-N-1 means 8 data bits (d), no parity (p), 1 stop bit
# -l: do not attempt to lock serial port
PICOCOM_FLAGS="-b 115200 -d 8 -p n -l -v"

#! Must be run from root of repo
# Builds app, strips headers and creates a file called "kernel8.img" in build
# kernel8.img can just be copied to a Pi SD card (provided it has already been flashed with
# raspberry pi os or similiar to provide the bootloader structure)
img:
	@./waf -v
	@$(AARCH64_GCC_PATH)/objcopy $(AARCH64_GCC_FLAGS) $(PWD)/$(BUILD_PATH)/$(EXECUTEABLE_NAME) $(PWD)/$(KERNEL8_PATH)
	@echo "kernel8.img created in $(KERNEL8_PATH) with $(EXECUTEABLE_NAME)"

flash:
	@cp $(KERNEL8_PATH) $(SD_CARD_PATH)
	@echo "kernel8.img copied to $(SD_CARD_PATH)."
	@sudo eject $(SD_CARD_PATH)
	@echo "SD card ejected."

uart:
	sudo picocom $(UART_PORT) $(PICOCOM_FLAGS)

tasks:
	@python3 ./gen_tasks.py

# The 2> /dev/null || true is to supress annoying error messages
clean:
	@./waf clean
	@rm $(PWD)/$(KERNEL8_PATH) 2> /dev/null || true

waf_config:
	@./waf configure --rtems=$(TOOLCHAIN_PATH) $(PI4_BSP)