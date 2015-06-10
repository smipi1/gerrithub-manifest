# =================================================
#  QSDK wrapper Makefile for the BSB002 IP bridge
# =================================================

PRODUCT=BSB002

STATE_DIR=.state
BUILD_DIR=build_dir
OTAU_BUILD_DIR=$(BUILD_DIR)/otau
RELEASE_DIR=release
QUALCOMM_DIR=qualcomm
QSDK_SOURCE_DEFINIONS=qsdkSource.mk
QSDK_DIR=$(QUALCOMM_DIR)/qsdk
QSDK_CONFIG_DEST=$(QSDK_DIR)/.config
QSDK_BUILD_DIR=$(QSDK_DIR)/build_dir
QSDK_BIN_DIR=$(QSDK_DIR)/bin/ar71xx
QSDK_MIPS_BUILD_DIR=$(QSDK_BUILD_DIR)/target-mips_*_uClibc-0.9.33.2
QSDK_HOST_BUILD_DIR=$(QSDK_BUILD_DIR)/host
QSDK_HOST_UBOOT_VERSION=2013.07-rc1
QSDK_HOST_UBOOT_BUILD_DIR=$(QSDK_HOST_BUILD_DIR)/u-boot-$(QSDK_HOST_UBOOT_VERSION)
QSDK_CONFIG_FILE=$(abspath configs/qualcomm_qsdk_openwrt_config)
CAE_DIR=cae
HOMEKIT_SOURCE_DEFINIONS=homekitSource.mk
HOMEKIT_SOURCE_DIR=$(CAE_DIR)/homekit
HUE_PACKAGES=$(shell ls packages)

# Ipbridge definitions and tools
FIRMWARE_DIR=../bridge
FIRMWARE_TOOLS_DIR=$(FIRMWARE_DIR)/tools
CREATE_FIRMWARE=python $(FIRMWARE_TOOLS_DIR)/make_firmware_image/create_fw2.py

# Development image definitions
FACTORY_RESET_SIDELOAD_UNLOCK=dev_nowhitelist_allowdowngrading_noreboot
STANDARD_SIDELOAD_UNLOCK=dev_nowhitelist_allowdowngrading_nofactorynew_noreboot
DEVELOPMENT_IMAGE_TYPES:= \
    dev_nowhitelist \
    dev_nowhitelist_noreboot \
    $(FACTORY_RESET_SIDELOAD_UNLOCK) \
    $(STANDARD_SIDELOAD_UNLOCK) \

# Upload definitions
GENERIC_UPLOAD_TARGETS=$(foreach image,$(DEVELOPMENT_IMAGE_TYPES),%.upload-$(image))

# Colorized output
RED=31
STEP_INFO_COLOR=$(RED)

# Relevant files in the QSDK build output
BIN_SOURCE_bsb002_uboot=$(QSDK_BIN_DIR)/openwrt-ar71xx-bsb002-qca-legacy-uboot.bin
BIN_SOURCE_bsb002_art=./images/bsb002/art.bin
BIN_SOURCE_cus531_nand_uboot=$(QSDK_BIN_DIR)/openwrt-ar71xx-cus531-nand-qca-legacy-uboot.bin
BIN_SOURCE_cus531_nand_art=./images/cus531_nand/art.bin
BIN_SOURCE_kernel=$(QSDK_BIN_DIR)/openwrt-ar71xx-generic-uImage-lzma.bin
BIN_SOURCE_root=$(QSDK_BIN_DIR)/openwrt-ar71xx-generic-bsb002-root-squashfs.ubi
BIN_SOURCE_overlay=$(QSDK_BIN_DIR)/openwrt-ar71xx-generic-bsb002-overlay-jffs2.ubi


define calcHex
	$(shell printf "0x%X" $$(($(1))))
endef

define noEraseBlocksToSize
	$(call calcHex,$(1) * $(NOR_ERASE_BLOCK_SIZE))
endef

# NOR device parametrics
KB=1024
NOR_ERASE_BLOCK_SIZE=$(call calcHex,64*$(KB))
ERASE_BLOCKS_UBOOT=4
ERASE_BLOCKS_UBOOT_ENV_STANDARD=1
ERASE_BLOCKS_UBOOT_ENV_REDUNDANT=2

