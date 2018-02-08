# -*- coding: utf-8 -*-
#
#             8  d'b .oPYo.         o
#             8  8       `8
# .oPYo. .oPYo8 o8P     oP' .oPYo. o8 ooYoYo.
# 8    ' 8    8  8   .oP'   8    '  8 8' 8  8
# 8    . 8    8  8   8'     8    .  8 8  8  8
# `YooP' `YooP'  8   8ooooo `YooP'  8 8  8  8
# :.....::.....::..::.......:.....::....:..:..
# ::::::::::::::::::::::::::::::::::::::::::::
#
"""
.. module:: cdf2cim.__init__.py

   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Package initializer.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
__author__ = "David Hassell, Mark A. Greenslade"
__copyright__ = "Copyright 2018 ES-DOC"
__date__ = "2016-07-25"
__license__ = "GPL/CeCILL-2.1"
__title__ = "cdf2cim"
__version__ = "0.2.1.1"



from cdf2cim.constants import IO_DIR
from cdf2cim.io_manager import dump as _dump
from cdf2cim.io_manager import move_scanned_to_published
from cdf2cim.io_manager import yield_scanned_files
from cdf2cim.logger import log
from cdf2cim.logger import log_warning
from cdf2cim.logger import log_error
from cdf2cim.mapper import execute as _map
from cdf2cim.reducer import execute as _reduce
from cdf2cim.publisher import execute as _publish
from cdf2cim.publisher import verify_credentials




def find(inputs):
    """Returns simulation metadata extracted from a scan of netCDF files.

    :param list inputs: File and/or directory pointers to netCDF files, e.g. ['IPSL/IPSL-CM5B-LR'].

    :returns: A generator yielding simulation metadata.
    :rtype: generator

    """
    # Reduce inputs.
    simulations, simulation_dates = _reduce(inputs)

    # Yield mapped outputs.
    for identifier, properties in simulations.iteritems():
        yield _map(identifier, properties, simulation_dates[identifier])


def scan(inputs, overwrite=False):
    """Scan NetCDF files and cdf2cim specific metadata to file-system.

    :param list inputs: File and/or directory pointers to NetCDF files, e.g. ['IPSL/IPSL-CM5B-LR'].
    :param bool overwrite: If True then overwrite an existing file.

    :returns: Tuple of scanned cdf2cim files written to file system.
    :rtype: tuple

    """
    return tuple(i for i in [_dump(j, overwrite) for j in find(inputs)] if i is not None)


def publish():
    """Publishes to remote ES-DOC cdf2cim web-service.

    :returns: 2 member tuple: successes, failures
    :rtype: tuple

    """
    successes = []
    failures = []
    for i in yield_scanned_files():
        try:
            _publish(i)
        except Exception as err:
            failures.append((i, err))
        else:
            successes.append(move_scanned_to_published(i))

    return tuple(successes), tuple(failures)

