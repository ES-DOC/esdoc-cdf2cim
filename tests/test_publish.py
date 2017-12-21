import inspect
import json
import os

import cdf2cim
from utils import *



def test_is_function():
    """ES-DOC :: cdf2cim :: write :: test cdf2cim supports publish function.

    """
    assert inspect.isfunction(cdf2cim.publish)


def test_publish_cmip5():
    """ES-DOC :: cdf2cim :: scan :: cmip5.

    """
    _test_publish(CMIP5_NETCDF_DIR)


def test_publish_cmip6():
    """ES-DOC :: cdf2cim :: scan :: cmip6.

    """
    _test_publish(CMIP6_NETCDF_DIR)


def _test_publish(dpath):
    scanned = cdf2cim.scan(dpath, True)
    published, errors = cdf2cim.publish()
    assert len(published) == len(scanned)
    assert len(errors) == 0
