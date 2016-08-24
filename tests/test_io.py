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

import cdf2cim


# Test criteria.
_CRITERIA = os.path.join(os.path.dirname(__file__), "test-data")




def test_encode():
    """ES-DOC :: cdf2cim :: io :: positive Test :: encode to JSON safe dictionary.

    """
    for obj in cdf2cim.find_simulations(_CRITERIA):
    	encoded = cdf2cim.io.encode(obj)
    	assert isinstance(encoded, dict)
    	assert json.dumps(encoded)
