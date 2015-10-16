#!/bin/bash

extractSpiCountCsv() {
	awk '
/BEGIN/ {
	lines=0
}

/console:/ {
	if(!start) {
		start=$1
	}
}

/dut>: spi_counters:/ {
	time=$1
	split($0, parts, "dut>: spi_counters:")
	split(parts[2], vks)
	for(i in vks) {
		split(vks[i], vk, ":")
		key=vk[2]
		value=vk[1]
		counters[key]=value
	}
	if(!lines) {
		printf("time")
		for(c in counters) {
			printf(", 0x%s", c)
		}
		printf("\n")
	}
	printf("%1.3f", time-start)
	for(c in counters) {
		printf(", %d", counters[c])
	}
	printf("\n")
	
	lines++
}
'
}

extractTests() {
	awk '
/BEGIN/ {
	printf("time, test, requests\n")
	requests=0
	test=""
}

/console:/ {
	if(!start) {
		start=$1
	}
}

/end:/ {
	test=""
}

/start:/ {
	time=$1
	split($0, parts, "start:")
	test=parts[2]
	sub(/^ */, "", test)
	printf("%1.3f, %s, %d\n", time-start, test, requests)
}

/clip:/ {
	requests++
	if(length(test)) {
		time=$1
		printf("%1.3f, %s, %d\n", time-start, test, requests)
	}
}
'
}

FILE=$1;shift

extractSpiCountCsv <${FILE} >${FILE}.spi_count.csv
extractTests <${FILE} >${FILE}.clip.csv

