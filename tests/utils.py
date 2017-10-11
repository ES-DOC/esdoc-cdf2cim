# -*- coding: utf-8 -*-

"""
.. module:: utils.py

   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Unit test utilities.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import json
import os



# Test NetCDF file directories.
NETCDF_DIR = os.path.join(os.path.dirname(__file__), "test-data")
CMIP5_NETCDF_DIR = os.path.join(NETCDF_DIR, 'cmip5')
CMIP6_NETCDF_DIR = os.path.join(NETCDF_DIR, 'cmip6/v1')

# CMIP5 directory / files.
CMIP5_NETCDF_DIR = os.path.join(NETCDF_DIR, 'cmip5')
CMIP5_NETCDF_FILE = os.path.join(CMIP5_NETCDF_DIR, 'tas_2005.nc')
CMIP5_NETCDF_FILES = [os.path.join(CMIP5_NETCDF_DIR, i) for i in os.listdir(CMIP5_NETCDF_DIR)]
CMIP5_NETCDF_FILE_COUNT = len(CMIP5_NETCDF_FILES)

# CMIP6 directory / files.
CMIP6_NETCDF_DIR = os.path.join(NETCDF_DIR, 'cmip6/v1')
CMIP6_NETCDF_FILE = os.path.join(CMIP6_NETCDF_DIR, 'tas_0.nc')
CMIP6_NETCDF_FILES = [os.path.join(CMIP6_NETCDF_DIR, i) for i in os.listdir(CMIP6_NETCDF_DIR)]
CMIP6_NETCDF_FILE_COUNT = len(CMIP6_NETCDF_FILES)

# All directory / files.
ALL_NETCDF_DIRS = [CMIP5_NETCDF_DIR, CMIP6_NETCDF_DIR]
ALL_NETCDF_FILES = CMIP5_NETCDF_FILES + CMIP6_NETCDF_FILES
ALL_NETCDF_FILE_COUNT = CMIP5_NETCDF_FILE_COUNT + CMIP6_NETCDF_FILE_COUNT

# Sample output.
SAMPLE_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "sample-output")
with open(os.path.join(SAMPLE_OUTPUT_DIR, 'cmip5.json'), 'r') as _fstream:
    SAMPLE_OUTPUT_CMIP5 = json.loads(_fstream.read())
with open(os.path.join(SAMPLE_OUTPUT_DIR, 'cmip6.json'), 'r') as _fstream:
    SAMPLE_OUTPUT_CMIP6 = json.loads(_fstream.read())
