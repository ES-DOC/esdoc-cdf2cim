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
    metadata_as_text = json.dumps(metadata)
    hash_id = hashlib.md5(metadata_as_text.encode('utf-8')).hexdigest()
    hash_id = f"{hash_id}{metadata['start_time']}{metadata['end_time']}"
    hash_id = hashlib.md5(hash_id.encode('utf-8')).hexdigest()

    return hash_id
