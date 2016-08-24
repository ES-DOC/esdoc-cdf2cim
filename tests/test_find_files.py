# -*- coding: utf-8 -*-

"""
.. module:: test_find_files.py

   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes find_files unit tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import inspect
import os
import uuid

import cdf2cim



# Pointers to various test data.
_TEST_DATA = os.path.join(os.path.dirname(__file__), "test-data")
_TEST_DIR = os.path.join(_TEST_DATA, 'cmip5')
_TEST_DIRS = [_TEST_DIR, os.path.join(_TEST_DATA, 'cmip6')]
_TEST_FILE = os.path.join(_TEST_DIR, 'tas_2005.nc')
_TEST_FILES = [os.path.join(_TEST_DIR, i) for i in os.listdir(_TEST_DIR)]



def test_is_function():
    """ES-DOC :: cdf2cim :: find_files :: postive Test :: cdf2cim supports find_files function

    """
    assert inspect.isfunction(cdf2cim.find_files)


def test_invalid_criteria():
    """ES-DOC :: cdf2cim :: find_files :: negative Test :: criteria = invalid

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
            cdf2cim.find_files(criteria)
        except cdf2cim.exceptions.InvalidFileSearchCriteria:
            try:
                cdf2cim.find_files([criteria])
            except cdf2cim.exceptions.InvalidFileSearchCriteria:
                pass


def test_single_file():
    """ES-DOC :: cdf2cim :: find_files :: positive Test :: criteria = a single file.

    """
    assert cdf2cim.find_files(_TEST_FILE) == set([_TEST_FILE])


def test_multiple_files():
    """ES-DOC :: cdf2cim :: find_files :: positive Test :: criteria = multiple files.

    """
    assert cdf2cim.find_files(_TEST_FILES) == set(_TEST_FILES)


def test_single_directory():
    """ES-DOC :: cdf2cim :: find_files :: positive Test :: criteria = a single directory.

    """
    assert cdf2cim.find_files(_TEST_DIR) == set(_TEST_FILES)


def test_multiple_directories():
    """ES-DOC :: cdf2cim :: find_files :: positive Test :: criteria = multiple directories.

    """
    assert cdf2cim.find_files(_TEST_DIRS).intersection(set(_TEST_FILES)) == set(_TEST_FILES)


def test_mixed_criteria():
    """ES-DOC :: cdf2cim :: find_files :: positive Test :: criteria = single file, single directory.

    """
    assert cdf2cim.find_files([_TEST_FILE, _TEST_DIR]) == set(_TEST_FILES)

