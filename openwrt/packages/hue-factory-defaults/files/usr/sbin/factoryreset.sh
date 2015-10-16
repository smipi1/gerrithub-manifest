#!/bin/sh
SELF=`basename $0`

# Includes
. /lib/functions/mtd.sh

log_tty() {
	log "$*" >/dev/ttyS0
}

log_tty "!!! Executing factoryreset !!!"
OVERLAY_IMG=/lib/images/factory-overlay.ubi

unmountOverlay() {
	mount | if ! grep -q '/overlay'; then
		log_tty "overlay not mounted..."
		return 0
	else
		log_tty "unmounting overlay..."
		umount -r /overlay
		return $?
	fi
}

eraseOverlay() {
	log_tty "erasing overlay..."
	eraseMtd ${OVERLAY_MTD}
}

writeOverlay() {
	log_tty "writing overlay..."
	writeMtd ${OVERLAY_MTD} <${OVERLAY_IMG}
}

flashOverlayAndAbortOnErrors() {
	local OVERLAY_IMAGE=$1
	local OVERLAY_MTD=`nameToMtdDevice overlay`
	if [ "$?" -ne "0" ]; then
		log_tty "error: Cannot determine overlay mtd device"
		return 1
	elif ! unmountOverlay; then
		log_tty "error: Cannot unmount -r ${OVERLAY_MTD}"
		return 1
	elif ! eraseOverlay; then
		log_tty "error: Cannot erase ${OVERLAY_MTD}"
		return 1
	elif ! writeOverlay; then
		log_tty "error: Cannot write ${OVERLAY_MTD}"
		return 1
	else
		return 0
	fi
}

setFactoryResetInProgress() {
	fw_setenv resetting_to_factory 1
}

clearFactoryResetInProgress() {
	fw_setenv resetting_to_factory
}

# Copy resetreason if provided
if [ -f /var/hue-ipbridge/resetreason ]; then
	local resetreason=`cat /var/hue-ipbridge/resetreason`
	fw_setenv resetreason ${resetreason}
fi

setFactoryResetInProgress
if flashOverlayAndAbortOnErrors ${OVERLAY_IMG}; then
	clearFactoryResetInProgress
fi
reboot
