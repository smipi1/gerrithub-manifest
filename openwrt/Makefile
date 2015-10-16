# =================================================
#  QSDK wrapper Makefile for the BSB002 IP bridge
# =================================================

toUppercase=$(shell echo "$1" | tr a-z A-Z)
toLowercase=$(shell echo "$1" | tr A-Z a-z)

PRODUCT_BUILD=product
DEVELOP_BUILD=develop
BUILD?=$(DEVELOP_BUILD)
PRODUCT=BSB002
product=$(call toLowercase,$(PRODUCT))
zigbee_soc=samr21

# Prints something in color
define printInColor
	echo -n "\033[$(1)m$(2)\033[0m\n"
endef

# Colorized output
RED=31
YELLOW=33
STEP_INFO_COLOR=$(RED)

ifneq "$(BUILD)" "$(DEVELOP_BUILD)"
  ifneq "$(BUILD)" "$(PRODUCT_BUILD)"
    $(error Invalid value: BUILD=$(BUILD). Valid values are '$(DEVELOP_BUILD)' or '$(PRODUCT_BUILD)')
  endif
endif

$(info $(shell $(call printInColor,$(YELLOW),Using BUILD=$(BUILD))))

# Tools required by openwrt build
REQUIRED_EXECUTABLES += \
  gcc g++ objcopy patch bzip2 flex make xgettext pkg-config unzip svn gawk ocamlyacc cmake hg pip

# Python modules required by openwrt build
REQUIRED_PYTHON_PACKAGES += \
  yaml magic

# Python module compatibility checks per package
PYTHON_PACKAGE_TEST_magic=magic.from_file("Makefile")

# Tools required by downstream tools
REQUIRED_EXECUTABLES += \
  openssl

# Tools required by this makefile
SREC_CAT=srec_cat
REQUIRED_EXECUTABLES += $(SREC_CAT)
CURL=curl
REQUIRED_EXECUTABLES += $(CURL)
PYTHON=python
REQUIRED_EXECUTABLES += $(PYTHON)
MKDIR=mkdir
REQUIRED_EXECUTABLES += $(MKDIR)
GIT=git
REQUIRED_EXECUTABLES += $(GIT)
GREP=grep
REQUIRED_EXECUTABLES += $(GREP)

# Directories
STATE_DIR=.state
BUILD_DIR=build_dir/$(BUILD)
TOOLS_DIR=tools
BUILD_LOG_DIR=$(BUILD_DIR)/build-logs
BUILD_LICENSES_DIR=$(BUILD_DIR)/licenses
LIST_OF_FILES_IN_ROOT=$(BUILD_LICENSES_DIR)/rootfs.list
OTAU_BUILD_DIR=$(BUILD_DIR)/otau
DEPS_BUILD_DIR=$(BUILD_DIR)/deps
RELEASE_DIR=release/$(BUILD)
RELEASE_UNLOCK_DIR=release/$(DEVELOP_BUILD)/unlock
RELEASE_FACTORY_DIR=$(RELEASE_DIR)/factory
RELEASE_LICENSES_DIR=$(RELEASE_DIR)/licenses
QUALCOMM_DIR=qualcomm
QSDK_SOURCE_DEFINIONS=qsdkSource.mk
QSDK_DIR=$(QUALCOMM_DIR)/qsdk
QSDK_DL_CACHE_GIT_DIR=$(QSDK_DIR)/dl/.git
QSDK_DL_CACHE_REPO=ssh://git@github.com/PhilipsHueDev/bsb002-system_openwrt_dl_cache.git
QSDK_CONFIG_DEST=$(QSDK_DIR)/.config
QSDK_BUILD_DIR=$(QSDK_DIR)/build_dir
QSDK_LOGS_DIR=$(QSDK_DIR)/logs
QSDK_PLATFORM=ar71xx
QSDK_BIN_DIR=$(QSDK_DIR)/bin/$(QSDK_PLATFORM)
QSDK_MIPS_BUILD_DIR=$(QSDK_BUILD_DIR)/target-mips_*_uClibc-*
QSDK_HOST_BUILD_DIR=$(QSDK_BUILD_DIR)/host
QSDK_HOST_UBOOT_BUILD_DIR=$(QSDK_HOST_BUILD_DIR)/u-boot-*
QSDK_HOST_BIN_DIR=$(QSDK_DIR)/staging_dir/host/bin
qsdkConfigFile=configs/qsdk.$(1).config
QSDK_CONFIG_FILE=$(call qsdkConfigFile,$(BUILD))
QSDK_LAST_WRITTEN_LOG_FILE=`find $(QSDK_LOGS_DIR)/ -type f -printf '%T@ %p\n' | sort -n | tail -1 | awk '{print $$2}'`
CAE_DIR=cae
HOMEKIT_SOURCE_DEFINIONS=homekitSource.mk
HOMEKIT_SOURCE_DIR=$(CAE_DIR)/homekit
PACKAGE_SOURCES_BUILD_DIR=$(BUILD_DIR)/package-sources

# Git built commit tracking
GIT_DIR_qsdk=$(QSDK_DIR)
GIT_DIR_uboot=$(QSDK_DIR)/qca/src/qca-legacy-uboot
gitHead=$(shell cd $(GIT_DIR_$(1)) && git log -1 --pretty=format:%H)
getLastBuiltCommit=$(shell cat $(QSDK_BIN_DIR)/$(1).built-commit 2>/dev/null)
define updateLastBuiltCommit
	@$(call printInColor,$(YELLOW),Built $(1)@$(call gitHead,$(1))) 
	@echo $(call gitHead,$(1)) >$(QSDK_BIN_DIR)/$(1).built-commit
