#!/bin/sh

SELF=`basename $0`
ABS_SELF=`readlink -e $0`
TOOLS_DIR=`dirname ${ABS_SELF}`
RELEASE_DIR=`readlink -e ${TOOLS_DIR}/../release`
TMPDIR=/tmp/${SELF}.$$
TMP_ROOT_DIR=${TMPDIR}/rootfs

QSDK_TOPDIR=`readlink -e ${TOOLS_DIR}/../qualcomm/qsdk`
QSDK_HOST_DIR=${QSDK_TOPDIR}/staging_dir/host

OTAU_ROOTFS_ARCHIVE=${RELEASE_DIR}/BSB002.fw2.rootfs.tar.gz

UBINIZE_CONFIG=${QSDK_TOPDIR}/target/linux/ar71xx/image/ubinize-root-bsb002.ini

MKSQUASHFS4=${QSDK_HOST_DIR}/bin/mksquashfs4
PADJFFS2=${QSDK_HOST_DIR}/bin/padjffs2
UBINIZE=${QSDK_HOST_DIR}/bin/ubinize

TARGET_FILE=$1;shift

error() {
	echo "error: $*" >&2
}

abort() {
	error "$*"
	exit 1
}

makeModifications() {
	touch $1/wies_and_pieter_wuz_here
}

toSquashFsImage() {
	${MKSQUASHFS4} $* -nopad -noappend -root-owned -comp xz -Xpreset 9 -Xe -Xlc 0 -Xlp 2 -Xpb 2  -b 256k -p '/dev d 755 0 0' -p '/dev/console c 600 0 0 5 1' -processors 1
	return $?
}

padSquashFsImage() {
	${PADJFFS2} $* 4 8 16 64 128 256
	return $?
}

ubinizeSquashFsImage() {
	${UBINIZE} -o $* -p 128KiB -m 2048 ${UBINIZE_CONFIG}
}

mkdir ${TMPDIR} || abort "cannot create temporary directory: ${TMPDIR}"
mkdir ${TMP_ROOT_DIR} || abort "cannot create temporary directory: ${TMP_ROOT_DIR}"
cd ${TMPDIR}

extractRootFsArchive() {
	tar -C $1 -xzf ${OTAU_ROOTFS_ARCHIVE}
}

extractRootFsArchive ${TMP_ROOT_DIR}
makeModifications ${TMP_ROOT_DIR} 
toSquashFsImage ${TMP_ROOT_DIR} root.squashfs
padSquashFsImage root.squashfs
ubinizeSquashFsImage ${TARGET_FILE}

rm -rf ${TMPDIR}
