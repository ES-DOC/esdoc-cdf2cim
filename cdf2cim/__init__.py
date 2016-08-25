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
__version__ = "0.1.3.0"

from cdf2cim.io import dump as _dump
from cdf2cim.mapper import execute as _map
from cdf2cim.reducer import execute as _reduce



def find(inputs):
    """Returns simulation metadata extracted from a scan of NetCDF files.

    :param list inputs: File and/or directory pointers to NetCDF files, e.g. ['IPSL/IPSL-CM5B-LR'].

    :returns: A generator yielding simulation metadata.
    :rtype: generator

    """
    # Reduce inputs.
    simulations, simulation_dates = _reduce(inputs)

    # Yield mapped outputs.
    for identifier, properties in simulations.iteritems():
        yield _map(identifier, properties, simulation_dates[identifier])


def write(inputs, output_dir):
    """Writes to file-system simulation metadata extracted from NetCDF files.

    :param list inputs: File and/or directory pointers to NetCDF files, e.g. ['IPSL/IPSL-CM5B-LR'].
    :param str output_dir: Path to directory to which simulation metadata will be written.

    """
    for obj in find(inputs):
        yield _dump(output_dir, obj)
