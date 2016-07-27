import re

import cf

from .constants  import cmip5_to_cim2, cmip6_to_cim2, cmip5_id, cmip6_id
from .find_files import find_files


#def simulation_id(file_properties):
#    '''
#    '''
#    if is_CMIP6(file_properties):
#        _id = cmip6_id
#    elif is_CMIP5(file_properties):
#        _id = cmip5_id
#
#    return tuple((x, file_properties.get(x)) for x in _id)

def simulation_id(cim2_properties):
    '''
    '''    
    return tuple([(k, v) for k, v in cim2_properties.iteritems()
                  if k not in ('contact',
                               'references',                              
                               'forcing',
                               'variant_info')
              ])
    
def find_simulations(inputs, verbose=False):
    '''
    
:Examples 1:

>>> cim2_docs = find_simulations(['IPSL/IPSL-CM5B-LR'])

:Parameters:

    inputs : sequence of str

:Returns:

    out : list of dict


    '''
    # List of dictionaries, one per simulation. Each dictionary's
    # key/value pairs fully define a simulation. This list is returned.
    out = []
    

    # Dictionary of simulations: key = a unique simulation identifier,
    # value = a list of dictionaries which describe each file of the
    # simulation
    simulations = {}
    
    # Dictionary of simulation dates: key = a unique simulation
    # identifier, value = a list of date-time objects which define the
    # time span of the simulation.
    simulation_dates = {}
    
    files = find_files(*inputs)

    if verbose:
        print 'files:\n', files, '\n'

    # For each the file ...
    for filename in files:
    
        # For each CF field in the file ...
        for f in cf.read(filename, ignore_read_error=True, verbose=False, aggregate=False):
            
            # Get the time coordinates and find the earliest and
            # latest dates
            time_coords = f.dim('T')
            dates = file_start_end_dates(time_coords)
            if not dates:
                continue
      
            # Simply map file properties to CIM2 properties
            file_properties = f.properties
            cim2_properties = {}
        
            CMIP5 = is_CMIP5(file_properties)            
            CMIP6 = is_CMIP6(file_properties)

            # Parse properties which only require a simple mapping
            if CMIP6:
                simple_mapping = cmip6_to_cim2
            elif CMIP5:
                simple_mapping = cmip5_to_cim2
    
            for file_prop, cim2_prop in simple_mapping.iteritems():
                cim2_properties[cim2_prop] = file_properties.get(file_prop)
    
            # Add the time corodiantes' calendar to the cim2 properties
            cim2_properties['calendar'] = get_calendar(time_coords)
    
            # Parse properties which require something more
            # complicated than a simple mapping
            if CMIP6:
                parse_cmip6_properties(cim2_properties, file_properties, time_coords)
            elif CMIP5:
                parse_cmip5_properties(cim2_properties, file_properties, time_coords)

            # Create a canonical identity for the simulation that this
            # field belongs to
            identity = simulation_id(cim2_properties)
            if not identity:
                # No identity was found - ignore this field
                continue
    
            simulation_dates.setdefault(identity, []).extend(dates) 

            cim2_properties.pop(None, None)
            simulations.setdefault(identity, []).append(cim2_properties)
        #--- End: for
        
        # Close a file to prevent a proliferation of open file handles
        cf.close_one_file()
    #--- End: for
    
    for identity, properties in simulations.iteritems():
    
        cim2_properties = properties[0].copy()

        # Find the start and end dates of the whole simulation
        simulation_start_end_dates(cim2_properties, simulation_dates.get(identity))
        
        # Include items from extra1 if they have a unique value
        extra1 = {
            'institution_id': [],
            'experiment_id' : [],        
            'forcing'       : [],
            'variant_info'  : [],
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

        # cim2_properties now contains everything needed to create
        # CIM2 Enemble, Ensemble Member and Simulation documents
        out.append(cim2_properties)
    #--- End: for

    if verbose:
        print 'out:\n',
        for x in out:
            print x, '\n'
            print x.keys()
    return out
#--- End: def

def simulation_start_end_dates(cim2_properties, dates):
    '''
:Parameters:

    cim2_properties : dict

    dates : dict

    '''
    # CIM2 start_time
    # CIM2 end_time
    if dates:
        dates = cf.Data(list(set(dates)), dt=True).asreftime()
        cim2_properties['start_time'] = str(dates.min().dtarray[0])
        cim2_properties['end_time']   = str(dates.max().dtarray[0])
        

def file_start_end_dates(time_coords):
    '''

:Parameters:

    time_coords : cf.Coordinate

:Returns:

    out : list
    '''

    if time_coords is None or not time_coords.Units.isreftime or time_coords.ndim > 1:
        # No (suitable) time coordinates - ignore this field
        return []
        
    # Find the earliest and latest dates for this field
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
    
    return dates

def parse_cmip6_properties(cim2_properties, file_properties, time_coords):
    '''

:Parameters:

    cim2_properties : dict

    file_properties : dict

    time_coords : cf.Coordinate

:Returns:

    None
    '''
    # ----------------------------------------------------------------
    # CIM2 parent_realization_index
    # CIM2 parent_initialization_index
    # CIM2 parent_physics_index
    # CIM2 parent_forcing_index
    # ----------------------------------------------------------------
    cim2_properties.update(
        zip(['parent_realization_index',
             'parent_initialization_index',
             'parent_physics_index',
             'parent_forcing_index'],
            map(int, re.findall('\d+', file_properties.get('parent_variant_label', 'none')))))
    
    # ----------------------------------------------------------------
    # CIM2 branch_time_in_parent
    # CIM2 branch_time
    # ----------------------------------------------------------------
    parent_branch_units = file_properties.get('parent_branch_units')            
    if parent_time_units is None:
        parent_time_units = time_coords.Units
    else:                
        m = re.match('(.*) *\((.*?)\)', parent_time_units)
        if m:
            parent_time_units = cf.Units(*m.groups())
        else:
            parent_time_units = cf.Units(parent_time_units, 
                                         cim2_properties['calendar'])
            
    branch_time_in_parent = file_properties.get('branch_time_in_parent')
    if branch_time_in_parent is not None:
        x = cf.Data([branch_time_in_parent], parent_time_units).dtarray[0]
        cim2_properties['branch_time_in_parent'] = str(x)

    branch_time_in_child = file_properties.get('branch_time_in_child')
    if branch_time_in_child is not None:
        x = cf.Data([branch_time_in_child], time_coords.Units).dtarray[0]
        cim2_properties['branch_time'] = str(x)
                  
def parse_cmip5_properties(cim2_properties, file_properties, time_coords):
    '''

:Parameters:

    cim2_properties : dict

    file_properties : dict

    time_coords : cf.Coordinate

:Returns:

    None
    '''      
    # ----------------------------------------------------------------
    # CIM2 parent_realization_index
    # CIM2 parent_initialization_index
    # CIM2 parent_physics_index
    # CIM2 parent_forcing_index
    # ----------------------------------------------------------------
    cim2_properties.update(
        zip(['parent_realization_index',
             'parent_initialization_index',
             'parent_physics_index',
             'parent_forcing_index'],
            map(int, re.findall('\d+', file_properties.get('parent_experiment_rip', 'none')))))


def is_CMIP5(file_properties):
    return file_properties.get('project_id') == 'CMIP5'
    
def is_CMIP6(file_properties):
    return file_properties.get('mip_era') == 'CMIP6'
    
def get_calendar(time_coords):
    return getattr(time_coords, 'calendar', 'gregorian')
    
