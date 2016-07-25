# Dictionary of CMIP6 -> CIM2 mappings. key = CMIP6 netCDF gloabl
# attribute name, value = equivalent CIM2 Simulation property name.
cmip6_to_cim2 = {
    'activity_id'             : None,
    'branch_method'           : None,                       # activity_classes.parent_simulation
    'branch_time_in_child'    : None,                       # activity_classes.parent_simulation
    'branch_time_in_parent'   : None,                       # activity_classes.parent_simulation
    'comment'                 : None,
    'contact'                 : 'contact',
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
    'references'              : 'references',
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
    'contact'              : 'contact',
    'experiment_id'        : 'experiment_id',
    'forcing'              : 'forcing',
    'initialization_method': 'initialization_index',
    'institute_id'         : 'institution_id', 
    'model_id'             : 'source_id',
    'project_id'           : 'mip_era',
    'parent_experiment_id' : 'parent_experiment_id',
    'parent_experiment_rip': 'parent_variant_label',
    'physics_version'      : 'physics_index',
    'references'           : 'references',
    'source_id'            : 'source',
    'realization'          : 'realization_index',
}        

cmip6_id = sorted([
    'further_info_url',
])

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
