# -*- coding: utf-8 -*-

"""
.. module:: mapper.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps parsed CF file info to a dictionary that will subsequently be transformed to CIM documents.

.. moduleauthor:: David Hassell <david.hassell@ncas.ac.uk>


"""
import cf



def execute(identifier, properties, dates):
    """Reduces mapped simulation.

    """
    cim2_properties = properties[0].copy()

    # Find the start and end dates of the whole simulation
    start_date, end_date = _get_simulation_start_end_dates(dates, cim2_properties['calendar'])
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

    # Include all items from extra2 from all files, omitting
    # duplicates, as a string
    extra2 = {
        'contact'   : [],
        'references': [],
    }

    for p in properties:
        for x, v in extra2.iteritems():
            v.append(p.get(x))

    for prop, v in extra2.iteritems():
        v = set(v)
        v.discard(None)
        if v:
            cim2_properties[prop] = ', '.join(sorted(v))

    # Include all items from extra3 from all files, omitting
    # duplicates, as a list
    extra3 = {
        'dataset_versions': [],
        'filenames'       : [],
    }

    for p in properties:
        for x, v in extra3.iteritems():
            v.append(p.get(x))

    for prop, v in extra3.iteritems():
        v = set(v)
        v.discard(None)
        if v:
            cim2_properties[prop] = tuple(sorted(v))

    # ------------------------------------------------------------
    # The cim2_properties dictionary now contains everything
    # needed to create CIM2 Enemble, Ensemble Member and
    # Simulation documents. So add it to the output list.
    # ------------------------------------------------------------
    return cim2_properties


def _get_simulation_start_end_dates(dates, calendar):
    """Returns the start and end times of the simulation and return them as ISO8601-like strings.

    """
    if dates:
        date = sorted(set(dates))
        units = cf.Units('days since '+str(dates[0]), calendar)
        dates = cf.Data(dates, units, dt=True)
        return str(dates.min().dtarray[0]), str(dates.max().dtarray[0])

    return (None, None)
