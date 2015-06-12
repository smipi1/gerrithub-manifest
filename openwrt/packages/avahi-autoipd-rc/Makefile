# Copyright (C) 2015 Philips Lighting

include $(TOPDIR)/rules.mk

PKG_NAME:=avahi-autoipd-rc
PKG_RELEASE:=0.0

PKG_BUILD_DIR := $(BUILD_DIR)/$(PKG_NAME)

include $(INCLUDE_DIR)/package.mk

define Package/avahi-autoipd-rc
  SECTION:=utils
  CATEGORY:=Hue
  TITLE:=avahi-autoipd action & startup scripts
  DEPENDS:=+avahi-autoipd
endef

define Package/avahi-autoipd-rc/description
  avahi-autoipd action & startup scripts
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	echo "do_nothing:" > $(PKG_BUILD_DIR)/Makefile
endef

define Package/avahi-autoipd-rc/install
	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./files/etc/init.d/avahi-autoipd $(1)/etc/init.d/
	$(INSTALL_DIR) $(1)/etc/avahi
	$(INSTALL_BIN) ./files/etc/avahi/avahi-autoipd.action $(1)/etc/avahi/
endef

$(eval $(call BuildPackage,avahi-autoipd-rc))
