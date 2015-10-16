#!/bin/bash

DUT=${1};shift
INIT_SLEEP_S=${1};shift 2>/dev/null

CURL_TIMEOUT=1
. `dirname $0`/dut.sh
[ -n "${DUT}" ] || abort "Device-under-test IP address not specified"

getConfig() {
	clip GET config
	return $?
}

if [ -n "${INIT_SLEEP_S}" ]; then
	sleep ${INIT_SLEEP_S}
fi

while ! getConfig; do
	echo -n "."
	sleep 0.5
done
echo

exit 0

