#!/bin/bash

# Import utils.
source $CDF2CIM_CLIENT_HOME/sh/utils.sh

# Main entry point.
main()
{
	cd $CDF2CIM_CLIENT_HOME
	python ./setup.py sdist upload

	log "cdf2cim client uploaded to pypi"
}

# Invoke entry point.
main