# Tools
MKENVIMAGE=$(QSDK_HOST_UBOOT_BUILD_DIR)/tools/mkenvimage
MKENVIMAGE_OPT_STANDARD=-b -p 0 -s $(NOR_ERASE_BLOCK_SIZE) 
MKENVIMAGE_OPT_REDUNDANT=-r $(MKENVIMAGE_OPT_STANDARD)

# NOR device partitioning - BSB002:
# WARNING: Keep in sync with ./config/bsb002.u-boot-environment.txt
NOR_OFFSET_bsb002_uboot=0x0
NOR_SIZE_bsb002_uboot=$(call noEraseBlocksToSize,$(ERASE_BLOCKS_UBOOT))
NOR_END_bsb002_uboot=$(call calcHex,$(NOR_OFFSET_bsb002_uboot) + $(NOR_SIZE_bsb002_uboot))
NOR_OFFSET_bsb002_uboot_environment=$(NOR_END_bsb002_uboot)
NOR_SIZE_bsb002_uboot_environment=$(call noEraseBlocksToSize,$(ERASE_BLOCKS_UBOOT_ENV_REDUNDANT))
NOR_END_bsb002_uboot_environment=$(call calcHex,$(NOR_OFFSET_bsb002_uboot_environment) + $(NOR_SIZE_bsb002_uboot_environment))
MKENVIMAGE_OPTS_bsb002=$(MKENVIMAGE_OPT_REDUNDANT)

# NOR device partitioning - CUS531-NAND:
# WARNING: Keep in sync with ./config/cus531_nand.u-boot-environment.txt
NOR_OFFSET_cus531_nand_uboot=0x0
NOR_SIZE_cus531_nand_uboot=$(call noEraseBlocksToSize,$(ERASE_BLOCKS_UBOOT))
NOR_END_cus531_nand_uboot=$(call calcHex,$(NOR_OFFSET_cus531_nand_uboot) + $(NOR_SIZE_cus531_nand_uboot))
NOR_OFFSET_cus531_nand_uboot_environment=$(NOR_END_cus531_nand_uboot)
NOR_SIZE_cus531_nand_uboot_environment=$(call noEraseBlocksToSize,$(ERASE_BLOCKS_UBOOT_ENV_STANDARD))
NOR_END_cus531_nand_uboot_environment=$(call calcHex,$(NOR_OFFSET_cus531_nand_uboot_environment) + $(NOR_SIZE_cus531_nand_uboot_environment))
MKENVIMAGE_OPTS_cus531_nand=$(MKENVIMAGE_OPT_STANDARD)

# File locations
OTAU_IMAGE=$(RELEASE_DIR)/$(PRODUCT).fw2
OTAU_ROOTFS_ARCHIVE=$(RELEASE_DIR)/$(PRODUCT).fw2.rootfs.tar.gz
OTAU_SOURCE_ROOTFS_ARCHIVE=$(QSDK_BIN_DIR)/openwrt-ar71xx-generic-BSB002-rootfs.tar.gz

include $(QSDK_SOURCE_DEFINIONS)
include $(HOMEKIT_SOURCE_DEFINIONS)

# Make sure that qsdk.* stamp files are placed in the state directory
vpath qsdk.% $(STATE_DIR)

# Make sure that homekit.* stamp files are placed in the state directory
vpath homekit.% $(STATE_DIR)

# Prints something in color
define printInColor
	@echo -n "\033[$(1)m$(2)\033[0m\n"
endef

# Prints the step information if called
define stepinfo
	$(call printInColor,$(STEP_INFO_COLOR),Making $@)
endef

# Marks a build step complete by making a stamp file in the state directory
define done
	@mkdir -p $(STATE_DIR)
	@touch $(STATE_DIR)/$@
	$(call printInColor,$(STEP_INFO_COLOR),Done: $@)
endef

# Automatic make target (first target defined is called if no make rule is specified)
.PHONY : all
all: qsdk.compile otauImage developmentImages factoryImages

