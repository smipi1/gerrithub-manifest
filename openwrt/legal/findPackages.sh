#!/bin/bash

TARGET_BUILD_DIR=`readlink -f qualcomm/qsdk/build_dir/target-*/`
TARGET_ROOT=`readlink -f ${TARGET_BUILD_DIR}/root-*/`
TARGET_LINUX_DIR=`readlink -f ${TARGET_BUILD_DIR}/linux-*_generic/`

INSTALLABLES=/tmp/installables

find `find ${TARGET_BUILD_DIR} -type d -and -name 'ipkg-ar71xx'` -type f | xargs -n 1 sha1sum >${INSTALLABLES}
find ${TARGET_ROOT} -type f | xargs -n 1 file | awk -F ':' '/(executable|ELF)/{print $1}' | xargs -n 1 sha1sum | while read SHA1SUM FILEPATH; do
	if ! awk '/'${SHA1SUM}'/{print $2}' ${INSTALLABLES}; then
		echo "not found: ${FILEPATH}"
	fi
done | while read FOUNDFILE; do
	echo "${FOUNDFILE##${TARGET_BUILD_DIR}/}"
done | sort
exit 0

