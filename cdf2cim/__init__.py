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
__version__ = "0.1.2.0"


from cdf2cim.mapper import execute as _map
from cdf2cim.reducer import execute as _reduce



def find_simulations(targets):
    """Converts a set of NetCDF files to dictionaries representing simulation level metadata.

    :param list targets: File and/or directory pointers to NetCDF files, e.g. ['IPSL/IPSL-CM5B-LR'].

    :returns: A generator yielding simulation level metadata.
    :rtype: generator

    """
    # Perform reduce.
    simulations, simulation_dates = _reduce(targets)

    # Yield mapped.
    for identifier, properties in simulations.iteritems():
        yield _map(identifier, properties, simulation_dates[identifier])
