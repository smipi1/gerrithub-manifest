#!/bin/bash

DUT=${1};shift
. `dirname $0`/dut.sh
[ -n "${DUT}" ] || abort "Device-under-test IP address not specified"

IDLE_AT_END=600
SENSOR_MIN=2
SENSOR_MAX=64
RULE_MIN=1
RULE_MAX=100

forAllSensors() {
	local DO=$1
	local SENSOR=${SENSOR_MIN}
	while [ "${SENSOR}" -le "${SENSOR_MAX}" ]; do
		${DO} ${SENSOR}
		let "SENSOR++"
	done
}

deleteSensor() {
	local SENSOR=$1
	delete sensors/${SENSOR} || exit 1
}

forAllRules() {
	local DO=$1
	local RULE=${RULE_MIN}
	while [ "${RULE}" -le "${RULE_MAX}" ]; do
		${DO} ${RULE}
		let "RULE++"
	done
}

deleteRule() {
	local RULE=$1
	delete rules/${RULE}
}

addRule() {
	clip POST rules \
'{
    "name": "Rule name",
    "conditions": [
        {
            "address": "/sensors/2/state/presence",
            "operator": "eq",
            "value": "true"
        },
        {
            "address": "/sensors/2/state/presence",
            "operator": "eq",
            "value": "true"
        },
        {
            "address": "/sensors/2/state/presence",
            "operator": "eq",
            "value": "true"
        },
        {
            "address": "/sensors/2/state/presence",
            "operator": "eq",
            "value": "true"
        }

    ],
    "actions": [
        {
            "address": "/lights/1/state",
            "method": "PUT",
            "body": {
                "alert": "select"
            }
        },
        {
            "address": "/lights/2/state",
            "method": "PUT",
            "body": {
                "alert": "select"
            }
        },
        {
            "address": "/lights/3/state",
            "method": "PUT",
            "body": {
                "alert": "select"
            }
        },
        {
            "address": "/lights/4/state",
            "method": "PUT",
            "body": {
                "alert": "select"
            }
        }
    ]
}' || exit 1
}

startTest() {
	log "start: $*"
}

endTest() {
	log "end: $*"
}

runTest() {
	local NAME=$1;shift
	startTest ${NAME}
	$*
	endTest ${NAME}
}

cleanupRules() {
	runTest rules_delete forAllRules deleteRule
}

cleanupSensors() {
	runTest sensors_delete forAllSensors deleteSensor
}

createRules() {
	runTest rules_create forAllRules addRule
}

createSensors() {
	runTest sensors_create forAllSensors addPresenceSensor
}

startMetrics() {
	dutExe "
while [ 1 ]; do
	top -b -n 1 | while read line; do
		echo \"top: \${line}\"
	done
	awk -F ':' '
	BEGIN {
		printf(\"spi_counters:\")
	}
	// {
		printf(\"%6d:%s \", \$2, \$1)
	}
	END {
		print \"\"
	}
	' /proc/spi_cmd
	sleep 1
done &
"
}

testDut() {
	local ITER=0
	local NO_ITERS=${1-1};shift
	local WAIT_FOR_IDLE=${1-1};shift
	openDutConsole
	startMetrics
	pressLink
	addValidUser
	releaseLink
	sleep 1
	while [ "${ITER}" -lt "${NO_ITERS}" ]; do
		createSensors
		createRules
		cleanupRules
		cleanupSensors
		let "ITER++"
	done
	sleep ${WAIT_FOR_IDLE}
	closeDutConsole
}

CMD=$1;shift

case "${CMD}" in
"cleans")
	cleanupSensors
	;;
"cleanr")
	cleanupRules
	;;
"cleanup")
	cleanupRules
	cleanupSensors
	;;
*)
	testDut $*
	;;
esac

exit 0

