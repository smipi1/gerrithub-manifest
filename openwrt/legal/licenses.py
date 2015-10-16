# default license filename is set to "LICENSE". 

from package import Package
from license import License
from PackageSource import PackageSource
from PlainPackageSource import PlainPackageSource
from DownloadedPackageSource import DownloadedPackageSource
from SymlinkedPackageSource import SymlinkedPackageSource
from GitPackageSource import GitPackageSource

NoVersion = None
NoWebsite = None
DontIgnoreIfOnTarget = None
IgnoreProprietaryCaeLicense = "proprietary CAE license"
IgnoreProprietaryPhilipsLicense = "proprietary Philips license"
OpenWrtRuntime = None
NoPatches = None
DefaultExcludes=["*\.o", "*\.a", "*\.so\.*", "*\.so", "*patches*", "\.pc", "\.hg"]

packages = [
     Package( "argp-standalone"
            , "1.3"
            , "https://github.com/jahrome/argp-standalone"
            , [ "argp-standalone-1.3" ]
            , [ License("GPL-2", None) ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget )
   , Package( "avahi"
            , "0.6.31"
            , "http://avahi.org/"
            , [ "avahi/nodbus/avahi-0.6.31" ]
            , [ License("LGPL-2.1", "LICENSE") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget )
   , Package( "avahi-autoipd-rc"
            , NoVersion
            , NoWebsite
            , [ "avahi-autoipd-rc" ]
            , [ License(None, None) ]
            , PackageSource()
            , IgnoreProprietaryPhilipsLicense )
   , Package( "binutils-2.22"
            , "2.22"
            , "http://www.gnu.org/software/binutils/"
            , [ "binutils-2.22" ]
            , [ License("GPL-2", None) ]
            , DownloadedPackageSource(
                "binutils-2.22.tar.bz2"
              , "toolchain/binutils/patches")
            , DontIgnoreIfOnTarget )
   , Package( "busybox"
            , "1.19.4"
            , "http://www.busybox.net/"
            , [ "busybox-1.19.4" ]
            , [ License("GPL-2", None) ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "bzip2"
            , "1.0.6"
            , "http://www.bzip.org/"
            , [ "bzip2-1.0.6" ]
            , [ License("<license>", "LICENSE") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget )
   , Package( "chacha20-simple"
            , "1.0"
            , "http://chacha20.insanecoding.org/"
            , [ "chacha20-simple-1.0" ]
            , [ License("ISC", None) ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget )
   , Package( "curve25519-donna"
            , "1.0"
            , "http://code.google.com/p/curve25519-donna/"
            , [ "curve25519-donna-1.0" ]
            , [ License("BSD-3", "LICENSE.md") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget )
   , Package( "dbus"
            , "1.8.8"
            , "http://dbus.freedesktop.org"
            , [ "dbus-1.8.8" ]
            , [ License("<license>", "COPYING") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "dnsmasq-nodhcpv6"
            , "2.66"
            , "http://www.thekelleys.org.uk/dnsmasq/"
            , [ "dnsmasq-nodhcpv6/dnsmasq-2.66" ]
            , [ License("GPL-2", None) ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "dropbear"
            , "2014.63"
            , "https://matt.ucc.asn.au/dropbear/dropbear.html"
            , [ "dropbear-2014.63" ]
            , [ License("MIT", "LICENSE"),
                License("BSD-2", "LICENSE") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget )
   , Package( "ed25519-donna"
            , "1.0"
            , "https://github.com/floodyberry/ed25519-donna"
            , [ "ed25519-donna-1.0" ]
            , [ License("PD", None) ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget )
   , Package( "elfutils-0.155"
            , NoVersion
            , "https://fedorahosted.org/elfutils/"
            , [ "elfutils-0.155" ]
            , [ License("<license>", "LICENSE") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "expat"
            , "2.0.1"
            , "http://www.libexpat.org/"
            , [ "expat-2.0.1" ]
            , [ License("<license>", "LICENSE") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "firewall"
            , "2014-03-20"
            , "https://openwrt.org/"
            , [ "firewall-2014-03-20" ]
            , [ License("ISC", None),
                License("MIT", None) ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "fstools"
            , "2014-04-07"
            , "https://openwrt.org/"
            , [ "fstools-2014-04-07" ]
            , [ License("LGPL-2.1", None) ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "gdb"
            , "7.5"
            , "http://www.gnu.org/software/gdb/"
            , [ "gdb-7.5" ]
            , [ License("<license>", "COPYING") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "tcpdump"
            , "4.5.1"
            , "http://www.tcpdump.org/"
            , [ "tcpdump-full/tcpdump-4.5.1" ]
            , [ License("<license>", "LICENSE") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "gdbm"
            , "1.10"
            , "http://www.gnu.org/software/gdbm"
            , [ "gdbm-1.10" ]
            , [ License("<license>", "LICENSE") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "hk_aac"
            , NoVersion
            , NoWebsite
            , [ "hk_aac" ]
            , [ License("<license>", "LICENSE") ]
            , PackageSource()
            , IgnoreProprietaryCaeLicense )
   , Package( "hk_common_osif"
            , "1.0.0"
            , NoWebsite
            , [ "hk_common_osif" ]
            , [ License("commercial", "LICENSE.txt") ]
            , PackageSource()
            , IgnoreProprietaryCaeLicense )
   , Package( "hk_core"
            , NoVersion
            , NoWebsite
            , [ "hk_core" ]
            , [ License("<license>", "LICENSE") ]
            , PackageSource()
            , IgnoreProprietaryCaeLicense )
   , Package( "hk_hap"
            , "1.0.0"
            , NoWebsite
            , [ "hk_hap" ]
            , [ License("commercial", "LICENSE.txt") ]
            , PackageSource()
            , IgnoreProprietaryCaeLicense )
   , Package( "hk_lib_philips"
            , "1.0.0"
            , NoWebsite
            , [ "hk_lib_philips" ]
            , [ License("commercial", "LICENSE.txt") ]
            , PackageSource()
            , IgnoreProprietaryCaeLicense )
   , Package( "hk_mdns"
            , "1.0.0"
            , NoWebsite
            , [ "hk_mdns" ]
            , [ License("commercial", "LICENSE.txt") ]
            , PackageSource()
            , IgnoreProprietaryCaeLicense )
   , Package( "hk_security"
            , NoVersion
            , NoWebsite
            , [ "hk_security" ]
            , [ License("<license>", "LICENSE") ]
            , PackageSource()
            , IgnoreProprietaryCaeLicense )
   , Package( "hk_wac"
            , NoVersion
            , NoWebsite
            , [ "hk_wac" ]
            , [ License("<license>", "LICENSE") ]
            , PackageSource()
            , IgnoreProprietaryCaeLicense )
   , Package( "hostapd-full"
            , "2015-01-20"
            , "https://w1.fi/hostapd/"
            , [ "hostapd-full/hostapd-2015-01-20" ]
            , [ License("BSD", "README") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "hue-factory-defaults"
            , "0.0.0"
            , NoWebsite
            , [ "hue-factory-defaults" ]
            , [ License(None, None) ]
            , PackageSource()
            , IgnoreProprietaryPhilipsLicense )
   , Package( "hue-ipbridge"
            , "6.5.0.14706"
            , NoWebsite
            , [ "hue-ipbridge" ]
            , [ License(None, None) ]
            , PackageSource()
            , IgnoreProprietaryPhilipsLicense )
   , Package( "hue-swupdate"
            , NoVersion
            , "http://www.meethue.com"
            , [ "hue-swupdate" ]
            , [ License(None, None) ]
            , PackageSource()
            , IgnoreProprietaryPhilipsLicense ) 
   , Package( "i2c-tools"
            , "2013-12-15"
            , "http://www.lm-sensors.org/wiki/I2CTools"
            , [ "i2c-tools-2013-12-15" ]
            , [ License("GPL-2", "COPYING"),
                License("LGPL-2.1", "COPYING.LGPL") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "iw"
            , "3.17"
            , "http://git.sipsolutions.net/iw.git/"
            , [ "iw-3.17" ]
            , [ License("ISC", None) ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget )
   , Package( "jsmn"
            , NoVersion
            , "http://zserge.com/jsmn.html"
            , [ "jsmn" ]
            , [ License("MIT", "LICENSE") ]
            , PlainPackageSource(
                "build_dir/target-mips_34kc_uClibc-0.9.33.2/jsmn/src/prj_jsmn",
                "qsdkRootDir",
                DefaultExcludes)
            , DontIgnoreIfOnTarget )
   , Package( "json-c"
            , "0.11"
            , "https://github.com/json-c/json-c/wiki"
            , [ "json-c-0.11" ]
            , [ License("MIT", "COPYING") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "libconfig"
            , "1.4.9"
            , "http://www.hyperrealm.com/libconfig/"
            , [ "libconfig-1.4.9" ]
            , [ License("LGPL-2.1", "COPYING.LIB") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "libdaemon"
            , "0.14"
            , "http://0pointer.de/lennart/projects/libdaemon/"
            , [ "libdaemon-0.14" ]
            , [ License("LGPL-2.1", "LICENSE") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "libiconv"
            , NoVersion
            , "http://www.gnu.org/software/libiconv/"
            , [ "libiconv" ]
            , [ License(None, "LICENSE") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "libiwinfo"
            , NoVersion
            , "http://wiki.openwrt.org/doc/devel/packages/iwinfo"
            , [ "libiwinfo" ]
            , [ License("GPL-2", "COPYING") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "libncurses"
            , "5.9"
            , "http://www.gnu.org/software/ncurses/"
            , [ "libncurses/ncurses-5.9" ]
            , [ License("BSD", "README") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "libnl"
            , "3.2.21"
            , "http://www.infradead.org/~tgr/libnl/"
            , [ "libnl-3.2.21" ]
            , [ License("LGPL-2.1", "COPYING") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "libnl-tiny"
            , "0.1"
            , "http://wiki.openwrt.org/doc/devel/packages/libnl-tiny"
            , [ "libnl-tiny-0.1" ]
            , [ License("LGPL-2.1", None) ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "libpcap"
            , "1.5.3"
            , "http://www.tcpdump.org"
            , [ "libpcap-1.5.3" ]
            , [ License("BSD", "LICENSE") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "libtool"
            , "2.4"
            , "http://www.gnu.org/software/libtool/libtool.html"
            , [ "libtool-2.4" ]
            , [ License(None, None) ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "libubox"
            , "2014-03-18"
            , "http://wiki.openwrt.org/doc/techref/ubox"
            , [ "libubox-2014-03-18" ]
            , [ License("ISC", "libubox.txt") 
              , License("GPL-2", None) 
              , License("LGPL-2.1", None) 
              , License("ISC", "libubox-avl.txt") 
              , License("ISC", "libubox-list.txt") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
    , Package( "openwrt-runtime"
            , NoVersion
            , "http://www.openwrt.org"
            , [ "linux-ar71xx_generic/button-hotplug",
                "linux-ar71xx_generic/base-files",
                "linux-ar71xx_generic/gpio-button-hotplug",
                "linux-ar71xx_generic/backports-20150324" ]
            , [ License("GPL-2", None) ]
            , GitPackageSource(".")
            , DontIgnoreIfOnTarget )
    , Package( "iptables"
            , "1.4.21"
            , "http://www.netfilter.org/"
            , [ "linux-ar71xx_generic/iptables-1.4.21" ]
            , [ License("GPL-2", "COPYING") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
    , Package( "libgpio"
            , "2015-01-15"
            , "https://github.com/Linutronix/libgpio"
            , [ "linux-ar71xx_generic/libgpio-2015-01-15" ]
            , [ License("LGPL-2.1", "COPYING") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
    , Package( "linux"
            , "3.14"
            , "http://www.kernel.org"
            , [ "linux-ar71xx_generic/linux-3.14",
                "linux-ar71xx_generic/packages" ]
            , [ License("GPL-2", "COPYING") ]
            , PlainPackageSource("linux-ar71xx_generic")
            , DontIgnoreIfOnTarget )
    , Package( "linux-atm"
            , "2.5.2"
            , "http://linux-atm.sourceforge.net/"
            , [ "linux-ar71xx_generic/linux-atm-2.5.2" ]
            , [ License("specific", "COPYING"),
                License("GPL-2", "COPYING.GPL"),
                License("LGPL-2.1", "COPYING.LGPL") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
    , Package( "mtd"
            , NoVersion
            , "http://wiki.openwrt.org/doc/techref/mtd"
            , [ "linux-ar71xx_generic/mtd" ]
            , [ License("GPL-2", None) ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget )
   , Package( "lua"
            , "5.1.5"
            , "http://www.lua.org/"
            , [ "lua-5.1.5" ]
            , [ License ("MIT", "COPYRIGHT") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "lzo"
            , "2.06"
            , "http://www.oberhumer.com/opensource/lzo/"
            , [ "lzo-2.06" ]
            , [ License ("GPL-2", "COPYING") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "mtd-utils"
            , "1.5.0"
            , "http://www.linux-mtd.infradead.org/"
            , [ "mtd-utils-1.5.0" ]
            , [ License ("GPL-2", "COPYING") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "netifd"
            , "2014-04-07"
            , "http://wiki.openwrt.org/doc/techref/netifd"
            , [ "netifd-2014-04-07" ]
            , [ License ("GPL-2", None) ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "ocf-crypto-headers"
            , NoVersion
            , NoWebsite
            , [ "ocf-crypto-headers" ]
            , []
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "odhcp6c"
            , "2014-03-31"
            , "http://wiki.openwrt.org/doc/techref/odhcp6c"
            , [ "odhcp6c-2014-03-31" ]
            , [ License("GPL-2", "COPYING") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "odhcpd"
            , "2014-04-06"
            , "https://github.com/sbyx/odhcpd"
            , [ "odhcpd-2014-04-06" ]
            , [ License("GPL-2", "COPYING") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "openssl"
            , "1.0.1j"
            , "http://www.openssl.org"
            , [ "openssl-1.0.1j" ]
            , [ License("OpenSSL", "LICENSE") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "opkg-unsigned"
            , "9c97d5ecd795709c8584e972bfdf3aee3a5b846d"
            , "http://code.google.com/p/opkg/"
            , [ "opkg-unsigned/opkg-9c97d5ecd795709c8584e972bfdf3aee3a5b846d" ]
            , [ License("GPL-2.0+", "COPYING") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget )
   , Package( "poly1305-donna"
            , "1.0"
            , "http://cr.yp.to/mac.html"
            , [ "poly1305-donna-1.0" ]
            , [ License("PD", None) ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget )
   , Package( "ppp-default"
            , "2.4.5"
            , NoWebsite
            , [ "ppp-default/ppp-2.4.5" ]
            , [ License("BSD", None),
                License("PD", None),
                License("GPL-2", None),
                License("LGPL-2.1", None) ]
            , PlainPackageSource("ppp-default")
            , DontIgnoreIfOnTarget ) 
   , Package( "procd"
            , "2014-03-18"
            , "http://wiki.openwrt.org/doc/techref/procd"
            , [ "procd-2014-03-18" ]
            , [ License("LGPL-2.1", None) ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "uboot"
            , "1.1.4"
            , "http://www.denx.de/wiki/U-Boot/WebHome"
            , [ "qca-legacy-uboot" ]
            , [ License("GPL-2.0+", "bsb002/COPYING") ]
            , PlainPackageSource("qca-legacy-uboot")
            , DontIgnoreIfOnTarget )
   , Package( "readline"
            , "6.2"
            , "http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html"
            , [ "readline-6.2" ]
            , [ License("GPL-3", "COPYING") ]
            , DownloadedPackageSource(
                "readline-6.2.tar.gz"
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
   , Package( "secure-console"
            , NoVersion
            , NoWebsite
            , [ "secure-console" ]
            , [ License(None, None) ]
            , PackageSource()
            , IgnoreProprietaryPhilipsLicense)
   , Package( "socat"
            , "1.7.2.1"
            , "http://www.dest-unreach.org/socat/"
            , [ "socat-1.7.2.1" ]
            , [ License("GPL-2", None) ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget )
   , Package( "srp"
            , "2.1.2"
            , "http://srp.stanford.edu/"
            , [ "srp-2.1.2" ]
            , [ License("BSD", "docs/LICENSE") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget )
   , Package( "sysfsutils"
            , "2.1.0"
            , "http://linux-diag.sourceforge.net/Sysfsutils.html"
            , [ "sysfsutils-2.1.0" ]
            , [ License("GPL-2.0", "cmd/GPL"),
                License("LGPL-2.1", "lib/LGPL") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "tomcrypt"
            , "1.17"
            , "https://github.com/libtom/libtomcrypt"
            , [ "tomcrypt-1.17" ]
            , [ License("PD", "LICENSE") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget )
   , Package( "tommath"
            , "0.42.0"
            , NoWebsite
            , [ "tommath-0.42.0" ]
            , [ License("PD", "LICENSE") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget )
   , Package( "u-boot"
            , "2013.10"
            , "http://www.denx.de/wiki/U-Boot"
            , [ "u-boot-2013.10" ]
            , [ License("BSD-2", "Licenses/bsd-2-clause.txt"),
                License("BSD-3", "Licenses/bsd-3-clause.txt"),
                License("ECOS-2.0", "Licenses/eCos-2.0.txt"),
                License("IBM-PIBS", "Licenses/ibm-pibs.txt"), 
                License("GPL-2.0", "Licenses/gpl-2.0.txt"), 
                License("LGPL-2.0", "Licenses/lgpl-2.0.txt"), 
                License("LGPL-2.1", "Licenses/lgpl-2.1.txt")]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "ubox"
            , "2014-03-27"
            , "https://openwrt.org/"
            , [ "ubox-2014-03-27" ]
            , [ License("LGPL-2.1", None) 
              , License("GPL-2", None) ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "ubus"
            , "2014-03-18"
            , "https://openwrt.org/"
            , [ "ubus-2014-03-18" ]
            , [ License("LGPL-2.1", None) ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "uci"
            , "2014-02-18.1"
            , "https://openwrt.org/"
            , [ "uci-2014-02-18.1" ]
            , [ License("LGPL-2.1", None) ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "util-linux"
            , "2.24.1"
            , "http://freecode.com/projects/util-linux"
            , [ "util-linux-2.24.1" ]
            , [ License("GPL-2.0", "COPYING"), License("GPL-2.0", "COPYING") ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "zlib"
            , "1.2.8"
            , "http://www.zlib.net"
            , [ "zlib-1.2.8" ]
            , [ License("ZLIB", None) ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "hostapd"
            , "2015-01-20"
            , "http://hostap.epitest.fi/hostapd/"
            , [ "hostapd-full/hostapd-2015-01-20" ]
            , [ License("BSD", None) ]
            , PlainPackageSource("hostapd-full")
            , DontIgnoreIfOnTarget ) 
   , Package( "wpa_supplicant"
            , "2015-01-20"
            , "http://hostap.epitest.fi/wpa_supplicant/"
            , [ "hostapd-supplicant-full/hostapd-2015-01-20"
              , "hostapd-supplicant-p2p/hostapd-2015-01-20" ]
            , [ License("BSD", None) ]
            , PlainPackageSource("hostapd-full")
            , DontIgnoreIfOnTarget )
   , Package( "wireless-tools"
            , "29"
            , "http://www.hpl.hp.com/personal/Jean_Tourrilhes/Linux/Tools.html"
            , [ "wireless_tools.29" ]
            , [ License("GPL-2", None) ]
            , PlainPackageSource()
            , DontIgnoreIfOnTarget )
   , Package( "valgrind"
            , "3.8.1"
            , "http://valgrind.org/"
            , [ "valgrind-3.8.1" ]
            , [ License("GPL", "COPYING") ]
            , PackageSource()
            , DontIgnoreIfOnTarget ) 
    , Package( "libgcc"
            , "0.9.33.2"
            , "https://gcc.gnu.org/onlinedocs/gccint/index.html"
            , [ "toolchain/ipkg-ar71xx/libgcc" ]
            , [ License("LGPL-2.1", None ) ]
            , DownloadedPackageSource(
                "gcc-linaro-4.8-2014.01.tar.xz"
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
    , Package( "uClibc"
            , "0.9.33.2"
            , "http://www.uclibc.org/"
            , [ "toolchain/ipkg-ar71xx/libc" ]
            , [ License("LGPL-2.1", None) ]
            , DownloadedPackageSource(
                "uClibc-0.9.33.2.tar.bz2"
              , "package/libs/uclibc++/patches")
            , DontIgnoreIfOnTarget ) 
    , Package( "libpthread"
            , "0.9.33.2"
            , "http://www.uclibc.org/"
            , [ "toolchain/ipkg-ar71xx/libpthread" ]
            , [ License("LGPL-2.1", None) ]
            , SymlinkedPackageSource(
                "uClibc-0.9.33.2.tar.bz2" )
            , DontIgnoreIfOnTarget ) 
    , Package( "librt"
            , "0.9.33.2"
            , "http://www.uclibc.org/"
            , [ "toolchain/ipkg-ar71xx/librt" ]
            , [ License("LGPL-2.1", None) ]
            , SymlinkedPackageSource(
                "uClibc-0.9.33.2.tar.bz2" )
            , DontIgnoreIfOnTarget ) 
   , Package( "gettext"
            , NoVersion
            , NoWebsite
            , [ "gettext" ]
            , [ License("LGPL-2.1", None) ]
            , SymlinkedPackageSource(
                "uClibc-0.9.33.2.tar.bz2" )
            , DontIgnoreIfOnTarget )
   ]




