#!/bin/sh
# Copyright (C) 2015 Philips Lighting

. /lib/functions/secure-console.sh

if [ -z "${UBOOT_SECURITY_STRING}" ]; then
	exec /bin/ash --login
else
	exec /bin/login
fi
