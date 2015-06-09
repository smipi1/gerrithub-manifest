
define BuildPackage
all:
$(call Package/$(1)/install,$(TARGET_ROOT_DIR))
endef
