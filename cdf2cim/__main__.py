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
_ARGS = argparse.ArgumentParser("ES-DOC netCDF to CIM publisher.")
_ARGS.add_argument(
    "-a", "--action",
    help="Action to be performed",
    choices=["publish", "write"],
    dest="action",
    default="publish",
    type=str
    )
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


def _publish(args):
    """Publishes cdf2cim files to web-service.

    """
    # Write to file system.
    _write(args)

    # Publish to web-service.
    cdf2cim.publish(args.input_dir, args.output_dir)


def _write(args):
    """Write cdf2cim files to file system.

    """
    cdf2cim.write(args.input_dir, args.output_dir)


# Map of actions to handlers.
_ACTIONS = {
    "publish":_publish,
    "write": _write
}

# Invoke action.
_ACTIONS[_ARGS.action](_ARGS)
