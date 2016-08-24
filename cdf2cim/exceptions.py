# -*- coding: utf-8 -*-

"""
.. module:: exceptions.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Package exceptions.

.. moduleauthor:: David Hassel <david.hassell@ncas.ac.uk>


"""

class InvalidFileSearchCriteria(Exception):
    """Raised if NetCDF4 file search criteria are deemed invalid.

    """
    def __init__(self, criteria):
        """Instance constructor.

        """
        super(InvalidFileSearchCriteria, self).__init__(
            "NETCDF FILE SEARCH CRITERIA ARE INVALID :: {}".format(criteria)
            )
