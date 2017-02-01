#!/bin/bash

# Import utils.
source $CDF2CIM_CLIENT_HOME/sh/utils.sh

# Main entry point.
main()
{
	export PYTHONPATH=$CDF2CIM_CLIENT_HOME:PYTHONPATH
	python $CDF2CIM_CLIENT_HOME/cdf2cim --action=publish -i $1 -o $2
}

# Invoke entry point.
main $1 $2