# Print help
.PHONY : help
help:
	@echo "Hue OpenWRT make"
	@echo ""
	@echo "Usage: make <rule(s)> [ <param>=<value> ]"
	@echo ""
	@echo "Supported make rules are:"
	@echo "	all (default)                 Compile the entire QSDK OpenWRT build. This generates factory- and OTAU images."
	@echo "	<ipaddr>.update               Use side-loading to update the bridge with the specified <ipaddr>."
	@echo "	                                NOTE: Does not re-compile the sources."
	@echo "	                                make force 192.168.1.10.update    # Re-compiles ipbridge and updates the"
	@echo "	                                                                  # bridge with IP address 192.168.1.10"
	@echo "	<ipaddr>.factory_update       Use side-loading to update the bridge, while resetting it to factory defaults."
	@echo "	                                NOTE: Does not re-compile the sources."
	@echo "	                                make force 192.168.1.10.factory_update"
	@echo "	                                                                  # Re-compiles ipbridge and updates the"
	@echo "	                                                                  # bridge with IP address 192.168.1.10, also"
	@echo "	                                                                  # resetting to factory defaults."
	@echo "	factoryImages                 Generate the factory images in the '$(RELEASE_DIR)' directory."
	@echo "	otauImage                     Generate the OTAU image in the '$(RELEASE_DIR)' directory."
	@echo "	developmentImages             Generate development images that modify the OTAU behavior."
	@echo "	force                         Same as 'all', but forces a re-compile of the hue packages."
	@echo "	clean                         Cleans the QSDK (Expect a complete rebuild on the next make all)."
	@echo "	rmproper                      Deletes the QSDK (Expect a complete checkout and rebuild on the next make)."
	@echo "	package/<rule>                Make a QSDK package rule"
	@echo "	                                make package/hue-ipbridge/compile # Compile the ipbridge package within the QSDK"
	@echo "	package/<name>/purge          Purge a QSDK package MIPS target build directory"
	@echo "	                                make package/hue-ipbridge/purge   # Purge the ipbridge target build dir"
	@echo "	package/<name>/force          Force a recompile of the QSDK package"
	@echo "	                                make package/hue-ipbridge/force   # Recompiles the ipbridge within the QSDK"
	@echo "	target/<rule>                 Make a QSDK target rule"
	@echo "	                                make target/linux/install         # Compile the linux target within the QSDK"
	@echo "	target/<name>/purge           Purge a QSDK target MIPS target build directory"
	@echo "	                                make target/linux/purge           # Purge the linux target build dir"
	@echo "	target/<name>/force           Force a recompile of the QSDK target"
	@echo "	                                make target/hue-ipbridge/force    # Recompiles the linux target within the QSDK"
	@echo "	qsdk/<rule>                   Makes the QSDK rule called <rule>"
	@echo "	                              Examples:"
	@echo "	                                make qsdk/world                   # Builds the entire QSDK"
	@echo "	                                make qsdk/package/hue-ipbridge    # Builds the ipbridge within the QSDK"
	@echo "	qsdk/menuconfig               Configure the QSDK/OpenWRT (Changes the config in the svn tree, so a commit will"
	@echo "	                                                          be needed afterwards)."
	@echo ""
	@echo "Run-once make rules (Will not be repeated once completed):"
	@echo "	qsdk.checkout                 Checks out the QSDK."
	@echo "	qsdk.configure                Configures the QSDK."
	@echo "	qsdk.update-feeds             Configures the QSDK feeds."
	@echo ""
	@echo "Redo run-once make rules:"
	@echo "	qsdk.checkout/force           Update the QSDK to the latest sources NOW."
	@echo "	qsdk.configure/force          Reconfigure the QSDK NOW."
	@echo "	qsdk.update-feeds/force       Update the QSDK feeds NOW."
	@echo ""
	@echo "Purge run-once make rules (Expect a redo of the run-once rule on the next make):"
	@echo "	qsdk.checkout/purge           Force a subsequent redo of 'qsdk.checkout'"
	@echo "	qsdk.configure/purge          Force a subsequent redo of 'qsdk.configure'"
	@echo "	qsdk.update-feeds/purge       Force a subsequent redo of 'qsdk.update-feeds'"
	@echo ""
	@echo "	qsdk.checkout/force           Forces a re-checkout of the qsdk sources"
	@echo ""
	@echo "Homekit tools:"
	@echo "	homekit.clean                 Cleans all homekit packages"
	@echo ""
	@echo "CAE OpenWRT build repository management:"
	@echo "	update-cae-openwrt-build      Updates the CAE OpenWRT build repository with the latest ipbridge binaries"
	@echo ""
	@echo "Developer assistance:"
	@echo "	print-<make variable>         Prints the specified make variable"
	@echo "	                              Examples:"
	@echo "	                                make print-HUE_PACKAGES           # Prints the HUE_PACKAGES make variable"
	@echo ""
	@echo "Useful examples:"
	@echo "	make target/linux/install V=s         Recompile the linux kernel and print the compile output"
	@echo "	make package/hue-ipbridge/force V=s   Recompile the ipbridge application and print the compile output"
	@echo ""

