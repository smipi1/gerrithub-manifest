#!/bin/bash

SELF=`basename $0`
QSDK_TOOLS_DIR=`dirname $(readlink -e $0)`
TOOLS_DIR=`readlink -e ${QSDK_TOOLS_DIR}/../..`

unset NEW_REMOTE_NAME
unset NEW_REMOTE_ROOT
unset RENAME_REMOTE_NAME
unset SOURCE
unset DIRECTORY
unset NO_POSITIONALS

C_NONE="\033[0m"
C_YELLOW="\033[1;33m"
C_RED="\033[1;31m"

log() {
	if [ -t 1 ]; then
		echo -e "${C_YELLOW}$*${C_NONE}"
	else
		echo "$*"
	fi
}

error() {
	if [ -t 2 ]; then
		echo -e "${C_RED}$*${C_NONE}"
	else
		echo "$*"
	fi >&2
}

abort() {
	error "$*"
	exit 1
}

showHelp()
{
	echo
	echo "${SELF}: Repo manifest relocater"
	echo
	echo "Copies manifest SOURCE(s) to a destination DIRECTORY. Optionally, the remote in SOURCE(S)"
	echo "can are renamed to NEW_REMOTE_NAME, and the remote root URL changed to NEW_REMOTE_ROOT."
	echo
	echo "Usage: ${SELF} [OPTIONS] SOURCE... DIRECTORY"
	echo
	echo "Options are:"
	echo "	-n NEW_REMOTE_NAME:NEW_REMOTE_ROOT   The new remote name and root URL to use"
	echo "	                                     E.g. github:ssh://git@github.com/PhilipsHueDev/"
	echo "	-e NEW_REMOTE_PREFIX                 The new remote prefix to use for each repository"
	echo "	                                     E.g. bsb002-"
	echo
}

abortShowHelp() {
	error "$*"
	showHelp >&2
	exit 1
}

toDest() {
	local SOURCE=$1;shift
	local DIRECTORY=$1;shift
	local OLD_REMOTE_NAME=$1;shift
	local NEW_REMOTE_NAME=$1;shift
	local DEST_FILENAME=`basename ${SOURCE}`
	if [ -n "${RENAME_REMOTE_NAME}" ]; then
		echo ${DIRECTORY}/${DEST_FILENAME//${OLD_REMOTE_NAME}/${NEW_REMOTE_NAME}}
	else
		echo ${DIRECTORY}/${DEST_FILENAME}
	fi
}

defaultRemote() {
	local SOURCE=$1;shift
	${QSDK_TOOLS_DIR}/manifest.py -f ${SOURCE} -d
	return $?
}

migrateManifest() {
	local SOURCE=$1;shift
	local DEST=$1;shift
${QSDK_TOOLS_DIR}/manifest.py -n ${NEW_REMOTE_NAME} -r ${NEW_REMOTE_ROOT} -e "${NEW_REMOTE_PREFIX}" -f ${SOURCE} -O ${DEST}
	return $?
}

copyManifest() {
	local SOURCE=$1;shift
	local DIRECTORY=$1;shift
	local OLD_REMOTE_NAME=`defaultRemote ${SOURCE}`
	[ "$?" -ne "0" ] && abort "Cannot determine default remote for ${SOURCE}"
	local DEST=`toDest ${SOURCE} ${DIRECTORY} ${OLD_REMOTE_NAME} ${NEW_REMOTE_NAME}`
	if [ -n "${NEW_REMOTE_NAME}" ]; then
		migrateManifest ${SOURCE} ${DEST} || abort "error: Cannot migrate ${SOURCE} to ${DEST}"
	else
		cp ${SOURCE} ${DEST} || abort "error: Cannot copy ${SOURCE} to ${DEST}"
	fi
}

while getopts ":n:e:rh" OPT; do
	case ${OPT} in
		n)
			IFS=":" read -r NEW_REMOTE_NAME NEW_REMOTE_ROOT <<< "${OPTARG}"
			[ -n "${NEW_REMOTE_ROOT}" ] || abortShowHelp "Option missing REMOTE_ROOT specification: -${OPT}"
			;;
		e)
			NEW_REMOTE_PREFIX=${OPTARG}
			;;
		r)
			RENAME_REMOTE_NAME=1
			;;
		h)
			showHelp
			exit 0
			;;
		:)
			abortShowHelp "Option is missing an argument: -${OPTARG}"
			;;
		\?)
			abortShowHelp "Invalid option: -${OPTARG}"
			;;
	esac
done

NO_POSITIONALS=`expr ${#} + 1 - ${OPTIND}`

[ "${NO_POSITIONALS}" -lt "1" ] && abortShowHelp "SOURCE not specified"
[ "${NO_POSITIONALS}" -lt "2" ] && abortShowHelp "DIRECTORY not specified"
[ -n "${RENAME_REMOTE_NAME}" ] && [ -z "${NEW_REMOTE_NAME}" ] && abortShowHelp "Option -r cannot be used without option -n"

SOURCE=${@:${OPTIND}:${NO_POSITIONALS}-1}
DIRECTORY=${@:${OPTIND}+${NO_POSITIONALS}-1:1}

for MANIFEST in ${SOURCE}; do
	copyManifest ${MANIFEST} ${DIRECTORY} || abort "error: Cannot copy ${MANIFEST} to ${DIRECTORY}"
done

