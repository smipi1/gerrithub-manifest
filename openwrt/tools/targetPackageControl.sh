#!/bin/sh
#set -x

SELF=`basename $0`
TOOLS_DIR=`readlink -e $(dirname $0)`
BUILD_DIR=`readlink -e ${TOOLS_DIR}/../qualcomm/qsdk/build_dir/target-*/`
TARGET=ar71xx
IPKG_DIR=ipkg-${TARGET}
IGNORE_TARGET_FINGERPRINT="-o StrictHostKeyChecking=no"

error() {
	echo "error: $*" >&2
}

abort() {
	error "$*"
	exit 1
}

showHelp() {
	echo "${SELF}: BSB002 target control tool"
	echo
	echo "Usage: ${SELF} IPADDR COMMAND PACKAGE"
	echo
	echo "Mandatory arguments:"
	echo "	IPADDR   IP address of the BSB002 target"
	echo "		E.g. 192.168.1.10"
	echo "	COMMAND  Command to perform"
	echo "		Supported commands are:"
	echo "			start          Start the PACKAGE"
	echo "			stop           Stop the PACKAGE"
	echo "			restart        Restart the PACKAGE"
	echo "			reload         Reload configuration files (or restart if that fails)"
	echo "			enable         Enable PACKAGE autostart"
	echo "			disable        Disable PACKAGE autostart"
	echo "			sync           Synchronizes all installable PACKAGE files with the target"
	echo "			               NOTE: May fail if the PACKAGE is not stopped"
	echo "			sync+restart   Stops, synchronizes and starts the PACKAGE"
	echo "	PACKAGE  Package on which the command should be performed"
}

abortShowHelp() {
	error "$*"
	echo >&2
	showHelp >&2
	exit 1
}

parseIpAddr() {
	if [ -z "${1}" ]; then
		abortShowHelp "IPADDR not specified"
	elif ! ping -q -c 3 -i 1 -f ${1} >/dev/null; then
		abort "IPADDR not reachable: ${1}"
	else
		echo ${1}
	fi
}

parseAction() {
	case ${1} in
	start|stop|restart|reload|enable|disable|sync|sync+restart)
		echo ${1}
		;;
	"")
		abortShowHelp "COMMAND not specified"
		;;
	*)
		abortShowHelp "COMMAND not supported: ${1}"
		;;
	esac
}

ipkgInstallDir() {
	local IPKG_DIR=`find ${BUILD_DIR}/${1}*/ -name ''${IPKG_DIR}''`
	if [ "$?" -ne "0" ]; then
		return 1
	fi
	local IPKG_INSTALL_DIR=`readlink -e ${IPKG_DIR}/${1}`
	if [ "$?" -ne "0" ]; then
		return 1
	elif ! [ -d "${IPKG_INSTALL_DIR}" ]; then
		return 1
	else
		echo ${IPKG_INSTALL_DIR}
		return 0
	fi
}

parsePackage() {
	if [ -z "${1}" ]; then
		abortShowHelp "PACKAGE not specified"
	fi
	local IPKG_INSTALL_DIR=`ipkgInstallDir ${1}`
	if [ "$?" -ne "0" ]; then
		abortShowHelp "No ${IPKG_DIR} for PACKAGE in ${BUILD_DIR}: ${1}"
	else
		echo ${IPKG_INSTALL_DIR}
	fi
}

getInitScripts() {
	local IPKG_INSTALL_DIR=${1};shift
	local ACTION=${1};shift
	local INIT_DIR=${IPKG_INSTALL_DIR}/etc/init.d
	local INIT_SCRIPTS=${INIT_DIR}/*
	local INIT_SCRIPT
	if [ -d "${INIT_DIR}" ] &&  [ -n "${INIT_SCRIPTS}" ]; then
		for INIT_SCRIPT in ${INIT_SCRIPTS}; do
			echo ${INIT_SCRIPT##${IPKG_INSTALL_DIR}}
		done
	else
		abort "cannot ${ACTION}: No init scripts found: ${INIT_DIR}"
	fi
}

listAllPackageFiles() {
	local IPKG_INSTALL_DIR=${1}
	local FILES="`find ${IPKG_INSTALL_DIR} -type f`"
	for FILE in ${FILES}; do
		TARGET_PATH=${FILE##${IPKG_INSTALL_DIR}/}
		if [ "${TARGET_PATH}" != "CONTROL/control" ]; then
			echo ${TARGET_PATH}
		fi
	done
}

forAllScripts() {
	local ACTION=$1;shift
	local IPADDR=$1;shift
	local INIT_SCRIPTS=$*
	local TARGET=root@${IPADDR}
	local RESULT=0
	local INIT_SCRIPT
	local COMMAND
	local COMMAND_RESULT
	for INIT_SCRIPT in ${INIT_SCRIPTS}; do
		COMMAND="${INIT_SCRIPT} ${ACTION}"
		echo ${TARGET}: ${COMMAND}
		ssh ${TARGET} -q ${IGNORE_TARGET_FINGERPRINT} ''${COMMAND}''
		COMMAND_RESULT=$?
		if [ "${COMMAND_RESULT}" -ne "0" ]; then
			error "${COMMAND}: exit code ${COMMAND_RESULT}"
			RESULT=${COMMAND_RESULT}
		fi
	done
}

syncAllFilesToTarget() {
	local IPADDR=$1;shift
	local IPKG_INSTALL_DIR=${1};shift
	local TARGET=root@${IPADDR}
	local PACKAGE_FILES="`listAllPackageFiles ${IPKG_INSTALL_DIR}`"
	local FILE
	echo ${TARGET}: tar -xz
	if ! tar -C ${IPKG_INSTALL_DIR} -cz ${PACKAGE_FILES}; then
		error "cannot pack files: ${IPKG_INSTALL_DIR}"
		return 0
	fi | if ! ssh ${TARGET} -q ${IGNORE_TARGET_FINGERPRINT} 'cd / && tar -xvz'; then
		error "cannot unpack files: ${TARGET}"
		return 1
	fi | while read FILE; do
		echo "	/${FILE}"
	done
	return 0
}

IPADDR=`parseIpAddr ${1}`
[ "$?" -eq "0" ] && shift || exit 1
ACTION=`parseAction ${1}`
[ "$?" -eq "0" ] && shift || exit 1
PACKAGE=${1}
IPKG_INSTALL_DIR=`parsePackage ${PACKAGE}`
[ "$?" -eq "0" ] && shift || exit 1
case "${ACTION}" in
start|stop|restart|reload|enable|disable)
	INIT_SCRIPTS=`getInitScripts ${IPKG_INSTALL_DIR} ${ACTION}`
	forAllScripts ${ACTION} ${IPADDR} ${INIT_SCRIPTS}
	;;
sync)
	syncAllFilesToTarget ${IPADDR} ${IPKG_INSTALL_DIR}
	;;
sync+restart)
	INIT_SCRIPTS=`getInitScripts ${IPKG_INSTALL_DIR} ${ACTION}`
	forAllScripts stop ${IPADDR} ${INIT_SCRIPTS}
	syncAllFilesToTarget ${IPADDR} ${IPKG_INSTALL_DIR}
	forAllScripts start ${IPADDR} ${INIT_SCRIPTS}
	;;
esac

