# Copyright (C) 2015 Philips Lighting

include $(TOPDIR)/rules.mk

PKG_NAME:=hue-ipbridge
PKG_RELEASE:=0.0

PKG_BUILD_DIR := $(BUILD_DIR)/$(PKG_NAME)

IPBRIDGE_BUILD?=release
IPBRIDGE_BUILD_DIR:=$(abspath $(TOPDIR)/../../../bridge/build)
IPBRIDGE_SOFTWARE_DIR:=$(abspath $(TOPDIR)/../../..)
IPBRIDGE_REVISION:=$(shell cat $(IPBRIDGE_SOFTWARE_DIR)/revision.txt 2>/dev/null)
ifeq "$(IPBRIDGE_REVISION)" ""
IPBRIDGE_REVISION:=local
endif
IPBRIDGE_OUTPUT_DIR:=$(IPBRIDGE_BUILD_DIR)/linux_qualcomm_$(IPBRIDGE_BUILD)
IPBRIDGE_APP:=$(IPBRIDGE_OUTPUT_DIR)/application/targets/ipbridge/ipbridge
IPBRIDGE_IO_APP:=$(IPBRIDGE_OUTPUT_DIR)/application/targets/ipbridge_io/ipbridge_io
IPBRIDGE_INSTALL_DIR:=/usr/sbin

ZIGBEE_SOC_UPDATER_APP:=$(IPBRIDGE_OUTPUT_DIR)/platform/targets/zigbee_soc_updater/zigbee_soc_updater

ZIGBEE_SOURCE_DIR:=$(abspath $(TOPDIR)/../../../zigbee/samr21)
ZIGBEE_FIRMWARE_IMAGE:=$(ZIGBEE_SOURCE_DIR)/ZigBeeBridge-HueV2-SAMR21_8001.sbl
ZIGBEE_FIRMWARE_RELEASE_INFO:=$(ZIGBEE_SOURCE_DIR)/ZigBeeBridge-HueV2-SAMR21.releaseinfo
ZIGBEE_FIRMWARE_VERSION:=$(PKG_BUILD_DIR)/version
BANNER_FILE:=$(PKG_BUILD_DIR)/banner

export PATH
export TARGET_TOOLDIR=$(dir $(shell which $(TARGET_CC)))
export TARGET_CC
export TARGET_CXX
export STAGING_DIR
export TARGET_LDFLAGS

include $(INCLUDE_DIR)/package.mk

define Package/hue-ipbridge
  SECTION:=utils
  CATEGORY:=Hue
  TITLE:=IP Bridge daemon
  DEPENDS:=+libpthread +librt +libgpio +libuci +libubus +libubox +libblobmsg-json +libopenssl \
           +hk_lib +ipb_homekit_cae +hue-factory-defaults +hue-swupdate 
endef

define Package/hue-ipbridge/description
 This package contains the Hue IP Bridge daemon.
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
endef

define Build/Configure
	$(MAKE) -C $(IPBRIDGE_BUILD_DIR) all.configure
endef

define Build/Compile
	$(MAKE) -C $(IPBRIDGE_BUILD_DIR) linux_qualcomm_$(IPBRIDGE_BUILD)
	awk -F '=' '/Version=/{print $$$$2}' $(ZIGBEE_FIRMWARE_RELEASE_INFO) >$(ZIGBEE_FIRMWARE_VERSION)
	sed 's/01999999/'$(IPBRIDGE_REVISION)'/g' ./files/etc/banner > ${BANNER_FILE}
endef

define Build/Clean
	-rm -rf $(IPBRIDGE_OUTPUT_DIR)
endef

define Package/hue-ipbridge/install
	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) $(IPBRIDGE_APP) $(1)/usr/sbin
	$(INSTALL_BIN) $(IPBRIDGE_IO_APP) $(1)/usr/sbin
	$(INSTALL_BIN) ./files/usr/sbin/factoryreset $(1)/usr/sbin
	$(INSTALL_BIN) ./files/usr/sbin/ipbridge_test $(1)/usr/sbin
	$(INSTALL_DIR) $(1)/etc
	$(INSTALL_BIN) ./files/etc/profile $(1)/etc
	$(INSTALL_BIN) ${BANNER_FILE} $(1)/etc
	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./files/etc/init.d/ipbridge $(1)/etc/init.d
	$(INSTALL_DIR) $(1)/etc/rc.button
	$(INSTALL_BIN) ./files/etc/rc.button/BTN_0 $(1)/etc/rc.button
	$(INSTALL_BIN) ./files/etc/rc.button/BTN_1 $(1)/etc/rc.button
	$(INSTALL_DIR) $(1)/home/ipbridge/var
	$(INSTALL_BIN) $(ZIGBEE_SOC_UPDATER_APP) $(1)$(IPBRIDGE_INSTALL_DIR)
	$(INSTALL_DIR) $(1)/lib/firmware
	$(CP) $(ZIGBEE_FIRMWARE_IMAGE) $(1)/lib/firmware/zigbee.sbl
	$(CP) $(ZIGBEE_FIRMWARE_VERSION) $(1)/lib/firmware/zigbee.version
endef


$(eval $(call BuildPackage,hue-ipbridge))

