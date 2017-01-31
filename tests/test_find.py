# -*- coding: utf-8 -*-

"""
.. module:: test_find.py

   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes find simulations unit tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import inspect

import cdf2cim
from cdf2cim import constants
from utils import *



def test_is_function():
    """ES-DOC :: cdf2cim :: find :: cdf2cim supports find function

    """
    assert inspect.isfunction(cdf2cim.find)


def test_find_cmip5():
    """ES-DOC :: cdf2cim :: find :: cmip5.

    """
    _assert_simulations(CMIP5_NETCDF_DIR, 2, SAMPLE_OUTPUT_CMIP5.keys())


def test_find_cmip6():
    """ES-DOC :: cdf2cim :: find :: cmip6.

    """
    _assert_simulations(CMIP6_NETCDF_DIR, 1, SAMPLE_OUTPUT_CMIP6.keys())


def _assert_simulations(criteria, expected_length, expected_fields):
    """Asserts a simulation item returned from find method.

    """
    total = 0
    for item in cdf2cim.find(criteria):
        _assert_simulation(item, expected_fields)
        total += 1
    assert total == expected_length, total


def _assert_simulation(obj, expected_fields):
    """Asserts a simulation item returned from find method.

    """
    assert isinstance(obj, dict)
    for key in expected_fields:
        assert key in obj
    assert obj['mip_era'] in constants.MIP_ERA
    assert cdf2cim.file_io.encode(obj)
