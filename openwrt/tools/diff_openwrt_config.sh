#!/bin/sh

REV=${1-HEAD}
DIFF_ARGS=${2-"-u"}

SELF=`basename $0`
OPENWRT_DIR=`dirname $0`/../
OPENWRT_CONFIG=qualcomm_qsdk_openwrt_config
TMP_DIR=/tmp/${SELF}.$$
CONFIG_OLD=${TMP_DIR}/${OPENWRT_CONFIG}@${REV}
CONFIG_CURRENT=${TMP_DIR}/${OPENWRT_CONFIG}
unset DIFF

error() {
	echo "error: $*" >&2
}

abort() {
	error "$*"
	tearDown
	exit 1
}

setUp() {
	mkdir -p ${TMP_DIR}
	if which colordiff >/dev/null; then
		DIFF=colordiff
	else
		DIFF=diff
	fi
}

tearDown() {
	rm -rf ${TMP_DIR}
}

sortConfigAndRemoveComments() {
	grep -v '^#' | sort -u
}

setUp

cd ${OPENWRT_DIR}/configs

if ! cat ${OPENWRT_CONFIG}; then
	abort "cannot read: ${OPENWRT_CONFIG}"
fi | if ! sortConfigAndRemoveComments; then
	abort "cannot sort and remove comments: ${OPENWRT_CONFIG}"
fi >${CONFIG_CURRENT}

if ! svn cat ${OPENWRT_CONFIG}@${REV}; then
	abort "cannot read: ${OPENWRT_CONFIG}@${REV}"
fi | if ! sortConfigAndRemoveComments; then
	abort "cannot sort and remove comments: ${OPENWRT_CONFIG}@${REV}"
fi >${CONFIG_OLD}

${DIFF} ${DIFF_ARGS} ${CONFIG_OLD} ${CONFIG_CURRENT}

