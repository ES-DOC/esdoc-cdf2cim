#!/bin/bash

# Import utils.
source $CDF2CIM_CLIENT_HOME/sh/utils.sh

# Main entry point.
main()
{
	export PYTHONPATH=$CDF2CIM_CLIENT_HOME:PYTHONPATH
	python $CDF2CIM_CLIENT_HOME/sh/scan.py -i $1
}

# Invoke entry point.
main $1
