#!/bin/sh
# Runs cdf2cim test suite.
CDF2CIM_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $CDF2CIM_DIR
export PYTHONPATH=PYTHONPATH:$CDF2CIM_DIR
nosetests -v -s tests
