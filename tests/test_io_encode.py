# -*- coding: utf-8 -*-

"""
.. module:: test_io_encode.py

   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes encoding related unit tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import json
import os

import pytest

import cdf2cim
from utils import *



# Test criteria.
_NETCDF_DIR = os.path.join(os.path.dirname(__file__), "test-data")


def test_encode():
    """ES-DOC :: cdf2cim :: io :: encode to JSON safe dictionary.

    """
    for obj in cdf2cim.find(NETCDF_DIR):
        assert isinstance(cdf2cim.io_manager.encode(obj), dict)


def test_json_conversion_failure():
    """ES-DOC :: cdf2cim :: io :: raw dictionary is not JSON encodeable.

    """
    with pytest.raises(TypeError):
        for obj in cdf2cim.find(NETCDF_DIR):
            json.dumps(obj)


def test_convert_to_json():
    """ES-DOC :: cdf2cim :: io :: encoded output is JSON encodeable.

    """
    for obj in cdf2cim.find(NETCDF_DIR):
        assert json.dumps(cdf2cim.io_manager.encode(obj))
