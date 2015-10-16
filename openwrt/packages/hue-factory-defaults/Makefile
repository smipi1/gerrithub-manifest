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
  DEPENDS:=+base-files +uboot-envtools +hk_hap +hk_mdns
endef

define Package/hue-factory-defaults/description
  This package restores the Hue bridge defaults after a factory reset:
  - Resolve network LAN address with DHCP
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	echo "do_nothing:" > $(PKG_BUILD_DIR)/Makefile
endef

define Build/Compile
	cd ./src && $(STAGING_DIR_HOST)/bin/ubinize -o $(PKG_BUILD_DIR)/factory-overlay.ubi -p 128KiB -m 2048 ubinize-overlay.ini
endef

define Package/hue-factory-defaults/install
	$(INSTALL_DIR) $(1)/lib/functions
	$(INSTALL_BIN) ./files/lib/functions/mtd.sh $(1)/lib/functions/
	$(INSTALL_DIR) $(1)/lib/preinit
	$(INSTALL_BIN) ./files/lib/preinit/75_factory_reset $(1)/lib/preinit/
	$(INSTALL_DIR) $(1)/etc/uci-defaults
	$(INSTALL_BIN) ./files/etc/uci-defaults/update-factory-reset-counter $(1)/etc/uci-defaults
	$(INSTALL_BIN) ./files/etc/uci-defaults/configure-homekit $(1)/etc/uci-defaults
	$(INSTALL_BIN) ./files/etc/uci-defaults/hbpl-695_ula_prefix $(1)/etc/uci-defaults
	$(INSTALL_BIN) ./files/etc/uci-defaults/remove_link_local_and_default_routes $(1)/etc/uci-defaults
	$(INSTALL_DIR) $(1)/etc/config
	$(INSTALL_BIN) ./files/etc/config/firewall $(1)/etc/config
	$(INSTALL_DIR) $(1)/lib/images
	$(CP) $(PKG_BUILD_DIR)/factory-overlay.ubi $(1)/lib/images/
	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./files/etc/init.d/factoryreset $(1)/etc/init.d
	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) ./files/usr/sbin/factoryreset.sh $(1)/usr/sbin
	$(INSTALL_BIN) ./files/usr/sbin/factoryreset_daemon $(1)/usr/sbin
	$(INSTALL_DIR) $(1)/home/homekit/var

	# Install the configs to ROM (functionally replace what the UCI default scripts would otherwise have done after a factory reset)
	$(INSTALL_DIR) $(1)/etc
	$(INSTALL_BIN) ./files/etc/fw_env.config $(1)/etc
	$(INSTALL_DIR) $(1)/etc/config
	$(INSTALL_BIN) ./files/etc/config/system $(1)/etc/config
	$(INSTALL_BIN) ./files/etc/config/network $(1)/etc/config
	$(INSTALL_BIN) ./files/etc/config/ubootenv $(1)/etc/config
endef

$(eval $(call BuildPackage,hue-factory-defaults))