endef
define updateLastBuiltCommits
	$(call updateLastBuiltCommit,qsdk)
	$(call updateLastBuiltCommit,uboot)
endef
LAST_BUILT_QSDK_COMMIT=$(call getLastBuiltCommit,qsdk)
LAST_BUILT_UBOOT_COMMIT=$(call getLastBuiltCommit,uboot)
AFFECTED_QSDK_MAKE_TARGETS=$(TOOLS_DIR)/affectedQsdkMakeTargets.py

ifndef TEST_LICENSES
LICENSES_DEPS=qsdk.compile
endif

#Added so that Lite-On can build without running into licensinhg errors
ifndef SKIP_LICENSES
LICENSES_TARGET=licenses
endif

# List Hue packages
HUE_PACKAGES=$(shell ls packages)

# Ipbridge definitions and tools
FIRMWARE_ROOT_DIR=..
FIRMWARE_ZIGBEE_DIR=$(FIRMWARE_ROOT_DIR)/zigbee
FIRMWARE_DIR=$(FIRMWARE_ROOT_DIR)/bridge
FIRMWARE_ARCHIVE_ID_FILE=$(FIRMWARE_DIR)/archiveid
FIRMWARE_REVISION_FILE=$(FIRMWARE_ROOT_DIR)/revision.txt
FIRMWARE_ARCHIVE_ID=$(shell cat $(FIRMWARE_ARCHIVE_ID_FILE))
FIRMWARE_REVISION=$(shell cat $(FIRMWARE_REVISION_FILE) 2>/dev/null)
ifneq "$(FIRMWARE_REVISION)" ""
FIRMWARE_REVISION_TAG=_$(shell printf "%02d%06d" $(FIRMWARE_ARCHIVE_ID) $(FIRMWARE_REVISION))
endif

FIRMWARE_TOOLS_DIR=$(FIRMWARE_DIR)/tools
FIRMWARE_DEV_PRIKEY=$(FIRMWARE_TOOLS_DIR)/make_firmware_image/certs/RSA_dev_01.pem
FIRMWARE_ZIGBEE_HEX_FILE=$(FIRMWARE_ZIGBEE_DIR)/$(zigbee_soc)/ZigBeeBridge-HueV2-SAMR21_8001.hex
FIRMWARE_KEY=$(basename $(notdir $(FIRMWARE_DEV_PRIKEY)))
SYNC_CONFIGS=$(TOOLS_DIR)/syncConfigs.py
CREATE_FIRMWARE=$(PYTHON) $(FIRMWARE_TOOLS_DIR)/make_firmware_image/create_fw2.py
CREATE_SIGN_PACKAGE=$(PYTHON) $(FIRMWARE_TOOLS_DIR)/make_firmware_image/create_sign_package.py 
TARGET_PACKAGE_CONTROL=./tools/targetPackageControl.sh 
PACKAGE_INIT_COMMANDS= \
  start \
  stop \
  restart \
  reload \
  enable \
  disable
PACKAGE_INIT_CMD_TARGETS=$(foreach command,$(PACKAGE_INIT_COMMANDS),package/%/init/$(command))
PACKAGE_SYNC_COMMANDS= \
  sync \
  sync+restart
PACKAGE_SYNC_CMD_TARGETS=$(foreach command,$(PACKAGE_SYNC_COMMANDS),package/%/$(command))

PACKAGE_ARCHIVE_TOOL=./legal/update-package-source-repo.sh
OPEN_SOURCE_COMPLIANCE_TOOL=./legal/openSourceCompliance.py \
  --qsdk-root-dir $(QSDK_DIR) \
  --target-build-root-dir $(QSDK_MIPS_BUILD_DIR) \
  --target-file-dir-name ipkg-$(QSDK_PLATFORM) \
  --dump-rootfs-listing-to $(LIST_OF_FILES_IN_ROOT)

# git helpers	
ASSERT_NO_UNCOMMITTED_FILES=[ -z "`$(GIT) ls-files --others`" ]
ASSERT_NO_LOCAL_CHANGES=$(GIT) diff-files --quiet
ASSERT_NO_STAGED_CHANGES=$(GIT) diff-index --quiet --cached HEAD
ASSERT_QSDK_DL_CACHE_REPO_UP_TO_DATE=($(ASSERT_NO_UNCOMMITTED_FILES) && $(ASSERT_NO_LOCAL_CHANGES) && $(ASSERT_NO_STAGED_CHANGES))

# Development image definitions
FACTORY_RESET_SIDELOAD_UNLOCK=nowhitelist_allowdowngrading_noreboot
STANDARD_SIDELOAD_UNLOCK=nowhitelist_allowdowngrading_nofactorynew_noreboot
UNLOCK_IMAGE_TYPES:= \
    nowhitelist \
    nowhitelist_noreboot \
    $(FACTORY_RESET_SIDELOAD_UNLOCK) \
    $(STANDARD_SIDELOAD_UNLOCK) \
    nowhitelist_noreboot_allowcommissioninginterface \
    nowhitelist_noreboot_allowfactoryinterface \
    nowhitelist_noreboot_allowtestinterface
UNLOCK_IMAGES=$(foreach image,$(UNLOCK_IMAGE_TYPES),$(RELEASE_UNLOCK_DIR)/$(image).fw2)

# Sideload definitions
PRODUCT_SIDELOAD_TARGET=sideload/$(PRODUCT)
UNLOCK_TARGETS=$(foreach image,$(UNLOCK_IMAGE_TYPES),unlock/$(image))

