# -*- coding: utf-8 -*-

"""
.. module:: io.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Enapsulates package IO operations.

.. moduleauthor:: David Hassel <david.hassell@ncas.ac.uk>


"""
import numpy



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

	return {k: _encode(v) for k, v in obj.iteritems()}
