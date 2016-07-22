import re

from os      import walk
from os.path import isdir, join

import cf

# Dictionary of CMIP6 -> CIM2 mappings. key = CMIP6 netCDF gloabl
# attribute name, value = equivalent CIM2 Simulation property name.
cmip6_to_cim2 = {
    'activity_id'             : None,
    'branch_method'           : None,                       # activity_classes.parent_simulation
    'branch_time_in_child'    : None,                       # activity_classes.parent_simulation
    'branch_time_in_parent'   : None,                       # activity_classes.parent_simulation
    'comment'                 : None,
    'Conventions'             : None,
    'creation_date'           : None,
    'data_specs_version'      : None,
    'experiment'              : None,
    'experiment_id'           : 'experiment_id',            # designing.numerical_experiment
    'external_variables'      : None,
    'forcing_index'           : 'forcing_index',            # int
    'frequency'               : None,
    'further_info_url'        : 'further_info_url',         # str
    'grid'                    : None,
    'grid_label'              : None,
    'grid_resolution'         : None,
    'history'                 : None,
    'initialization_index'    : 'initialization_index',     # int
    'institution'             : None,
    'institution_id'          : 'institution_id',           # shared_classes.party
    'license'                 : None,
    'mip_era'                 : 'mip_era',                  # list of designing_classes.project
    'parent_activity_id'      : None,
    'parent_experiment_id'    : 'parent_experiment_id',     # activity_classes.parent_simulation
    'parent_mip_era'          : 'parent_mip_era',           # activity_classes.parent_simulation
    'parent_source_id'        : 'parent_source_id',         # activity_classes.parent_simulation
    'parent_sub_experiment_id': 'parent_sub_experiment_id', # activity_classes.parent_simulation
    'parent_time_units'       : None,                       # activity_classes.parent_simulation
    'parent_variant_label'    : None,                       # activity_classes.parent_simulation
    'physics_index'           : 'physics_index',            # int
    'product'                 : None,
    'realization_index'       : 'realization_index',        # int
    'realm'                   : None,
    'source'                  : 'source',                   # science.model
    'source_id'               : None,
    'source_type'             : None,
    'sub_experiment'          : 'sub_experiment',           # designing.numerical_experiment
    'sub_experiment_id'       : 'sub_experiment_id',        # designing.numerical_experiment
    'table_id'                : None,
    'title'                   : None,
    'tracking_id'             : None,
    'variant_id'              : 'variant_id',
    'variant_info'            : 'variant_info',
    'variant_label'           : None,
}

# Dictionary of CMIP5 -> CIM2 mappings. key = CMIP5 netCDF gloabl
# attribute name, value = equivalent CIM2 Simulation property name.
cmip5_to_cim2 = {
    'branch_time'          : 'branch_time_in_parent', 
    'experiment_id'        : 'experiment_id',
    'initialization_method': 'initialization_index',
    'institute_id'         : 'institution_id', 
    'model_id'             : 'source_id',
    'project_id'           : 'mip_era',
    'parent_experiment_id' : 'parent_experiment_id',
    'parent_experiment_rip': 'parent_variant_label',
    'physics_version'      : 'physics_index',
    'source'               : None,
    'source_id'            : 'source',
    'realization'          : 'realization_index',
}          


def find_files(*inputs):
    '''
'''

#infiles='/net/jasmin/chestnut/data-15/jonathan/cmip5/tas/tas_Amon_FGOALS-g2*'
#infiles = '/badc/cmip5/data/cmip5/output1/IPSL/IPSL-CM5B-LR/abr*'
#infiles = '/badc/cmip5/data/cmip5/output1/IPSL/IPSL-CM5B-LR'
#infiles = '/badc/cmip5/data/cmip5/output1/IPSL/IPSL-CM5B-LR/amip4xCO2'
#infiles = '/badc/cmip5/data/cmip5/output1/IPSL/IPSL-CM5B-LR/abrupt4xCO2/yr/ocnBgchem/Oyr/r1i1p1/v20120430/d*'

    if not inputs:
        raise ValueError("Must supply at least one file or directory")

    outfiles = []
    
    for filename in inputs:
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

def simulation_id(properties):
    '''
    '''
    if properties.get('mip_era') == 'CMIP6':
        return properties.get('further_info_url')
    elif properties.get('mip_era') == 'CMIP5':
        # Need to do something different for CMIP5
        return tuple((x, properties.get(x)) for x in ('activity_id',
                                                      'experiment_id',
                                                      'initialization_index',
                                                      'institute_id',
                                                      'model_id',
                                                      'physics_index',
                                                      'source',
                                                      'realization_index'))
        

