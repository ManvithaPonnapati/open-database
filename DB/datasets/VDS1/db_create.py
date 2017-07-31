# GET JOB DATA ?


    if func_name == 'smina_dock':
        table_type = 'docked_ligand'
        data_type = 'dock'
    elif func_name == 'reorder':
        table_type = 'reorder_ligand'
        data_type = 'reorder'


    elif func_name in ['split_ligand','split_receptor']:
        download_idx = table_param['download_idx']
        download_list = db.get_all_success(download_idx)

        finished_list = db.get_all_success(table_idx)
        finished_list = map(lambda x:(x[0],),finished_list)
        failed_list = db.get_all_failed(table_idx)
        failed_list = map(lambda x:(x[0],), failed_list)

        if FLAGS.orchestra:
            jobindex = FLAGS.jobindex 
            jobsize = FLAGS.jobsize
            download_list = sorted(list(set(download_list)))[jobindex-1::jobsize]

        if FLAGS.retry_failed:
            rest_list = list(set(download_list) - set(finished_list) | set(failed_list))
        else:
            rest_list = list(set(download_list) - set(finished_list) - set(failed_list))

        total = len(set(download_list))
        finished = len(set(finished_list)-set(failed_list))
        failed = len(set(failed_list))

    elif func_name in ['reorder', 'dock']:
        rec_idx = table_param['receptor_idx']
        rec_list = db.get_all_success(rec_idx)

        lig_idx = table_param['ligand_idx']
        lig_list = db.get_all_success(lig_idx)

        finished_list = db.get_all_success(table_idx)
        failed_list = db.get_all_failed(table_idx)

        if FLAGS.orchestra:
            jobindex = FLAGS.jobindex 
            jobsize = FLAGS.jobsize
            rest_list = sorted(list(set(rest_list)))[jobindex-1::jobsize]

        if FLAGS.retry_failed:
            rest_list = list(set(rec_list) & set(lig_list) - set(finished_list) | set(failed_list))
        else:
            rest_list = list(set(rec_list) & set(lig_list) - set(finished_list) - set(failed_list))

        total = len(set(rec_list) & set(lig_list))
        finished = len(set(finished_list)-set(failed_list))
        failed = len(set(failed_list))

    elif func_name in ['rmsd', 'overlap']:
        cry_idx = table_param['crystal_idx']
        cry_list = db.get_all_success(cry_idx)

        doc_idx = table_param['docked_idx']
        doc_list = db.get_all_success(doc_idx)

        finished_list = db.get_all_success(table_idx)
        finished_list = map(lambda x: x[:-1], finished_list)
        failed_list = db.get_all_failed(table_idx)
        failed_list = map(lambda x: x[:-1], failed_list)

        if FLAGS.orchestra:
            jobindex = FLAGS.jobindex 
            jobsize = FLAGS.jobsize
            rest_list = sorted(list(set(rest_list)))[jobindex-1::jobsize] 
 
        if FLAGS.retry_failed:
            rest_list = list(set(cry_list) & set(doc_list) - set(finished_list) | set(failed_list))
        else:
            rest_list = list(set(cry_list) & set(doc_list) - set(finished_list) - set(failed_list))

        total = len(set(cry_list) & set(doc_list))
        finished = len(set(finished_list)-set(failed_list))
        failed = len(set(failed_list))

    elif func_name == 'native_contact':
        rec_idx = table_param['receptor_idx']
        rec_list = db.get_all_success(rec_idx)

        cry_idx = table_param['crystal_idx']
        cry_list = db.get_all_success(cry_idx)

        doc_idx = table_param['docked_idx']
        doc_list = db.get_all_success(doc_idx)

        finished_list = db.get_all_success(table_idx)
        finished_list = map(lambda x: x[:-1], finished_list)
        failed_list = db.get_all_failed(table_idx)
        failed_list = map(lambda x: x[:-1], failed_list)

        if FLAGS.orchestra:
            jobindex = FLAGS.jobindex 
            jobsize = FLAGS.jobsize
            rest_list = sorted(list(set(rest_list)))[jobindex-1::jobsize]

        if FLAGS.retry_failed:
            rest_list = list(set(rec_list) & set(cry_list) & set(doc_list) - set(finished_list) | set(failed_list))
        else:
            rest_list = list(set(rec_list) & set(cry_list) & set(doc_list) - set(finished_list) - set(failed_list))

        total = len(set(rec_list) & set(cry_list) & set(doc_list))
        finished = len(set(finished_list)- set(failed_list))
        failed = len(set(failed_list))
    elif func_name == 'binding_affinity':
        
        finished_list = db.get_all_success(table_idx)
        failed_list = db.get_all_failed(table_idx)

        total = len(set(finished_list) | set(failed_list))
        finished = len(set(finished_list) - set(failed_list))
        failed = len(set(failed_list))

        # binding affinity finished at the first time it launched
        # no rest entry left to continue
        rest_list = [[]]

    elif func_name == 'exclusion':
        finished_list = db.get_all_success(table_idx)
        failed_list = db.get_all_failed(table_idx)

        total = len(set(finished_list) | set(failed_list))
        finished = len(set(finished_list) - set(failed_list))
        failed = len(set(failed_list))

        rest_list = [[]]

    else:
        raise Exception("unknown func_name %s" % func_name)

    if progress:
        return (total, finished, failed)
    else:
        return rest_list

