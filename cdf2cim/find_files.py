# -*- coding: utf-8 -*-

"""
.. module:: find_files.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encpasulates determining which NetCDF files are considered within scope.

.. moduleauthor:: David Hassel <david.hassell@ncas.ac.uk>


"""
import collections
import os

from cdf2cim import exceptions



def find_files(criteria):
    """Return all NetCDF files implied by the criteria.

    :param str|sequence criteria: Pointer(s) to file(s) and/or directorie(s). Directories (including symbolic links) are searched recursively.

    :returns: A set of file paths.
    :rtype: set

    :raises exceptions.InvalidFileSearchCriteria: if search criteria are invalid

    """
    # Convert to sequence (if necessary).
    if isinstance(criteria, basestring):
        criteria = [criteria]

    # Exception if passed invalid pointers.
    if not isinstance(criteria, collections.Iterable):
        raise exceptions.InvalidFileSearchCriteria(criteria)
    if [i for i in criteria if not isinstance(i, basestring)]:
        raise exceptions.InvalidFileSearchCriteria(criteria)
    if [i for i in criteria if not os.path.exists(i)]:
        raise exceptions.InvalidFileSearchCriteria(criteria)

    # Determine set of absolute file pointers.
    outfiles = []
    for target in criteria:
        if os.path.isfile(target):
            outfiles.append(os.path.abspath(target))
        elif os.path.isdir(target):
            outfiles.extend(
                os.path.abspath(os.path.join(folder, f))
                for folder, _, filenames in os.walk(target, followlinks=True)
                for f in filenames
            )

    return set(outfiles)
