# -*- coding: utf-8 -*-

"""
.. module:: reducer.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Reduces CF files to information used to create CIM documents.

.. moduleauthor:: David Hassell <david.hassell@ncas.ac.uk>


"""
import collections

from cdf2cim import parser



def execute(targets):
    """Returns simulation information dervied from a set of CF files.

    :param list targets: File and/or directory pointers to NetCDF files, e.g. ['IPSL/IPSL-CM5B-LR'].

	:returns: 2 member tuple - map of simulation identifiers to dict,
							   map of simulation identifiers to list of dates
	:rtype: tuple

    """
    # Map of simulation identifiers to a list of dictionaries
    # (each of which describes a single file of the simulation).
    simulations = collections.defaultdict(list)

    # Map of simulation identifiers to a list of date-time objects which
    # collectively define the time span of the simulation.
    simulation_dates = collections.defaultdict(list)

    # ----------------------------------------------------------------
    # Split the input files into groups so that all of the files in
    # a group belong to the same simulation
    # ----------------------------------------------------------------
    # For each CF field in this input file ...
    for _, identifier, cim2_properties, dates in parser.yield_parsed(targets):
        cim2_properties.pop(None, None)
    	simulation_dates[identifier].extend(dates)
        simulations[identifier].append(cim2_properties)

    return simulations, simulation_dates
