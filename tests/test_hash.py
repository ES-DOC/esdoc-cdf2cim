# -*- coding: utf-8 -*-

"""
.. module:: test_hash.py

   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes hashifier unit tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import inspect
import json
import os
import tempfile

import cf

import cdf2cim
from utils import *


def test_is_function():
    """ES-DOC :: cdf2cim :: hashifier :: cdf2cim.hashify function is supported.

    """
    assert inspect.isfunction(cdf2cim.hashifier.hashify)


def test_equal_hash_id():
    """ES-DOC :: cdf2cim :: scan

    """
    filename = os.path.join(CMIP6_NETCDF_DIR, 'tas_0.nc')
    tmpfile = tempfile.mkstemp('_test_hash.nc', dir=os.getcwd())[1]

    # Create a temporary file that has different, but non-hashable
    # properties
    f = cf.read(filename, verbose=1)[0]
    for attr in cdf2cim.constants.NON_HASH_FIELDS:
        f.set_property(attr, 'DIFFERENT VALUE '+tmpfile)

    cf.write(f, tmpfile)

    blob = set()
    for f in (filename, tmpfile):
        for x in cdf2cim.scan(f):
            try:
                blob.add(x[0])
            except IndexError:
                pass
            else:
                break

    os.remove(tmpfile)

    # Test that both files produced the same blob, and therefore have
    # the same hash
    assert len(blob) == 1
