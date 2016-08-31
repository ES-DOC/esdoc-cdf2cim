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



# Pointers to various test data.
_TEST_DATA = os.path.join(os.path.dirname(__file__), "test-data")
_DIR = os.path.join(_TEST_DATA, 'cmip5')
_DIRS = [os.path.join(_TEST_DATA, 'cmip5'), os.path.join(_TEST_DATA, 'cmip6')]
_FILE = os.path.join(_DIR, 'tas_2005.nc')
_FILES = [os.path.join(_DIR, i) for i in os.listdir(_DIR)]


def test_is_function():
    """ES-DOC :: cdf2cim :: yield_simulation_info :: cdf2cim supports target function

    """
    assert inspect.isfunction(cdf2cim.cf_parser.yield_parsed)


def test_single_file():
    """ES-DOC :: cdf2cim :: yield_simulation_info :: criteria = a single file.

    """
    _assert_simulations(_FILE, 1)


def test_multiple_files():
    """ES-DOC :: cdf2cim :: yield_simulation_info :: criteria = multiple files.

    """
    _assert_simulations(_FILES, 6)


def test_single_directory():
    """ES-DOC :: cdf2cim :: yield_simulation_info :: criteria = a single directory.

    """
    _assert_simulations(_DIR, 6)


def test_multiple_directories():
    """ES-DOC :: cdf2cim :: yield_simulation_info :: criteria = multiple directories.

    """
    _assert_simulations(_DIRS, 6)


def test_mixed_criteria():
    """ES-DOC :: cdf2cim :: yield_simulation_info :: criteria = single file, single directory.

    """
    _assert_simulations([_FILE, _DIR], 6)


def _assert_simulations(criteria, expected_length):
    """Asserts a collection of simulations.

    """
    total = 0
    for item in cdf2cim.cf_parser.yield_parsed(criteria):
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
