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



# Pointers to various test data.
_TEST_DATA = os.path.join(os.path.dirname(__file__), "test-data")
_DIR = os.path.join(_TEST_DATA, 'cmip5')
_DIRS = [os.path.join(_TEST_DATA, 'cmip5'), os.path.join(_TEST_DATA, 'cmip6')]
_FILE = os.path.join(_DIR, 'tas_2005.nc')
_FILES = [os.path.join(_DIR, i) for i in os.listdir(_DIR)]
_ALL_FILES = _FILES + [os.path.join(os.path.join(_TEST_DATA, 'cmip6'), i)
                       for i in os.listdir(os.path.join(_TEST_DATA, 'cmip6'))]



def test_is_function():
    """ES-DOC :: cdf2cim :: yield_files :: cdf2cim supports target function

    """
    assert inspect.isfunction(cdf2cim.io.yield_files)


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
            os.path.join(_TEST_DATA, 'xxx')
        }:
        try:
            cdf2cim.io.yield_files(criteria)
        except cdf2cim.exceptions.InvalidFileSearchCriteria:
            try:
                cdf2cim.io.yield_files([criteria])
            except cdf2cim.exceptions.InvalidFileSearchCriteria:
                pass


def test_single_file():
    """ES-DOC :: cdf2cim :: yield_files :: criteria = a single file.

    """
    _assert_files(_FILE, [_FILE])


def test_multiple_files():
    """ES-DOC :: cdf2cim :: yield_files :: criteria = multiple files.

    """
    _assert_files(_FILES, _FILES)


def test_single_directory():
    """ES-DOC :: cdf2cim :: yield_files :: criteria = a single directory.

    """
    _assert_files(_DIR, _FILES)


def test_multiple_directories():
    """ES-DOC :: cdf2cim :: yield_files :: criteria = multiple directories.

    """
    _assert_files(_DIRS, _ALL_FILES)


def test_mixed_criteria():
    """ES-DOC :: cdf2cim :: yield_files :: criteria = single file, single directory.

    """
    _assert_files([_FILE, _DIR], _FILES)


def _assert_files(criteria, expected):
    """Asserts a collection of CF files.

    """
    actual = set()
    for item in cdf2cim.io.yield_files(criteria):
        _assert_file(item)
        actual.add(item)
    assert actual == set(expected)


def _assert_file(fpath):
    """Asserts a single CF file.

    """
    assert os.path.isfile(fpath)
