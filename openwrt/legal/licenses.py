# default license filename is set to "LICENSE". 

from package import Package
from license import License
from GitPackageSource import GitPackageSource
from PackageSource import PackageSource
from DownloadedPackageSource import DownloadedPackageSource

NoVersion = None
NoWebsite = None
DontIgnoreIfOnTarget = None
IgnoreProprietaryCaeLicense = "proprietary CAE license"
IgnoreProprietaryPhilipsLicense = "proprietary Philips license"
OpenWrtRuntime = None
NoPatches = None

packages = [
     Package( "argp-standalone"
            , "1.3"
            , "https://github.com/jahrome/argp-standalone"
            , [ "argp-standalone-1.3" ]
            , [ License("GPL-2", None) ]
            , DownloadedPackageSource(
                "argp-standalone-1.3.tar.gz"
              , "qca/feeds/oldpackages/libs/argp-standalone/patches")
            , DontIgnoreIfOnTarget )
   , Package( "avahi"
            , "0.6.31"
            , "http://avahi.org/"
            , [ "avahi/nodbus/avahi-0.6.31" ]
            , [ License("LGPL-2.1", "LICENSE") ]
            , DownloadedPackageSource(
                "avahi-0.6.31.tar.gz"
              , "qca/feeds/oldpackages/libs/avahi/patches")
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
              , "../../qualcomm/qsdk/toolchain/binutils/patches")
            , DontIgnoreIfOnTarget )
   , Package( "busybox"
            , "1.19.4"
            , "http://www.busybox.net/"
            , [ "busybox-1.19.4" ]
            , [ License("GPL-2", None) ]
            , DownloadedPackageSource(
                OpenWrtRuntime
              , "package/utils/busybox/patches")
            , DontIgnoreIfOnTarget ) 
   , Package( "bzip2"
            , "1.0.6"
            , "http://www.bzip.org/"
            , [ "bzip2-1.0.6" ]
            , [ License("<license>", "LICENSE") ]
            , DownloadedPackageSource(
                "bzip2-1.0.6.tar.gz"
              , NoPatches)
            , DontIgnoreIfOnTarget )
   , Package( "chacha20-simple"
            , "1.0"
            , "http://chacha20.insanecoding.org/"
            , [ "chacha20-simple-1.0" ]
            , [ License("ISC", None) ]
            , DownloadedPackageSource(
                "chacha20-simple-1.0.tar.bz2"
              , "../../cae/homekit/package/chacha20-simple/patches")
            , DontIgnoreIfOnTarget )
   , Package( "curve25519-donna"
            , "1.0"
            , "http://code.google.com/p/curve25519-donna/"
            , [ "curve25519-donna-1.0" ]
            , [ License("BSD-3", "LICENSE.md") ]
            , DownloadedPackageSource(
                "curve25519-donna-28772f37a4b8a57ab9439b9e79b19f9abee686da.tar.gz"
              , "../../cae/homekit/package/curve25519-donna/patches")
            , DontIgnoreIfOnTarget )
   , Package( "dbus"
            , "1.8.8"
            , "http://dbus.freedesktop.org"
            , [ "dbus-1.8.8" ]
            , [ License("<license>", "COPYING") ]
            , DownloadedPackageSource(
                "dbus-1.8.8.tar.gz"
              , "qca/feeds/oldpackages/libs/dbus-glib/patches")
            , DontIgnoreIfOnTarget ) 
   , Package( "dnsmasq-nodhcpv6"
            , "2.66"
            , "http://www.thekelleys.org.uk/dnsmasq/"
            , [ "dnsmasq-nodhcpv6/dnsmasq-2.66" ]
            , [ License("GPL-2", None) ]
            , DownloadedPackageSource(
                "dnsmasq-2.66.tar.gz"
              , "package/network/services/dnsmasq/patches")
            , DontIgnoreIfOnTarget ) 
   , Package( "dropbear"
            , "2014.63"
            , "https://matt.ucc.asn.au/dropbear/dropbear.html"
            , [ "dropbear-2014.63" ]
            , [ License("MIT", "LICENSE"),
                License("BSD-2", "LICENSE") ]
            , DownloadedPackageSource(
                "dropbear-2014.63.tar.bz2"
              , "package/network/services/dropbear/patches")
            , DontIgnoreIfOnTarget )
   , Package( "ed25519-donna"
            , "1.0"
            , "https://github.com/floodyberry/ed25519-donna"
            , [ "ed25519-donna-1.0" ]
            , [ License("PD", None) ]
            , DownloadedPackageSource(
                "ed25519-donna-8757bd4cd209cb032853ece0ce413f122eef212c.tar.gz"
              , "../../cae/homekit/package/ed25519-donna/patches")
            , DontIgnoreIfOnTarget )
   , Package( "elfutils-0.155"
            , NoVersion
            , "https://fedorahosted.org/elfutils/"
            , [ "elfutils-0.155" ]
            , [ License("<license>", "LICENSE") ]
            , DownloadedPackageSource(
                "elfutils-0.155.tar.bz2"
              , "qca/feeds/oldpackages/libs/elfutils/patches")
            , DontIgnoreIfOnTarget ) 
   , Package( "expat"
            , "2.0.1"
            , "http://www.libexpat.org/"
            , [ "expat-2.0.1" ]
            , [ License("<license>", "LICENSE") ]
            , DownloadedPackageSource(
                "expat-2.0.1.tar.gz"
              , "qca/feeds/oldpackages/lang/luaexpat/patches")
            , DontIgnoreIfOnTarget ) 
   , Package( "firewall"
            , "2014-03-20"
            , "https://openwrt.org/"
            , [ "firewall-2014-03-20" ]
            , [ License("ISC", None),
                License("MIT", None) ]
            , DownloadedPackageSource(
                "firewall-2014-03-20-93aea77092b0c178fefe3ab95fc040534eda90a3.tar.gz"
              , "package/network/config/firewall/patches")
            , DontIgnoreIfOnTarget ) 
   , Package( "fstools"
            , "2014-04-07"
            , "https://openwrt.org/"
            , [ "fstools-2014-04-07" ]
            , [ License("LGPL-2.1", None) ]
            , DownloadedPackageSource(
                "fstools-2014-04-07-a1f48fc0444f5c3c44ee6ef1005cd8da65decefd.tar.gz"
              , "qca/feeds/oldpackages/utils/dosfstools/patches")
            , DontIgnoreIfOnTarget ) 
   , Package( "gdb"
            , "7.5"
            , "http://www.gnu.org/software/gdb/"
            , [ "gdb-7.5" ]
            , [ License("<license>", "COPYING") ]
            , DownloadedPackageSource(
                "gdb-7.5.tar.bz2"
              , "toolchain/gdb/patches") ###TODO: add toolchain/gdb/patches
            , DontIgnoreIfOnTarget ) 
   , Package( "tcpdump"
            , "4.5.1"
            , "http://www.tcpdump.org/"
            , [ "tcpdump-full/tcpdump-4.5.1" ]
            , [ License("<license>", "LICENSE") ]
            , DownloadedPackageSource(
                "tcpdump-4.5.1.tar.gz"
              , "package/network/utils/tcpdump/patches")
            , DontIgnoreIfOnTarget ) 
   , Package( "gdbm"
            , "1.10"
            , "http://www.gnu.org/software/gdbm"
            , [ "gdbm-1.10" ]
            , [ License("<license>", "LICENSE") ]
            , DownloadedPackageSource(
                "gdbm-1.10.tar.gz"
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
   , Package( "gettext"
            , NoVersion
            , NoWebsite
            , [ "gettext" ]
            , [ License("<license>", "LICENSE") ]
            , DownloadedPackageSource(
                OpenWrtRuntime
              , NoPatches)
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
            , DownloadedPackageSource(
                "hostapd-2015-01-20.tar.bz2"
              , "package/network/services/hostapd/patches") ### TODO: more patches??
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
            , DownloadedPackageSource(
                "i2c-tools-2013-12-15-r6204.tar.gz"
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
   , Package( "iw"
            , "3.17"
            , "http://git.sipsolutions.net/iw.git/"
            , [ "iw-3.17" ]
            , [ License("ISC", None) ]
            , DownloadedPackageSource(
                "iw-3.17.tar.xz"
              , "package/network/utils/iw/patches")
            , DontIgnoreIfOnTarget )
   , Package( "jsmn"
            , NoVersion
            , "http://zserge.com/jsmn.html"
            , [ "jsmn" ]
            , [ License("MIT", "LICENSE") ]
            , DownloadedPackageSource(
                OpenWrtRuntime
              , "../../cae/homekit/package/jsmn/patches")
            , DontIgnoreIfOnTarget )
   , Package( "json-c"
            , "0.11"
            , "https://github.com/json-c/json-c/wiki"
            , [ "json-c-0.11" ]
            , [ License("MIT", "COPYING") ]
            , DownloadedPackageSource(
                "json-c-0.11.tar.gz"
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
   , Package( "libconfig"
            , "1.4.9"
            , "http://www.hyperrealm.com/libconfig/"
            , [ "libconfig-1.4.9" ]
            , [ License("LGPL-2.1", "COPYING.LIB") ]
            , DownloadedPackageSource(
                "libconfig-1.4.9.tar.gz"
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
   , Package( "libdaemon"
            , "0.14"
            , "http://0pointer.de/lennart/projects/libdaemon/"
            , [ "libdaemon-0.14" ]
            , [ License("LGPL-2.1", "LICENSE") ]
            , DownloadedPackageSource(
                "libdaemon-0.14.tar.gz"
              , "qca/feeds/oldpackages/libs/libdaemon/patches")
            , DontIgnoreIfOnTarget ) 
   , Package( "libiconv"
            , NoVersion
            , "http://www.gnu.org/software/libiconv/"
            , [ "libiconv" ]
            , [ License(None, "LICENSE") ]
            , DownloadedPackageSource(
                OpenWrtRuntime
              , "package/libs/libiconv-full/patches")
            , DontIgnoreIfOnTarget ) 
   , Package( "libiwinfo"
            , NoVersion
            , "http://wiki.openwrt.org/doc/devel/packages/iwinfo"
            , [ "libiwinfo" ]
            , [ License("GPL-2", "COPYING") ]
            , DownloadedPackageSource(
                OpenWrtRuntime
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
   , Package( "libncurses"
            , "5.9"
            , "http://www.gnu.org/software/ncurses/"
            , [ "libncurses/ncurses-5.9" ]
            , []
            , DownloadedPackageSource(
                OpenWrtRuntime
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
   , Package( "libnl"
            , "3.2.21"
            , "http://www.infradead.org/~tgr/libnl/"
            , [ "libnl-3.2.21" ]
            , [ License("LGPL-2.1", "COPYING") ]
            , DownloadedPackageSource(
                "libnl-3.2.21.tar.gz"
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
   , Package( "libnl-tiny"
            , "0.1"
            , "http://wiki.openwrt.org/doc/devel/packages/libnl-tiny"
            , [ "libnl-tiny-0.1" ]
            , [ License("LGPL-2.1", None) ]
            , DownloadedPackageSource(
                OpenWrtRuntime
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
   , Package( "libpcap"
            , "1.5.3"
            , "http://www.tcpdump.org"
            , [ "libpcap-1.5.3" ]
            , [ License("BSD", "LICENSE") ]
            , DownloadedPackageSource(
                OpenWrtRuntime
              , "package/libs/libpcap/patches")
            , DontIgnoreIfOnTarget ) 
   , Package( "libtool"
            , "2.4"
            , "http://www.gnu.org/software/libtool/libtool.html"
            , [ "libtool-2.4" ]
            , [ License(None, None) ]
            , DownloadedPackageSource(
                "libtool-2.4.tar.gz"
              , "tools/libtool/patches")
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
            , DownloadedPackageSource(
                "libubox-2014-03-18-4f44401ae8d23465261cef80b87630ffccd5a864.tar.gz"
              , NoPatches)
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
            , DownloadedPackageSource(
                "iptables-1.4.21.tar.bz2"
              , "package/network/utils/iptables/patches")
            , DontIgnoreIfOnTarget ) 
    , Package( "libgpio"
            , "2015-01-15"
            , "https://github.com/Linutronix/libgpio"
            , [ "linux-ar71xx_generic/libgpio-2015-01-15" ]
            , [ License("LGPL-2.1", "COPYING") ]
            , DownloadedPackageSource(
                "libgpio-2015-01-15-0356a62b38919401f189df7a60b7dae5d4f1e32e.tar.gz"
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
    , Package( "linux"
            , "3.14"
            , "http://www.kernel.org"
            , [ "linux-ar71xx_generic/linux-3.14",
                "linux-ar71xx_generic/packages" ]
            , [ License("GPL-2", "COPYING") ]
            , DownloadedPackageSource(
                "linux-3.14.tar.xz"
              , "") ### TODO: multiple patch dirs
            , DontIgnoreIfOnTarget )
    , Package( "linux-atm"
            , "2.5.2"
            , "http://linux-atm.sourceforge.net/"
            , [ "linux-ar71xx_generic/linux-atm-2.5.2" ]
            , [ License("specific", "COPYING"),
                License("GPL-2", "COPYING.GPL"),
                License("LGPL-2.1", "COPYING.LGPL") ]
            , DownloadedPackageSource(
                "linux-atm-2.5.2.tar.gz"
              , "package/network/utils/linux-atm/patches")
            , DontIgnoreIfOnTarget ) 
    , Package( "mtd"
            , NoVersion
            , "http://wiki.openwrt.org/doc/techref/mtd"
            , [ "linux-ar71xx_generic/mtd" ]
            , [ License("GPL-2", None) ]
            , DownloadedPackageSource(
                OpenWrtRuntime
              , "tools/mtd-utils/patches")
            , DontIgnoreIfOnTarget )
   , Package( "lua"
            , "5.1.5"
            , "http://www.lua.org/"
            , [ "lua-5.1.5" ]
            , [ License ("MIT", "COPYRIGHT") ]
            , DownloadedPackageSource(
                OpenWrtRuntime
              , "package/utils/lua/patches")
            , DontIgnoreIfOnTarget ) 
   , Package( "lzo"
            , "2.06"
            , "http://www.oberhumer.com/opensource/lzo/"
            , [ "lzo-2.06" ]
            , [ License ("GPL-2", "COPYING") ]
            , DownloadedPackageSource(
                "lzo-2.06.tar.gz"
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
   , Package( "mtd-utils"
            , "1.5.0"
            , "http://www.linux-mtd.infradead.org/"
            , [ "mtd-utils-1.5.0" ]
            , [ License ("GPL-2", "COPYING") ]
            , DownloadedPackageSource(
                "mtd-utils-1.5.0.tar.gz"
              , "tools/mtd-utils/patches")
            , DontIgnoreIfOnTarget ) 
   , Package( "netifd"
            , "2014-04-07"
            , "http://wiki.openwrt.org/doc/techref/netifd"
            , [ "netifd-2014-04-07" ]
            , [ License ("GPL-2", None) ]
            , DownloadedPackageSource(
                "netifd-2014-04-07-5df59a6cf9fd307378bd5cbea809a22f6de9f33d.tar.gz"
              , "package/network/config/netifd/patches")
            , DontIgnoreIfOnTarget ) 
   , Package( "ocf-crypto-headers"
            , NoVersion
            , NoWebsite
            , [ "ocf-crypto-headers" ]
            , []
            , DownloadedPackageSource(
                OpenWrtRuntime
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
   , Package( "odhcp6c"
            , "2014-03-31"
            , "http://wiki.openwrt.org/doc/techref/odhcp6c"
            , [ "odhcp6c-2014-03-31" ]
            , [ License("GPL-2", "COPYING") ]
            , DownloadedPackageSource(
                "odhcp6c-2014-03-31.tar.bz2"
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
   , Package( "odhcpd"
            , "2014-04-06"
            , "https://github.com/sbyx/odhcpd"
            , [ "odhcpd-2014-04-06" ]
            , [ License("GPL-2", "COPYING") ]
            , DownloadedPackageSource(
                "odhcpd-2014-04-06.tar.bz2"
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
   , Package( "openssl"
            , "1.0.1j"
            , "http://www.openssl.org"
            , [ "openssl-1.0.1j" ]
            , [ License("OpenSSL", "LICENSE") ]
            , DownloadedPackageSource(
                "openssl-1.0.1j.tar.gz"
              , "package/libs/openssl/patches")
            , DontIgnoreIfOnTarget ) 
   , Package( "opkg-unsigned"
            , "9c97d5ecd795709c8584e972bfdf3aee3a5b846d"
            , "http://code.google.com/p/opkg/"
            , [ "opkg-unsigned/opkg-9c97d5ecd795709c8584e972bfdf3aee3a5b846d" ]
            , [ License("GPL-2.0+", "COPYING") ]
            , DownloadedPackageSource(
                "opkg-9c97d5ecd795709c8584e972bfdf3aee3a5b846d.tar.gz"
              , "package/system/opkg/patches")
            , DontIgnoreIfOnTarget )
   , Package( "poly1305-donna"
            , "1.0"
            , "http://cr.yp.to/mac.html"
            , [ "poly1305-donna-1.0" ]
            , [ License("PD", None) ]
            , DownloadedPackageSource(
                "../../../cae/homekit/security/external/origins/poly1305-donna.tar.gz"
              , "../../cae/homekit/package/poly1305-donna/patches")
            , DontIgnoreIfOnTarget )
   , Package( "ppp-default"
            , "2.4.5"
            , NoWebsite
            , [ "ppp-default/ppp-2.4.5" ]
            , [ License("BSD", None),
                License("PD", None),
                License("GPL-2", None),
                License("LGPL-2.1", None) ]
            , DownloadedPackageSource(
                "ppp-2.4.5.tar.gz"
              , "package/network/services/ppp/patches")
            , DontIgnoreIfOnTarget ) 
   , Package( "procd"
            , "2014-03-18"
            , "http://wiki.openwrt.org/doc/techref/procd"
            , [ "procd-2014-03-18" ]
            , [ License("LGPL-2.1", None) ]
            , DownloadedPackageSource(
                "procd-2014-03-18-7a9cbcd88b6cf3c0cbee6d4f76c2adaedc54058d.tar.gz"
              , "package/system/procd/patches")
            , DontIgnoreIfOnTarget ) 
   , Package( "uboot"
            , "1.1.4"
            , "http://www.denx.de/wiki/U-Boot/WebHome"
            , [ "qca-legacy-uboot" ]
            , [ License("GPL-2.0+", "bsb002/COPYING") ]
            , GitPackageSource("qca/src/qca-legacy-uboot")
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
            , DownloadedPackageSource(
                "socat-1.7.2.1.tar.bz2"
              , "qca/feeds/oldpackages/net/socat/patches")
            , DontIgnoreIfOnTarget )
   , Package( "srp"
            , "2.1.1"
            , "http://srp.stanford.edu/"
            , [ "srp-2.1.2" ]
            , [ License("BSD", "docs/LICENSE") ]
            , DownloadedPackageSource(
                "srp-2.1.2.tar.gz"
              , "../.././cae/homekit/package/srp/patches")
            , DontIgnoreIfOnTarget )
   , Package( "sysfsutils"
            , "2.1.0"
            , "http://linux-diag.sourceforge.net/Sysfsutils.html"
            , [ "sysfsutils-2.1.0" ]
            , [ License("GPL-2.0", "cmd/GPL"),
                License("LGPL-2.1", "lib/LGPL") ]
            , DownloadedPackageSource(
                "sysfsutils-2.1.0.tar.gz"
              , "package/libs/sysfsutils/patches")
            , DontIgnoreIfOnTarget ) 
   , Package( "tomcrypt"
            , "1.17"
            , "https://github.com/libtom/libtomcrypt"
            , [ "tomcrypt-1.17" ]
            , [ License("PD", "LICENSE") ]
            , DownloadedPackageSource(
                "tomcrypt-bbc52b9e1bf4b22ac4616e667b06d217c6ab004e.tar.gz"
              , "../../cae/homekit/package/tomcrypt/patches")
            , DontIgnoreIfOnTarget )
   , Package( "tommath"
            , "0.42.0"
            , NoWebsite
            , [ "tommath-0.42.0" ]
            , [ License("PD", "LICENSE") ]
            , DownloadedPackageSource(
                "tommath-6f5bf561220a04962fbcd56db940085de4b53327.tar.gz"
              , "../../cae/homekit/package/tommath/patches")
            , DontIgnoreIfOnTarget )
    , Package( "libpthread"
            , "0.9.33.2"
            , "http://www.uclibc.org/"
            , [ "toolchain/ipkg-ar71xx/libpthread" ]
            , [ License("LGPL-2.1", None) ]
            , DownloadedPackageSource(
                OpenWrtRuntime
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
    , Package( "librt"
            , "0.9.33.2"
            , "http://www.uclibc.org/"
            , [ "toolchain/ipkg-ar71xx/librt" ]
            , [ License("LGPL-2.1", None) ]
            , DownloadedPackageSource(
                OpenWrtRuntime
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
    , Package( "libgcc"
            , "0.9.33.2"
            , "https://gcc.gnu.org/onlinedocs/gccint/index.html"
            , [ "toolchain/ipkg-ar71xx/libgcc" ]
            , [ License("LGPL-2.1", None ) ]
            , DownloadedPackageSource(
                OpenWrtRuntime
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
    , Package( "uClibc"
            , "0.9.33.2"
            , "http://www.uclibc.org/"
            , [ "toolchain/ipkg-ar71xx/libc" ]
            , [ License("LGPL-2.1", None) ]
            , DownloadedPackageSource(
                OpenWrtRuntime
              , "package/libs/uclibc++/patches")
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
            , DownloadedPackageSource(
                "u-boot-2013.10.tar.bz2"
              , "target/linux/at91/image/u-boot/patches") ### TODO: multiple patches
            , DontIgnoreIfOnTarget ) 
   , Package( "ubox"
            , "2014-03-27"
            , "https://openwrt.org/"
            , [ "ubox-2014-03-27" ]
            , [ License("LGPL-2.1", None) 
              , License("GPL-2", None) ]
            , DownloadedPackageSource(
                "ubox-2014-03-27-1d9d2e6ae99c9ba72d1bc40e554d5f422c9b9196.tar.gz"
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
   , Package( "ubus"
            , "2014-03-18"
            , "https://openwrt.org/"
            , [ "ubus-2014-03-18" ]
            , [ License("LGPL-2.1", None) ]
            , DownloadedPackageSource(
                "ubus-2014-03-18-1d5ac421a5b3dca60562e876ba70d0c2fe46b3d2.tar.gz"
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
   , Package( "uci"
            , "2014-02-18.1"
            , "https://openwrt.org/"
            , [ "uci-2014-02-18.1" ]
            , [ License("LGPL-2.1", None) ]
            , DownloadedPackageSource(
                "uci-2014-02-18.1.tar.gz"
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
   , Package( "util-linux"
            , "2.24.1"
            , "http://freecode.com/projects/util-linux"
            , [ "util-linux-2.24.1" ]
            , [ License("GPL-2.0", "COPYING"), License("GPL-2.0", "COPYING") ]
            , DownloadedPackageSource(
                "util-linux-2.24.1.tar.xz"
              , "package/utils/util-linux/patches")
            , DontIgnoreIfOnTarget ) 
   , Package( "zlib"
            , "1.2.8"
            , "http://www.zlib.net"
            , [ "zlib-1.2.8" ]
            , [ License("ZLIB", None) ]
            , DownloadedPackageSource(
                "zlib-1.2.8.tar.gz"
              , NoPatches)
            , DontIgnoreIfOnTarget ) 
   , Package( "hostapd"
            , "2015-01-20"
            , "http://hostap.epitest.fi/hostapd/"
            , [ "hostapd-full/hostapd-2015-01-20" ]
            , [ License("BSD", None) ]
            , DownloadedPackageSource(
                "hostapd-2015-01-20.tar.bz2"
              , "package/network/services/hostapd/patches")
            , DontIgnoreIfOnTarget ) 
   , Package( "wpa_supplicant"
            , "2015-01-20"
            , "http://hostap.epitest.fi/wpa_supplicant/"
            , [ "hostapd-supplicant-full/hostapd-2015-01-20"
              , "hostapd-supplicant-p2p/hostapd-2015-01-20" ]
            , [ License("BSD", None) ]
            , DownloadedPackageSource(
                OpenWrtRuntime
              , NoPatches)
            , DontIgnoreIfOnTarget )
   , Package( "wireless-tools"
            , "29"
            , "http://www.hpl.hp.com/personal/Jean_Tourrilhes/Linux/Tools.html"
            , [ "wireless_tools.29" ]
            , [ License("GPL-2", None) ]
            , DownloadedPackageSource(
                "wireless_tools.29.tar.gz"
              , "package/network/utils/wireless-tools/patches")
            , DontIgnoreIfOnTarget )            
   , Package( "libncurses"
            , "5.9"
            , "http://www.gnu.org/software/ncurses/"
            , [ "libncurses/ncurses-5.9" ]
            , [ License("BSD", "README") ]
            , PackageSource()
            , DontIgnoreIfOnTarget ) 
   , Package( "valgrind"
            , "3.8.1"
            , "http://valgrind.org/"
            , [ "valgrind-3.8.1" ]
            , [ License("GPL", "COPYING") ]
            , PackageSource()
            , DontIgnoreIfOnTarget ) 
   ]




