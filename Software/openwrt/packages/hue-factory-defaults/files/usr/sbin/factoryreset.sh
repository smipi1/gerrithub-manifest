#!/bin/sh

echo "!!! Executing factoryreset !!!" > /dev/ttyS0

# Copy resetreason if provided
if [ -f /var/hue-ipbridge/resetreason ]; then
	local resetreason=`cat /var/hue-ipbridge/resetreason`
	fw_setenv resetreason ${resetreason}
fi

/etc/init.d/ipbridge stop
/etc/init.d/swupdate stop

rm -rf /overlay/*
cd /
sync

reboot
