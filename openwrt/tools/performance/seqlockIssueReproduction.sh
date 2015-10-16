#!/bin/bash

DUT=${1};shift
. `dirname $0`/dut.sh
[ -n "${DUT}" ] || abort "Device-under-test IP address not specified"

getConfig() {
	clip GET config
	return $?
}

setDhcp() {
	local HOSTNAME=$1
	clip PUT config \
'{
  "dhcp": true
}'
	return $?
}

setStaticIp() {
	local IPADDR=$1
	clip PUT config \
'{
  "dhcp": false,
  "ipaddress": "130.145.210.171",
  "netmask": "255.255.255.0",
  "gateway": "130.145.210.254"
}'
	return $?
}
	
openDutConsole
pressLink
addValidUser
releaseLink

while [ 1 ]; do
	setStaticIp ${DUT} || abort "cannot set static ip"
	rebootDut || abort "cannot reboot dut"
	setDhcp || abort "cannot set dhcp"
	getConfig || abort "cannot get config"
done

exit 0

