# -*- coding: utf-8 -*-

"""
.. module:: test_io_yield_cf_files.py

   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes CF file yielder unit tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import inspect
import os

import cf

import cdf2cim



# Pointers to various test data.
_TEST_DATA = os.path.join(os.path.dirname(__file__), "test-data")
_DIR = os.path.join(_TEST_DATA, 'cmip5')
_DIRS = [os.path.join(_TEST_DATA, 'cmip5'), os.path.join(_TEST_DATA, 'cmip6')]
_FILE = os.path.join(_DIR, 'tas_2005.nc')
_FILES = [os.path.join(_DIR, i) for i in os.listdir(_DIR)]



def test_is_function():
    """ES-DOC :: cdf2cim :: yield_cf_files :: cdf2cim supports target function

    """
    assert inspect.isfunction(cdf2cim.io.yield_cf_files)


def test_single_file():
    """ES-DOC :: cdf2cim :: yield_cf_files :: criteria = a single file.

    """
    _assert_cf_files(_FILE, 1)


def test_multiple_files():
    """ES-DOC :: cdf2cim :: yield_cf_files :: criteria = multiple files.

    """
    _assert_cf_files(_FILES, 6)


def test_single_directory():
    """ES-DOC :: cdf2cim :: yield_cf_files :: criteria = a single directory.

    """
    _assert_cf_files(_DIR, 6)


def test_multiple_directories():
    """ES-DOC :: cdf2cim :: yield_cf_files :: criteria = multiple directories.

    """
    _assert_cf_files(_DIRS, 6)


def test_mixed_criteria():
    """ES-DOC :: cdf2cim :: yield_cf_files :: criteria = single file, single directory.

    """
    _assert_cf_files([_FILE, _DIR], 6)


def _assert_cf_files(criteria, expected_length):
    """Asserts a collection of CF files.

    """
    total = 0
    for item in cdf2cim.io.yield_cf_files(criteria):
        _assert_cf_file(item)
        total += 1
    assert total == expected_length


def _assert_cf_file(cf_file):
    """Asserts a single CF file.

    """
    assert isinstance(cf_file, cf.Field)
