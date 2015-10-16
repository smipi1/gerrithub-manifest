#!/bin/sh

SELF=`basename $0`
TOOLS_DIR=`readlink -e $(dirname $0)`
DEST_DIR=/tmp/${SELF}.$$
DEST_REPO="ssh://git@github.com/PhilipsHueDev/bsb002-cae-build.git"
SRC_DIR=`readlink -e ${TOOLS_DIR}/../..`
OPENWRT_DIR=openwrt
SRC_OPENWRT_DIR=${SRC_DIR}/${OPENWRT_DIR}
DEST_OPENWRT_DIR=${DEST_DIR}/${OPENWRT_DIR}
DEST_IPBRIDGE_MOCK_MAKEFILE=${DEST_DIR}/bridge/build/Makefile
SRC_OPENWRT_BUILD_DIR=`readlink -e ${SRC_OPENWRT_DIR}/qualcomm/qsdk/build_dir/target-*/`
SRC_OPENWRT_ROOT_DIR=`readlink -e ${SRC_OPENWRT_BUILD_DIR}/root-*/`
PACKAGE_MAKE_MOCK_DIR=`readlink -e ${TOOLS_DIR}/update-cae-build-repo`
COMMIT_MESSAGE_PATH=${DEST_DIR}/.git/COMMIT_EDITMSG
ADDITIONAL_SRC_FILES="
	zigbee/samr21/ZigBeeBridge-HueV2-SAMR21.releaseinfo
	bridge/tools/make_firmware_image/create_fw2.py
	bridge/tools/make_firmware_image/create_rsa_signature.py
	bridge/tools/make_firmware_image/certs/RSA_dev_01.pem
"
TOUCHED_SRC_FILES="
	zigbee/samr21/ZigBeeBridge-HueV2-SAMR21_8001.hex
"

# Include git and svn helpers
. ${TOOLS_DIR}/git-svn-helpers.sh

cleanUp() {
	rm -rf ${DEST_DIR}
}

error() {
	echo "error: $*" >&2
}

abort() {
	error $*
	cleanUp
	exit 1
}

recursivelyListVersionedItems() {
	local TYPE=$1;shift
	local DIRECTORY=$1;shift
	local GREP_ARG
	case "${TYPE}" in
	f)
		GREP_ARG=-v
		;;
	d)
		GREP_ARG=
		;;
	*)
		error "recursivelyListVersionedItems(): Unsupported type: ${TYPE}"
		return 1
		;;
	esac
	if ! cd ${DIRECTORY}; then
		error "cannot cd to directory: ${DIRECTORY}"
		return 1
	elif ! svn ls -R; then
		error "svn cannot list versioned items: ${DIRECTORY}"
		return 1
	fi | if ! grep ${GREP_ARG} '/$'; then
		error "cannot filter out directories: ${DIRECTORY}"
		return 1
	fi
	return 0
}

copyVersionedFilesInSrcToDest() {
	local SRC=$1;shift
	local DEST=$1;shift
	if ! mkdir -p ${DEST}; then
		error "cannot create destination directory: ${DEST}"
		return 1
	elif ! recursivelyListVersionedItems f ${SRC}; then
		error "cannot list versioned files: ${SRC}"
		return 1
	fi | if ! xargs tar -C ${SRC} -c; then
		error "cannot archive versioned files: ${SRC}"
		return 1
	fi | if ! tar -C ${DEST} -x; then
		error "cannot extract versioned files: ${DEST}"
		return 1
	fi
}

migrateIgnoresFromSrcToDest() {
	local SRC=$1;shift
	local DEST=$1;shift
	local SRC_DIR
	if ! mkdir -p ${DEST}; then
		error "cannot create destination directory: ${DEST}"
		return 1
	elif ! echo "."; then
		error "cannot add root: ${SRC}"
		return 1
	elif ! recursivelyListVersionedItems d ${SRC}; then
		error "cannot list versioned files: ${SRC}"
		return 1
	fi | while read SRC_DIR; do
		IGNORE_FILE=${DEST}/${SRC_DIR}/.gitignore
		if ! svn propget svn:ignore ${SRC}/${SRC_DIR} > ${IGNORE_FILE}; then
			rm -f ${IGNORE_FILE}
		fi 
	done
	return 0
}

copyFromSrcToDestSpecifiedPaths() {
	local SRC_DIR=$1;shift
	local DEST_DIR=$1;shift
	local FILE_PATHS="$*";shift
	local FILE_PATH
	local FILE_DEST_DIR
	for FILE_PATH in ${FILE_PATHS}; do
		FILE_DEST_DIR=`dirname ${DEST_DIR}/${FILE_PATH}`
		if ! mkdir -p ${FILE_DEST_DIR}; then
			error "cannot create destination directory: ${FILE_DEST_DIR}"
			return 1
		elif ! cp -a ${SRC_DIR}/${FILE_PATH} ${DEST_DIR}/${FILE_PATH}; then
			error "cannot copy file: ${SRC_DIR}/${FILE_PATH} -> ${DEST_DIR}/${FILE_PATH}"
			return 1
		fi
	done
}

