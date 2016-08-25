"""
.. module:: cdf2cim.__main__.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: cdf2cim main entry point.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import argparse

import cdf2cim



# Define command line arguments.
_ARGS = argparse.ArgumentParser("ES-DOC NetCDF to CIM file manager.")
_ARGS.add_argument(
    "-i", "--in-dir",
    help="Path to a directory where CF files are to be found",
    dest="input_dir",
    type=str
    )
_ARGS.add_argument(
    "-o", "--out-dir",
    help="Path to a directory to which generated simulation metadata will be written",
    dest="output_dir",
    type=str
    )

# Set command line options.
_ARGS = _ARGS.parse_args()



cdf2cim.write(_ARGS.input_dir, _ARGS.output_dir)

