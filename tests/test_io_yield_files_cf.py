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
from utils import *



def test_is_function():
    """ES-DOC :: cdf2cim :: yield_cf_files :: cdf2cim supports target function

    """
    assert inspect.isfunction(cdf2cim.io_manager.yield_cf_files)


def test_cmip5_single_file():
    """ES-DOC :: cdf2cim :: yield_cf_files :: cmip5 :: criteria = a single file.

    """
    _assert_cf_files(CMIP5_NETCDF_FILE, 1)


def test_cmip5_multiple_files():
    """ES-DOC :: cdf2cim :: yield_cf_files :: cmip5 :: criteria = multiple files.

    """
    _assert_cf_files(CMIP5_NETCDF_FILES, CMIP5_NETCDF_FILE_COUNT)


def test_cmip5_single_directory():
    """ES-DOC :: cdf2cim :: yield_cf_files :: cmip5 :: criteria = a single directory.

    """
    _assert_cf_files(CMIP5_NETCDF_DIR, CMIP5_NETCDF_FILE_COUNT)


def test_cmip6_single_file():
    """ES-DOC :: cdf2cim :: yield_cf_files :: cmip6 :: criteria = a single file.

    """
    _assert_cf_files(CMIP6_NETCDF_FILE, 1)


def test_cmip6_multiple_files():
    """ES-DOC :: cdf2cim :: yield_cf_files :: cmip6 :: criteria = multiple files.

    """
    _assert_cf_files(CMIP6_NETCDF_FILES, CMIP6_NETCDF_FILE_COUNT)


def test_cmip6_single_directory():
    """ES-DOC :: cdf2cim :: yield_cf_files :: cmip6 :: criteria = a single directory.

    """
    _assert_cf_files(CMIP6_NETCDF_DIR, CMIP6_NETCDF_FILE_COUNT)


def test_multiple_directories():
    """ES-DOC :: cdf2cim :: yield_cf_files :: criteria = multiple directories.

    """
    _assert_cf_files(ALL_NETCDF_DIRS, ALL_NETCDF_FILE_COUNT)


def test_mixed_criteria():
    """ES-DOC :: cdf2cim :: yield_cf_files :: criteria = single file, single directory.

    """
    _assert_cf_files(
        [CMIP5_NETCDF_FILE, CMIP6_NETCDF_DIR],
        CMIP6_NETCDF_FILE_COUNT + 1
        )


def _assert_cf_files(criteria, expected_length):
    """Asserts a collection of CF files.

    """
    total = 0
    for item in cdf2cim.io_manager.yield_cf_files(criteria):
#        _assert_cf_file(item)
        _assert_list_of_cf_fields(item)
        total += 1
    assert total == expected_length


def _assert_list_of_cf_fields(cf_file):
    """Asserts a single CF file.

    """
    for f in cf_file:
        assert isinstance(f, cf.Field)

def _assert_cf_file(cf_file):
    """Asserts a single CF file.

    """
    assert isinstance(cf_file, cf.Field)
