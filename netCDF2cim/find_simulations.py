import re

import cf

from .constants  import cmip5_to_cim2, cmip6_to_cim2, cmip5_id, cmip6_id
from .find_files import find_files


#def simulation_id(global_attributes):
#    '''
#    '''
#    if is_CMIP6_file(global_attributes):
#        _id = cmip6_id
#    elif is_CMIP5_file(global_attributes):
#        _id = cmip5_id
#
#    return tuple((x, global_attributes.get(x)) for x in _id)

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
    # ----------------------------------------------------------------
    # Initialise variables
    # ----------------------------------------------------------------
    # List of dictionaries, one per simulation. Each dictionary's
    # key/value pairs fully define a simulation. This list is returned.
    out = []

    # Dictionary of simulations: key = a unique simulation identifier,
    # value = a list of dictionaries, each of which describes a single
    # file of the simulation
    simulations = {}
    
    # Dictionary of simulation dates: key = a unique simulation
    # identifier, value = a list of date-time objects which
    # collectively define the time span of the simulation.
    simulation_dates = {}
    
    # ----------------------------------------------------------------
    # Get the input files
    # ----------------------------------------------------------------
    input_files = find_files(inputs)

    if verbose:
        print 'Input files:\n', '\n'.join(sorted(input_files)), '\n'

    # ----------------------------------------------------------------
    # Split the input files into groups such that all of the files in
    # a group belong to the same simulation
    # ----------------------------------------------------------------
    for filename in input_files:
    
        # For each CF field in this input file ...
        for f in cf.read(filename, ignore_read_error=True, verbose=False, aggregate=False):
            
            # Get the time coordinates and find the earliest and
            # latest dates
            time_coords = f.dim('T')
            dates = file_start_end_dates(time_coords)
            if not dates:
                # No valid dates were found, so ignore this file.
                continue

            # Get the netCDF global attributes
            global_attributes = f.properties

            # Find out which mip-era file we have
            mip_era = MIP_era(global_attributes)

            # Simply map file properties to CIM2 properties
            cim2_properties = {}
            
            # Parse properties which only require a simple mapping
            if mip_era == 'CMIP6':
                simple_mapping = cmip6_to_cim2
            elif mip_era == 'CMIP5':
                simple_mapping = cmip5_to_cim2
    
            for file_prop, cim2_prop in simple_mapping.iteritems():
                cim2_properties[cim2_prop] = global_attributes.get(file_prop)
    
            # Add the time coordinates' calendar to the cim2 properties
            cim2_properties['calendar'] = get_calendar(time_coords)
    
            # Parse properties which require something more
            # complicated than a simple mapping
            if mip_era == 'CMIP6':
                parse_cmip6_properties(cim2_properties, global_attributes, time_coords)
            elif mip_era == 'CMIP5':
                parse_cmip5_properties(cim2_properties, global_attributes, time_coords)

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
    
    # ----------------------------------------------------------------
    # For each simulation, set some simulation properties which can
    # only be known when of all the contributing files have been
    # identified.
    # ----------------------------------------------------------------
    for identity, properties in simulations.iteritems():
    
        cim2_properties = properties[0].copy()

        # Find the start and end dates of the whole simulation
        start_date, end_date = simulation_start_end_dates(simulation_dates.get(identity))
        if start_date:
            cim2_properties['start_time'] = start_date
            cim2_properties['end_time']   = end_date

        # Include items from extra1 only if all files have the same value
        extra1 = {
            'institution_id': [],
            'experiment_id' : [],        
            'forcing'       : [],
            'variant_info'  : [],
        }
    
        for p in properties:
            for x, v in extra1.iteritems():
                v.append(p.get(x))
    
        for prop, v in extra1.iteritems():
            v = set(v)
            v.discard(None)
            if len(v) == 1:
                cim2_properties[prop] = v.pop()

        # Include all items from extra2 from all files, omitting duplicates.
        extra2 = {
            'contact'    : [],
            'references' : [], 
        }
    
        for p in properties:
            for x, v in extra2.iteritems():
                v.append(p.get(x))
    
        for prop, v in extra2.iteritems():
            v = set(v)
            v.discard(None)
            if v:
                cim2_properties[prop] = ', '.join(sorted(v))

        # ------------------------------------------------------------
        # The cim2_properties dictionary now contains everything
        # needed to create CIM2 Enemble, Ensemble Member and
        # Simulation documents. So add it to the output list.
        # ------------------------------------------------------------
        out.append(cim2_properties)
    #--- End: for

    if verbose:
        print 'Simulations:\n',
        for x in out:
            print x.keys(), '\n'
            print x, '\n'

    return out
