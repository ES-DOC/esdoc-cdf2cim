# -*- coding: utf-8 -*-

"""
.. module:: io.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Enapsulates package IO operations.

.. moduleauthor:: David Hassel <david.hassell@ncas.ac.uk>


"""
import collections
import json
import os
import uuid

import cf
import numpy

from cdf2cim import exceptions
from cdf2cim import logger



def encode(obj):
    """Encodes an output from a map/reduce as a JSON safe dictionary.

    :param dict obj: Output from a map/reduce job.

    :returns: A JSON safe dictionary
    :rtype: dict

    """
    def _encode(value):
        """Encodes a value.

        """
        if isinstance(value, numpy.float64):
            return float(value)
        elif isinstance(value, numpy.int32):
            return int(value)
        else:
            return value

    result = collections.OrderedDict()
    for k in sorted(obj.keys()):
        result[k] = _encode(obj[k])

    return result


def yield_files(criteria):
    """Yields files implied by the criteria.

    :param str|sequence criteria: Pointer(s) to file(s) and/or directorie(s). Directories (including symbolic links) are searched recursively.

    :returns: Generator yielding files for processing.
    :rtype: generator

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

    # De-dupe criteria.
    criteria = set(criteria)
    for target in sorted(criteria):
        if os.path.dirname(target) in criteria:
            criteria.remove(target)

    # Determine set of absolute file pointers.
    for target in criteria:
        if os.path.isfile(target):
            yield os.path.abspath(target)
        elif os.path.isdir(target):
            for folder, _, fnames in os.walk(target, followlinks=True):
                for fname in fnames:
                    yield os.path.abspath(os.path.join(folder, fname))


def yield_cf_files(targets):
    """Yields CF files for further processing.

    :param str|sequence targets: Pointer(s) to file(s) and/or directorie(s).

    :returns:  Generator yielding CF files.
    :rtype: generator

    """
    for fpath in yield_files(targets):
        try:
#            print  fpath
            cf_file = cf.read(fpath, ignore_read_error=False, verbose=False, aggregate=False)
        except (IOError, OSError):
            logger.log_warning("Non NetCDF file rejected: {}".format(fpath))
        else:
            yield cf_file
            # ... close file to prevent a proliferation of open file handles
            cf.close_one_file()


def dump(output_dir, obj):
    """Writes simulation metadata to file system.

    :param str output_dir: Directory to which output will be written.
    :param dict obj: Simulation metadata.

    :returns: Path to written file.
    :rtype: str

    """
    fname = "{}.json".format(unicode(uuid.uuid4()))
    fpath = os.path.join(output_dir, fname)
    with open(fpath, 'w') as fstream:
        fstream.write(json.dumps(encode(obj), indent=4))

    return fpath
