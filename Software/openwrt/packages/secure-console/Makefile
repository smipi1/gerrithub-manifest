# Copyright (C) 2015 Philips Lighting

include $(TOPDIR)/rules.mk

PKG_NAME:=secure-console
PKG_RELEASE:=0.0

PKG_BUILD_DIR := $(BUILD_DIR)/$(PKG_NAME)

include $(INCLUDE_DIR)/package.mk

define Package/secure-console
  SECTION:=utils
  CATEGORY:=Hue
  TITLE:=Secure console
endef

define Package/secure-console/description
 This package makes the serial console secure. If a u-boot environment variable named `security`
 is defined, it wil be used as the root password hash in /etc/shadow. Any attempts to get a
 console on the serial port will result in a login prompt. If `security` is not defined in the
 u-boot environment, the user is dropped straight into the ash shell without a login prompt.
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	echo "do_nothing:" > $(PKG_BUILD_DIR)/Makefile
endef

define Package/secure-console/install
	$(INSTALL_DIR) $(1)/etc
	$(INSTALL_BIN) ./files/etc/inittab $(1)/etc
	$(INSTALL_DIR) $(1)/bin
	$(INSTALL_BIN) ./files/bin/secure-console.sh $(1)/bin
	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) ./files/usr/sbin/ssh-factory-key $(1)/usr/sbin
	$(INSTALL_DIR) $(1)/lib/functions
	$(INSTALL_BIN) ./files/lib/functions/secure-console.sh $(1)/lib/functions
	$(INSTALL_DIR) $(1)/etc/uci-defaults
	$(INSTALL_BIN) ./files/etc/uci-defaults/31-secure-console $(1)/etc/uci-defaults
	$(INSTALL_BIN) ./files/etc/uci-defaults/32-factory-keys $(1)/etc/uci-defaults
	$(INSTALL_DIR) $(1)/lib/preinit
	$(INSTALL_BIN) ./files/lib/preinit/99_10_failsafe_login $(1)/lib/preinit
endef

$(eval $(call BuildPackage,secure-console))
