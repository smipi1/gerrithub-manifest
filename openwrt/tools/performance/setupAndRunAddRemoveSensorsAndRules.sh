#!/bin/bash

DUT=$1;shift

waitUntilReachableOnSsh() {
	local HOST=$1	
	while ! ssh root@${HOST} -o StrictHostKeyChecking=no 'exit'; do
		sleep 1
	done
}

waitUntilReachableOnSsh ${DUT}
./addRemoveSensorsAndRules.sh ${DUT} test $*

