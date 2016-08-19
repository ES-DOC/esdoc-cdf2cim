from os      import walk
from os.path import isdir, join, abspath
 
def find_files(inputs):
    '''Return all of the files implied by the inputs.

The inputs may be filenames or directories. In the latter case,
directories are searched recursively.

:Parameters:

    inputs : sequence of str
        The files and directories to find. Directories are searched
        recursively. Directories pointed by symbolic links are
        searched.

:Returns:

    out : set
        A set of the names of all of the files found. Files names are
        in normalised, absolutised form.

:Examples:

>>> import os
>>> os.getcwd()
'/badc/cmip5'
>>> find_files(['data/cmip5/output1/IPSL/IPSL-CM5B-LR/amip4xCO2/tas.nc'])
{'/badc/cmip5/data/cmip5/output1/IPSL/IPSL-CM5B-LR/amip4xCO2/tas.nc'}
>>> find_files(['cmip5/data/cmip5/output1/IPSL/IPSL-CM5B-LR/amip4xCO2/tas.nc',
...             '/badc/cmip5/data/cmip5/output1/IPSL/IPSL-CM5B-LR/abrupt4xCO2'])
{'/badc/cmip5/data/cmip5/output1/IPSL/IPSL-CM5B-LR/amip4xCO2/tas.nc'
 '/badc/cmip5/data/cmip5/output1/IPSL/IPSL-CM5B-LR/abrupt4xCO2/orog.nc',
 '/badc/cmip5/data/cmip5/output1/IPSL/IPSL-CM5B-LR/abrupt4xCO2/yr/tas.nc',
 '/badc/cmip5/data/cmip5/output1/IPSL/IPSL-CM5B-LR/abrupt4xCO2/yr/pr.nc'}

    '''

#infiles='/net/jasmin/chestnut/data-15/jonathan/cmip5/tas/tas_Amon_FGOALS-g2*'
#infiles = '/badc/cmip5/data/cmip5/output1/IPSL/IPSL-CM5B-LR/abr*'
#infiles = '/badc/cmip5/data/cmip5/output1/IPSL/IPSL-CM5B-LR'
#infiles = '/badc/cmip5/data/cmip5/output1/IPSL/IPSL-CM5B-LR/amip4xCO2'
#infiles = '/badc/cmip5/data/cmip5/output1/IPSL/IPSL-CM5B-LR/abrupt4xCO2/yr/ocnBgchem/Oyr/r1i1p1/v20120430/d*'

    if not inputs:
        raise ValueError(
"Must provide at least one file or directory from which files can be found")

    if isinstance(inputs, basestring):
        raise ValueError(
"The input files and directories must comprise a sequence of strings, not {!r}".format(inputs))

    # List of the output files
    outfiles = []
    
    for filename in inputs:
        if isdir(filename):
            # Recursively find all files in this directory
            outfiles.extend(
                abspath(join(path, f))
                for path, subdirs, filenames in walk(filename, followlinks=True)
                for f in filenames
            )
        else:
            # Just add this file to the list
            outfiles.append(abspath(filename))

    return set(outfiles)
