#!/bin/bash

#quick rename script

for FILENAME in $(ls test | grep -P "payload[0-9]*\.xml"); do
	mv test/$FILENAME test/${FILENAME//.xml/_test.xml}
done