touchDestSpecifiedPaths() {
	local DEST_DIR=$1;shift
	local FILE_PATHS="$*";shift
	local FILE_PATH
	local FILE_DEST_DIR
	for FILE_PATH in ${FILE_PATHS}; do
		FILE_DEST_DIR=`dirname ${DEST_DIR}/${FILE_PATH}`
		if ! mkdir -p ${FILE_DEST_DIR}; then
			error "cannot create destination directory: ${FILE_DEST_DIR}"
			return 1
		elif ! touch ${DEST_DIR}/${FILE_PATH}; then
			error "cannot touch file: ${DEST_DIR}/${FILE_PATH}"
			return 1
		fi
	done
}

filterForInstalledOutOfPackageFiles() {
	awk '/^install [^\.]/{print $2, $3}'
	return $?
}

filterOutSourcePaths() {
	local PATH_TO_FILTER=$1
	grep -v '^'${PATH_TO_FILTER}''
	return 0
}

toSourceDirRelativePaths() {
	sed 's#^'${SRC_DIR}'/##g'
	return $?
}

copyDestToNewSourceDir() {
	local NEW_SRC_DIR=$1;shift
	local SRC_PATH
	local NEW_SRC_PATH
	local DEST_PATH
	while read SRC_PATH DEST_PATH; do
		if [ -d "${DEST_PATH}" ]; then
			DEST_PATH=${DEST_PATH}/`basename ${SRC_PATH}`
		fi
		NEW_SRC_PATH=${NEW_SRC_DIR}/${SRC_PATH}
		mkdir -p `dirname ${NEW_SRC_PATH}`
		cp -a ${DEST_PATH} ${NEW_SRC_PATH}
	done
	return 0
}

copyInstalledOutOfPackageSources() {
	local MAKEFILE=$1
	if ! make TOPDIR=${PACKAGE_MAKE_MOCK_DIR} INCLUDE_DIR=${PACKAGE_MAKE_MOCK_DIR} BUILD_DIR=${SRC_OPENWRT_BUILD_DIR} TARGET_ROOT_DIR=${SRC_OPENWRT_ROOT_DIR} -f ${MAKEFILE}; then
		error "cannot determine installed files: ${MAKEFILE}"
		return 1
	fi | if ! filterForInstalledOutOfPackageFiles; then
		error "cannot find out-of-package files: ${MAKEFILE}"
		return 1
	fi | if ! filterOutSourcePaths ${SRC_OPENWRT_BUILD_DIR}; then
		error "cannot filter build directory paths out of source paths: ${MAKEFILE}"
		return 1
	fi | if ! toSourceDirRelativePaths; then
		error "cannot generate relative out-of-package file paths: ${MAKEFILE}"
		return 1
	fi | if ! copyDestToNewSourceDir ${DEST_DIR}; then
		error "cannot copy to new source directory: ${MAKEFILE}"
		return 1
	fi 
}

addIpBridgeMockedMakefile() {
	local DEST=$1;shift
	local DEST_DIR=`dirname ${DEST}`
	if ! mkdir -p ${DEST_DIR}; then
		error "cannot create directory: ${DEST_DIR}"
		return 1
	elif ! cat >${DEST}; then
		error "cannot write data: ${DEST}"
		return 1
	elif [ -z ${DEST} ]; then
		error "destination file empty: ${DEST}"
		return 1
	else
		return 0
	fi <<EOF
all.configure:

linux_qualcomm_release:

EOF
}

if ! setupEmptyGitWorkspaceForSvnSrcDir ${SRC_DIR} ${DEST_DIR} ${DEST_REPO}; then
	abort "cannot create temporary directory: ${DEST_DIR}"
elif ! copyVersionedCommitMessage ${SRC_DIR} ${COMMIT_MESSAGE_PATH}; then
	abort "cannot copy commit message: ${COMMIT_MESSAGE_PATH}"
elif ! copyVersionedFilesInSrcToDest ${SRC_OPENWRT_DIR} ${DEST_OPENWRT_DIR}; then
	abort "cannot copy versioned files: ${SRC_OPENWRT_DIR} -> ${DEST_OPENWRT_DIR}"
elif ! migrateIgnoresFromSrcToDest ${SRC_OPENWRT_DIR} ${DEST_OPENWRT_DIR}; then
	abort "cannot migrate ignored files: ${SRC_OPENWRT_DIR} -> ${DEST_OPENWRT_DIR}"
elif ! copyFromSrcToDestSpecifiedPaths ${SRC_DIR} ${DEST_DIR} ${ADDITIONAL_SRC_FILES}; then
	abort "cannot copy additional files"
elif ! touchDestSpecifiedPaths ${DEST_DIR} ${TOUCHED_SRC_FILES}; then
	abort "cannot copy additional files"
elif ! addIpBridgeMockedMakefile ${DEST_IPBRIDGE_MOCK_MAKEFILE}; then
	abort "cannot add ipbridge mocked Makefile"
else
	for MAKEFILE in ${SRC_OPENWRT_DIR}/packages/*/Makefile; do
		copyInstalledOutOfPackageSources ${MAKEFILE} ${DEST_DIR}
	done
fi

TAG=`getRelease ${SRC_DIR}`

if ! commitTagAndPushAllFiles ${DEST_DIR} ${COMMIT_MESSAGE_PATH} ${TAG}; then
	abort "cannot commit, tag and push git workspace: ${DEST_DIR}"
fi

cleanUp

exit 0
