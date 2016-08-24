# -*- coding: utf-8 -*-

"""
.. module:: find_simulations.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encpasulates scanning a directory of CDF files and emitting simulation level metadata.

.. moduleauthor:: David Hassel <david.hassell@ncas.ac.uk>


"""
import re

import cf

from cdf2cim.constants  import CMIP5_TO_CIM2
from cdf2cim.constants  import CMIP6_TO_CIM2
from cdf2cim.constants  import CMIP5_ID
from cdf2cim.constants  import CMIP6_ID
from cdf2cim.find_files import find_files



def find_simulations(inputs, verbose=False):
    """Converts a set of NetCDF files to dictoinaries representing simulation level metadata.

    :param list inputs: Pointers to NetCDF files, e.g. ['IPSL/IPSL-CM5B-LR'].
    :param bool verbose: Flag indicating whether logging is verbose or not.

    :returns: A list of dictionaries representing simulation level metadata.
    :rtype: list"

    """
    # ----------------------------------------------------------------
    # Initialise variables
    # ----------------------------------------------------------------
    # List of dictionaries, one per simulation. Each dictionary's
    # key/value pairs fully define a simulation. This list is returned.
    out = []

    # Dictionary of simulations: key = a unique simulation identifier,
    # value = a list of dictionaries, each of which describes a single
    # file of the simulation
    simulations = {}

    # Dictionary of simulation dates: key = a unique simulation
    # identifier, value = a list of date-time objects which
    # collectively define the time span of the simulation.
    simulation_dates = {}

    # ----------------------------------------------------------------
    # Get the input files
    # ----------------------------------------------------------------
    input_files = find_files(inputs)
    if verbose:
        print 'Input files:\n', '\n'.join(sorted(input_files)), '\n'

    # ----------------------------------------------------------------
    # Split the input files into groups so that all of the files in
    # a group belong to the same simulation
    # ----------------------------------------------------------------
    for filename in input_files:

        # For each CF field in this input file ...
        for f in cf.read(filename, ignore_read_error=True, verbose=False, aggregate=False):

            # Get the time coordinates and find the earliest and
            # latest dates
            time_coords = f.dim('T')
            dates = _get_file_start_end_dates(time_coords)
            if not dates:
                # No valid dates were found, so ignore this file.
                continue

            # Get the netCDF global attributes
            global_attributes = f.properties

            # Find out which mip-era file we have
            mip_era = _get_mip_era(global_attributes)

            # Simply map file properties to CIM2 properties
            cim2_properties = {}

            # Parse properties which only require a simple mapping
            if mip_era == 'CMIP6':
                simple_mapping = CMIP6_TO_CIM2
            elif mip_era == 'CMIP5':
                simple_mapping = CMIP5_TO_CIM2

            for file_prop, cim2_prop in simple_mapping.iteritems():
                cim2_properties[cim2_prop] = global_attributes.get(file_prop)

            # Add the time coordinates' calendar to the cim2 properties
            cim2_properties['calendar'] = _get_calendar(time_coords)

            # Parse properties which require something more
            # complicated than a simple mapping
            if mip_era == 'CMIP6':
                _parse_cmip6_properties(cim2_properties, global_attributes, time_coords)
            elif mip_era == 'CMIP5':
                _parse_cmip5_properties(cim2_properties, global_attributes, time_coords)

            # Create a canonical identity for the simulation that this
            # field belongs to
            identity = _get_simulation_id(cim2_properties)
            if not identity:
                # No identity was found - ignore this field
                continue

            simulation_dates.setdefault(identity, []).extend(dates)

            cim2_properties.pop(None, None)
            simulations.setdefault(identity, []).append(cim2_properties)
        #--- End: for

        # Close a file to prevent a proliferation of open file handles
        cf.close_one_file()
    #--- End: for

    # ----------------------------------------------------------------
    # For each simulation, set some simulation properties which can
    # only be known when of all the contributing files have been
    # identified.
    # ----------------------------------------------------------------
    for identity, properties in simulations.iteritems():

        cim2_properties = properties[0].copy()

        # Find the start and end dates of the whole simulation
        start_date, end_date = _get_simulation_start_end_dates(simulation_dates.get(identity))
        if start_date:
            cim2_properties['start_time'] = start_date
            cim2_properties['end_time']   = end_date

        # Include items from extra1 only if all files have the same value
        extra1 = {
            'institution_id': [],
            'experiment_id' : [],
            'forcing'       : [],
            'variant_info'  : [],
        }

        for p in properties:
            for x, v in extra1.iteritems():
                v.append(p.get(x))

        for prop, v in extra1.iteritems():
            v = set(v)
            v.discard(None)
            if len(v) == 1:
                cim2_properties[prop] = v.pop()

        # Include all items from extra2 from all files, omitting duplicates.
        extra2 = {
            'contact'    : [],
            'references' : [],
        }

        for p in properties:
            for x, v in extra2.iteritems():
                v.append(p.get(x))

        for prop, v in extra2.iteritems():
            v = set(v)
            v.discard(None)
            if v:
                cim2_properties[prop] = ', '.join(sorted(v))

        # ------------------------------------------------------------
        # The cim2_properties dictionary now contains everything
        # needed to create CIM2 Enemble, Ensemble Member and
        # Simulation documents. So add it to the output list.
        # ------------------------------------------------------------
        out.append(cim2_properties)
    #--- End: for

    if verbose:
        print 'Simulations:\n',
        for x in out:
            print x.keys(), '\n'
            print x, '\n'

    return out
#--- End: def


def _get_simulation_id(cim2_properties):
    """Returns a canonical simulation identifier.

    """
    return tuple([(k, v) for k, v in cim2_properties.iteritems()
                  if k not in ('contact',
                               'references',
                               'forcing',
                               'variant_info')
              ])


def _get_simulation_start_end_dates(dates):
    """Returns the start and end times of the simulation and return them as ISO8601-like strings.

    """
    if dates:
        dates = cf.Data(list(set(dates)), dt=True).asreftime()
        return str(dates.min().dtarray[0]), str(dates.max().dtarray[0])

    return (None, None)


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


def _parse_cmip5_properties(cim2_properties, global_attributes, time_coords):
    """Extends cim2 proeprty set with CMIP5 specific properties.


    """
    cim2_properties.update(
        zip(['parent_realization_index',
             'parent_initialization_index',
             'parent_physics_index',
             'parent_forcing_index'],
            map(int, re.findall('\d+', global_attributes.get('parent_experiment_rip', 'none')))))


def _get_mip_era(global_attributes):
    """Returns mip era associated with a file.

    """
    if global_attributes.get('mip_era') == 'CMIP6':
        return 'CMIP6'
    elif global_attributes.get('project_id') == 'CMIP5':
        return 'CMIP5'


def _get_calendar(time_coords):
    """Returns calendar type from time co-ordinates (defaults to gregorian).

    """
    return getattr(time_coords, 'calendar', 'gregorian')
