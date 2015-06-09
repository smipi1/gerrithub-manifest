#!/bin/sh

isValidPemPublicKey() {
	openssl rsa -inform PEM -pubin 2>/dev/null
	return $?
}

pemPayloadOnOneLine() {
	awk '/^[^-]/{printf $1}'
	return $?
}

pemPublicKeyToPemString() {
	if ! isValidPemPublicKey; then
		echo "error: input not a PEM formatted public key" >&2
		return 1
	fi | if ! pemPayloadOnOneLine; then
		echo "error: cannot reformat payload" >&2
		return 1
	fi
}

addPemPublicKeyHeaderAndFooter() {
	echo "-----BEGIN PUBLIC KEY-----" || return 1
	cat || return 1
	echo
	echo "-----END PUBLIC KEY-----" || return 1
	return 0
}

splitLines64chars() {
	sed 's/\n//g;s/.\{64\}/&\n/g'
	return $?
}

removeEmptyLines() {
	sed '/^[\t ]*$/d'
	return $?
}

pemStringToPemPublicKey() {
	if ! splitLines64chars; then
		echo "error: cannot split string into rows" >&2
		return 1
	fi | if ! addPemPublicKeyHeaderAndFooter; then
		echo "error: cannot add header and footer" >&2
		return 1
	fi | if ! removeEmptyLines; then
		echo "error: cannot remove empty lines" >&2
		return 1
	fi | if ! isValidPemPublicKey; then
		echo "error: input not a PEM payload string" >&2
		return 1
	fi
}

