from os      import walk
from os.path import isdir, join
 
#infiles='/net/jasmin/chestnut/data-15/jonathan/cmip5/tas/tas_Amon_FGOALS-g2*'
#infiles = '/badc/cmip5/data/cmip5/output1/IPSL/IPSL-CM5B-LR/abr*'
#infiles = '/badc/cmip5/data/cmip5/output1/IPSL/IPSL-CM5B-LR'
#infiles = '/badc/cmip5/data/cmip5/output1/IPSL/IPSL-CM5B-LR/amip4xCO2'
#infiles = '/badc/cmip5/data/cmip5/output1/IPSL/IPSL-CM5B-LR/abrupt4xCO2/yr/ocnBgchem/Oyr/r1i1p1/v20120430/d*'


def find_files(inputs):
    '''
'''
    outfiles = []
    
    for filename in infiles:
        if isdir(filename):
            # Recursively find all files in this directory
            outfiles.extend(
                join(path, f)
                for path, subdirs, filenames in walk(filename, followlinks=True)
                for f in filenames
            )
        else:
            outfiles.append(filename) 

    return set(outfiles)
