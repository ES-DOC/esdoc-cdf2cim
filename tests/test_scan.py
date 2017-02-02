# -*- coding: utf-8 -*-

"""
.. module:: test_write.py

   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes write simulations unit tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import inspect
import os

import cdf2cim
from utils import *



def test_is_function():
    """ES-DOC :: cdf2cim :: write :: test cdf2cim supports scan function.

    """
    assert inspect.isfunction(cdf2cim.scan)


def test_scan_cmip5():
    """ES-DOC :: cdf2cim :: scan :: cmip5.

    """
    _assert_scan(CMIP5_NETCDF_DIR, 2)


def test_scan_cmip6():
    """ES-DOC :: cdf2cim :: scan :: cmip6.

    """
    _assert_scan(CMIP6_NETCDF_DIR, 1)


def _assert_scan(dpath, expected_count):
    """Asserts scan inpits/outputs.

    """
    assert os.path.isdir(dpath)
    outputs = cdf2cim.scan(dpath)
    assert len(outputs) == expected_count
    for fpath in outputs:
        assert os.path.isfile(fpath)

