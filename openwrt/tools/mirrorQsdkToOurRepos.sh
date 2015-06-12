#!/bin/bash

SELF=`basename $0`
QSDK_TOOLS_DIR=`dirname $0`
QSDK_ROOT=`pwd`

C_NONE="\033[0m"
C_YELLOW="\033[1;33m"
C_RED="\033[1;31m"

unset OUR_REMOTE_ROOT
unset OUR_REMOTE_NAME
unset PUSH_BY_BRANCH

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

isValidGitProject() {
	if git remote 1>/dev/null 2>/dev/null; then
		return 0
	else
		return 1
	fi
}

deleteAllBranches() {
	log "deleting all branches"
	for branch in `git branch | grep -v '(no branch)' | grep -v '(detached from'`; do
		git branch -D ${branch} || abort "cannot delete branch (${branch}) in `pwd`"
	done
}

removeAllOtherRemotes() {
	local REMOTE_TO_KEEP=$1
	log "remove all remotes other than ${REMOTE_TO_KEEP}"
	for remote in `git remote | grep -v ${REMOTE_TO_KEEP}`; do
		git remote remove ${remote} || abort "cannot remove remote: ${remote}"
	done
}

fetchFromAllRemotes() {
	local REMOTE_NAME=$1
	log "fetching latest from ${REMOTE_NAME}"
	git fetch -f ${REMOTE_NAME} '*:*' || abort "cannot pull from ${REMOTE_NAME}"
}

trackAllBranchesOnRemote() {
	local REMOTE_NAME=$1
	local LOCAL_BRANCH
	log "track all branches on ${REMOTE_NAME}"
	for branch in `git branch -r | grep ${REMOTE_NAME} | sed 's/^ \+'${REMOTE_NAME}'\///'`; do
		git branch ${branch} --track refs/remotes/${REMOTE_NAME}/${branch} || abort "cannot add tracking branch: ${branch} -> ${REMOTE_NAME}/${branch}"
	done
}

addRemote() {
	local REMOTE_NAME=$1;shift
	local REMOTE_REPO=$1;shift
	log "add remote: ${REMOTE_NAME} -> ${REMOTE_REPO}"
	git remote add ${REMOTE_NAME} ${REMOTE_REPO} || abort "cannot add remote: ${REMOTE_NAME} -> ${REMOTE_REPO}"
}

pushAllRefs() {
	local REMOTE_NAME=$1;shift
	log "push all refs to ${REMOTE_NAME}"
	if [ -n "${PUSH_BY_BRANCH}" ]; then
		git for-each-ref refs/heads refs/tags | while read commit type ref; do
			log "pushing ${ref}" 
			git push -f ${REMOTE_NAME} ${ref} || abort "cannot push to remote: ${REMOTE_NAME}"
		done
	else
		git push -f ${REMOTE_NAME} '*:*' || abort "cannot push to remote: ${REMOTE_NAME}"
	fi
}

function pullAndPushAllTheirBranchesAndTagsToOurRemote() {
	local THEIR_REMOTE_NAME=$1;shift
	local OUR_REMOTE_NAME=$1;shift
	local OUR_REMOTE_REPO=$1;shift
	fetchFromAllRemotes ${THEIR_REMOTE_NAME}
	deleteAllBranches
	removeAllOtherRemotes ${THEIR_REMOTE_NAME}
	trackAllBranchesOnRemote ${THEIR_REMOTE_NAME}
	addRemote ${OUR_REMOTE_NAME} ${OUR_REMOTE_REPO}
	pushAllRefs ${OUR_REMOTE_NAME}
}

showHelp() {
	echo "${SELF}: QSDK repository mirroring tool"
	echo
	echo "Usage: ${SELF} [OPTIONS] -n OUR_REMOTE_NAME -r OUR_REMOTE_ROOT"
	echo
	echo "	OUR_REMOTE_NAME  The remote name to use for the destination repositories"
	echo "	                 E.g. github"
	echo "	OUR_REMOTE_ROOT  The destination root URL where all QSDK archives should be pushed to"
	echo "	                 E.g. ssh://git@github.com/PhilipsHueDev/"
	echo
	echo "Options:"
	echo "	-b                    Push by branch: Use a slower but more robust way to push large repositories"
	echo "	-e OUR_REMOTE_PREFIX  A remote prefix to use for each repository"
	echo "	                      E.g. -p bsb002-"
}

abortShowHelp() {
	error "$*"
	showHelp >&2
	exit 1
}

while getopts ":n:r:e:bh" OPT; do
	case ${OPT} in
		n)
			OUR_REMOTE_NAME=${OPTARG}
			;;
		r)
			OUR_REMOTE_ROOT=${OPTARG}
			;;
		e)
			OUR_REMOTE_PREFIX=${OPTARG}
			;;
		b)
			PUSH_BY_BRANCH=1
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

[ -z "${OUR_REMOTE_NAME}" ] && abortShowHelp "Missing mandatory option: -n"
[ -z "${OUR_REMOTE_ROOT}" ] && abortShowHelp "Missing mandatory option: -r"

${QSDK_TOOLS_DIR}/qsdk.py -n ${OUR_REMOTE_NAME} -r ${OUR_REMOTE_ROOT} -e "${OUR_REMOTE_PREFIX}" -l | while read PROJECT_PATH THEIR_REMOTE_NAME OUR_REMOTE_REPO; do
	ABS_PROJECT_PATH=${QSDK_ROOT}/${PROJECT_PATH}
	log "========================================"
	log "Project: ${PROJECT_PATH}"
	log "----------------------------------------"
	cd ${ABS_PROJECT_PATH} || abort "cannot cd to ${ABS_PROJECT_PATH}"
	isValidGitProject || abort "not a valid git project: ${ABS_PROJECT_PATH}"
	pullAndPushAllTheirBranchesAndTagsToOurRemote ${THEIR_REMOTE_NAME} ${OUR_REMOTE_NAME} ${OUR_REMOTE_REPO}
done

exit $?

