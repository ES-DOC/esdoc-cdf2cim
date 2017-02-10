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
__copyright__ = "Copyright 2016 ES-DOC"
__date__ = "2016-07-25"
__license__ = "GPL/CeCILL-2.1"
__title__ = "cdf2cim"
__version__ = "0.1.5.0"

import glob

from cdf2cim.constants import IO_DIR
from cdf2cim.io_manager import dump as _dump
from cdf2cim.mapper import execute as _map
from cdf2cim.reducer import execute as _reduce
from cdf2cim.publisher import execute as _publish



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


def scan(inputs, name='md5', overwrite=True):
    """Scan NetCDF files and cdf2cim specific metadata to file-system.

    :param list inputs: File and/or directory pointers to NetCDF files, e.g. ['IPSL/IPSL-CM5B-LR'].
    :param str name: Style of output file name: 'md5' for md5 (not unique), 'uuid' for UUID (different every time)
    :param bool overwrite: If True then overwrite an existing file.

    :returns: Tuple of written cdf2cim formatted files.
    :rtype: tuple

    """
    return tuple(_dump(i, name, overwrite) for i in find(inputs))


def publish():
    """Publishes to remote ES-DOC cdf2cim web-service.

    :returns: List of publishing errors.
    :rtype: list

    """
    files = glob.iglob("{}/*.json".format(IO_DIR))

    return tuple(i for i in [(j, _publish(j)) for j in files] if i[1] is not None)
