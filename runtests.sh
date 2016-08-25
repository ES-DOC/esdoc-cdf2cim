#!/bin/sh

# Set paths.
CDF2CIM_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $CDF2CIM_DIR

# Ensure that tests  tmp directory is empty.
rm -rf $CDF2CIM_DIR/tests/test-output
mkdir $CDF2CIM_DIR/tests/test-output

# Extend python path.
export PYTHONPATH=PYTHONPATH:$CDF2CIM_DIR

# Run test suite.
nosetests -v -s tests
