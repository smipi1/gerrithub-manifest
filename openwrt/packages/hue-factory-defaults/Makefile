# Copyright (C) 2015 Philips Lighting

include $(TOPDIR)/rules.mk

PKG_NAME:=hue-factory-defaults
PKG_RELEASE:=0.0

PKG_BUILD_DIR := $(BUILD_DIR)/$(PKG_NAME)

include $(INCLUDE_DIR)/package.mk

define Package/hue-factory-defaults
  SECTION:=utils
  CATEGORY:=Hue
  TITLE:=Hue bridge factory defaults
endef

define Package/hue-factory-defaults/description
  This package restores the Hue bridge defaults after a factory reset:
  - Resolve network LAN address with DHCP
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	echo "do_nothing:" > $(PKG_BUILD_DIR)/Makefile
endef

define Package/hue-factory-defaults/install
	$(INSTALL_DIR) $(1)/etc/uci-defaults
	$(INSTALL_BIN) ./files/etc/uci-defaults/Z01-update-factory-reset-counter $(1)/etc/uci-defaults
	$(INSTALL_BIN) ./files/etc/uci-defaults/Z02-setup-networking-defaults $(1)/etc/uci-defaults
	$(INSTALL_BIN) ./files/etc/uci-defaults/Z03-configure-homekit $(1)/etc/uci-defaults
	$(INSTALL_BIN) ./files/etc/uci-defaults/Z04-configure-firewall $(1)/etc/uci-defaults
	$(INSTALL_DIR) $(1)/etc/config
	$(INSTALL_BIN) ./files/etc/config/firewall $(1)/etc/config
	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./files/etc/init.d/factoryreset $(1)/etc/init.d
	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) ./files/usr/sbin/factoryreset.sh $(1)/usr/sbin
	$(INSTALL_BIN) ./files/usr/sbin/factoryreset_daemon $(1)/usr/sbin
	$(INSTALL_DIR) $(1)/home/homekit/var
endef

$(eval $(call BuildPackage,hue-factory-defaults))