# Recompile the QSDK, forcing a recompile of the hue packages 
.PHONY : force
force: qsdk.compile/purge $(foreach package,$(HUE_PACKAGES),package/$(package)/purge) all

$(RELEASE_DIR):
	@mkdir -p $(RELEASE_DIR)

# Creates the U-Boot 
$(MKENVIMAGE):
	@echo Within $(QSDK_HOST_UBOOT_BUILD_DIR): make tools-all
	@$(MAKE) --no-print-directory -C $(QSDK_HOST_UBOOT_BUILD_DIR) tools-all

.SECONDEXPANSION:
$(RELEASE_DIR)/bsb002/bsb002_uboot_and_environment.bin: $$(@D)/bsb002_uboot.bin $$(@D)/bsb002_uboot_environment.bin
	$(call stepinfo)
	@srec_cat $(foreach bin,$^,$(bin) -binary -offset $(NOR_OFFSET_$(basename $(notdir $(bin)))) -fill 0xff $(NOR_OFFSET_$(basename $(notdir $(bin)))) $(NOR_END_$(basename $(notdir $(bin))))) -o $@ -binary

.SECONDEXPANSION:
$(RELEASE_DIR)/cus531_nand/cus531_nand_uboot_and_environment.bin: $$(@D)/cus531_nand_uboot.bin $$(@D)/cus531_nand_uboot_environment.bin
	$(call stepinfo)
	@srec_cat $(foreach bin,$^,$(bin) -binary -offset $(NOR_OFFSET_$(basename $(notdir $(bin)))) -fill 0xff $(NOR_OFFSET_$(basename $(notdir $(bin)))) $(NOR_END_$(basename $(notdir $(bin))))) -o $@ -binary

# Creates the appropriate U-Boot environment image in the release directory
#   %.bin is taken as the destination name
#   BIN_SOURCE_% must be defined to specify the source path 
.SECONDEXPANSION:
%_uboot_environment.bin: configs/$$(notdir $$*).u-boot-environment.txt $(MKENVIMAGE)
	$(call stepinfo)
	@mkdir -p $(dir $@)
	@$(MKENVIMAGE) $(MKENVIMAGE_OPTS_$(notdir $*)) $< | \
	  srec_cat - -Binary -Fill 0xFF 0x0 $(NOR_SIZE_$(notdir $*)_uboot_environment) -Output - -Binary >$@

# Copies an image bin file to the release directory
#   %.bin is taken as the destination name
#   BIN_SOURCE_% must be defined to specify the source path 
.SECONDEXPANSION:
%.bin: $$(BIN_SOURCE_$$(notdir $$*))
	$(call stepinfo)
	@mkdir -p $(dir $@)
	@cp $< $@

# Copies an image bin file to the release directory
#   %.bin is taken as the destination name
#   BIN_SOURCE_% must be defined to specify the source path 
.SECONDEXPANSION:
$(OTAU_ROOTFS_ARCHIVE): $(OTAU_SOURCE_ROOTFS_ARCHIVE)
	$(call stepinfo)
	@mkdir -p $(dir $@)
	@cp $< $@

# Generates an over-the-air update / side-loading image in the release directory
.PHONY : otauImage
otauImage: $(OTAU_IMAGE) $(OTAU_ROOTFS_ARCHIVE)

