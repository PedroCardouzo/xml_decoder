#!/bin/bash

PROGRAM='xml_decoder.sh'

RED='\033[0;31m'
GREEN='\033[0;32m' 
NO_COLOR='\033[0m'

TESTS_PASSED=0
TOTAL_TESTS=0
echo -e '\nRunning tests...'


for TEST_FILE in $(ls test/*_test.xml | sort -V); do 
	EXPECTED_FILE=${TEST_FILE//_test/_expected}
	DIFF_FILE=${TEST_FILE//_test/_diff}
    OUT_FILE=${TEST_FILE//_test/_out}

    # run test
    $(./$PROGRAM < $TEST_FILE > $OUT_FILE 2>&1)
    DIFF_BUFFER=$(diff -w $OUT_FILE $EXPECTED_FILE)

    # if both files are equal (not considering whitespaces as per -w option on diff)
    if [ $? -eq 0 ]; then
        echo -ne $GREEN
        echo "TEST" \"$TEST_FILE\"": OK"
        echo -ne $NO_COLOR
        let "TESTS_PASSED++"
    else
        echo -ne $RED
        echo "TEST" \"$TEST_FILE\"": ERROR"
        echo -ne $NO_COLOR
        # dont know if this is a good idea, but for not i'm both sending to a file and showing in terminal if diff exists
        # my doubts are on the last part
        echo "Diff:"
        echo $DIFF_BUFFER | tee $DIFF_FILE
    fi

    let "TOTAL_TESTS++"
done

if [[ $TESTS_PASSED = $TOTAL_TESTS ]]; then
    echo -ne $GREEN
else
    echo -ne $RED
fi

echo $TESTS_PASSED/$TOTAL_TESTS "TESTS PASSED"
