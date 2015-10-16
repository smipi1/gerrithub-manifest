#!/bin/bash

DUT=${1};shift
. `dirname $0`/dut.sh
[ -n "${DUT}" ] || abort "Device-under-test IP address not specified"

setHostname() {
	local HOSTNAME=$1
	clip PUT config \
'{
  "name": "'${HOSTNAME}'"
}'
	return $?
}

openDutConsole
pressLink
addValidUser
releaseLink

while [ 1 ]; do
	setHostname "Name1" || abort "Device unreachable"
	setHostname "Name2" || abort "Device unreachable"
done

exit 0

