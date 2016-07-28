#  return {
#        'type': 'class',
#        'base': 'activity.activity',
#        'is_abstract': False,
#        'properties': [
#            ('part_of_project', 'linked_to(designing.project)', '1.N',
#                'Project or projects for which simulation was run'),
#            ('ran_for_experiments', 'linked_to(designing.numerical_experiment)', '1.N',
#                'One or more experiments with which the simulation is associated'),
#            ('sub_experiment', 'designing.numerical_experiment', '0.1',
#                'For start-date ensembles, this will indicate the beginning year; for offline models driven by output from another model, this will provide the source_id and variant_label for the "driving" model.'),
#            ('used', 'linked_to(science.model)', '1.1',
#                'The model used to run the simulation'),
#            ('primary_ensemble', 'linked_to(activity.ensemble)', '0.1',
#                'Primary Ensemble (ensemble for which this simulation was first run).'),
#            ('insitution', 'shared.party', '0.1',
#                'institution which carried out the simulation'),
#            ('parent_simulation', 'activity.parent_simulation', '0.1',
#                'If appropriate, detailed information about how this simulation branched from a previous one'),
#
#            # Time
#            ('start_time', 'time.date_time', '0.1',
#                'The start date-time of the simulation. e.g. 2012-04-01 00:00:00'),
#            ('end_time', 'time.date_time', '0.1',
#                'The start date-time of the simulation. e.g. 2087-11-30 12:00:00'),
#            ('calendar', 'time.calendar', '0.1',
#                'The calendar used in the simulation'),
#
#            # Ensemble member attributes
#            ('realization_index', 'int', '0.1',
#                'realization number, e.g. 5'),
#            ('initialization_index', 'int', '0.1',
#                'Index variant of initialization method, e.g. 1'),
#            ('physics_index', 'int', '0.1',
#                'index for model physics, e.g. 3'),
#            ('forcing_index', 'int', '0.1',
#                'index for variant of forcing, e.g. 2'),
#            ('variant_info', 'str', '0.1',
#                'description of run variant differences, e.g. forcing: black carbon aerosol only'),
#
#            # Further Info URL
#            ('further_info_url', 'str', '0.1',
#                'On-line location of documentation'),
#
#            # Extra attributes
#            ('extra_attributes','shared.extra_attribute', '0.N',
#                'Additional attributes provided with simulation.')
#            ],
#
#        'constraints':[
#            ('cardinality', 'rationale', '0.0'),
#        ]
#    }

# Dictionary of CMIP6 -> CIM2 mappings. key = CMIP6 netCDF gloabl
# attribute name, value = equivalent CIM2 Simulation property name.
cmip6_to_cim2 = {
    #-------------------------  ------------------------
    # CMIP6 attribute           CIM2 Simulation property
    #-------------------------  ------------------------
    'activity_id'             : None,                    # E.g. 'CMIP, 'PMIP', 'LS3MIP LUMIP'
    'branch_method'           : None,                    # E.g. 'standard', 'none provided'
    'branch_time_in_child'    : None,                    # E.g. 365.0D0, 0.0D0
    'branch_time_in_parent'   : None,                    # E.g. 3650.0D0
    'comment'                 : None,                    
    'contact'                 : 'contact',               
    'Conventions'             : None,                    # E.g. 'CF-1.7 CMIP-6.0', 'CF-1.7 CMIP-6.0 UGRID-0.9'
    'creation_date'           : None,                    
    'data_specs_version'      : None,                    
    'experiment'              : None,                    # E.g. 'pre-industrial control',  'abrupt quadrupling of CO2'
    'experiment_id'           : 'ran_for_experiments',   # E.g. 'historical', 'abrupt4xCO2'
    'external_variables'      : None,                    # E.g. 'areacello'
    'forcing_index'           : 'forcing_index',         # E.g. 2
    'frequency'               : None,                    # E.g. 'day'
    'further_info_url'        : 'further_info_url',      # E.g. 'http://furtherinfo.es-doc.org/cmip6.MOHC.HadCM3.historical.none.r3i1p1f1'
    'grid'                    : None,                    
    'grid_label'              : None,                    
    'grid_resolution'         : None,                    
    'history'                 : None,                    
    'initialization_index'    : 'initialization_index',  # E.g. 1
    'institution'             : None,                    # E.g. 'Meteorological Research Institute'
    'institution_id'          : 'institution',           # E.g. 'IPSL'
    'license'                 : None,
    'mip_era'                 : 'mip_era',               # E.g. 'CMIP6', 'CMIP7'
    'parent_activity_id'      : None,                    # E.g. 'CMIP'
    'parent_experiment_id'    : None,                    # E.g. 'piControl'
    'parent_mip_era'          : None,                    # E.g. 'CMIP5', 'CMIP6'
    'parent_source_id'        : None,                    # E.g. 'CanCM4'
    'parent_time_units'       : None,                    # E.g. 'days since 1850-1-1', 'days since 1000-1-1 (noleap)'
    'parent_variant_label'    : None,                    # E.g. 'r1i1p1f1', 'r1i2p223f3', 'no parent'
    'physics_index'           : 'physics_index',         # E.g. 3
    'product'                 : None,                    # E.g. 'output'
    'realization_index'       : 'realization_index',     # E.g. 5
    'realm'                   : None,                    # E.g. 'atmos', 'ocean', 'atmosChem atmos' 
    'references'              : 'references',              
    'source'                  : 'source',                # E.g. 'GFDL CM2.1: cycle 2.1.14'
    'source_id'               : None,                    # E.g. 'GFDL-CM2-1'
    'source_type'             : None,                    # E.g. 'AGCM', 'OGCM', 'AOGCM', 'ISM', 'AOGCM ISM'                      
    'sub_experiment'          : None,
    'sub_experiment_id'       : 'sub_experiment',        # E.g. 's1960', 's1965', 'none'
    'table_id'                : None,                    # E.g. 'Amon'
    'title'                   : None,
    'tracking_id'             : None,
    'variable_id'             : None,                    # E.g. 'tas', 'pr', 'ua'
    'variant_info'            : 'variant_info',          # E.g. 'forcing: black carbon aerosol only'
    'variant_label'           : None,                    # E.g. 'r1i1p1f1', 'f1i2p223f3'
}

# Dictionary of CMIP5 -> CIM2 mappings. key = CMIP5 netCDF gloabl
# attribute name, value = equivalent CIM2 Simulation property name.
cmip5_to_cim2 = {
    #-------------------------  ------------------------
    # CMIP5 attribute           CIM2 Simulation property
    #-------------------------  ------------------------
    'branch_time'             : 'branch_time_in_parent', 
    'contact'                 : 'contact',
    'experiment_id'           : 'experiment_id',
    'forcing'                 : 'forcing',
    'initialization_method'   : 'initialization_index',
    'institute_id'            : 'institution_id', 
    'model_id'                : 'source_id',
    'project_id'              : 'mip_era',
    'parent_experiment_id'    : 'parent_experiment_id',
    'parent_experiment_rip'   : None,
    'physics_version'         : 'physics_index',
    'references'              : 'references',
    'source_id'               : 'source',
    'realization'             : 'realization_index',
}        


# CMIP6 file properties from which a simulation id can be constructed
cmip6_id = sorted([
    'further_info_url',
])

# CMIP5 file properties from which a simulation id can be constructed
cmip5_id = sorted([
    'activity_id',
    'experiment_id',
    'initialization_index',
    'institute_id',
    'model_id',
    'physics_index',
    'source',
    'realization_index',
])
