#!/bin/sh

SELF=`basename $0`
LEGAL_DIR=`readlink -e $(dirname $0)`
TOOLS_DIR=`readlink -e ${LEGAL_DIR}/../tools`
DEST_REPO="ssh://git@github.com/PhilipsHueDev/bsb002-legal-sources.git"
SRC_DIR=`readlink -e ${LEGAL_DIR}/../..`
SOURCES_DIR=openwrt

# Include git and svn helpers
. ${TOOLS_DIR}/git-svn-helpers.sh

error() {
	echo "error: $*" >&2
}

abort() {
	error $*
	exit 1
}

help() {
	echo "
${SELF} [OPTIONS] FUNCTION

Package sources archiving tool. This tool is used to prepare, commit and push all
open-source packages so that they are available for open-source compliance. Packages
are pushed to: ${DEST_REPO}
under the current svn branch.
Note that this script only performs the git work. It is the responsibility of other
tooling to collect and copy the source artefacts to DEST_DIR in between the -p and -c
steps.

Any one of the following FUNCTIONs can be specified:
	-h                       Prints this help
	-p DEST_DIR              Prepares DEST_DIR so that package source archives can be added
	-c DEST_DIR              Commits and pushes the contents of DEST_DIR to
	                         ${DEST_REPO}
"
}

abortAndPrintHelp() {
	error "$*"
	help >&2
	exit 1
}

prepare() {
	local SRC_DIR=$1;shift
	local DEST_DIR=$1
	rm -rf ${DEST_DIR}
	if ! setupEmptyGitWorkspaceForSvnSrcDir ${SRC_DIR} ${DEST_DIR} ${DEST_REPO}; then
		abort "cannot create temporary directory: ${DEST_DIR}"
	elif ! copyVersionedCommitMessage ${SRC_DIR} ${COMMIT_MESSAGE_PATH}; then
		abort "cannot copy commit message: ${COMMIT_MESSAGE_PATH}"
	fi
}

limitToSingleFunction() {
	local NEW_FUNCTION=$1
	if [ -n "${FUNCTION}" ]; then
		abort "functions cannot be combined: -${NEW_FUNCTION} and -${FUNCTION}"
	else
		FUNCTION=${NEW_FUNCTION}
	fi
}

while getopts ":p:c:h" OPT; do
	case ${OPT} in
		p)
			limitToSingleFunction ${OPT}
			DEST_DIR=${OPTARG}
			;;
		c)
			limitToSingleFunction ${OPT}
			DEST_DIR=${OPTARG}
			;;
		h)
			limitToSingleFunction ${OPT}
			;;
		:)
			abortShowHelp "Option is missing an argument: -${OPTARG}"
			;;
		\?)
			abortShowHelp "Invalid option: -${OPTARG}"
			;;
	esac
done

DEST_SOURCES_DIR=${DEST_DIR}/${SOURCES_DIR}
DEST_DIR=`readlink -e ${DEST_DIR}`
COMMIT_MESSAGE_PATH=${DEST_DIR}/.git/COMMIT_EDITMSG
TAG=`getRelease ${SRC_DIR}`

if [ -z "${FUNCTION}" ]; then
	abortAndPrintHelp "FUNCTION not specified"
elif [ "${FUNCTION}" = "h" ]; then
	help
	exit 0
elif [ "${FUNCTION}" = "p" ]; then
	if ! prepare ${SRC_DIR} ${DEST_DIR}; then
		abort "cannot prepare a git worspace: ${DEST_DIR}" 
	fi
elif [ "${FUNCTION}" = "c" ]; then
	if ! commitTagAndPushAllFiles ${DEST_DIR} ${COMMIT_MESSAGE_PATH} ${TAG}; then
		abort "cannot commit, tag and push git workspace: ${DEST_DIR}"
	fi
else
	abortAndPrintHelp "nothing to do"
	exit 1
fi
