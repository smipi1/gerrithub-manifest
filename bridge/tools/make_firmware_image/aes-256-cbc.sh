#!/bin/sh

SELF=`basename $0`

unset FUNCTION
unset KEY_FILE
unset OUTPUT_FILE
unset INPUT_FILE
IV_FILE=/tmp/${SELF}.$$.iv
KEY_SIZE=32
IV_SIZE=16

cleanUp() {
	rm -f ${IV_FILE}
}

error() {
	echo "error: $*" >&2
}

abort() {
	cleanUp
	error "$*"
	exit 1
}

sourceInput() {
	if [ -n "${INPUT_FILE}" ]; then
		cat "${INPUT_FILE}"
	else
		cat
	fi
}

sinkOutput() {
	if [ -n "${OUTPUT_FILE}" ]; then
		cat >"${OUTPUT_FILE}"
	else
		cat
	fi
}

encrypt() {
	local KEY_HEX=`hexdump -v -e '/1 "%02X"' ${KEY_FILE}`
	if [ "$?" -ne "0" ]; then
		abort "cannot read key file"
	fi
	if ! openssl rand ${IV_SIZE}; then
		abort "cannot generate initialization vector"
	fi >${IV_FILE}

	# Send to stdout so that it ends in the encrypted file
	cat ${IV_FILE}
	
	local IV_HEX=`hexdump -v -e '/1 "%02X"' ${IV_FILE}`
	if [ "$?" -ne "0" ]; then
		abort "cannot convert initialization vector to hex"
	fi
	if ! openssl enc -e -nosalt -aes-256-cbc -K ${KEY_HEX} -iv ${IV_HEX}; then
		abort "cannot encrypt data"	
	fi
}

decrypt() {
	local KEY_HEX=`hexdump -v -e '/1 "%02X"' ${KEY_FILE}`
	if [ "$?" -ne "0" ]; then
		abort "cannot read key file"
	fi
	if ! dd bs=1 count=${IV_SIZE}; then
		abort "cannot extract initialization vector"
	fi >${IV_FILE} 2>/dev/null

	local IV_HEX=`hexdump -v -e '/1 "%02X"' ${IV_FILE}`
	if [ "$?" -ne "0" ]; then
		abort "cannot convert initialization vector to hex"
	fi
	if ! openssl enc -d -nosalt -aes-256-cbc -K ${KEY_HEX} -iv ${IV_HEX}; then
		abort "cannot decrypt data"	
	fi
}

showHelp() {
	echo
	echo "${SELF}: aes-256-cbc encryption / decryption tool"
	echo
	echo "Usage: ${SELF} [OPERATION] [OPTIONS]"
	echo
	echo "Opertations:"
	echo "	-h                    Shows this help"
	echo "	-e                    Encrypt"
	echo "	-d                    Decrypt"
	echo
	echo "Options:"
	echo "	-k KEY_FILE           Key file to use (mandatory for encryption / decryption)"
	echo "	-f INPUT_FILE         Input file to encrypt / decrypt"
	echo "	                      If omitted, uses stdin"
	echo "	-o OUTPUT_FILE        Output file (result of encryption / decryption)"
	echo "	                      If omitted, uses stdout"
	echo
}

abortShowHelp() {
	error "$*"
	showHelp >&2
	exit 1
}

limitToSingleFunction() {
	local NEW_FUNCTION=$1
	if [ -n "${FUNCTION}" ]; then
		abortShowHelp "options cannot be combined: -${NEW_FUNCTION} and -${FUNCTION}"
	else
		FUNCTION=${NEW_FUNCTION}
	fi
}

abortIfKeyFileInvalid() {
	[ -n "${KEY_FILE}" ] || abortShowHelp "mandatory option not specified: -k"
	[ -f "${KEY_FILE}" ] || abortShowHelp "mandatory option does not point to a file: -k"
	[ -s "${KEY_FILE}" ] || abortShowHelp "mandatory option does points to an empty file: -k"
}

while getopts ":hedk:f:o:" OPT; do
	case ${OPT} in
		h)
			limitToSingleFunction ${OPT}
			;;
		e)
			limitToSingleFunction ${OPT}
			;;
		d)
			limitToSingleFunction ${OPT}
			;;
		k)
			KEY_FILE=${OPTARG}
			;;
		f)
			INPUT_FILE=${OPTARG}
			;;
		o)
			OUTPUT_FILE=${OPTARG}
			;;
		:)
			abortShowHelp "option is missing an argument: -${OPTARG}"
			;;
		\?)
			abortShowHelp "invalid option: -${OPTARG}"
			;;
	esac
done

if [ -z "${FUNCTION}" ]; then
	abortShowHelp "no operation specified"
elif [ "${FUNCTION}" = "h" ]; then
	showHelp
elif [ "${FUNCTION}" = "e" ]; then
	abortIfKeyFileInvalid
	sourceInput | encrypt | sinkOutput
elif [ "${FUNCTION}" = "d" ]; then
	abortIfKeyFileInvalid
	sourceInput | decrypt | sinkOutput
fi

exit 0
