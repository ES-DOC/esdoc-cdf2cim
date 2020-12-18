"""
.. module:: encoder.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encodes cdf2cim data prior to I/O operation.

.. moduleauthor:: David Hassell <david.hassell@ncas.ac.uk>


"""
import collections

import numpy

from cdf2cim import hashifier
from cdf2cim.constants import NON_HASH_FIELDS



def encode(obj: dict) -> collections.OrderedDict:
    """Encodes output from map/reduce as a JSON safe dictionary.

    :param dict obj: Output from a map/reduce job.

    :returns: A JSON safe dictionary

    """
    def _encode(key, value):
        """Encodes a value.

        """
        if isinstance(value, numpy.float64):
            return float(value)
        if isinstance(value, numpy.int32):
            return int(value)
        if key.endswith("_index"):
            return int(value)
        return value

    result = collections.OrderedDict()
    for k in sorted(obj.keys()):
        result[k] = _encode(k, obj[k])

    return result
