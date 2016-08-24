# -*- coding: utf-8 -*-

"""
.. module:: test_io.py

   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes I/O unit tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import json
import os

import nose

import cdf2cim



# Test criteria.
_CRITERIA = os.path.join(os.path.dirname(__file__), "test-data")



def test_encode():
    """ES-DOC :: cdf2cim :: io :: positive test :: encode to JSON safe dictionary.

    """
    for obj in cdf2cim.find_simulations(_CRITERIA):
    	assert isinstance(cdf2cim.io.encode(obj), dict)


@nose.tools.raises(TypeError)
def test_json_conversion_failure():
    """ES-DOC :: cdf2cim :: io :: negative test :: convert encoded to JSON.

    """
    for obj in cdf2cim.find_simulations(_CRITERIA):
    	assert  json.dumps(obj)


def test_convert_to_json():
    """ES-DOC :: cdf2cim :: io :: positive test :: convert encoded to JSON.

    """
    for obj in cdf2cim.find_simulations(_CRITERIA):
    	assert  json.dumps(cdf2cim.io.encode(obj))
