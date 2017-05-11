# -*- coding: utf-8 -*-

"""
.. module:: hashifier.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encpasulates hashing of cdf2cim entities.

.. moduleauthor:: David Hassel <david.hassell@ncas.ac.uk>


"""
import json
import hashlib



def hashify(metadata):
	"""Returns hashes dervied from a cdf2cim metadata blob.

    :param dict metadata: Simulation metadata.

	"""
	hash1 = hashlib.md5(json.dumps(metadata)).hexdigest()

	hash2 = "{}{}{}".format(hash1, metadata['start_time'], metadata['end_time'])
	hash2 = hashlib.md5(hash2).hexdigest()

	return hash1