def find_simulations(*inputs):
    '''
    
:Examples 1:

>>> cim2_docs = find_simulations(['IPSL/IPSL-CM5B-LR']

:Parameters:

    inputs : sequence of str

:Returns:

    out : list of dict


    '''
    # Dictionary of simulations: key = a unique simulation identifier,
    # value = a list of fields for the simulation.
    simulations = {}
    
    # Dictionary of simulation dates: key = a unique simulation
    # identifier, value = a list of date-time objects which define the
    # time span of the simulation.
    simulation_dates = {}
    
    files = find_files(*inputs)

    for filename in files:
        for f in cf.read(filename, ignore_read_error=True, verbose=False, aggregate=False):
            
            # Get the time coordinates
            time_coords = f.dim('T')
            
            if time_coords is None or not time_coords.Units.isreftime or time_coords.ndim > 1:
                # No (suitable) time coordinates - ignore this field
                continue
            
            properties = f.properties #(copy=False)
            cim2_properties = {}
        
            if properties.get('mip_era') == 'CMIP6':
                mapping = cmip6_to_cim2
            elif properties.get('project_id') == 'CMIP5':
                mapping = cmip5_to_cim2
    
            for cmip_attr, cim2_attr in mapping.iteritems():
                if cim2_attr is None:
                    continue
                cim2_properties[cim2_attr] = properties.pop(cmip_attr, None)
    
            cim2_properties['calendar'] = getattr(time_coords, 'calendar', 'gregorian')
            cim2_properties.pop(None, None)
    
            if mapping is cmip6_to_cim2:
                # Special CMIP6 to CIM2 processing which has not been
                # provided by the mapping
                
                # parent_variant_label
                cim2_properties.update(
                    zip(['parent_realization_index',
                         'parent_initialization_index',
                         'parent_physics_index',
                         'parent_forcing_index'],
                        re.findall('\d+', properties.get('parent_variant_label', 'none'))))
    
                # branch_time_in_child
                # branch_time_in_parent
                # parent_time_units
                parent_branch_units = properties.get('parent_branch_units')            
                if parent_time_units is None:
                    parent_time_units = time_coords.Units
                else:                
                    m = re.match('(.*) *\((.*?)\)', parent_time_units)
                    if m:
                        parent_time_units = cf.Units(*m.groups())
                    else:
                        parent_time_units = cf.Units(parent_time_units, 
                                                     cim2_properties['calendar'])
                
                branch_time_in_parent = properties.get('branch_time_in_parent')
                if branch_time_in_parent is not None:
                    x = cf.Data([branch_time_in_parent], parent_time_units).dtarray[0]
                    cim2_properties['branch_time_in_parent'] = str(x)
                    
                branch_time_in_child = properties.get('branch_time_in_child')
                if branch_time_in_child is not None:
                    x = cf.Data([branch_time_in_child], time_coords.Units).dtarray[0]
                    cim2_properties['branch_time'] = str(x)
                    
            elif mapping is cmip5_to_cim2:
                # Special CMIP5 to CIM2 processing which has not been
                # provided by the mapping
                pass

            # Find a canonical identity for the simulation that this
            # field belongs to
            identity = simulation_id(cim2_properties)
            if not identity:
                # No identity was found - ignore this field
                continue
    
            simulations.setdefault(identity, []).append(cim2_properties)
            
            # --------------------------------------------------------
            # Find the earliest and latest dates for this field
            # --------------------------------------------------------
            if time_coords.size == 1:
                index = 0
            else:
                index = [0, -1]

            if time_coords.hasbounds:
                # Get the time span from the time coordinate bounds
                dates = time_coords.bounds.subspace[index].dtarray.flat
            else:
                # In the absence of bounds, get the time span from the
                # time coordinates
                dates = time_coords.subspace[index].dtarray
            
            # Add the first and last time_coords to the list of
            # date-time_coords for this simulation
            simulation_dates.setdefault(identity, []).extend(dates)    
        #--- End: for
        
        # Close the file to prevent a proliferation of open file
        # handles
        cf.close_one_file()
    #--- End: for
    
    cim2_documents = []
    
    for identity, properties in simulations.iteritems():
    
        # Include items from extra1 if they have a unique value
        extra1 = {
            'institution' : [],
            'experiment'  : [],        
            'forcing'     : [],
            'variant_info': [],
        }
    
        dates = []
        for p in properties:
            for x, v in extra1.iteritems():
                v.append(p.get(x))
    
        # Include items from extra1 if they have a unique value
        for prop, v in extra1.iteritems():
            v = set(v)
            v.discard(None)
            if len(v) == 1:
                cim2_properties[prop] = v.pop()

        # Include all unique items from extra2
        extra2 = {
            'contact'    : [],
            'references' : [], 
        }
    
        dates = []
        for p in properties:
            for x, v in extra2.iteritems():
                v.append(p.get(x))
    
        for prop, v in extra2.iteritems():
            v = set(v)
            v.discard(None)
            if len(v) == 1:
                cim2_properties[prop] = ', '.join(sorted(v))

        cim2_properties = properties[0].copy()

        dates = simulation_dates.get(identity)
        if dates:
            dates = cf.Data(list(set(dates)), dt=True).asreftime()
            cim2_properties['start_time'] = str(dates.min().dtarray[0])
            cim2_properties['end_time']   = str(dates.max().dtarray[0])

        cim2_documents.append(cim2_properties)
    #--- End: for

    return cim2_documents
#--- End: def
