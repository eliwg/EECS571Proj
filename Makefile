EXECUTEABLE_NAME=hello.exe
AARCH64_GCC_FLAGS=-Obinary
KERNEL8_PATH=build/kernel8.img

# May need to change these if you used a different folder structure for the toolchain
BUILD_PATH=build/aarch64-rtems6-raspberrypi4b
TOOLCHAIN_PATH=~/development/rtems/6
PI4_BSP=--rtems-bsp=aarch64/raspberrypi4b
AARCH64_GCC_PATH=~/development/rtems/6/aarch64-rtems6/bin

#! Must be run from root of repo
# Builds app, strips headers and creates a file called "kernel8.img" in build
# kernel8.img can just be copied to a Pi SD card (provided it has already been flashed with
# raspberry pi os or similiar to provide the bootloader structure)
img:
	@./waf
	@$(AARCH64_GCC_PATH)/objcopy $(AARCH64_GCC_FLAGS) $(PWD)/$(BUILD_PATH)/$(EXECUTEABLE_NAME) $(PWD)/$(KERNEL8_PATH)
	@echo "kernel8.img created in $(KERNEL8_PATH) with $(EXECUTEABLE_NAME)"

tasks:
	@python3 ./gen_tasks.py

# The 2> /dev/null || true is to supress annoying error messages
clean:
	@rm $(PWD)/$(KERNEL8_PATH) 2> /dev/null || true

waf_config:
	@./waf configure --rtems=$(TOOLCHAIN_PATH) $(PI4_BSP)