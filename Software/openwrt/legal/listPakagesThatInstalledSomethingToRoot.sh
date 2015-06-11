#!/bin/sh
# 
# How to use:
#   To list all packages that install things in the rootfs:
#     ./tool/listPakagesThatInstalledSomethingToRoot.sh
#   Specific information about what a package installs can be read with:
#     ./tool/listPakagesThatInstalledSomethingToRoot.sh <package_name>
#     <package_name> does not have to have the full package name. The first few chars is sufficient.

TOOLS_DIR=`readlink -e $(dirname $0)`
BUILD_DIR=`readlink -e ${TOOLS_DIR}/../qualcomm/qsdk/build_dir/target-*/`
ROOT_DIR=`readlink -e ${BUILD_DIR}/root-*`

allFiles() {
	find -type f
}

toFilenameAndType() {
	xargs file | awk -F ':' '{print $1, $2}'
}

filterOutTextEmptyAndData() {
	egrep -v ' ASCII text$' | grep -v ' empty$' | grep -v ' data$'
}

listAllApplicableFiles() {
	cd ${ROOT_DIR}
	allFiles | toFilenameAndType | filterOutTextEmptyAndData
	cd - >/dev/null
}

rootDirName() {
	grep -v '^'`basename ${ROOT_DIR}`'' | if [ -n "${PACKAGE}" ]; then
		grep '^'${PACKAGE}''
	else
		awk -F '/' '
			// {
				print $1
			}
			/^linux-ar71xx_generic\// {
				print $1 "/" $2
			}'
	fi
}

sortAndShowUniqueValues() {
	sort -u
}

fileNamesToFindArgs() {
	local PATHNAME
	local TYPE
	local FILENAME
	local FIND_ARGS
	while read PATHNAME TYPE; do
		FILENAME=`basename ${PATHNAME}`
		if [ -n "${FIND_ARGS}" ]; then
			FIND_ARGS="${FIND_ARGS} -or"
		fi
		FIND_ARGS="${FIND_ARGS} -name ${FILENAME}"
	done
	echo ${FIND_ARGS}
}

listPackagesThatContainFiles() {
	cd ${BUILD_DIR}
	local FIND_ARGS="`listAllApplicableFiles | fileNamesToFindArgs`"
	find * ${FIND_ARGS} | rootDirName | sortAndShowUniqueValues
	cd - >/dev/null
}

PACKAGE=$1

listAllApplicableFiles | listPackagesThatContainFiles

