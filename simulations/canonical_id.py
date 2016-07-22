def simulation_id(cim2_properties):
    '''
'''
    canoncical_properties = ('mip_era',
                             'realization_index',
                             'initialization_index',
                             'physics_index',
                             'forcing_index',
)
    
    sid = [cim2_properties.get(prop) for prop in canonical_properties]

    return tuple(sorted(sid))
        