# Relevant factory source files
BIN_SOURCE_$(product)_uboot=$(QSDK_BIN_DIR)/openwrt-$(QSDK_PLATFORM)-$(product)-qca-legacy-uboot.bin
BIN_SOURCE_$(product)_art=./images/$(product)/art.bin
BIN_SOURCE_kernel=$(QSDK_BIN_DIR)/openwrt-$(QSDK_PLATFORM)-generic-uImage-lzma.bin
BIN_SOURCE_root=$(QSDK_BIN_DIR)/openwrt-$(QSDK_PLATFORM)-generic-$(product)-root-squashfs.ubi
BIN_SOURCE_overlay=$(QSDK_MIPS_BUILD_DIR)/hue-factory-defaults/factory-overlay.ubi
BIN_SOURCE_uboot_and_environment=$(RELEASE_FACTORY_DIR)/$(product)/$(product)_uboot_and_environment.bin
BIN_SOURCE_$(zigbee_soc)=$(FIRMWARE_ZIGBEE_DIR)/$(zigbee_soc)/ZigBeeBridge-HueV2-SAMR21_8001.hex

# Relevant signing package source files
SIGNING_SOURCE_root=$(QSDK_BIN_DIR)/openwrt-$(QSDK_PLATFORM)-generic-$(PRODUCT)-rootfs.tar.gz
SIGNING_SOURCE_ubinize_ini=$(QSDK_DIR)/target/linux/$(QSDK_PLATFORM)/image/ubinize-root-$(product).ini
SIGNING_SOURCE_zigbee_version=$(FIRMWARE_ZIGBEE_DIR)/$(zigbee_soc)/ZigBeeBridge-HueV2-SAMR21.releaseinfo

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
NOR_OFFSET_$(product)_uboot=0x0
NOR_SIZE_$(product)_uboot=$(call noEraseBlocksToSize,$(ERASE_BLOCKS_UBOOT))
NOR_END_$(product)_uboot=$(call calcHex,$(NOR_OFFSET_$(product)_uboot) + $(NOR_SIZE_$(product)_uboot))
NOR_OFFSET_$(product)_uboot_environment=$(NOR_END_$(product)_uboot)
NOR_SIZE_$(product)_uboot_environment=$(call noEraseBlocksToSize,$(ERASE_BLOCKS_UBOOT_ENV_REDUNDANT))
NOR_END_$(product)_uboot_environment=$(call calcHex,$(NOR_OFFSET_$(product)_uboot_environment) + $(NOR_SIZE_$(product)_uboot_environment))
MKENVIMAGE_OPTS_$(product)=$(MKENVIMAGE_OPT_REDUNDANT)

# Output files
OTAU_IMAGE=$(RELEASE_DIR)/$(PRODUCT)$(FIRMWARE_REVISION_TAG).$(BUILD).$(FIRMWARE_KEY).fw2

ifeq "$(BUILD)" "$(PRODUCT_BUILD)"
  OTAU_SIGN_PACKAGE=$(RELEASE_DIR)/$(PRODUCT)$(FIRMWARE_REVISION_TAG).$(BUILD).to_sign.tar.gz
endif

include $(QSDK_SOURCE_DEFINIONS)
include $(HOMEKIT_SOURCE_DEFINIONS)

# Make sure that qsdk.* stamp files are placed in the state directory
vpath qsdk.% $(STATE_DIR)

# Make sure that homekit.* stamp files are placed in the state directory
vpath homekit.% $(STATE_DIR)

# Prints the step information if called
define stepinfo
	@$(call printInColor,$(STEP_INFO_COLOR),Making $@)
endef

# Marks a build step complete by making a stamp file in the state directory
define done
	@$(MKDIR) -p $(STATE_DIR)
	@touch $(STATE_DIR)/$@
	@$(call printInColor,$(STEP_INFO_COLOR),Done: $@)
endef

# Make sure the build-logs directory exists
ifeq "$(shell $(MKDIR) -p $(BUILD_LOG_DIR) && echo $(BUILD_LOG_DIR))" ""
$(error mkdir $(BUILD_LOG_DIR))
endif

# Hides the output in a log file, but shows the output if an error occurs
ifneq "$(V)" "s"
CURRENT_LOG_FILE=$(BUILD_LOG_DIR)/$(subst /,_,$@)
quietUnlessErrorsOrVerbose=>$(CURRENT_LOG_FILE) 2>&1 || (cat $(CURRENT_LOG_FILE); exit 1)
endif

ifneq "$(V)" "s"
define dumpBuildLogIfError
|| ( \
$(call printInColor,$(YELLOW),\
\n============================================================================\
\nLast build log file:\
\n  $(QSDK_LAST_WRITTEN_LOG_FILE)\
\n----------------------------------------------------------------------------\
); cat $(QSDK_LAST_WRITTEN_LOG_FILE); $(call printInColor,$(YELLOW),\
\n============================================================================\
\n\
); exit 1 )
endef
endif

# Automatic make target (first target defined is called if no make rule is specified)
.PHONY : all
all: assert-build-requirements cleanReleaseDir otauImage unlockImages factoryImages $(LICENSES_TARGET)

define printPackageInitHelp
	printf "	package/<name>/init/%-9s Executes '/etc/init.d/<package_init_script> $(1)' on the target at IPADDR.\n" $(1);
endef

define printSideloadHelp
	printf "	%s\n" $(1);
endef

