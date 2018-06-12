# -*- coding: utf-8 -*-

"""
.. module:: io.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Enapsulates package IO operations.

.. moduleauthor:: David Hassell <david.hassell@ncas.ac.uk>


"""
import collections
import glob
import json
import os
import shutil
import uuid

import cf
import numpy

from cdf2cim import exceptions
from cdf2cim import hashifier
from cdf2cim import logger
from cdf2cim.constants import FILE_STATUS_PUBLISHED
from cdf2cim.constants import FILE_STATUS_SCANNED_NEW
from cdf2cim.constants import FILE_STATUS_SCANNED_QUEUED
from cdf2cim.constants import IO_DIR_SCANNED
from cdf2cim.constants import IO_DIR_PUBLISHED



def encode(obj):
    """Encodes an output from a map/reduce as a JSON safe dictionary.

    :param dict obj: Output from a map/reduce job.

    :returns: A JSON safe dictionary
    :rtype: dict

    """
    def _encode(key, value):
        """Encodes a value.

        """
        if isinstance(value, numpy.float64):
            return float(value)
        elif isinstance(value, numpy.int32):
            return int(value)
        elif key.endswith("_index"):
            return int(value)
        else:
            return value

    result = collections.OrderedDict()
    for k in sorted(obj.keys()):
        result[k] = _encode(k, obj[k])

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
                for fname in [i for i in fnames if not i.startswith('.')]:
                    yield os.path.abspath(os.path.join(folder, fname))


def yield_cf_files(targets):
    """Yields CF files for further processing.

    :param str|sequence targets: Pointer(s) to file(s) and/or directorie(s).

    :returns:  Generator yielding CF files.
    :rtype: generator

    """
    for fpath in yield_files(targets):
        try:
            cf_files = cf.read(fpath, ignore_read_error=False, verbose=False, aggregate=False)
        except (IOError, OSError):
            logger.log_warning("Non netCDF file rejected: {}".format(fpath))
        else:
            # Save the netCDF file name (from which we can extract the dataset version)
            for cf_file in cf_files:
                cf_file.fpath = fpath

            yield cf_files

            # ... close file to prevent a proliferation of open file handles
            cf.close_one_file()


def dump(obj, overwrite):
    """Writes simulation metadata to file system.

    :param dict obj: Simulation metadata.
    :param bool overwrite: If True then overwrite an existing file.

    :returns: Path to written file.
    :rtype: str

    """
    # Set metadata (a JSON serializable ordered dictionary).
    metadata = encode(obj)

    # Set hash id.
    metadata['_hash_id'] = hashifier.hashify(metadata)

    # Set output directory.
    dpath = IO_DIR_SCANNED
    dpath = os.path.join(dpath, metadata['mip_era'].lower())
    dpath = os.path.join(dpath, metadata['institution_id'].lower())
    dpath = os.path.join(dpath, metadata['source_id'].lower())
    dpath = os.path.join(dpath, metadata['experiment_id'].lower())

    # Set output file path.
    fname = "{}.json".format(metadata['_hash_id'])
    fpath = os.path.join(dpath, fname)

    # Escape if already scanned/published;
    if not overwrite:
        if os.path.isfile(fpath):
            return (FILE_STATUS_SCANNED_QUEUED, fpath)
        else:
            fpath_published = fpath.replace(IO_DIR_SCANNED, IO_DIR_PUBLISHED)
            if os.path.isfile(fpath_published):
                return (FILE_STATUS_PUBLISHED, fpath_published)

    # Write to file system.
    if not os.path.isdir(dpath):
        os.makedirs(dpath)
    with open(fpath, 'w') as fstream:
        fstream.write(json.dumps(metadata, indent=4))

    return (FILE_STATUS_SCANNED_NEW, fpath)


def yield_scanned_files():
    """Yields set of scanned files for further processing.

    """
    result = []
    for dpath, _, fnames in os.walk(IO_DIR_SCANNED):
        for fname in fnames:
            yield os.path.join(dpath, fname)


def move_scanned_to_published(fpath):
    """Moves a successfully published file from scanned to published.

    :param str fpath: Path to a scanned file.

    :returns: Path to published file.
    :rtype: str

    """
    dest = fpath.replace(IO_DIR_SCANNED, IO_DIR_PUBLISHED)
    if not os.path.isdir(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))
    shutil.move(fpath, dest)

    return dest