#--- End: def

def simulation_start_end_dates(dates):
    '''Given a sequence of date-time objects which collectively define the
time span of the simulation, find the start and end times of the
simulation and return them as ISO8601=-like strings.

:Parameters:

    dates : sequence of date-time objects

:Returns:

    start, end : str, str
        The start and end dates of the simulation

:Examples:

>>> simulation_start_end_dates(dates)
'1016-05-04 00:00:00', '2045-12-31 12:30:00'

    '''
    if dates:
        dates = cf.Data(list(set(dates)), dt=True).asreftime()
        return str(dates.min().dtarray[0]), str(dates.max().dtarray[0])

    return (None, None)
        

def file_start_end_dates(time_coords):
    '''Given a time coordinate object from the netCDF file, return
earliest and latest date-time objects.

:Parameters:

    time_coords : cf.Coordinate

:Returns:

    out : numpy array of date-time objects

:Examples:

>>> file_start_end_dates(time_coords)
array([ 450-11-16 00:00:00,  451-10-16 12:00:00], dtype=object)

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

def parse_cmip6_properties(cim2_properties, global_attributes, time_coords):
    '''

:Parameters:

    cim2_properties : dict

    global_attributes : dict
        The netCDF global attributes of the file.

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
            map(int, re.findall('\d+', global_attributes.get('parent_variant_label', 'none')))))
    
    # parent_time_units
    parent_time_units = global_attributes.get('parent_time_units')            
    if parent_time_units is None:
        # parent_time_units has not been set in file, so they are
        # assumed to be the same as the child time units
        parent_time_units = time_coords.Units
    else:                
        # parent_time_units have been set in file
        m = re.match('(.*) *\((.*?)\)', parent_time_units)
        if m:
            parent_time_units = cf.Units(*m.groups())
        else:
            parent_time_units = cf.Units(parent_time_units,
                                         cim2_properties['calendar'])
            
    # ----------------------------------------------------------------
    # CIM2 branch_time_in_parent
    # ----------------------------------------------------------------
    branch_time_in_parent = global_attributes.get('branch_time_in_parent')
    if branch_time_in_parent is not None:
        x = cf.Data([branch_time_in_parent], units=parent_time_units).dtarray[0]
        cim2_properties['branch_time_in_parent'] = str(x)

    # ----------------------------------------------------------------
    # CIM2 branch_time_in_child 
    # ----------------------------------------------------------------
    branch_time_in_child = global_attributes.get('branch_time_in_child')
    if branch_time_in_child is not None:
        x = cf.Data([branch_time_in_child], units=time_coords.Units).dtarray[0]
        cim2_properties['branch_time_in_child'] = str(x)
                  
def parse_cmip5_properties(cim2_properties, global_attributes, time_coords):
    '''

:Parameters:

    cim2_properties : dict

    global_attributes : dict
        The netCDF global attributes of the file.

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
            map(int, re.findall('\d+', global_attributes.get('parent_experiment_rip', 'none')))))


def MIP_era(global_attributes):
    '''The mip era of the file.

:Parameters:

    global_attributes : dict
        The netCDF global attributes of the file.
    
:Returns:

    out : str or None
        The mip era. One of ``'CMIP5'``, ``'CMIP6'`` or `None` if the
        mip-era can not be determined.

:Examples:

>>> MIP_era(global_attributes)
'CMIP6'

    '''
    if global_attributes.get('mip_era') == 'CMIP6':
        return 'CMIP6'
    elif global_attributes.get('project_id') == 'CMIP5':
        return 'CMIP5'
    
def get_calendar(time_coords):
    return getattr(time_coords, 'calendar', 'gregorian')
    
