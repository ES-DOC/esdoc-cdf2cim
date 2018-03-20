# -*- coding: utf-8 -*-

"""
.. module:: cli.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: cdf2cim client command line interface.

.. moduleauthor:: David Hassell <david.hassell@ncas.ac.uk>


"""
import argparse
import sys

import cdf2cim



def verify_credentials():
    """Verifies that passed credentials are deemed valid by ES-DOC cdf2cim web-service.

    """
    try:
        cdf2cim.verify_credentials()
    except Exception as err:
        cdf2cim.log_error('Credentials verification failed: {}'.format(err))
        sys.exit(1)
    else:
        cdf2cim.log('Credentials verification succeeded')
        sys.exit(0)


def scan():
    """Scan NetCDF files and cdf2cim specific metadata to file-system.

    :returns: Tuple of scanned cdf2cim files written to file system.
    :rtype: tuple

    """
    # Parse command line args.
    parser = argparse.ArgumentParser("ES-DOC netCDF scanner.")
    parser.add_argument(
        "-i", "--in-dir",
        help="Path to a directory where CF files are to be found",
        dest="input_dir",
        type=str
        )
    args = parser.parse_args()

    # Invoke.
    try:
        for fpath in cdf2cim.scan(args.input_dir):
            cdf2cim.log("Scanned file: {}".format(fpath))
    except Exception as err:
        cdf2cim.log_error('Scan error: {}'.format(err))
        sys.exit(1)
    else:
        cdf2cim.log('Scan succeeded')
        sys.exit(0)


def publish():
    """Publishes to remote ES-DOC cdf2cim web-service.

    :returns: 2 member tuple: successes, failures
    :rtype: tuple

    """
    try:
        successes, failures = cdf2cim.publish()
    except Exception as err:
        cdf2cim.log_error('Publication error: {}'.format(err))
        sys.exit(1)
    else:
        for fpath, err in failures:
            cdf2cim.log_warning("Publication error: {} :: {}".format(fpath, err))
        for fpath in successes:
            cdf2cim.log("Published file: {}".format(fpath))
        sys.exit(0)
