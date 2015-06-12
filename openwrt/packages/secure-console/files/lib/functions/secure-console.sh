#!/bin/sh
# Copyright (C) 2015 Philips Lighting

unset UBOOT_SECURITY_STRING
unset SHADOW_SECURITY_STRING

abort() {
	echo -e "$*"
	sleep 1
	exit 1
}

isUBootEnvironmentReady() {
	fw_printenv >/dev/null 2>/dev/null
	return $?
}

updateUBootSecurityString() {
	UBOOT_SECURITY_STRING=`fw_printenv -n security 2>/dev/null`
	return $?
}

updateShadowSecurityString() {
	SHADOW_SECURITY_STRING=`awk -F ':' '/^root:/{print $2}' /etc/shadow`
	return $?
}

escapeStringForSed() {
	echo "$1" | sed -e 's/[\/&]/\\&/g'
}

patchShadowSecurityString() {
	local ESCAPED_SECURITY_STRING=`escapeStringForSed $1`
	sed -i 's/^\(root:\)\([^:]*\)\(.*\)$/\1'${ESCAPED_SECURITY_STRING}'\3/g' /etc/shadow
	return $?
}

syncShadowWithUBootSecurityString() {
	updateUBootSecurityString
	updateShadowSecurityString
	if [ "${SHADOW_SECURITY_STRING}" != "${UBOOT_SECURITY_STRING}" ]; then
		patchShadowSecurityString ${UBOOT_SECURITY_STRING}
	fi
	return $?
}

if ! isUBootEnvironmentReady; then
	abort "Init in progress: Please try again later..."
fi

if ! syncShadowWithUBootSecurityString; then
	unset UBOOT_SECURITY_STRING
fi

