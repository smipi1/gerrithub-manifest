#!/bin/bash
set -o pipefail

TOOL_DIR=`dirname $0`

${TOOL_DIR}/benchmarkFilesystem.sh $* | gawk -F ':' '
function dumpResults() {
	if(firstIter) {
		for(r in results) {
			out = out sprintf("%s\t", r)
		}
		out = out sprintf("\n")
		firstIter = 0
	}
	for(r in results) {
		out = out sprintf("%f\t", results[r])
	}
	out = out sprintf("\n")
	delete results
}
BEGIN {
	out = ""
	firstIter = 1
}
// {
	print $0
}
/test:/ {
	test=$2
	sub(/^ */, "", test)
	sub(/ *$/, "", test)
}
/dut>: real/ {
	if(test in results) {
		dumpResults()
	}
	split($2, p, " ")
	sub(/m$/, "", p[2])
	sub(/s$/, "", p[3])
	time=p[2] * 60 + p[3]
	results[test] = time
}
END {
	dumpResults()
	printf("----------------------------------------\n")
	printf(out)
}
'