# Print help
.PHONY : help
help:
	@echo "Hue OpenWRT make"
	@echo ""
	@echo "Usage: make <rule(s)> [ <param>=<value> ]"
	@echo ""
	@echo "Standard make rules:"
	@echo "	all (default)                 Compile the entire QSDK OpenWRT build. This generates factory- and OTAU images."
	@echo "	factoryImages                 Generate the factory images in the '$(RELEASE_DIR)' directory."
	@echo "	otauImage                     Generate the OTAU image in the '$(RELEASE_DIR)' directory."
	@echo "	unlockImages                  Generate unlock images."
	@echo "	licenses                      Generates open-source license information for the target."
	@echo "	pushPackageSources            Pushes open-source package archives to github for open-source compliance."
	@echo "	force                         Same as 'all', but forces a re-compile of the hue packages."
	@echo "	clean                         Cleans the QSDK (Expect a complete rebuild on the next make all)."
	@echo "	rmproper                      Deletes the QSDK (Expect a complete checkout and rebuild on the next make)."
	@echo "	package/<rule>                Make a QSDK package rule"
	@echo "	package/<name>/purge          Purge a QSDK package MIPS target build directory"
	@echo "	package/<name>/force          Force a recompile of the QSDK package"
	@echo "	target/<rule>                 Make a QSDK target rule"
	@echo "	target/<name>/purge           Purge a QSDK target MIPS target build directory"
	@echo "	target/<name>/force           Force a recompile of the QSDK target"
	@echo "	qsdk/<rule>                   Makes the QSDK rule called <rule>"
	@echo "	qsdk/menuconfig               Configure the QSDK/OpenWRT (Changes the config in the svn tree, so a commit will"
	@echo "	                                                          be needed afterwards)."
	@echo "	qsdk.assert-download-cache-up-to-date"
	@echo "	                              Checks that the QSDK download cache is up to date"
	@echo "	qsdk.commit-download-cache    Commit changes to the QSDK download cache repository"
	@echo "	qsdk.clean-download-cache     Cleans uncommitted changes from the QSDK download cache"
	@echo
	@echo "Variables that affect all the above rules:"
	@echo "	IPBRIDGE_BUILD=debug          When the ipbridge daemon is compiled / installed, the debug variant is used"
	@echo "	                              Unless otherwise specified, the release build is always used."
	@echo "	TEST_LICENSES=1               Suppresses compiling of the QSDK when using the licenses target."
	@echo
	@echo "Make rules for $(PRODUCT_BUILD) builds (Will fail if BUILD != $(PRODUCT_BUILD))"
	@echo "	signPackage                   Generate a package for $(PRODUCT_BUILD) signing in the '$(RELEASE_DIR)' directory."
	@echo
	@echo "Make rules that interact with the target (Will fail if IPADDR is not defined):"
	@echo "	package/<name>/sync           Synchronize all installables for the specified package to the target at IPADDR."
	@echo "	package/<name>/sync+restart   Synchronize and restart the specified package to the target at IPADDR."
	@$(foreach command,$(PACKAGE_INIT_COMMANDS),$(call printPackageInitHelp,$(command)))
	@echo
	@echo "Standard sideload targets (Will fail if IPADDR is not defined):"
	@echo "	sideload                      Sideload the target at IPADDR."
	@echo "	sideload/factory              Sideload the target at IPADDR, resetting to factory defaults."
	@echo
	@echo "	NOTES:"
	@echo "	  allowdowngrading is automatically unlocked."
	@echo "	  If BUILD=$(DEVELOP_BUILD), the $(DEVELOP_BUILD) image is side-loaded." 
	@echo "	  If BUILD=$(PRODUCT_BUILD), the $(PRODUCT_BUILD) image is side-loaded." 
	@echo
	@echo "Additional sideload targets (Will fail if IPADDR is not defined):"
	@echo "	$(PRODUCT_SIDELOAD_TARGET)"
	@$(foreach unlocker,$(UNLOCK_TARGETS),$(call printSideloadHelp,$(unlocker)))
	@echo
	@echo "Run-once make rules (Will not be repeated unless dependencies change):"
	@echo "	qsdk.checkout                 Checks out the QSDK."
	@echo "	qsdk.update-feeds             Configures the QSDK feeds."
	@echo "	qsdk.update-download-cache    Updates the QSDK download cache"
	@echo
	@echo "Redo run-once make rules:"
	@echo "	qsdk.checkout/force           Update the QSDK to the latest sources NOW."
	@echo "	qsdk.update-feeds/force       Update the QSDK feeds NOW."
	@echo ""
	@echo "Purge run-once make rules (Expect a redo of the run-once rule on the next make):"
	@echo "	qsdk.checkout/purge           Force a subsequent redo of 'qsdk.checkout'"
	@echo "	qsdk.update-feeds/purge       Force a subsequent redo of 'qsdk.update-feeds'"
	@echo "	qsdk.checkout/force           Forces a re-checkout of the qsdk sources"
	@echo ""
	@echo "Homekit tools:"
	@echo "	homekit.clean                 Cleans all homekit packages"
	@echo ""
	@echo "CAE OpenWRT build repository management:"
	@echo "	update-cae-openwrt-build      Updates the CAE OpenWRT build repository with the latest ipbridge binaries"
	@echo ""
	@echo "Developer assistance:"
	@echo "	print-<make_variable>         Prints the specified make variable"
	@echo ""
	@echo "Useful examples:"
	@echo
	@echo "	Prints the REQUIRED_EXECUTABLES make variable"
	@echo "	  make print-REQUIRED_EXECUTABLES"
	@echo
	@echo "	Compile the linux target within the QSDK with verbose output:"
	@echo "	  make target/linux/install V=s"
	@echo
	@echo "	Purge the linux target within the QSDK:"
	@echo "	  make target/linux/purge"
	@echo
	@echo "	Recompile the linux target within the QSDK:"
	@echo "	  make target/linux/force"
	@echo
	@echo "	Purge (clean) the Hue ipbridge build directory:"
	@echo "	  make package/hue-ipbridge/purge"
	@echo
	@echo "	Recompile the Hue ipbridge package with verbose output:"
	@echo "	  make package/hue-ipbridge/force V=s"
	@echo
	@echo "	Recompile the debug variant of the Hue ipbridge package with verbose output:"
	@echo "	  make package/hue-ipbridge/force V=s IPBRIDGE_BUILD=debug"
	@echo
	@echo "	Synchronize the latest compiled Hue ipbridge installables to the target with verbose output:"
	@echo "	  make IPADDR=192.168.1.10 package/hue-ipbridge/sync V=s"
	@echo
	@echo "	Synchronize and restart the Hue ipbridge daemon on the target with verbose output:"
	@echo "	  make IPADDR=192.168.1.10 package/hue-ipbridge/sync+restart V=s"
	@echo
	@echo "	Recompile the Hue ipbridge package, syncronize and restart the Hue ipbridge daemon with verbose output:"
	@echo "	  make IPADDR=192.168.1.10 package/hue-ipbridge/{force,sync+restart} V=s"
	@echo
	@echo "	Restart the Hue ipbridge daemon:"
	@echo "	  make IPADDR=192.168.1.10 package/hue-ipbridge/init/restart V=s"
	@echo
	@echo "	Sideload the target with the latest compiled image:"
	@echo "	  make IPADDR=192.168.1.10 sideload"
	@echo
	@echo "	Sideload the target with the latest compiled image, resetting to factory settings:"
	@echo "	  make IPADDR=192.168.1.10 sideload/factory"
	@echo
	@echo "	Unlock the commissioning interface on the target:"
	@echo "	  make IPADDR=192.168.1.20 unlock/nowhitelist_noreboot_allowcommissioninginterface"
	@echo
	@echo "	Unlock the factory interface on the target:"
	@echo "	  make IPADDR=192.168.1.20 unlock/nowhitelist_noreboot_allowfactoryinterface"
	@echo
	@echo "	Unlock the test interface on the target:"
	@echo "	  make IPADDR=192.168.1.20 unlock/nowhitelist_noreboot_allowtestinterface"
	@echo
	@echo "	Rebuild the rootfs with a debug variant of the ipbridge daemon and sideload the target:"
	@echo "	  make IPADDR=192.168.1.10 IPBRIDGE_BUILD=debug force sideload"
	@echo
	@echo "	Rebuild the rootfs with a debug variant of the ipbridge daemon, sideload the target and reset to factory defaults:"
	@echo "	  make IPADDR=192.168.1.10 IPBRIDGE_BUILD=debug force sideload/factory"
	@echo

