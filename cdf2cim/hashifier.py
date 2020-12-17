"""
.. module:: hashifier.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encpasulates hashing of cdf2cim entities.

.. moduleauthor:: David Hassell <david.hassell@ncas.ac.uk>


"""
import collections
import json
import hashlib

from cdf2cim.constants import NON_HASH_FIELDS


def hashify(metadata: collections.OrderedDict) -> str:
    """Returns hashes derived from a cdf2cim metadata blob.

    :param dict metadata: Simulation metadata.

    """
	target = metadata.copy()
	for field in _NON_HASH_FIELDS:
		target.pop(field, None)

    return hashlib.md5(json.dumps(target).encode('utf-8')).hexdigest()
