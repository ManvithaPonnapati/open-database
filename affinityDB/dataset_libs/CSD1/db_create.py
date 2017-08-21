    #CSD upload
    elif FLAGS.action == 'local_csd_load':
        if FLAGS.folder_name is None:
            raise Exception("folder_name required")
        folder_name = FLAGS.folder_name
        table_param = {
            'func':'local_csd_load',
            'output_folder': folder_name,
            'solvent_smiles':np.load('/home/urops/ryanh/solvent_smiles.npy').tolist(),
            'all_smiles':np.load('/home/urops/ryanh/csd_smiles.npy').tolist()
        }
