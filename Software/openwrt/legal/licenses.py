# default license filename is set to "LICENSE". 

from package import Package
from license import License

packages = [
             Package( "argp-standalone"
                    , "1.3"
                    , "https://github.com/jahrome/argp-standalone"
                    , "argp-standalone-1.3"
                    , [License("GPL-2", None)]
                    , False
                    , None )
           , Package( "avahi"
                    , "0.6.31"
                    , "http://avahi.org/"
                    , "avahi/nodbus/avahi-0.6.31"
                    , [License("LGPL-2.1", "LICENSE")]
                    , True
                    , None )
           , Package( "avahi-autoipd-rc"
                    , None
                    , None
                    , "avahi-autoipd-rc"
                    , [License(None, None)]
                    , True
                    , "Philips Code" )
           , Package( "binutils-2.22"
                    , "2.22"
                    , "http://www.gnu.org/software/binutils/"
                    , "binutils-2.22"
                    , [License("<license>", "LICENSE")]
                    , False
                    , None )
           , Package( "busybox"
                    , "1.19.4"
                    , "http://www.busybox.net/"
                    , "busybox-1.19.4"
                    , [License("GPL-2", None)]
                    , True
                    , None ) 
           , Package( "bzip2"
                    , "1.0.6"
                    , "http://www.bzip.org/"
                    , "bzip2-1.0.6"
                    , [License("<license>", "LICENSE")]
                    , False 
                    , None )
           , Package( "chacha20-simple"
                    , "1.0"
                    , "http://chacha20.insanecoding.org/"
                    , "chacha20-simple-1.0"
                    , [License("ISC", None)]
                    , True
                    , None )
           , Package( "curve25519-donna"
                    , "1.0"
                    , "http://code.google.com/p/curve25519-donna/"
                    , "curve25519-donna-1.0"
                    , [License("BSD-3", "LICENSE.md")]
                    , True
                    , None )
           , Package( "dbus"
                    , "1.8.8"
                    , "http://dbus.freedesktop.org"
                    , "dbus-1.8.8"
                    , [License("<license>", "COPYING")]
                    , False 
                    , None ) 
           , Package( "dnsmasq-nodhcpv6"
                    , "2.66"
                    , "http://www.thekelleys.org.uk/dnsmasq/"
                    , "dnsmasq-nodhcpv6"
                    , [License("GPL-2", None)]
                    , True 
                    , None ) 
           , Package( "dropbear"
                    , "2014.63"
                    , "https://matt.ucc.asn.au/dropbear/dropbear.html"
                    , "dropbear-2014.63"
                    , [License("MIT", "LICENSE"), License("BSD-2", "LICENSE")]
                    , True 
                    , None )
           , Package( "ed25519-donna"
                    , "1.0"
                    , "https://github.com/floodyberry/ed25519-donna"
                    , "ed25519-donna-1.0"
                    , [License("PD", None)]
                    , True
                    , None )
           , Package( "elfutils-0.155"
                    , "<version>"
                    , "https://fedorahosted.org/elfutils/"
                    , "elfutils-0.155"
                    , [License("<license>", "LICENSE")]
                    , False 
                    , None ) 
           , Package( "expat"
                    , "2.0.1"
                    , "http://www.libexpat.org/"
                    , "expat-2.0.1"
                    , [License("<license>", "LICENSE")]
                    , False 
                    , None ) 
           , Package( "firewall"
                    , "2014-03-20"
                    , "https://openwrt.org/"
                    , "firewall-2014-03-20"
                    , [License("ISC", None), License("MIT", None)]
                    , True 
                    , None ) 
           , Package( "fstools"
                    , "2014-04-07"
                    , "https://openwrt.org/"
                    , "fstools-2014-04-07"
                    , [License("LGPL-2.1", None)]
                    , True 
                    , None ) 
           , Package( "gdb"
                    , "7.5"
                    , "http://www.gnu.org/software/gdb/"
                    , "gdb-7.5"
                    , [License("<license>", "LICENSE")]
                    , False 
                    , None ) 
           , Package( "gdbm"
                    , "1.10"
                    , "http://www.gnu.org/software/gdbm"
                    , "gdbm-1.10"
                    , [License("<license>", "LICENSE")]
                    , False 
                    , None ) 
           , Package( "gettext"
                    , "<version>"
                    , "<website>"
                    , "gettext"
                    , [License("<license>", "LICENSE")]
                    , False 
                    , None )
           , Package( "hk_aac"
                    , "<version>"
                    , "<website>"
                    , "hk_aac"
                    , [License("<license>", "LICENSE")]
                    , False
                    , "CAE" )
           , Package( "hk_common_osif"
                    , "1.0.0"
                    , None
                    , "hk_common_osif"
                    , [License("commercial", "LICENSE.txt")]
                    , True
                    , "CAE" )
           , Package( "hk_core"
                    , "<version>"
                    , "<website>"
                    , "hk_core"
                    , [License("<license>", "LICENSE")]
                    , False
                    , "CAE" )
           , Package( "hk_hap"
                    , "1.0.0"
                    , None
                    , "hk_hap"
                    , [License("commercial", "LICENSE.txt")]
                    , True
                    , "CAE" )
           , Package( "hk_lib_philips"
                    , "1.0.0"
                    , None
                    , "hk_lib_philips"
                    , [License("commercial", "LICENSE.txt")]
                    , True
                    , "CAE" )
           , Package( "hk_mdns"
                    , "1.0.0"
                    , None
                    , "hk_mdns"
                    , [License("commercial", "LICENSE.txt")]
                    , True
                    , "CAE" )
           , Package( "hk_security"
                    , "<version>"
                    , "<website>"
                    , "hk_security"
                    , [License("<license>", "LICENSE")]
                    , False
                    , "CAE" )
           , Package( "hk_wac"
                    , "<version>"
                    , "<website>"
                    , "hk_wac"
                    , [License("<license>", "LICENSE")]
                    , False
                    , "CAE" )
           , Package( "hostapd-full"
                    , "2015-01-20"
                    , "https://w1.fi/hostapd/"
                    , "hostapd-full/hostapd-2015-01-20"
                    , [License("BSD", "README")]
                    , True 
                    , None ) 
           , Package( "hue-factory-defaults"
                    , "0.0.0"
                    , None
                    , "hue-factory-defaults"
                    , [License(None, None)]
                    , True 
                    , "Philips Code" )
           , Package( "hue-ipbridge"
                    , "6.5.0.14706"
                    , None
                    , "hue-ipbridge"
                    , [License(None, None)]
                    , True 
                    , "Philips Code" )
           , Package( "hue-swupdate"
                    , None
                    , "http://www.meethue.com"
                    , "hue-swupdate"
                    , [License(None, None)]
                    , True 
                    , "Philips Code" ) 
           , Package( "i2c-tools"
                    , "2013-12-15"
                    , "http://www.lm-sensors.org/wiki/I2CTools"
                    , "i2c-tools-2013-12-15"
                    , [License("GPL-2", "COPYING"), License("LGPL-2.1", "COPYING.LGPL")]
                    , True 
                    , None ) 
           , Package( "iw"
                    , "3.17"
                    , "http://git.sipsolutions.net/iw.git/"
                    , "iw-3.17"
                    , [License("ISC", None)]
                    , True 
                    , None )
           , Package( "jsmn"
                    , None
                    , "http://zserge.com/jsmn.html"
                    , "jsmn"
                    , [License("MIT", "LICENSE")]
                    , True
                    , None )
           , Package( "json-c"
                    , "0.11ls "
                    , "https://github.com/json-c/json-c/wiki"
                    , "json-c-0.11"
                    , [License("MIT", "COPYING")]
                    , True 
                    , None ) 
           , Package( "libconfig"
                    , "1.4.9"
                    , "http://www.hyperrealm.com/libconfig/"
                    , "libconfig-1.4.9"
                    , [License("LGPL-2.1", "COPYING.LIB")]
                    , True 
                    , None ) 
           , Package( "libdaemon"
                    , "0.14"
                    , "http://0pointer.de/lennart/projects/libdaemon/"
                    , "libdaemon-0.14"
                    , [License("LGPL-2.1", "LICENSE")]
                    , True 
                    , None ) 
           , Package( "libiconv"
                    , None
                    , "http://www.gnu.org/software/libiconv/"
                    , "libiconv"
                    , [License(None, "LICENSE")]
                    , False 
                    , None ) 
           , Package( "libiwinfo"
                    , None
                    , "http://wiki.openwrt.org/doc/devel/packages/iwinfo"
                    , "libiwinfo"
                    , [License("GPL-2", "COPYING")]
                    , True 
                    , None ) 
           , Package( "libncurses"
                    , "5.9"
                    , "http://www.gnu.org/software/ncurses/"
                    , "libncurses/ncurses-5.9"
                    , []
                    , False 
                    , None ) 
           , Package( "libnl"
                    , "3.2.21"
                    , "http://www.infradead.org/~tgr/libnl/"
                    , "libnl-3.2.21"
                    , [License("LGPL-2.1", "COPYING")]
                    , True 
                    , None ) 
           , Package( "libnl-tiny"
                    , "0.1"
                    , "http://wiki.openwrt.org/doc/devel/packages/libnl-tiny"
                    , "libnl-tiny-0.1"
                    , [License("LGPL-2.1", None)]
                    , True 
                    , None ) 
           , Package( "libpcap"
                    , "1.5.3"
                    , "http://www.tcpdump.org"
                    , "libpcap-1.5.3"
                    , [License("BSD", "LICENSE")]
                    , False 
                    , None ) 
           , Package( "libtool"
                    , "2.4"
                    , "http://www.gnu.org/software/libtool/libtool.html"
                    , "libtool-2.4"
                    , [License(None, None)]
                    , False 
                    , None ) 
           , Package( "libubox"
                    , "2014-03-18"
                    , "http://wiki.openwrt.org/doc/techref/ubox"
                    , "libubox-2014-03-18"
                    , [License("LGPL-2.1", None)]
                    , True 
                    , None ) 
           , Package( "linux-ar71xx_generic"
                    , "<version>"
                    , "<website>"
                    , "linux-ar71xx_generic"
                    , [License("<license>", "LICENSE")]
                    , True 
                    , "TODO: Contains lots of subpackages" ) 
           , Package( "lua"
                    , "5.1.5"
                    , "http://www.lua.org/"
                    , "lua-5.1.5"
                    , [License ("MIT", "COPYRIGHT")]
                    , False 
                    , None ) 
           , Package( "lzo"
                    , "2.06"
                    , "http://www.oberhumer.com/opensource/lzo/"
                    , "lzo-2.06"
                    , [License ("GPL-2", "COPYING")]
                    , False 
                    , None ) 
           , Package( "mtd-utils"
                    , "1.5.0"
                    , "http://www.linux-mtd.infradead.org/"
                    , "mtd-utils-1.5.0"
                    , [License ("GPL-2", "COPYING")]
                    , True 
                    , None ) 
           , Package( "netifd"
                    , "2014-04-07"
                    , "http://wiki.openwrt.org/doc/techref/netifd"
                    , "netifd-2014-04-07"
                    , [License ("GPL-2", None)]
                    , True 
                    , None ) 
           , Package( "ocf-crypto-headers"
                    , None
                    , None
                    , "ocf-crypto-headers"
                    , []
                    , False 
                    , None ) 
           , Package( "odhcp6c"
                    , "2014-03-31"
                    , "http://wiki.openwrt.org/doc/techref/odhcp6c"
                    , "odhcp6c-2014-03-31"
                    , [License("GPL-2", "COPYING")]
                    , True 
                    , None ) 
           , Package( "odhcpd"
                    , "2014-04-06"
                    , "https://github.com/sbyx/odhcpd"
                    , "odhcpd-2014-04-06"
                    , [License("GPL-2", "COPYING")]
                    , True 
                    , None ) 
           , Package( "openssl"
                    , "1.0.1j"
                    , "http://www.openssl.org"
                    , "openssl-1.0.1j"
                    , [License("OpenSSL", "LICENSE")]
                    , True 
                    , None ) 
           , Package( "opkg-unsigned"
                    , "9c97d5ecd795709c8584e972bfdf3aee3a5b846d"
                    , "http://code.google.com/p/opkg/"
                    , "opkg-unsigned/opkg-9c97d5ecd795709c8584e972bfdf3aee3a5b846d"
                    , [License("GPL-2.0+", "COPYING")]
                    , True 
                    , None )
           , Package( "poly1305-donna"
                    , "1.0"
                    , "http://cr.yp.to/mac.html"
                    , "poly1305-donna-1.0"
                    , [License("PD", None)]
                    , True
                    , None )
           , Package( "ppp-default"
                    , "2.4.5"
                    , None
                    , "ppp-default/ppp-2.4.5"
                    , [License("BSD", None), License("PD", None), License("GPL-2", None), License("LGPL-2.1", None)]
                    , True 
                    , None ) 
           , Package( "procd"
                    , "2014-03-18"
                    , "http://wiki.openwrt.org/doc/techref/procd"
                    , "procd-2014-03-18"
		            , [License("LGPL-2.1", None)]
                    , True 
                    , None ) 
           , Package( "qca-legacy-uboot"
                    , None
                    , "http://www.denx.de/wiki/U-Boot/WebHome"
                    , "qca-legacy-uboot"
                    , [License("GPL-2.0+", "/bsb002/COPYING")]
                    , True 
                    , None ) 
           , Package( "readline"
                    , "6.2"
                    , "http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html"
                    , "readline-6.2"
                    , [License("GPL-3", "COPYING")]
                    , False 
                    , None ) 
           , Package( "root-ar71xx"
                    , None
                    , None
                    , "root-ar71xx"
                    , [License(None, None)]
                    , False
                    , "No package: rootfs")
           , Package( "secure-console"
                    , None
                    , None
                    , "secure-console"
                    , [License(None, None)]
                    , True 
                    , "!!!TODO!!!")
           , Package( "srp"
                    , "2.1.1"
                    , "http://srp.stanford.edu/"
                    , "srp-2.1.2"
                    , [License("BSD", "/docs/LICENSE")]
                    , True
                    , None )
           , Package( "sysfsutils"
                    , "2.1.0"
                    , "http://linux-diag.sourceforge.net/Sysfsutils.html"
                    , "sysfsutils-2.1.0"
                    , [License("GPL-2.0", "/cmd/GPL"), License("LGPL-2.1", "/lib/LGPL")]
                    , True 
                    , None ) 
           , Package( "tcpdump-full"
                    , "4.5.1"
                    , "http://www.tcpdump.org"
                    , "tcpdump-full/tcpdump-4.5.1"
                    , [License("BSD", "LICENSE")]
                    , False 
                    , None )
           , Package( "tomcrypt-1.17"
                    , "1.17"
                    , "https://github.com/libtom/libtomcrypt"
                    , "tomcrypt-1.17"
                    , [License("PD", "LICENSE")]
                    , True
                    , None )
           , Package( "tommath"
                    , "0.42.0"
                    , None
                    , "tommath-0.42.0"
                    , [License("PD", "LICENSE")]
                    , True
                    , None )
           , Package( "toolchain"
                    , "<version>"
                    , "<website>"
                    , "toolchain"
                    , [License("<license>", "LICENSE")]
                    , True 
                    , "TODO" ) 
           , Package( "u-boot"
                    , "2013.10"
                    , "http://www.denx.de/wiki/U-Boot"
                    , "u-boot-2013.10/Licenses"
                    , [ License("BSD-2", "bsd-2-clause.txt"),
                        License("BSD-3", "bsd-3-clause.txt"),
                        License("ECOS-2.0", "eCos-2.0.txt"),
                        License("IBM-PIBS", "ibm-pibs.txt"), 
                        License("GPL-2.0", "gpl-2.0.txt"), 
                        License("LGPL-2.0", "lgpl-2.0.txt"), 
                        License("LGPL-2.1", "lgpl-2.1.txt")]
                    , True 
                    , None ) 
           , Package( "ubox"
                    , "2014-03-27"
                    , "https://openwrt.org/"
                    , "ubox-2014-03-27"
                    , [License("LGPL-2.1", None)]
                    , True 
                    , None ) 
           , Package( "ubus"
                    , "2014-03-18"
                    , "https://openwrt.org/"
                    , "ubus-2014-03-18"
                    , [License("LGPL-2.1", None)]
                    , True 
                    , None ) 
           , Package( "uci"
                    , "2014-02-18.1"
                    , "https://openwrt.org/"
                    , "uci-2014-02-18.1"
                    , [License("LGPL-2.1", None)]
                    , True 
                    , None ) 
           , Package( "util-linux"
                    , "2.24.1"
                    , "http://freecode.com/projects/util-linux"
                    , "util-linux-2.24.1"
                    , [License("GPL-2.0", "COPYING"), License("GPL-2.0", "COPYING")]
                    , True 
                    , None ) 
           , Package( "zlib"
                    , "1.2.8"
                    , "http://www.zlib.net"
                    , "zlib-1.2.8"
                    , [License("ZLIB", None)]
                    , True 
                    , None ) 
           ]