.PHONY : cleanReleaseDir
cleanReleaseDir:
	@$(call printInColor,$(STEP_INFO_COLOR),Cleaning $(RELEASE_DIR))
	@rm -rf $(RELEASE_DIR)

$(RELEASE_DIR) $(DEPS_BUILD_DIR):
	@$(MKDIR) -p $@

.PHONY : assert-build-requirements
assert-build-requirements: $(foreach package,$(REQUIRED_EXECUTABLES),$(package).checkCallable) $(foreach package,$(REQUIRED_PYTHON_PACKAGES),$(package).checkUsablePython)
	$(call stepinfo)

.PHONY : %.checkCallable
%.checkCallable:
	@which $* >/dev/null || ( $(call printInColor,$(STEP_INFO_COLOR),error: '$*' missing on build host. Please install via apt-get.); exit 1 )

.PHONY : %.checkUsablePython
%.checkUsablePython: $(DEPS_BUILD_DIR)
	@echo 'import $*' > $</$@.py
	@python $</$@.py >/dev/null 2>&1 || ( $(call printInColor,$(STEP_INFO_COLOR),error: '$*' python package missing on build host. Install with: sudo pip install python-$*); exit 1 )
	@echo '$(PYTHON_PACKAGE_TEST_$*)' >> $</$@.py
	@python $</$@.py >/dev/null 2>&1 || ( $(call printInColor,$(STEP_INFO_COLOR),error: '$*' wrong python package or version. Please first remove '$*'. Then install with: sudo pip install python-$*); exit 1 )

# Creates the U-Boot 
$(MKENVIMAGE):
	@$(call printInColor,$(STEP_INFO_COLOR),Making $(notdir $@))
	@$(MAKE) -C $(QSDK_HOST_UBOOT_BUILD_DIR) tools-all $(call quietUnlessErrorsOrVerbose)

# Recompile the QSDK, forcing a recompile of the hue packages 
.PHONY : force
force: qsdk.compile/purge $(foreach package,$(HUE_PACKAGES),package/$(package)/purge) all

.SECONDEXPANSION:
$(BIN_SOURCE_uboot_and_environment): $$(@D)/$(product)_uboot.bin $$(@D)/$(product)_uboot_environment.bin
	$(call stepinfo)
	@$(SREC_CAT) $(foreach bin,$^,$(bin) -binary -offset $(NOR_OFFSET_$(basename $(notdir $(bin)))) -fill 0xff $(NOR_OFFSET_$(basename $(notdir $(bin)))) $(NOR_END_$(basename $(notdir $(bin))))) -o $@ -binary

