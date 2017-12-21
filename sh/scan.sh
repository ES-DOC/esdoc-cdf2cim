#!/bin/bash

# Import utils.
source $CDF2CIM_CLIENT_HOME/sh/utils.sh

# Main entry point.
main()
{
	python $CDF2CIM_CLIENT_HOME/sh/scan.py -i $1
}

# Invoke entry point.
main $1
