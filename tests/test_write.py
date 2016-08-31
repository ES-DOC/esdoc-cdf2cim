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
from cdf2cim import constants


# Test inputs.
_INPUTS = os.path.join(os.path.dirname(__file__), "test-data")

# Test output directory.
_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "test-output")



def test_is_function():
    """ES-DOC :: cdf2cim :: write :: test cdf2cim supports write function.

    """
    assert inspect.isfunction(cdf2cim.write)


def test_output_dir():
    """ES-DOC :: cdf2cim :: write :: test output directory exists.

    """
    assert os.path.exists(_OUTPUT_DIR)



def test_write():
    """ES-DOC :: cdf2cim :: write :: test writing output to file system.

    """
    for fpath in cdf2cim.write(_INPUTS, _OUTPUT_DIR):
        assert os.path.isfile(fpath)
