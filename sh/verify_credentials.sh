#!/bin/bash

# Import utils.
source $CDF2CIM_CLIENT_HOME/sh/utils.sh

# Main entry point.
main()
{
	python $CDF2CIM_CLIENT_HOME/sh/verify_credentials.py
}

# Invoke entry point.
main
