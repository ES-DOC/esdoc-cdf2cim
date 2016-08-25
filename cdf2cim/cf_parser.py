# -*- coding: utf-8 -*-

"""
.. module:: parser.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encpasulates parsing a cf file.

.. moduleauthor:: David Hassel <david.hassell@ncas.ac.uk>


"""
import re

import cf

from cdf2cim import constants
from cdf2cim import io




def yield_parsed(targets):
    """Yields simulation information derived from a parse of cf files.

    :param str|sequence targets: Pointer(s) to file(s) and/or directorie(s).

    :returns:  Generator yielding simulation information derived from a parse of cf files.
    :rtype: generator

    """
    for cf_file in io.yield_cf_files(targets):
        identifier, properties, dates = parse(cf_file)
        if identifier:
            yield cf_file, identifier, properties, dates


def parse(cf_file):
    """Parses a CF file returning a simulation identifer, a set of CIM properties, & associated dates.

    :param cf.FieldList cf_file: A CF file to be mapped.

    :returns: A 3 member tuple - (simulation identifer, CIM properties, simulation dates).
    :rtype: tuple

    """
    # Get the time coordinates & earliest/latest dates.
    time_coords = cf_file.dim('T')
    dates = _get_file_start_end_dates(time_coords)
    if not dates:
        return None, None, None

    # Get the netCDF global attributes
    global_attributes = cf_file.properties

    # Find out which mip-era file we have
    mip_era = _get_mip_era(global_attributes)

    # Simply map file properties to CIM2 properties
    cim2_properties = {}

    # Parse properties which only require a simple mapping
    if mip_era == constants.CMIP6:
        simple_mapping = constants.CMIP6_TO_CIM2
    elif mip_era == constants.CMIP5:
        simple_mapping = constants.CMIP5_TO_CIM2

    for file_prop, cim2_prop in simple_mapping.iteritems():
        cim2_properties[cim2_prop] = global_attributes.get(file_prop)

    # Add the time coordinates' calendar to the cim2 properties
    cim2_properties['calendar'] = _get_calendar(time_coords)

    # Parse non-simple mappable properties.
    if mip_era == constants.CMIP6:
        _parse_cmip6_properties(cim2_properties, global_attributes, time_coords)
    elif mip_era == constants.CMIP5:
        _parse_cmip5_properties(cim2_properties, global_attributes, time_coords)

    return _get_simulation_id(cim2_properties), cim2_properties, dates


def _get_file_start_end_dates(time_coords):
    """Returns earliest and latest date-time objects from a time coordinate.

    """
    if time_coords is None or not time_coords.Units.isreftime or time_coords.ndim > 1:
        # No (suitable) time coordinates - ignore this field
        return []

    # Find the earliest and latest dates for this field
    if time_coords.size == 1:
        index = 0
    else:
        index = [0, -1]

    if time_coords.hasbounds:
        # Get the time span from the time coordinate bounds
        dates = time_coords.bounds.subspace[index].dtarray.flat
    else:
        # In the absence of bounds, get the time span from the
        # time coordinates
        dates = time_coords.subspace[index].dtarray

    return dates


def _get_calendar(time_coords):
    """Returns calendar type from time co-ordinates (defaults to gregorian).

    """
    return getattr(time_coords, 'calendar', 'gregorian')


def _parse_cmip5_properties(cim2_properties, global_attributes, time_coords):
    """Extends cim2 proeprty set with CMIP5 specific properties.


    """
    cim2_properties.update(
        zip(['parent_realization_index',
             'parent_initialization_index',
             'parent_physics_index',
             'parent_forcing_index'],
            map(int, re.findall('\d+', global_attributes.get('parent_experiment_rip', 'none')))))


def _parse_cmip6_properties(cim2_properties, global_attributes, time_coords):
    """Extends cim2 proeprty set with CMIP6 specific properties.


    """
    cim2_properties.update(
        zip(['parent_realization_index',
             'parent_initialization_index',
             'parent_physics_index',
             'parent_forcing_index'],
            map(int, re.findall('\d+', global_attributes.get('parent_variant_label', 'none')))))

    # parent_time_units
    parent_time_units = global_attributes.get('parent_time_units')
    if parent_time_units is None:
        # parent_time_units has not been set in file, so they are
        # assumed to be the same as the child time units
        parent_time_units = time_coords.Units
    else:
        # parent_time_units have been set in file
        m = re.match('(.*) *\((.*?)\)', parent_time_units)
        if m:
            parent_time_units = cf.Units(*m.groups())
        else:
            parent_time_units = cf.Units(parent_time_units,
                                         cim2_properties['calendar'])

    # ----------------------------------------------------------------
    # CIM2 branch_time_in_parent
    # ----------------------------------------------------------------
    branch_time_in_parent = global_attributes.get('branch_time_in_parent')
    if branch_time_in_parent is not None:
        x = cf.Data([branch_time_in_parent], units=parent_time_units).dtarray[0]
        cim2_properties['branch_time_in_parent'] = str(x)

    # ----------------------------------------------------------------
    # CIM2 branch_time_in_child
    # ----------------------------------------------------------------
    branch_time_in_child = global_attributes.get('branch_time_in_child')
    if branch_time_in_child is not None:
        x = cf.Data([branch_time_in_child], units=time_coords.Units).dtarray[0]
        cim2_properties['branch_time_in_child'] = str(x)


def _get_mip_era(global_attributes):
    """Returns mip era associated with a file.

    """
    if global_attributes.get('mip_era') == constants.CMIP6:
        return constants.CMIP6
    elif global_attributes.get('project_id') == constants.CMIP5:
        return constants.CMIP5


def _get_simulation_id(cim2_properties):
    """Returns a canonical simulation identifier.

    """
    return tuple([(k, v) for k, v in cim2_properties.iteritems()
                  if k not in ('contact',
                               'references',
                               'forcing',
                               'variant_info')
              ])
