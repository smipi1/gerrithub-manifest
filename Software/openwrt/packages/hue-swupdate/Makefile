# Copyright (C) 2015 Philips Lighting

include $(TOPDIR)/rules.mk

PKG_NAME:=hue-swupdate
PKG_RELEASE:=0.0

PKG_BUILD_DIR := $(BUILD_DIR)/$(PKG_NAME)

IPBRIDGE_BUILD_TYPE:=release


SWUPDATE_DECRYPT:=enc.k
SWUPDATE_PROD_PUB_KEY:=enc.k
SWUPDATE_TOOLS_DIR=$(abspath $(TOPDIR)/../../../bridge/tools/make_firmware_image)
SWUPDATE_CERTS_SOURCE_DIR=$(SWUPDATE_TOOLS_DIR)/certs
SWUPDATE_DECRYPT_KEY_LOCATION:=$(SWUPDATE_CERTS_SOURCE_DIR)/enc.k
SWUPDATE_PROD_PUB_KEY_LOCATION:=$(SWUPDATE_CERTS_SOURCE_DIR)/RSA_rel_01_pub.pem
SWUPDATE_DEV_PUB_KEY_LOCATION:=$(SWUPDATE_CERTS_SOURCE_DIR)/RSA_dev_01_pub.pem

include $(INCLUDE_DIR)/package.mk

define Package/hue-swupdate
  SECTION:=utils
  CATEGORY:=Hue
  TITLE:=Software Update daemon
  DEPENDS:=+hue-ipbridge
endef

define Package/hue-swupdate/description
 This package contains the Hue software update daemon.
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	echo "do_nothing:" > $(PKG_BUILD_DIR)/Makefile
endef

define Package/hue-swupdate/install
	$(INSTALL_DIR) $(1)/lib/functions
	$(INSTALL_BIN) ./files/lib/functions/certs.sh $(1)/lib/functions
	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) ./files/usr/sbin/swupdate $(1)/usr/sbin
	$(INSTALL_BIN) $(SWUPDATE_TOOLS_DIR)/aes-256-cbc.sh $(1)/usr/sbin 
	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./files/etc/init.d/swupdate $(1)/etc/init.d
	$(INSTALL_DIR) $(1)/etc/uci-defaults
	$(INSTALL_BIN) ./files/etc/uci-defaults/32-swupdate $(1)/etc/uci-defaults
	$(INSTALL_DIR) $(1)/home/swupdate/certs
	$(CP) $(SWUPDATE_DECRYPT_KEY_LOCATION) $(1)/home/swupdate/certs/
	$(CP) $(SWUPDATE_PROD_PUB_KEY_LOCATION) $(1)/home/swupdate/certs/
	$(CP) $(SWUPDATE_DEV_PUB_KEY_LOCATION) $(1)/home/swupdate/certs/
endef

$(eval $(call BuildPackage,hue-swupdate))