def db_create():
    print('Action ', FLAGS.action)
    if FLAGS.action == 'download':
        if FLAGS.folder_name is None:
            raise Exception("folder_name required")

        folder_name = FLAGS.folder_name
        table_param = {
            'func':'download',
            'output_folder': folder_name,
        }

        }

    elif FLAGS.action == 'insert_column':
        """
        python database_create.py --create --action=insert_column --column_name=[column1, column2, ...] --column_dtype=[column1Type, column2Type, ...] --folder_name=insert_column --download_idx=[table_id]
        """
        if FLAGS.folder_name is None:
            raise Exception("folder_name required")
        if FLAGS.download_idx is None:
            raise Exception('download_idx required')
        folder_name = FLAGS.folder_name
        download_idx = FLAGS.download_idx
        column_name = FLAGS.column_name
        column_dtype = FLAGS.column_dtype
        column_data = FLAGS.column_data
        #FIX THIS! Just for testing..
        download_folder = db.get_folder(download_idx)
        table_param = {
            'func':'insert_column',
            'output_folder':folder_name,
            'download_idx': download_idx,
            'column_name': column_name,
            'column_dtype': column_dtype,
            'input_download_folder':'{}_{}'.format(download_idx, download_folder),
            'depend':[download_idx],
            'column_data':column_data
        }

    elif FLAGS.action == 'split_receptor':
        if FLAGS.folder_name is None:
            raise Exception("folder_name required")
        if FLAGS.download_idx is None:
            raise Exception('download_idx required')

        folder_name = FLAGS.folder_name
        download_idx = FLAGS.download_idx
        download_folder = db.get_folder(download_idx)
        table_param = {
            'func':'split_receptor',
            'output_folder':folder_name,
            'download_idx':download_idx,
            'input_download_folder':'{}_{}'.format(download_idx, download_folder),
            'depend':[download_idx]
        }


    elif FLAGS.action == 'split_ligand':
        if FLAGS.folder_name is None:
            raise Exception("folder_name required")
        if FLAGS.download_idx is None:
            raise Exception('download_idx required')
        
        folder_name = FLAGS.folder_name
        download_idx = FLAGS.download_idx
        download_folder = db.get_folder(download_idx)
        table_param = {
            'func':'split_ligand',
            'output_folder': folder_name,
            'download_idx': download_idx,
            'input_download_folder': '{}_{}'.format(download_idx, download_folder),
            'depend':[download_idx],
            'fit_box_size':20
        } 


        
    elif FLAGS.action == 'reorder':
        if FLAGS.folder_name is None:
            raise Exception("folder_name required")
        if FLAGS.receptor_idx is None:
            raise Exception('receptor_idx required')
        if FLAGS.ligand_idx is None:
            raise Exception('ligand_idx required')

        folder_name = FLAGS.folder_name
        receptor_idx = FLAGS.receptor_idx
        receptor_folder = db.get_folder(receptor_idx)
        ligand_idx = FLAGS.ligand_idx
        ligand_folder = db.get_folder(ligand_idx)
        table_param = {
            'func': 'reorder',
            'output_folder': folder_name,
            'receptor_idx':receptor_idx,
            'input_receptor_folder':'{}_{}'.format(receptor_idx,receptor_folder),
            'ligand_idx': ligand_idx,
            'input_ligand_folder': '{}_{}'.format(ligand_idx, ligand_folder),
            'depend':[receptor_idx, ligand_idx],
            'smina_param':config.smina_dock_pm['reorder']
        }


    elif FLAGS.action == 'smina_dock':
        if FLAGS.folder_name is None:
            raise Exception("folder_name required")
        if FLAGS.receptor_idx is None:
            raise Exception('receptor_idx required')
        if FLAGS.ligand_idx is None:
            raise Exception('ligand_idx required')
        if FLAGS.param is None:
            raise Exception('param required')

        dock_param = FLAGS.param
        if not dock_param in config.smina_dock_pm.keys():
            raise KeyError("dock param {} doesn't exists. ".format(dock_param)\
                            + "available options are: {}".format(', '.join(config.smina_dock_pm.keys())))
        dock_param = config.smina_dock_pm[dock_param]
        folder_name = FLAGS.folder_name
        receptor_idx = FLAGS.receptor_idx
        receptor_folder = db.get_folder(receptor_idx)
        ligand_idx = FLAGS.ligand_idx
        ligand_folder = db.get_folder(ligand_idx)
        table_param = {
            'func': 'smina_dock',
            'output_folder': folder_name,
            'receptor_idx':receptor_idx,
            'input_receptor_folder': '{}_{}'.format(receptor_idx, receptor_folder),
            'ligand_idx': ligand_idx,
            'input_ligand_folder': '{}_{}'.format(ligand_idx, ligand_folder),
            'depend':[receptor_idx, ligand_idx],
            'smina_param':dock_param
        }

    
    elif FLAGS.action == 'rmsd':
        if FLAGS.crystal_idx is None:
            raise Exception('crystal_idx required')
        if FLAGS.docked_idx is None:
            raise Exception('docked_idx required')

        crystal_idx = FLAGS.crystal_idx
        crystal_folder = db.get_folder(crystal_idx)
        docked_idx = FLAGS.docked_idx
        docked_folder = db.get_folder(docked_idx)
        table_param = {
            'func':'rmsd',
            'crystal_idx': crystal_idx,
            'input_crystal_folder':'{}_{}'.format(crystal_idx, crystal_folder),
            'docked_idx': docked_idx,
            'input_docked_folder':'{}_{}'.format(docked_idx, docked_folder),
            'depend':[crystal_idx, docked_idx]
        }


    elif FLAGS.action == 'overlap':
        if FLAGS.crystal_idx is None:
            raise Exception('crystal_idx require')
        if FLAGS.docked_idx is None:
            raise Exception('docked_idx required')
        if FLAGS.param is None:
            raise Exception('param required')
        overlap_param = FLAGS.param
        if not overlap_param in config.overlap_pm.keys():
            raise KeyError("dock param {} doesn't exists. ".format(overlap_param) \
                           + "available options are: {}".format(', '.join(config.overlap_pm.keys())))

        crystal_idx = FLAGS.crystal_idx
        crystal_folder = db.get_folder(crystal_idx)
        docked_idx = FLAGS.docked_idx
        docked_folder = db.get_folder(docked_idx)
        
        
        table_param = {
            'func':'overlap',
            'crystal_idx': crystal_idx,
            'input_crystal_folder':'{}_{}'.format(crystal_idx, crystal_folder),
            'docked_idx': docked_idx,
            'input_docked_folder':'{}_{}'.format(docked_idx, docked_folder),
            'depend':[crystal_idx, docked_idx],
            'overlap_param':config.overlap_pm[overlap_param]
        }
        #table_param.update(overlap_param)
        


    elif FLAGS.action == 'native_contact':
        if FLAGS.receptor_idx is None:
            raise Exception('receptor_idx required')
        if FLAGS.crystal_idx is None:
            raise Exception('crystal_idx require')
        if FLAGS.docked_idx is None:
            raise Exception('docked_idx required')
        if FLAGS.param is None:
            raise Exception('param required')
        native_contact_param = FLAGS.param
        if not native_contact_param in config.native_contact_pm.keys():
            raise KeyError("dock param {} doesn't exists. ".format(native_contact_param) \
                           + "available options are: {}".format(', '.join(config.native_contact_pm.keys())))

        native_contact_param = config.native_contact_pm[native_contact_param]

        receptor_idx = FLAGS.receptor_idx
        receptor_folder = db.get_folder(receptor_idx)
        crystal_idx = FLAGS.crystal_idx
        crystal_folder = db.get_folder(crystal_idx)
        docked_idx = FLAGS.docked_idx
        docked_folder = db.get_folder(docked_idx)
        table_param = {
            'func':'native_contact',
            'receptor_idx': receptor_idx,
            'input_receptor_folder':'{}_{}'.format(receptor_idx, receptor_folder),
            'crystal_idx': crystal_idx,
            'input_crystal_folder':'{}_{}'.format(crystal_idx, crystal_folder),
            'docked_idx': docked_idx,
            'input_docked_folder':'{}_{}'.format(docked_idx, docked_folder),
            'depend': [receptor_idx, crystal_idx, docked_idx],
        }

        table_param.update(native_contact_param)
