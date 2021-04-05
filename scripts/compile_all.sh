#!/bin/bash
SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
g++ ${SCRIPTPATH}/../src/enumCycleE1.cpp -o ${SCRIPTPATH}/../enumCycleE1
g++ ${SCRIPTPATH}/../src/enumCycleE2.cpp -o ${SCRIPTPATH}/../enumCycleE2 -fopenmp
g++ ${SCRIPTPATH}/../src/enumCycleE3.cpp -o ${SCRIPTPATH}/../enumCycleE3 -fopenmp
exit 0
