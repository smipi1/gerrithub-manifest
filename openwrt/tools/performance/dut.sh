#!/bin/bash
set -o pipefail

USER=aValidUser
URI=http://${DUT}/api/${USER}
DUT_STDIN="/tmp/`basename $0`-dut.$$"
DUT_STDOUT_STDERR="/tmp/`basename $0`-stdout_stderr.$$"

log() {
	echo "`date +%s.%N` $*"
}

error() {
	echo "error: $*" >&2
}

abort() {
	error "$*"
	exit 1
}

logStdin() {
	local LINE
	local PREFIX=$1
	if [ -n "${PREFIX}" ]; then
		PREFIX="${PREFIX}: "
	fi
	while read LINE; do
		log "${PREFIX}${LINE}"
	done
}

clip() {
	local METHOD=$1;shift
	local RESOURCE=$1;shift
	local DATA=$1;shift
	local URL=${1-${URI}}/${RESOURCE}
	local OPERATION="${METHOD} ${URL}"
	local CURL_ARGS="-X ${OPERATION}${DATA:+ -d '${DATA}'}${CURL_TIMEOUT:+ -m ${CURL_TIMEOUT}}"
	if echo -n "${OPERATION}: " && eval "curl -s ${CURL_ARGS}" && echo; then
		return 0
	else
		return 1
	fi | logStdin clip
}

addValidUser() {
	clip POST "" \
'{
  "devicetype": "CLIP API Debugger",
  "username": "aValidUser"
}' "http://${DUT}/api" || exit 1
}

delete() {
	local RESOURCE=$1
	clip DELETE ${RESOURCE} || exit 1
}

dutConsole() {
	local line
	ssh root@${DUT} -o StrictHostKeyChecking=no
}

logAndDetectPrompt() {
	local FIFO=$1
	local LINE
	while read LINE; do
		local R=${LINE#<|}
		R=${R%|>}
		if [ "${LINE}" = "<|${R}|>" ]; then
			echo "${R}" >> ${FIFO}
		else
			log "dut>: ${LINE}"
		fi
	done
}

waitForPrompt() {
	local FIFO=$1
	local RESULT
	read RESULT <${FIFO}
	return ${RESULT}
}

printResult() {
	echo 'printf "<|%d|>\n" $?' >>${DUT_STDIN}
}

openDutConsole() {
	local line
	rm -f ${DUT_STDOUT_STDERR}
	mkfifo ${DUT_STDOUT_STDERR}
	touch ${DUT_STDIN}
	echo "uname -a" >>${DUT_STDIN}
	printResult
	log "console: ssh root@${DUT}"
	tail -f ${DUT_STDIN} | dutConsole | logAndDetectPrompt ${DUT_STDOUT_STDERR} &
	waitForPrompt ${DUT_STDOUT_STDERR}
}

dutExe() {
	log ">dut: $*"
	echo "$*" >>${DUT_STDIN}
	printResult
	if [ "$*" != "exit" ]; then
		waitForPrompt ${DUT_STDOUT_STDERR}
	fi
}

closeDutConsole() {
	dutExe exit
	rm -f ${DUT_STDIN}
	rm -f ${DUT_STDOUT_STDERR}
}

rebootDut() {
	dutExe "reboot && exit"
while ping -W 1 -c 1 ${DUT} >/dev/null; do
		sleep 1
	done
	echo "${DUT} unreachable"
	rm -f ${DUT_STDIN}
	while ! ping -W 3 -c 1 ${DUT} >/dev/null; do
		sleep 1
	done
	echo "${DUT} reachable"
	openDutConsole
}

pressLink() {
	dutExe "
ACTION=pressed /etc/rc.button/BTN_0
"
	sleep 1
}

releaseLink() {
	dutExe "
ACTION=released /etc/rc.button/BTN_0
"
	sleep 1
}