# Creates the appropriate U-Boot environment image in the release directory
#   %.bin is taken as the destination name
.SECONDEXPANSION:
%_uboot_environment.bin: configs/$$(notdir $$*).u-boot-environment.txt $(MKENVIMAGE)
	$(call stepinfo)
	@$(MKDIR) -p $(dir $@)
	@$(MKENVIMAGE) $(MKENVIMAGE_OPTS_$(notdir $*)) $< | \
	  $(SREC_CAT) - -Binary -Fill 0xFF 0x0 $(NOR_SIZE_$(notdir $*)_uboot_environment) -Output - -Binary >$@

# Copies an image bin or hex file to the release directory
#   %.bin or %.hex is taken as the destination name
#   BIN_SOURCE_% must be defined to specify the source path 
%.bin %.hex: qsdk.compile
	$(call stepinfo)
	@$(MKDIR) -p $(dir $@)
	@cp $(BIN_SOURCE_$(notdir $*)) $@

# Generates an over-the-air update / side-loading image in the release directory
.PHONY : otauImage
otauImage: qsdk.compile $(OTAU_IMAGE)

.PHONY: signPackage
signPackage: otauImage $(OTAU_SIGN_PACKAGE)

# Generates a number of develop images to change the software update behavior of the board
.PHONY : unlockImages
unlockImages: assert-build-requirements $(UNLOCK_IMAGES)

.SECONDEXPANSION:
.PHONY : $(RELEASE_FACTORY_DIR)/$(product)
$(RELEASE_FACTORY_DIR)/$(product): $$@/$$(notdir $$@)_uboot_and_environment.bin $$@/$$(notdir $$@)_uboot.bin $$@/$$(notdir $$@)_uboot_environment.bin $$@/$$(notdir $$@)_art.bin $$@/kernel.bin $$@/root.bin $$@/overlay.bin $$@/$(zigbee_soc).hex
	$(call stepinfo)

# Generates the factory images in the release directory
.PHONY : factoryImages
factoryImages: qsdk.compile $(RELEASE_FACTORY_DIR)/$(product)
	$(call stepinfo)

.PHONY : licenses
licenses: $(LICENSES_DEPS)
	$(call stepinfo)
	@$(MKDIR) -p $(dir $(LIST_OF_FILES_IN_ROOT))
	@$(OPEN_SOURCE_COMPLIANCE_TOOL) --licenses-dest-dir $(RELEASE_LICENSES_DIR) $(call quietUnlessErrorsOrVerbose)
 
.PHONY : pushPackageSources
pushPackageSources: $(LICENSES_DEPS)
	$(call stepinfo)
ifneq "$(BUILD)" "$(PRODUCT_BUILD)"
	@echo "$@ not supported when BUILD=$(BUILD)" >&2
	exit 1
endif
	@rm -rf $(PACKAGE_SOURCES_BUILD_DIR)
	@$(MKDIR) $(PACKAGE_SOURCES_BUILD_DIR)
	@$(PACKAGE_ARCHIVE_TOOL) -p $(PACKAGE_SOURCES_BUILD_DIR) # Prepare directory for git push
	@$(OPEN_SOURCE_COMPLIANCE_TOOL) --package-source-dest-dir $(PACKAGE_SOURCES_BUILD_DIR) $(call quietUnlessErrorsOrVerbose)
ifndef TEST_PACKAGE_SOURCE_GENERATION
	@$(PACKAGE_ARCHIVE_TOOL) -c $(PACKAGE_SOURCES_BUILD_DIR) # Push package source changes and tag revision
endif

# Generates a zipped tar container with the kernel and rootfs 
.SECONDEXPANSION:
$(OTAU_BUILD_DIR)/container.tar.gz: $$(dir $$@)kernel.bin $$(dir $$@)root.bin
	$(call stepinfo)
	@tar -C $(dir $@) -czf $@ $(notdir $^)

$(OTAU_SIGN_PACKAGE): $(OTAU_BUILD_DIR)/kernel.bin $(RELEASE_DIR)
	$(call assertBuildIs,$(PRODUCT_BUILD))
	$(call stepinfo)
	@$(CREATE_SIGN_PACKAGE) --kernel-image $< \
	                        --root-archive $(SIGNING_SOURCE_root) \
	                        --ubinize-ini-file $(SIGNING_SOURCE_ubinize_ini) \
	                        --host-staging-bin-dir $(QSDK_HOST_BIN_DIR) \
	                        --bootloader-image-file-path $(BIN_SOURCE_uboot_and_environment)\
	                        --overlay-image-file-path $(BIN_SOURCE_overlay) \
	                        --zigbee-soc-hex-file-path $(BIN_SOURCE_$(zigbee_soc)) \
	                        --zigbee-soc-info-file-path $(SIGNING_SOURCE_zigbee_version) \
	                        --revision-file $(FIRMWARE_REVISION_FILE) \
	                        --output-file-path $@ $(call quietUnlessErrorsOrVerbose)

# Generates an over-the-air update / side-loading image in the release directory
$(OTAU_IMAGE): $(OTAU_BUILD_DIR)/container.tar.gz $(RELEASE_DIR)
	$(call stepinfo)
	@$(CREATE_FIRMWARE) -allowLocalVersion -product $(PRODUCT) -priKey=$(FIRMWARE_DEV_PRIKEY) -versionFile $(FIRMWARE_ROOT_DIR)/revision.txt -out $@ $< $(call quietUnlessErrorsOrVerbose)

