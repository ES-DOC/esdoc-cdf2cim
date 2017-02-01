"""
.. module:: publish.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: cdf2cim cf file scanner entry point.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import argparse

import cdf2cim



# Define command line arguments.
_ARGS = argparse.ArgumentParser("ES-DOC netCDF scanner.")
_ARGS.add_argument(
    "-i", "--in-dir",
    help="Path to a directory where CF files are to be found",
    dest="input_dir",
    type=str
    )


def _main(args):
    """Write cdf2cim files to file system.

    """
    cdf2cim.scan(args.input_dir)


# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
