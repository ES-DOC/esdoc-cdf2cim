# -*- coding: utf-8 -*-

"""
.. module:: test_find.py

   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes find simulations unit tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import inspect
import os

import cdf2cim
from cdf2cim import constants



# Test criteria.
_CRITERIA = os.path.join(os.path.dirname(__file__), "test-data")

# Set of expected simulation attributes.
_ATTRIBUTES = sorted([
    'parent_initialization_index',
    'parent_experiment_id',
    'start_time',
    'parent_realization_index',
    'references',
    'mip_era',
    'physics_index',
    'calendar',
    'branch_time_in_parent',
    'institution_id',
    'initialization_index',
    'realization_index',
    'source',
    'contact',
    'end_time',
    'experiment_id',
    'source_id',
    'forcing',
    'parent_physics_index'
    ])


def test_is_function():
    """ES-DOC :: cdf2cim :: find :: cdf2cim supports find function

    """
    assert inspect.isfunction(cdf2cim.find)


def test_find():
    """ES-DOC :: cdf2cim :: find :: criteria = multiple files.

    """
    _assert_simulations(_CRITERIA, 1)


def _assert_simulations(criteria, expected_length):
    """Asserts a simulation item returned from find method.

    """
    total = 0
    for item in cdf2cim.find(criteria):
        _assert_simulation(item)
        total += 1
    assert total == expected_length


def _assert_simulation(obj):
    """Asserts a simulation item returned from find method.

    """
    assert isinstance(obj, dict)
    for key in _ATTRIBUTES:
        assert key in obj
    assert obj['mip_era'] in constants.MIP_ERA
    assert cdf2cim.io.encode(obj)
