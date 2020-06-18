import inspect
import json
import os
import shutil

import pytest

import cdf2cim
from cdf2cim.constants import IO_DIR
from cdf2cim.constants import IO_DIR_PUBLISHED
from cdf2cim.constants import IO_DIR_SCANNED
from utils import *




def setup_method():
    shutil.rmtree(IO_DIR)


def test_is_function():
    """ES-DOC :: cdf2cim :: publish :: cdf2cim.publish function is supported.

    """
    assert inspect.isfunction(cdf2cim.publish)


def test_publish_cmip5():
    """ES-DOC :: cdf2cim :: publish :: cmip5.

    """
    _test_publish(CMIP5_NETCDF_DIR)


def test_publish_cmip6():
    """ES-DOC :: cdf2cim :: publish :: cmip6.

    """
    _test_publish(CMIP6_NETCDF_DIR)


def _test_publish(dpath):
    """Inner test.

    """
    scanned, _, _ = cdf2cim.scan(dpath, True)
    published, published_errors = cdf2cim.publish()
    assert len(published_errors) == 0, published_errors
    print(published)
    print(scanned)
    assert len(published) == len(scanned)
    for fpath in scanned:
        assert fpath.replace(IO_DIR_SCANNED, IO_DIR_PUBLISHED) in published
