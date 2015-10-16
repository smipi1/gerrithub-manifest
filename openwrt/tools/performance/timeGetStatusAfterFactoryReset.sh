#!/bin/bash

PERF_DIR=`dirname $0`
DUT=${1};shift
CURL_TIMEOUT=1
. `dirname $0`/dut.sh
[ -n "${DUT}" ] || abort "Device-under-test IP address not specified"

getConfig() {
	clip GET config >/dev/null
	return $?
}

openDutConsole
dutExe "factoryreset.sh"

time ${PERF_DIR}/waitUntilConfigCanBeRead.sh ${DUT} 5

exit 0

