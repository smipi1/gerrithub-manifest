#!/bin/bash


DUT=${1};shift
. `dirname $0`/dut.sh
[ -n "${DUT}" ] || abort "Device-under-test IP address not specified"

FS_TYPE=${1};shift
case "${FS_TYPE}" in
	ubifs)
		;;
	jffs2)
		;;
	*)
		abort "Unsupported or no file-system type specified"
		;;
		
esac

ITERATIONS=${1-1};shift 2>/dev/null
echo "ITERATIONS=${ITERATIONS}"

FILESIZE=${1-10M};shift 2>/dev/null
echo "FILESIZE=${FILESIZE}"

setHostname() {
	local HOSTNAME=$1
	clip PUT config \
'{
  "name": "'${HOSTNAME}'"
}'
	return $?
}

unmountTestVolume() {
	dutExe "mount | grep '/tmp/test' && umount /tmp/test || mkdir -p /tmp/test"
}

getSpareRootPartition() {
	dutExe 'SELF=benchmark'
	dutExe '. /lib/functions/mtd.sh'
	dutExe 'BOOTSLOT=`fw_printenv -n bootslot`'
	dutExe 'let "NEXT_BOOTSLOT=!${BOOTSLOT}"'
	dutExe 'SPARE_ROOTFS_MTD=`nameToMtdDevice root-${NEXT_BOOTSLOT}`'
	dutExe 'echo "SPARE_ROOTFS_MTD=${SPARE_ROOTFS_MTD}"'
}

detachSpareRootPartition() {
	dutExe 'if [ -c /dev/ubi2 ]; then ubidetach -p /dev/${SPARE_ROOTFS_MTD}; fi'
}

formatSpareRootPartition() {
	dutExe 'ubiformat /dev/${SPARE_ROOTFS_MTD}'
}

attachSpareRootPartition() {
	dutExe 'ubiattach -p /dev/${SPARE_ROOTFS_MTD}'
}

makeTestVolume() {
	dutExe 'ubimkvol /dev/ubi2 -N test -m'
}

mountTestJffs2Volume() {
	dutExe 'TEST_MTD=`nameToMtdDevice test`'
	dutExe 'mount -t jffs2 /dev/${TEST_MTD//mtd/mtdblock} /tmp/test/'
}

mountTestUbifsVolume() {
	dutExe 'TEST_MTD=`nameToMtdDevice test`'
	dutExe 'mount -t ubifs ubi2:test /tmp/test/'
}

mountTestVolume() {
	local FS_TYPE=$1
	case "$1" in
	jffs2)
		mountTestJffs2Volume
		;;
	ubifs)
		mountTestUbifsVolume
		;;
	esac
	local RESULT=$?
	[ "${RESULT}" -eq "0" ]  && dutExe 'mount | grep test'
	return ${RESULT}
}

test() {
	log "test: $*"
}

timeFileWriteAndSync() {
	test "fileWrite[s]"
	dutExe "time dd if=/dev/urandom of=/tmp/test/dummy count=1 bs=${FILESIZE} 2>&1" || return $?
	test "fileWriteSync[s]"
	dutExe "time fsync /tmp/test/dummy /tmp/test 2>&1" || return $?
}

timeFileRead() {
	test "fileRead[s]"
	dutExe "time dd if=/tmp/test/dummy of=/dev/null count=1 bs=${FILESIZE} 2>&1"
}

timeFileDeleteAndSync() {
	test "fileDelete[s]"
	dutExe "time rm /tmp/test/dummy 2>&1" || return $?
	test "fileDeleteSync[s]"
	dutExe "time fsync /tmp/test 2>&1" || return $?
}

parseSummary() {
	awk -F ':' '
// {
	print $0
}
/test:/ {
	TEST=$2
}
/real/ {
	split($1,t," ")
	min=t[2]
	sec=t[3]
	printf("min=%s, sec=%s\n", min, sec)
}
'
}

openDutConsole
unmountTestVolume || abort "cannot unmount test volume"
getSpareRootPartition || abort "cannot determine spare root partition"
detachSpareRootPartition || abort "cannot detach spare root partition"
formatSpareRootPartition || abort "cannot format spare root partition"
attachSpareRootPartition || abort "cannot attach spare root partition"
makeTestVolume || abort "cannot make test volume"
mountTestVolume ${FS_TYPE} || abort "cannot mount test volume"
for i in `seq 1 ${ITERATIONS}`; do
	log "iteration: $i"
	timeFileWriteAndSync || abort "cannot time file write"
	timeFileRead || abort "cannot time file read"
	timeFileDeleteAndSync || abort "cannot time file read"
done
closeDutConsole
exit 0

