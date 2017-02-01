# -*- coding: utf-8 -*-

"""
.. module:: test_io_yield_simulation_info.py

   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes simulation yielder unit tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import inspect
import os

import cf
import numpy

import cdf2cim
from utils import *



def test_is_function():
    """ES-DOC :: cdf2cim :: yield_simulation_info :: cdf2cim supports target function

    """
    assert inspect.isfunction(cdf2cim.parser.yield_parsed)


def test_cmip5_single_file():
    """ES-DOC :: cdf2cim :: yield_simulation_info :: cmip5 :: criteria = a single file.

    """
    _assert_simulations(CMIP5_NETCDF_FILE, 1)


def test_cmip5_multiple_files():
    """ES-DOC :: cdf2cim :: yield_simulation_info :: cmip5 :: criteria = multiple files.

    """
    _assert_simulations(CMIP5_NETCDF_FILES, CMIP5_NETCDF_FILE_COUNT)


def test_cmip5_single_directory():
    """ES-DOC :: cdf2cim :: yield_simulation_info :: cmip5 :: criteria = a single directory.

    """
    _assert_simulations(CMIP5_NETCDF_DIR, CMIP5_NETCDF_FILE_COUNT)


def test_cmip6_single_file():
    """ES-DOC :: cdf2cim :: yield_simulation_info :: cmip6 :: criteria = a single file.

    """
    _assert_simulations(CMIP6_NETCDF_FILE, 1)


def test_cmip6_multiple_files():
    """ES-DOC :: cdf2cim :: yield_simulation_info :: cmip6 :: criteria = multiple files.

    """
    _assert_simulations(CMIP6_NETCDF_FILES, CMIP6_NETCDF_FILE_COUNT)


def test_cmip6_single_directory():
    """ES-DOC :: cdf2cim :: yield_simulation_info :: cmip6 :: criteria = a single directory.

    """
    _assert_simulations(CMIP6_NETCDF_DIR, CMIP6_NETCDF_FILE_COUNT)


def test_multiple_directories():
    """ES-DOC :: cdf2cim :: yield_simulation_info :: criteria = multiple directories.

    """
    _assert_simulations(ALL_NETCDF_DIRS, ALL_NETCDF_FILE_COUNT)


def test_mixed_criteria():
    """ES-DOC :: cdf2cim :: yield_simulation_info :: criteria = single file, single directory.

    """
    _assert_simulations(
        [CMIP5_NETCDF_FILE, CMIP6_NETCDF_DIR],
        CMIP6_NETCDF_FILE_COUNT + 1
        )


def _assert_simulations(criteria, expected_length):
    """Asserts a collection of simulations.

    """
    total = 0
    for item in cdf2cim.parser.yield_parsed(criteria):
        _assert_simulation(item)
        total += 1
    assert total == expected_length


def _assert_simulation(simulation):
    """Asserts a single simulation.

    """
    assert isinstance(simulation, tuple)
    assert len(simulation) == 4
    cf_file, identifier, properties, dates = simulation
    assert isinstance(cf_file, cf.Field)
    assert isinstance(identifier, tuple)
    assert isinstance(properties, dict)
    assert isinstance(dates, numpy.flatiter)
