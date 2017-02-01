# -*- coding: utf-8 -*-

"""
.. module:: test_io_yield_files.py

   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes file yielding unit tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import inspect
import os
import uuid

import cdf2cim
from utils import *



def test_is_function():
    """ES-DOC :: cdf2cim :: yield_files :: cdf2cim supports target function

    """
    assert inspect.isfunction(cdf2cim.file_io.yield_files)


def test_invalid_criteria():
    """ES-DOC :: cdf2cim :: yield_files :: criteria = invalid

    """
    for criteria in {
            None,
            True,
            123,
            uuid.uuid4,
            uuid.uuid4(),
            unicode(uuid.uuid4()),
            os.path.join(NETCDF_DIR, 'xxx')
        }:
        try:
            cdf2cim.file_io.yield_files(criteria)
        except cdf2cim.exceptions.InvalidFileSearchCriteria:
            try:
                cdf2cim.file_io.yield_files([criteria])
            except cdf2cim.exceptions.InvalidFileSearchCriteria:
                pass


def test_cmip5_single_file():
    """ES-DOC :: cdf2cim :: yield_files :: cmip5 :: criteria = a single file.

    """
    _assert_files(CMIP5_NETCDF_FILE, [CMIP5_NETCDF_FILE])


def test_cmip5_multiple_files():
    """ES-DOC :: cdf2cim :: yield_files :: cmip5 :: criteria = multiple files.

    """
    _assert_files(CMIP5_NETCDF_FILES, CMIP5_NETCDF_FILES)


def test_cmip5_single_directory():
    """ES-DOC :: cdf2cim :: yield_files :: cmip5 :: criteria = a single directory.

    """
    _assert_files(CMIP5_NETCDF_DIR, CMIP5_NETCDF_FILES)


def test_cmip6_single_file():
    """ES-DOC :: cdf2cim :: yield_files :: cmip6 :: criteria = a single file.

    """
    _assert_files(CMIP6_NETCDF_FILE, [CMIP6_NETCDF_FILE])


def test_cmip6_multiple_files():
    """ES-DOC :: cdf2cim :: yield_files :: cmip6 :: criteria = multiple files.

    """
    _assert_files(CMIP6_NETCDF_FILES, CMIP6_NETCDF_FILES)


def test_cmip6_single_directory():
    """ES-DOC :: cdf2cim :: yield_files :: cmip6 :: criteria = a single directory.

    """
    _assert_files(CMIP6_NETCDF_DIR, CMIP6_NETCDF_FILES)


def test_multiple_directories():
    """ES-DOC :: cdf2cim :: yield_files :: criteria = multiple directories.

    """
    _assert_files(ALL_NETCDF_DIRS, ALL_NETCDF_FILES)


def test_mixed_criteria():
    """ES-DOC :: cdf2cim :: yield_files :: criteria = single file, single directory.

    """
    _assert_files(
        [CMIP5_NETCDF_FILE, CMIP6_NETCDF_DIR],
        [CMIP5_NETCDF_FILE] + CMIP6_NETCDF_FILES
        )


def _assert_files(criteria, expected):
    """Asserts a collection of CF files.

    """
    actual = set()
    for item in cdf2cim.file_io.yield_files(criteria):
        _assert_file(item)
        actual.add(item)
    assert actual == set(expected)


def _assert_file(fpath):
    """Asserts a single CF file.

    """
    assert os.path.isfile(fpath)
