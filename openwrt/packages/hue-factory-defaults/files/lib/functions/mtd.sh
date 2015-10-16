#!/bin/sh

if [ -z "${SELF}" ]; then
	echo "error: SELF undefined including mtd.sh" >/dev/ttyS0
	exit 1
fi

log() {
	echo "$*"
	logger -p daemon.notice -t ${SELF} "$*"
}

error() {
	echo "error: $*" >&2
	logger -p daemon.error -t ${SELF} "$*"
}

abort() {
	error "$*"
	exit 1
}

pipeToLog() {
	local LINE
	while read LINE; do
		log "${LINE}"
	done
}

nameToMtdDevice() {
	local PARTITION_NAME=$1
	awk '
		BEGIN {
			FS=":"
		}
		/^mtd[0-9]+:[ \t]+([0-9a-f]{8}[ \t]){2}"'${PARTITION_NAME}'"/ {
			print $1
		}
	' /proc/mtd
}

isNandDevice() {
	local DEV_TYPE=`cat /sys/class/mtd/$1/type`
	if [ "${DEV_TYPE}" != "nor" ]; then
		return 0
	else
		return 1
	fi
}

eraseNand() {
	local DEVICE=$1
	log "Erasing ${DEVICE} (NAND)"
	if ! flash_eraseall -q /dev/${DEVICE} 2>&1; then
		return 1
	else
		return 0
	fi | pipeToLog
}

eraseNor() {
	local DEVICE=$1
	log "Erasing ${DEVICE} (NOR)"
	if ! mtd erase ${DEVICE} 2>&1; then
		return 1
	else
		return 0
	fi | pipeToLog
}

eraseMtd() {
	local DEVICE=$1
	if isNandDevice ${DEVICE}; then
		eraseNand ${DEVICE}
		return $?
	else
		eraseNor ${DEVICE}
		return $?
	fi
}

writeNand() {
	local DEVICE=$1
	log "Writing ${DEVICE} (NAND)"
	if ! nandwrite -p /dev/${DEVICE} - 2>&1; then
		return 1
	else
		return 0
	fi | pipeToLog
}

writeNor() {
	local DEVICE=$1
	log "Writing ${DEVICE} (NOR)"
	if ! mtd write - ${DEVICE} 2>&1; then
		return 1
	else
		return 0
	fi | pipeToLog
}

writeMtd() {
	local DEVICE=$1
	log "Writing unused boot-slot"
	if isNandDevice ${DEVICE}; then
		writeNand ${DEVICE}
		return $?
	else
		writeNor ${DEVICE}
		return $?
	fi
}