# Generates a number of development images to change the software update behavior of the board
.PHONY : developmentImages
developmentImages: $(foreach image,$(DEVELOPMENT_IMAGE_TYPES),$(RELEASE_DIR)/$(image).fw2)

.SECONDEXPANSION:
.PHONY : $(RELEASE_DIR)/bsb002 $(RELEASE_DIR)/cus531_nand
$(RELEASE_DIR)/bsb002 $(RELEASE_DIR)/cus531_nand: $$@/$$(notdir $$@)_uboot_and_environment.bin $$@/$$(notdir $$@)_uboot.bin $$@/$$(notdir $$@)_uboot_environment.bin $$@/$$(notdir $$@)_art.bin $$@/kernel.bin $$@/root.bin $$@/overlay.bin
	$(call stepinfo)

# Generates the factory images in the release directory
.PHONY : factoryImages
factoryImages: $(RELEASE_DIR)/bsb002 $(RELEASE_DIR)/cus531_nand
	$(call stepinfo)

# Generates a zipped tar container with the kernel and rootfs 
.SECONDEXPANSION:
$(OTAU_BUILD_DIR)/container.tar.gz: $$(dir $$@)kernel.bin $$(dir $$@)root.bin
	$(call stepinfo)
	@tar -C $(dir $@) -czf $@ $(notdir $^)

# Generates an over-the-air update / side-loading image in the release directory
$(OTAU_IMAGE): $(OTAU_BUILD_DIR)/container.tar.gz $(RELEASE_DIR)
	$(call stepinfo)
	-rm $(OTAU_BUILD_DIR)/revision.txt
	-cp $(FIRMWARE_DIR)/revision.txt $(OTAU_BUILD_DIR)/revision.txt
	@$(CREATE_FIRMWARE) -product $(PRODUCT) -dev -versionFile $(OTAU_BUILD_DIR)/revision.txt -out $@ $< >/dev/null

$(RELEASE_DIR)/%.fw2: $(RELEASE_DIR)
	$(call stepinfo)
	@$(CREATE_FIRMWARE) -product $(PRODUCT) -$(subst _, -,$*) -out $@ >/dev/null
 
# Deletes the QSDK
.PHONY : rmproper
rmproper: clean
	$(call stepinfo)
	@rm -rf $(QUALCOMM_DIR) $(RELEASE_DIR)

# Clean the QSDK 
.PHONY : clean
clean:
	@-cd $(QSDK_DIR) && make clean
	@rm -rf $(STATE_DIR)

# Clone the homekit sources
$(HOMEKIT_SOURCE_DIR):
	$(call stepinfo)
	@mkdir -p $(dir $@)
	@git clone $(HOMEKIT_REPOSITORY) $@

# Check the QSDK out from the source archives
qsdk.checkout: $(QSDK_SOURCE_DEFINIONS)
	$(call stepinfo)
	@mkdir -p $(QUALCOMM_DIR)
	@cd $(QUALCOMM_DIR) && repo init -u $(MANIFEST_REPOSITORY) -b $(MANIFEST_BRANCH) -m $(MANIFEST_FILE) --repo-url=$(REPO_REPOSITORY) --repo-branch=$(REPO_BRANCH) && repo sync
	$(call done)

define cleanHomekitPackages
	-@$(MAKE) -C $(QSDK_DIR) $(foreach package,$(notdir $(wildcard $(HOMEKIT_SOURCE_DIR)/package/hk_*)),package/$(package)/clean)
endef

define syncQsdkConfig
	@cp -a $(QSDK_CONFIG_FILE) $(QSDK_CONFIG_DEST)
	@$(MAKE) -C $(QSDK_DIR) defconfig
endef

.PHONY: update-cae-openwrt-build
update-cae-openwrt-build:
	$(call stepinfo)
	@./tools/update-cae-build-repo.sh
 
.PHONY: homekit.clean 
homekit.clean:
	$(call stepinfo)
	$(call cleanHomekitPackages)

