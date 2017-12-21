#!/bin/sh

# Import utils.
source $CDF2CIM_CLIENT_HOME/sh/utils.sh

# Main entry point.
main()
{
    log "ERRATA-TESTS : execution starts ..."

    nosetests -v -s $CDF2CIM_CLIENT_HOME/tests
    # nosetests -v -s $CDF2CIM_CLIENT_HOME/tests/test_publish.py

    log "ERRATA-TESTS : execution complete ..."
}

# Invoke entry point.
main