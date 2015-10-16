#!/bin/bash

SELF=`basename $0`
QSDK_TOOLS_DIR=`dirname $(readlink -e $0)`
TOOLS_DIR=`readlink -e ${QSDK_TOOLS_DIR}/../..`
QSDK_ROOT=`pwd`

C_NONE="\033[0m"
C_YELLOW="\033[1;33m"
C_RED="\033[1;31m"

THEIR_MANIFEST_NAME=caf
THEIR_MANIFEST_REPO=git://codeaurora.org/quic/qsdk/releases/manifest/qstak
THEIR_PROJECTS_TO_PRUNE="quic/qsdk/oss/kernel/linux-msm oss/system/feeds/alljoyn quic/qsdk/oss/system/feeds/luci"
OUR_REMOTE_REPO_NAME=github
OUR_REMOTE_REPO_ROOT=ssh://git@github.com/PhilipsHueDev/
OUR_REMOTE_PREFIX=bsb002-
OUR_MANIFEST_REPO=${OUR_REMOTE_REPO_ROOT}${OUR_REMOTE_PREFIX}manifests.git
OUR_MANIFEST_PROJECT=.repo/ourManifests

unset MIRROR_ARGS

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

showHelp() {
	echo "${SELF}: QSDK repository migration tool"
	echo
	echo "Usage: ${SELF} [OPTIONS] -m THEIR_MANIFEST_FILE"
	echo
	echo "Mandatory:"
	echo "	-m THEIR_MANIFEST_FILE   Name of the manifest file in the source manifest repository"
	echo
	echo "Options:"
	echo "	-h                       Show this help"
	echo "	-b                       Push by branch: Use a slower but more robust way to push large repositories"
}

abortShowHelp() {
	error "$*"
	showHelp >&2
	exit 1
}

while getopts ":m:bh" OPT; do
	case ${OPT} in
		m)
			THEIR_MANIFEST_FILE=${OPTARG}
			;;
		b)
			MIRROR_ARGS=-b
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

[ -n "${THEIR_MANIFEST_FILE}" ] || abortShowHelp "manifest file name not specified"

OUR_MANIFEST_FILE=${THEIR_MANIFEST_FILE//${THEIR_MANIFEST_NAME}/${OUR_REMOTE_REPO_NAME}}
OUR_PRUNED_MANIFEST_FILE=${THEIR_MANIFEST_FILE//${THEIR_MANIFEST_NAME}/${OUR_REMOTE_REPO_NAME}_pruned}

log "initializing repo"
repo init -u ${THEIR_MANIFEST_REPO} -b release -m ${THEIR_MANIFEST_FILE} --repo-url=git://codeaurora.org/tools/repo --repo-branch=caf-stable || abort "cannot init repo"

log "syncing repo"
repo sync || abort "cannot sync repo"

log "cloning our manifest project: ${OUR_MANIFEST_REPO} -> ${OUR_MANIFEST_PROJECT}"
rm -rf ${OUR_MANIFEST_PROJECT}
git clone ${OUR_MANIFEST_REPO} ${OUR_MANIFEST_PROJECT} || abort "cannot clone our manifest project: ${OUR_MANIFEST_REPO} -> ${OUR_MANIFEST_PROJECT}"

log "create a manifest for our repos: ${OUR_MANIFEST_PROJECT}/${OUR_MANIFEST_FILE}"
${QSDK_TOOLS_DIR}/manifest.py -n ${OUR_REMOTE_REPO_NAME} -r ${OUR_REMOTE_REPO_ROOT} -e ${OUR_REMOTE_PREFIX} -O ${OUR_MANIFEST_PROJECT}/${OUR_MANIFEST_FILE} || abort "cannot create a manifest for our repos"

log "create a pruned manifest for our repos: ${OUR_MANIFEST_PROJECT}/${OUR_PRUNED_MANIFEST_FILE}"
${QSDK_TOOLS_DIR}/manifest.py -n ${OUR_REMOTE_REPO_NAME} -r ${OUR_REMOTE_REPO_ROOT} -e ${OUR_REMOTE_PREFIX} -O ${OUR_MANIFEST_PROJECT}/${OUR_PRUNED_MANIFEST_FILE} -u "${THEIR_PROJECTS_TO_PRUNE}" || abort "cannot create a pruned manifest for our repos"

log "mirroring all QSDK branches and tags to our repos"
${QSDK_TOOLS_DIR}/mirrorQsdkToOurRepos.sh ${MIRROR_ARGS} -n ${OUR_REMOTE_REPO_NAME} -r ${OUR_REMOTE_REPO_ROOT} -e "${OUR_REMOTE_PREFIX}" || abort "cannot mirror all qsdk repos"

log "commit the manifest for our repos: ${OUR_MANIFEST_PROJECT}/${OUR_MANIFEST_FILE}"
cd ${OUR_MANIFEST_PROJECT} || abort "cannot cd to ${OUR_MANIFEST_PROJECT}"
git add ${OUR_MANIFEST_FILE} || abort "cannot add ${OUR_MANIFEST_FILE}"
git add ${OUR_PRUNED_MANIFEST_FILE} || abort "cannot add ${OUR_PRUNED_MANIFEST_FILE}"
git commit -m "Migration and intake of ${THEIR_MANIFEST_FILE} in ${THEIR_MANIFEST_REPO}" || abort "cannot commit new manifest file"
git push || abort "cannot push new manifest files"