$(RELEASE_UNLOCK_DIR)/%.fw2 $(RELEASE_DIR)/%.fw2:
	$(call stepinfo)
	@$(MKDIR) -p $(dir $@)
	@$(CREATE_FIRMWARE) -allowLocalVersion -product $(PRODUCT) -priKey=$(FIRMWARE_DEV_PRIKEY) -$(subst _, -,$*) -out $@ $(call quietUnlessErrorsOrVerbose)
 
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

# Check the QSDK out from the source archives
qsdk.checkout: $(QSDK_SOURCE_DEFINIONS)
	$(call stepinfo)
	@$(MKDIR) -p $(QUALCOMM_DIR)
	@cd $(QUALCOMM_DIR) && repo init -u $(MANIFEST_REPOSITORY) -b $(MANIFEST_BRANCH) -m $(MANIFEST_FILE) --repo-url=$(REPO_REPOSITORY) --repo-branch=$(REPO_BRANCH) && repo sync
	$(call done)

define syncQsdkConfig
	@$(call printInColor,$(STEP_INFO_COLOR),Using $(QSDK_CONFIG_FILE))
	@cp -a $(QSDK_CONFIG_FILE) $(QSDK_CONFIG_DEST)
	@$(MAKE) -C $(QSDK_DIR) defconfig $(call quietUnlessErrorsOrVerbose)
endef

define qsdkMake
	$(call syncQsdkConfig)
	@$(call printInColor,$(STEP_INFO_COLOR),Within $(QSDK_DIR): make $(1))
	$(2)@$(MAKE) --no-print-directory -C $(QSDK_DIR) $(1) 
endef

