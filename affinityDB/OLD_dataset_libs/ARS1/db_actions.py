def binding_affinity(bucket, table_idx, param, input_data):
    # todo(maksym) generalize this function into from_txt_into_database_column

    '''
    Parse binding affintiy from the bindingdb, bindmoad or pdbbind.
    Args:
        table_idx: int
        param: dict
                {
                    'bind_param':{
                        'index':'...',
                        'parse_func':'...'
                }
                
        input_data: None

    Returns: None

    '''
    try:
        bind_param = param['bind_param']
        bind_index = bind_param['index']
    
        parse_func = bind_param['parse_func'] 
        parse_func = parse_bind_func[parse_func]
        #error happening at parse_bind_func
        PDB_bind = parse_func(bind_index)
        records = [[PDB_bind.pdb_names[i].upper(), PDB_bind.ligand_names[i],
                 PDB_bind.log_affinities[i], PDB_bind.normalized_affinities[i],
                 PDB_bind.states[i], PDB_bind.comments[i]]
                 for i in range(len(PDB_bind.pdb_names))]
        #print('Records', records)
        print('Records', records)
        db.insert(table_idx, records, bucket=bucket)
    except Exception as e:
        print ('Error occured', e)

def binding_affinity(bucket, table_idx, param, input_data):
    # todo(maksym) generalize this function into from_txt_into_database_column

    '''
    Parse binding affintiy from the bindingdb, bindmoad or pdbbind.
    Args:
        table_idx: int
        param: dict
                {
                    'bind_param':{
                        'index':'...',
                        'parse_func':'...'
                }
                
        input_data: None

    Returns: None

    '''
    try:
        bind_param = param['bind_param']
        bind_index = bind_param['index']
    
        parse_func = bind_param['parse_func'] 
        parse_func = parse_bind_func[parse_func]
        #error happening at parse_bind_func
        PDB_bind = parse_func(bind_index)
        records = [[PDB_bind.pdb_names[i].upper(), PDB_bind.ligand_names[i],
                 PDB_bind.log_affinities[i], PDB_bind.normalized_affinities[i],
                 PDB_bind.states[i], PDB_bind.comments[i]]
                 for i in range(len(PDB_bind.pdb_names))]
        #print('Records', records)
        print('Records', records)
        db.insert(table_idx, records, bucket=bucket)
    except Exception as e:
        print ('Error occured', e)
