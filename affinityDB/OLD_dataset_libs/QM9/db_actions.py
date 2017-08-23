def local_qm9_load(bucket, table_idx, param, input_data):
    try:
        receptor = input_data                                           # todo(maksym) pdb_id
        output_folder = param['output_folder']
        output_folder_name = '{}_{}'.format(table_idx, output_folder)
        dest_dir = '/home/maksym/ryan/QM9_PDB'

        pdb_path = os.path.join(dest_dir, receptor)
        if not os.path.exists(pdb_path):
            return
        #header = prody.parsePDBHeader(pdb_path)
        pdbFile = open(pdb_path)
        lines = pdbFile.read().splitlines()
        energyLine = lines[0].split('\t')
        energyValues = [float(energy) for energy in energyLine[1:]]        
        moleculeId = [int(energyLine[0].split()[-1])]
        #record = [receptor, header['experiment'], header['resolution'], 1, 'success']
        record = moleculeId + energyValues + [1, '']
        records = [record]
        db.insert(table_idx, records, bucket=bucket)
    except Exception as e:
        record = [input_data, 'unk', 0, 0, str(e)]                      # todo maksym (unk) = failed
        records = [record]
        db.insert(table_idx, records, bucket=bucket)   