BUILT_HOMEKIT_PACKAGES=$(strip $(foreach package,$(notdir $(wildcard $(HOMEKIT_SOURCE_DIR)/package/*)),$(if $(wildcard $(QSDK_MIPS_BUILD_DIR)/$(package)*),$(package),)))

define cleanHomekitPackages
        $(if $(call BUILT_HOMEKIT_PACKAGES),$(call qsdkMake,$(foreach package,$(call BUILT_HOMEKIT_PACKAGES),package/$(package)/clean),-) $(call quietUnlessErrorsOrVerbose),)
endef

define assertIpAddrDefined
	@[ -n "$(IPADDR)" ] || ( $(call printInColor,$(STEP_INFO_COLOR),error: $@: IPADDR is not defined.); exit 1 )
endef

define onLocalChangesToDlCache
$(call printInColor,$(YELLOW),\
\n+--------------------------------------------------------------------------+\
\n| !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! WARNING !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! |\
\n+--------------------------------------------------------------------------+\
\n| The QSDK download cache has changed which can later cause build breakage |\
\n+--------------------------------------------------------------------------+\
\n|                                                                          |\
\n| This likely is the result of having added packages with:                 |\
\n|     make qsdk/menuconfig                                                 |\
\n|                                                                          |\
\n| If the changes are needed upstream / in the trunk you commit them:       |\
\n|     make qsdk.commit-download-cache                                      |\
\n|                                                                          |\
\n| Alternatively you can clean up your local download cache by running:     |\
\n|     make qsdk.clean-download-cache                                       |\
\n|                                                                          |\
\n+--------------------------------------------------------------------------+\
\n\
)
endef

.PHONY: update-cae-openwrt-build
update-cae-openwrt-build:
	$(call stepinfo)
	@./tools/update-cae-build-repo.sh
 
.PHONY: homekit.clean 
homekit.clean:
	$(call stepinfo)
	$(call cleanHomekitPackages)

# Clone the homekit sources
$(HOMEKIT_SOURCE_DIR):
	$(call stepinfo)
	@$(MKDIR) -p $(dir $@)
	@$(GIT) clone $(HOMEKIT_REPOSITORY) $@

homekit.checkout: $(HOMEKIT_SOURCE_DIR) $(HOMEKIT_SOURCE_DEFINIONS)
	$(call stepinfo)
	$(call cleanHomekitPackages)
	@cd $< && $(GIT) fetch --all && $(GIT) fetch --tags && $(GIT) checkout -q $(HOMEKIT_RELEASE)
	$(call done)

$(QSDK_DL_CACHE_GIT_DIR): qsdk.update-feeds
	$(call stepinfo)
	@$(MKDIR) -p $(dir $@)
	@(cd $(dir $@) && $(GIT) init . && ($(GIT) remote rm origin >/dev/null 2>&1; $(GIT) remote add origin $(QSDK_DL_CACHE_REPO))) $(call quietUnlessErrorsOrVerbose)

# Updates the package download cache
# We use a download cache to prevent unavailability any of the numerous package download sites from breaking our build. Essentially
# we are consolodating our point of failure on github, without which we can do very little anyway 
qsdk.update-download-cache: $(QSDK_DL_CACHE_GIT_DIR) $(QSDK_CONFIG_FILE)
	$(call stepinfo)
	@(cd $(dir $<) && $(GIT) fetch -q --depth 1 origin $(product) && $(GIT) checkout -q -f $(product) && $(GIT) reset -q --hard origin/$(product)) $(call quietUnlessErrorsOrVerbose)
	$(call done)
	
.PHONY : qsdk.assert-download-cache-up-to-date
qsdk.assert-download-cache-up-to-date:
	$(call stepinfo)
	@cd $(dir $(QSDK_DL_CACHE_GIT_DIR)) && $(ASSERT_QSDK_DL_CACHE_REPO_UP_TO_DATE) || $(call onLocalChangesToDlCache) 

.PHONY : qsdk.clean-download-cache
qsdk.clean-download-cache:
	$(call stepinfo)
	@cd $(dir $(QSDK_DL_CACHE_GIT_DIR)) && $(GIT) clean -f

.PHONY : qsdk.commit-download-cache
qsdk.commit-download-cache:
	$(call stepinfo)
	@cd $(dir $(QSDK_DL_CACHE_GIT_DIR)) && $(GIT) add -A && $(GIT) commit && $(GIT) push origin HEAD

# Update the QSDK feeds
qsdk.update-feeds: $(QSDK_CONFIG_FILE) qsdk.checkout homekit.checkout
	$(call stepinfo)
	$(call qsdkMake,package/symlinks) $(call quietUnlessErrorsOrVerbose)
	$(call done)

ifeq "$(LAST_BUILT_QSDK_COMMIT)" ""
CHANGED_QSDK_BUILD_TARGETS:=target/linux
else
CHANGED_QSDK_BUILD_TARGETS:=
endif

ifneq "$(LAST_BUILT_UBOOT_COMMIT)" "$(call gitHead,uboot)"
CHANGED_QSDK_BUILD_TARGETS+=package/qca-legacy-uboot
endif

changedQsdkBuildTargets=\
  $(if $(LAST_BUILT_QSDK_COMMIT),$(shell $(AFFECTED_QSDK_MAKE_TARGETS) $(LAST_BUILT_QSDK_COMMIT)),target/linux) \
  $(if $(LAST_BUILT_UBOOT_COMMIT),$(if $(filter-out $(LAST_BUILT_UBOOT_COMMIT),$(call gitHead,uboot)),package/qca-legacy-uboot),package/qca-legacy-uboot)

define warnFileChangeAffecting
	@$(call printInColor,$(YELLOW),Detected file changes affecting: $(1))
endef

.PHONY : qsdk.clean-changed-packages
qsdk.clean-changed-packages:
	$(call warnFileChangeAffecting,$(call changedQsdkBuildTargets))
	$(call qsdkMake,$(foreach target,$(call changedQsdkBuildTargets),$(target)/clean),-) $(call quietUnlessErrorsOrVerbose)

# Compile the QSDK
.PHONY : qsdk.compile
qsdk.compile: assert-build-requirements qsdk.update-download-cache qsdk.update-feeds qsdk.clean-changed-packages qsdk/world qsdk.assert-download-cache-up-to-date
	$(call stepinfo)
	$(call updateLastBuiltCommits)

define sideloadImage
	$(call stepinfo)
	$(call assertIpAddrDefined)
	@echo Posting: $(1)
	@$(CURL) --form "fileupload=@$(1)" http://$(IPADDR)/updater
	@echo
endef

.PHONY : $(UNLOCK_TARGETS)
$(UNLOCK_TARGETS): $(UNLOCK_IMAGES)
	$(call sideloadImage,$(RELEASE_UNLOCK_DIR)/$(notdir $@).fw2)

.PHONY : $(PRODUCT_SIDELOAD_TARGET)
$(PRODUCT_SIDELOAD_TARGET):
	$(call sideloadImage,$(OTAU_IMAGE))

# Update the bridge
.PHONY : sideload
sideload : unlock/$(STANDARD_SIDELOAD_UNLOCK) $(PRODUCT_SIDELOAD_TARGET)

# Deprecation warning
.PHONY : %.update
%.update :
	@echo "error: 'make $@' is deprecated. Please use 'make IPADDR=$* sideload'." >&2; exit 1

# Update the bridge using factory defaults
.PHONY : sideload/factory
sideload/factory : unlock/$(FACTORY_RESET_SIDELOAD_UNLOCK) $(PRODUCT_SIDELOAD_TARGET)

# Deprecation warning
.PHONY : %.factory_update
%.factory_update :
	@echo "error: 'make $@' is deprecated. Please use 'make IPADDR=$* sideload/factory'." >&2; exit 1

# Forcefully rebuild the specified QSDK package
.PHONY : package/%/force
package/%/force: package/%/purge package/%/compile
	$(call stepinfo)

# Controls / syncs specified QSDK package
.PHONY : $(PACKAGE_INIT_CMD_TARGETS) $(PACKAGE_SYNC_CMD_TARGETS)
$(PACKAGE_INIT_CMD_TARGETS) $(PACKAGE_SYNC_CMD_TARGETS):
	$(call stepinfo)
	$(call assertIpAddrDefined)
	@$(TARGET_PACKAGE_CONTROL) $(IPADDR) $(notdir $@) $* $(call quietUnlessErrorsOrVerbose)

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
qsdk/menuconfig: assert-build-requirements qsdk.update-feeds
	$(call stepinfo)
	$(call qsdkMake,$(notdir $@))
	@$(SYNC_CONFIGS) --product-config $(call qsdkConfigFile,$(PRODUCT_BUILD)) \
	                 --develop-config $(call qsdkConfigFile,$(DEVELOP_BUILD)) \
	                 --new-config $(QSDK_DIR)/.config --$(BUILD)

# Execute a QSDK make rule
.PHONY : qsdk/% 
qsdk/%: assert-build-requirements qsdk.update-feeds
	$(call stepinfo)
	$(call qsdkMake,$*) $(dumpBuildLogIfError)

# Purges a local make step so that the step will be redone on the next build
.PHONY : qsdk.%/purge 
qsdk.%/purge: assert-build-requirements
	$(call stepinfo)
	@rm -f $(STATE_DIR)/qsdk.$*
	@echo step.$* purged

# Forcefully rebuild the run-once rule
.PHONY : qsdk.%/force
qsdk.%/force: assert-build-requirements
	$(call stepinfo)
	@$(MAKE) qsdk.$*

# Helper to print internal make variables
.PHONY : print-%
print-%:
	@echo $*=$($*)
