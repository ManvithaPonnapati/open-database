# database action to load CSD structures

def local_csd_load(bucket, table_idx, param, input_data):
    '''
    Perform CCDC commands on input_data and upload to table
    
    Args:
        table_idx: id for download table 
        param: dict
            {
                'output_folder':'...',
                ...
            }
        input_data: str CSD identifier

    Returns:
    '''
    start_time = time.time()
    try:
        csd_identifier = input_data
        csd_reader = io.EntryReader('CSD')
        csd_identifier_entry = csd_reader.entry(csd_identifier)
        csd_identifier_crystal = csd_reader.crystal(csd_identifier)
        csd_identifier_molecule = csd_reader.molecule(csd_identifier)
        #Filtering the submolecules into the "main molecule"
        #main_component = csd_identifier_molecule.heaviest_component

        #solvent_smiles = np.load('/home/urops/ryanh/solvent_smiles.npy').tolist()
        solvent_smiles = param['solvent_smiles']
        #Iterate through the components, stripping those that are not in 
        non_solvents = []
        for mol in csd_identifier_molecule.components:
            if str(mol.smiles) not in solvent_smiles:
                non_solvents.append(mol)
        #Now check the non_solvents already have smiles strings in the database
        #all_smiles = np.load('/home/urops/ryanh/csd_smiles.npy').tolist()
        all_smiles = param['all_smiles']
        unique_mol = []
        for mol in non_solvents:
            if str(mol.smiles) not in all_smiles or len(non_solvents) == 1:
                unique_mol.append(mol)
        if len(unique_mol) == 0:
            raise Exception
        unique_mol = sorted(unique_mol, key=lambda mol: mol.molecular_weight)
        main_component = unique_mol[-1] #pick heaviest component
        molecule_elems = ""
        for atom in main_component.atoms:
            label_string = str(atom.label)+','
            molecule_elems += label_string
        molecule_coords = repr([[atom.coordinates[0], atom.coordinates[1], atom.coordinates[2]] if atom.coordinates is not None else ['None', 'None', 'None'] for atom in main_component.atoms])
        molecule_smiles = main_component.smiles
        #molecule_data = csd_identifier_molecule.to_string('mol2')
        hbond_acceptors, hbond_donors = hydrogen_bond_count(main_component) 
        rotatable_bonds = rotatable_bond_count(main_component)
        has_disorder = 1 if csd_identifier_entry.has_disorder else 0
        has_3d_structure = 1 if csd_identifier_entry.has_3d_structure else 0
        is_organometallic = 1 if csd_identifier_entry.is_organometallic else 0
        is_polymeric = 1 if csd_identifier_entry.is_polymeric else 0
        is_organic = 1 if csd_identifier_entry.is_organic else 0
        r_factor = csd_identifier_entry.r_factor
        if r_factor is None:
            r_factor = 'None'
        temperature = csd_identifier_entry.temperature
        if temperature is None:
            temperature = 'None'
        molecular_weight = csd_identifier_molecule.molecular_weight
        #crystal_data = csd_identifier_crystal.to_string('mol2')
        #entry_data = csd_identifier_entry.to_string('mol2')

        # record = [csd_identifier, molecule_data, crystal_data, entry_data, str(molecule_smiles), hbond_donors, hbond_acceptors, has_disorder, has_3d_structure, is_organometallic, is_polymeric, is_organic, r_factor, molecular_weight, temperature, rotatable_bonds, 1, 'success']
        #print(record)
        #record = [csd_identifier, molecule_data, crystal_data, entry_data, molecule_smiles, 1, 'success']
        # molecule_data, crystal_data, entry_data, 

        record = [csd_identifier, molecule_coords, molecule_elems, str(molecule_smiles), hbond_donors, hbond_acceptors, has_disorder, has_3d_structure, is_organometallic, is_polymeric, is_organic, r_factor, molecular_weight, temperature, rotatable_bonds, 1, 'success']
        records = [record]
        db.insert(table_idx, records, bucket=bucket)
        print("Elapsed", time.time() - start_time)
    except Exception as e:
        print(e)
        # 'error', 'error', 'error', 
        #record = [input_data, 'error', 'error', 'error', 'error', 'error', 'error', 'error', 'error', 'error', 'error', 'error', 'error', 'error', 'error', 0, 0, str(e)]
        record = [csd_identifier, 'error', 'error', 'error', 0, 0, 0, 0, 0, 0, 0, 'error', 'error', 'error', 'error', 0, str(e)]
        records = [record]
        db.insert(table_idx, records, bucket=bucket)