homekit.checkout: $(HOMEKIT_SOURCE_DIR) $(HOMEKIT_SOURCE_DEFINIONS)
	$(call stepinfo)
	$(call syncQsdkConfig)
	$(call cleanHomekitPackages)
	@cd $< && git fetch --all && git fetch --tags && git checkout -q $(HOMEKIT_RELEASE)
	$(call done)

# Update the QSDK feeds
qsdk.update-feeds: $(QSDK_CONFIG_FILE) qsdk.checkout homekit.checkout
	$(call stepinfo)
	$(call syncQsdkConfig)
	@$(MAKE) -C $(QSDK_DIR) package/symlinks
	$(call done)

# Configure the QSDK
qsdk.configure: $(QSDK_CONFIG_FILE) qsdk.update-feeds
	$(call stepinfo)
	$(call syncQsdkConfig)
	$(call done)

# Compile the QSDK
.PHONY : qsdk.compile
qsdk.compile: qsdk.configure qsdk/world
	$(call stepinfo)

.PHONY : $(GENERIC_UPLOAD_TARGETS)
$(GENERIC_UPLOAD_TARGETS):
	$(call stepinfo)
	@curl --form "fileupload=@$(RELEASE_DIR)/$(patsubst .upload-%,%,$(suffix $@)).fw2" http://$(*)/updater
	@echo

# Update the bridge
.PHONY : %.update
%.update : %.upload-$(STANDARD_SIDELOAD_UNLOCK)
	$(call stepinfo)
	@curl --form "fileupload=@$(RELEASE_DIR)/$(PRODUCT).fw2" http://$(*)/updater
	@echo

# Update the bridge
.PHONY : %.factory_update
%.factory_update : %.upload-$(FACTORY_RESET_SIDELOAD_UNLOCK)
	$(call stepinfo)
	@curl --form "fileupload=@$(RELEASE_DIR)/$(PRODUCT).fw2" http://$(*)/updater
	@echo

# Forcefully rebuild the specified QSDK package
.PHONY : package/%/force
package/%/force: package/%/purge package/%/compile
	$(call stepinfo)

# Purge the specified QSDK package from the MIPS target build directory
.PHONY : package/%/purge
package/%/purge:
	$(call stepinfo)
	@-rm -rf $(QSDK_MIPS_BUILD_DIR)/$*
	@echo $* purged

# Execute a QSDK package make rule
.PHONY : package/%
package/%: qsdk/package/%
	$(call stepinfo)

# Forcefully rebuild the specified QSDK target
.PHONY : target/%/force
target/%/force: target/%/purge target/%/compile
	$(call stepinfo)

# Purge the specified QSDK target from the MIPS target build directory
.PHONY : target/%/purge
target/%/purge:
	$(call stepinfo)
	@-rm -rf $(QSDK_MIPS_BUILD_DIR)/$*
	@echo $* purged

# Execute a QSDK target make rule
.PHONY : target/%
target/%: qsdk/target/%
	$(call stepinfo)

# Execute a QSDK make rule
.PHONY : qsdk/menuconfig 
qsdk/menuconfig: qsdk.checkout qsdk.configure/force
	$(call stepinfo)
	@echo Within $(QSDK_DIR): make $*
	@$(MAKE) --no-print-directory -C $(QSDK_DIR) $(notdir $@)
	@echo Synchronizing changes to QSDK config
	@grep -v '^#' $(QSDK_DIR)/.config | sort -u >$(QSDK_CONFIG_FILE) 

# Execute a QSDK make rule
.PHONY : qsdk/% 
qsdk/%: qsdk.checkout
	$(call stepinfo)
	@echo Within $(QSDK_DIR): make $*
	@$(MAKE) --no-print-directory -C $(QSDK_DIR) $*

# Purges a local make step so that the step will be redone on the next build
.PHONY : qsdk.%/purge 
qsdk.%/purge:
	$(call stepinfo)
	@rm -f $(STATE_DIR)/qsdk.$*
	@echo step.$* purged

# Forcefully rebuild the run-once rule
.PHONY : qsdk.%/force
qsdk.%/force:
	$(call stepinfo)
	@$(MAKE) qsdk.$*

# Helper to print internal make variables
.PHONY : print-%
print-%:
	@echo $*=$($*)
