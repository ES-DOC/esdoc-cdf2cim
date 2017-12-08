# -*- coding: utf-8 -*-

"""
.. module:: hashifier.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encpasulates hashing of cdf2cim entities.

.. moduleauthor:: David Hassell <david.hassell@ncas.ac.uk>


"""
import json
import hashlib



def hashify(metadata):
	"""Returns hashes dervied from a cdf2cim metadata blob.

    :param dict metadata: Simulation metadata.

	"""
	hash_id = hashlib.md5(json.dumps(metadata)).hexdigest()
	hash_id = "{}{}{}".format(hash_id, metadata['start_time'], metadata['end_time'])
	hash_id = hashlib.md5(hash_id).hexdigest()

	return hash_id
