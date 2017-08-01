# GET JOB DATA ?
import os 
import sys 
sys.path.append('../..')
import re 
import logging
import time 
import pprint 
import argparse 
import subprocess 
import multiprocessing 
from multiprocessing.managers import BaseManager, NamespaceProxy
from glob import glob
from functools import partial
import config
from db_create import get_baseparser, monitering, run_multiprocess, db_creator, db_continue, db_delete, db_progress, db_param, DBManager
from db import AffinityDatabase
from db_action import DatabaseAction as db_action_dict
from action import DatabaseAction as action_dict 

action_dict.update(db_action_dict)

db = AffinityDatabase()
manager = DBManager()
manager.start()
bucket = manager.bucket() 

class db_create(db_creator):
    def __init__(self, FLAGS, db):
        super(db_create, self).__init__(FLAGS, db)

        create_func_dict = {
            'reorder':self.data_reorder,
            'dock':self.data_dock,
            'rmsd':self.data_rmsd,
            'overlap':self.data_overlap,
            'native_contact':self.data_native_contact            
        }

        data_func_dict = {
            'reorder':self.create_reorder,
            'dock':self.create_dock,
            'rmsd':self.create_rmsd,
            'overlap':self.create_overlap,
            'native_contact':self.create_native_contact            
        }

        self.create_func_dict.update(create_func_dict)

        self.data_func_dict.update(data_func_dict)

        self.run()

    def run(self):
        table_idx, table_param, data = self.run_create()
        func_name = table_param['func']
        func = action_dict[func_name]
        run_multiprocess(data, partial(func, bucket, table_idx, table_param), monitering, bucket, db)

    def create_reorder(self):
        if self.FLAGS.folder_name is None:
            raise Exception("folder_name required")
        if self.FLAGS.receptor_idx is None:
            raise Exception('receptor_idx required')
        if self.FLAGS.ligand_idx is None:
            raise Exception('ligand_idx required')

        folder_name = self.FLAGS.folder_name
        receptor_idx = self.FLAGS.receptor_idx
        receptor_folder = self.db.get_folder(receptor_idx)
        ligand_idx = self.FLAGS.ligand_idx
        ligand_folder = self.db.get_folder(ligand_idx)
        table_param = {
            'func': 'reorder',
            'output_folder': folder_name,
            'receptor_idx':receptor_idx,
            'input_receptor_folder':'{}_{}'.format(receptor_idx,receptor_folder),
            'ligand_idx': ligand_idx,
            'input_ligand_folder': '{}_{}'.format(ligand_idx, ligand_folder),
            'depend':[receptor_idx, ligand_idx],
            'smina_param':config.dock_pm['reorder']
        }

        return table_param

    def create_dock(self):
        if self.FLAGS.folder_name is None:
            raise Exception("folder_name required")
        if self.FLAGS.receptor_idx is None:
            raise Exception('receptor_idx required')
        if self.FLAGS.ligand_idx is None:
            raise Exception('ligand_idx required')
        if self.FLAGS.param is None:
            raise Exception('param required')

        dock_param = self.FLAGS.param
        if not dock_param in config.dock_pm.keys():
            raise KeyError("dock param {} doesn't exists. ".format(dock_param)\
                            + "available options are: {}".format(', '.join(config.dock_pm.keys())))
        dock_param = config.dock_pm[dock_param]
        folder_name = self.FLAGS.folder_name
        receptor_idx = self.FLAGS.receptor_idx
        receptor_folder = self.db.get_folder(receptor_idx)
        ligand_idx = self.FLAGS.ligand_idx
        ligand_folder = self.db.get_folder(ligand_idx)
        table_param = {
            'func': 'dock',
            'output_folder': folder_name,
            'receptor_idx':receptor_idx,
            'input_receptor_folder': '{}_{}'.format(receptor_idx, receptor_folder),
            'ligand_idx': ligand_idx,
            'input_ligand_folder': '{}_{}'.format(ligand_idx, ligand_folder),
            'depend':[receptor_idx, ligand_idx],
            'smina_param':dock_param
        }

        return table_param

    def create_rmsd(self):
        if self.FLAGS.crystal_idx is None:
            raise Exception('crystal_idx required')
        if self.FLAGS.docked_idx is None:
            raise Exception('docked_idx required')

        crystal_idx = self.FLAGS.crystal_idx
        crystal_folder = self.db.get_folder(crystal_idx)
        docked_idx = self.FLAGS.docked_idx
        docked_folder = self.db.get_folder(docked_idx)
        table_param = {
            'func':'rmsd',
            'crystal_idx': crystal_idx,
            'input_crystal_folder':'{}_{}'.format(crystal_idx, crystal_folder),
            'docked_idx': docked_idx,
            'input_docked_folder':'{}_{}'.format(docked_idx, docked_folder),
            'depend':[crystal_idx, docked_idx]
        }

        return table_param

    def create_overlap(self):
        if self.FLAGS.crystal_idx is None:
            raise Exception('crystal_idx require')
        if self.FLAGS.docked_idx is None:
            raise Exception('docked_idx required')
        if self.FLAGS.param is None:
            raise Exception('param required')
        overlap_param = self.FLAGS.param
        if not overlap_param in config.overlap_pm.keys():
            raise KeyError("dock param {} doesn't exists. ".format(overlap_param) \
                           + "available options are: {}".format(', '.join(config.overlap_pm.keys())))

        crystal_idx = self.FLAGS.crystal_idx
        crystal_folder = self.db.get_folder(crystal_idx)
        docked_idx = self.FLAGS.docked_idx
        docked_folder = self.db.get_folder(docked_idx)
        
        
        table_param = {
            'func':'overlap',
            'crystal_idx': crystal_idx,
            'input_crystal_folder':'{}_{}'.format(crystal_idx, crystal_folder),
            'docked_idx': docked_idx,
            'input_docked_folder':'{}_{}'.format(docked_idx, docked_folder),
            'depend':[crystal_idx, docked_idx],
            'overlap_param':config.overlap_pm[overlap_param]
        }

        return table_param

    def create_native_contact(self):
        if self.FLAGS.receptor_idx is None:
            raise Exception('receptor_idx required')
        if self.FLAGS.crystal_idx is None:
            raise Exception('crystal_idx require')
        if self.FLAGS.docked_idx is None:
            raise Exception('docked_idx required')
        if self.FLAGS.param is None:
            raise Exception('param required')
        native_contact_param = self.FLAGS.param
        if not native_contact_param in config.native_contact_pm.keys():
            raise KeyError("dock param {} doesn't exists. ".format(native_contact_param) \
                           + "available options are: {}".format(', '.join(config.native_contact_pm.keys())))

        native_contact_param = config.native_contact_pm[native_contact_param]

        receptor_idx = self.FLAGS.receptor_idx
        receptor_folder = self.db.get_folder(receptor_idx)
        crystal_idx = self.FLAGS.crystal_idx
        crystal_folder = self.db.get_folder(crystal_idx)
        docked_idx = self.FLAGS.docked_idx
        docked_folder = self.db.get_folder(docked_idx)
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

        return table_param

    def data_split_ligand(self, table_idx, table_param, progress=False):

        download_idx = table_param['download_idx']
        download_list = self.db.get_all_success(download_idx)

        finished_list = self.db.get_all_success(table_idx)
        finished_list = map(lambda x:(x[0],),finished_list)
        failed_list = self.db.get_all_failed(table_idx)
        failed_list = map(lambda x:(x[0],), failed_list)

        if self.FLAGS.retry_failed:
            rest_list = list(set(download_list) - set(finished_list) | set(failed_list))
        else:
            rest_list = list(set(download_list) - set(finished_list) - set(failed_list))

        total = len(set(download_list))
        finished = len(set(finished_list)-set(failed_list))
        failed = len(set(failed_list))

        if progress:
            return (total, finished, failed)
        else:
            return rest_list   

    def data_split_receptor(self, table_idx, table_param, progress=False):

        download_idx = table_param['download_idx']
        download_list = self.db.get_all_success(download_idx)

        finished_list = self.db.get_all_success(table_idx)
        finished_list = map(lambda x:(x[0],),finished_list)
        failed_list = self.db.get_all_failed(table_idx)
        failed_list = map(lambda x:(x[0],), failed_list)

        if self.FLAGS.retry_failed:
            rest_list = list(set(download_list) - set(finished_list) | set(failed_list))
        else:
            rest_list = list(set(download_list) - set(finished_list) - set(failed_list))

        total = len(set(download_list))
        finished = len(set(finished_list)-set(failed_list))
        failed = len(set(failed_list))

        if progress:
            return (total, finished, failed)
        else:
            return rest_list   

    def data_reorder(self, table_idx, table_param, progress=False):

        rec_idx = table_param['receptor_idx']
        rec_list = self.db.get_all_success(rec_idx)

        lig_idx = table_param['ligand_idx']
        lig_list = self.db.get_all_success(lig_idx)

        finished_list = self.db.get_all_success(table_idx)
        failed_list = self.db.get_all_failed(table_idx)

        if self.FLAGS.retry_failed:
            rest_list = list(set(rec_list) & set(lig_list) - set(finished_list) | set(failed_list))
        else:
            rest_list = list(set(rec_list) & set(lig_list) - set(finished_list) - set(failed_list))

        total = len(set(rec_list) & set(lig_list))
        finished = len(set(finished_list)-set(failed_list))
        failed = len(set(failed_list))

        if progress:
            return (total, finished, failed)
        else:
            return rest_list   


    def data_dock(self, table_idx, table_param, progress=False):

        rec_idx = table_param['receptor_idx']
        rec_list = self.db.get_all_success(rec_idx)

        lig_idx = table_param['ligand_idx']
        lig_list = self.db.get_all_success(lig_idx)

        finished_list = self.db.get_all_success(table_idx)
        failed_list = self.db.get_all_failed(table_idx)

        if self.FLAGS.retry_failed:
            rest_list = list(set(rec_list) & set(lig_list) - set(finished_list) | set(failed_list))
        else:
            rest_list = list(set(rec_list) & set(lig_list) - set(finished_list) - set(failed_list))

        total = len(set(rec_list) & set(lig_list))
        finished = len(set(finished_list)-set(failed_list))
        failed = len(set(failed_list))

        if progress:
            return (total, finished, failed)
        else:
            return rest_list   

    def data_rmsd(self, table_idx, table_param, progress=False):

        cry_idx = table_param['crystal_idx']
        cry_list = self.db.get_all_success(cry_idx)

        doc_idx = table_param['docked_idx']
        doc_list = self.db.get_all_success(doc_idx)

        finished_list = self.db.get_all_success(table_idx)
        finished_list = map(lambda x: x[:-1], finished_list)
        failed_list = self.db.get_all_failed(table_idx)
        failed_list = map(lambda x: x[:-1], failed_list)

        if self.FLAGS.retry_failed:
            rest_list = list(set(cry_list) & set(doc_list) - set(finished_list) | set(failed_list))
        else:
            rest_list = list(set(cry_list) & set(doc_list) - set(finished_list) - set(failed_list))

        total = len(set(cry_list) & set(doc_list))
        finished = len(set(finished_list)-set(failed_list))
        failed = len(set(failed_list))

        if progress:
            return (total, finished, failed)
        else:
            return rest_list   

    def data_overlap(self, table_idx, table_param, progress=False):

        cry_idx = table_param['crystal_idx']
        cry_list = self.db.get_all_success(cry_idx)

        doc_idx = table_param['docked_idx']
        doc_list = self.db.get_all_success(doc_idx)

        finished_list = self.db.get_all_success(table_idx)
        finished_list = map(lambda x: x[:-1], finished_list)
        failed_list = self.db.get_all_failed(table_idx)
        failed_list = map(lambda x: x[:-1], failed_list)

        if self.FLAGS.retry_failed:
            rest_list = list(set(cry_list) & set(doc_list) - set(finished_list) | set(failed_list))
        else:
            rest_list = list(set(cry_list) & set(doc_list) - set(finished_list) - set(failed_list))

        total = len(set(cry_list) & set(doc_list))
        finished = len(set(finished_list)-set(failed_list))
        failed = len(set(failed_list))

        if progress:
            return (total, finished, failed)
        else:
            return rest_list            

    def data_native_contact(self, table_idx, table_param, progress=False):

        rec_idx = table_param['receptor_idx']
        rec_list = self.db.get_all_success(rec_idx)

        cry_idx = table_param['crystal_idx']
        cry_list = self.db.get_all_success(cry_idx)

        doc_idx = table_param['docked_idx']
        doc_list = self.db.get_all_success(doc_idx)

        finished_list = self.db.get_all_success(table_idx)
        finished_list = map(lambda x: x[:-1], finished_list)
        failed_list = self.db.get_all_failed(table_idx)
        failed_list = map(lambda x: x[:-1], failed_list)

        if self.FLAGS.retry_failed:
            rest_list = list(set(rec_list) & set(cry_list) & set(doc_list) - set(finished_list) | set(failed_list))
        else:
            rest_list = list(set(rec_list) & set(cry_list) & set(doc_list) - set(finished_list) - set(failed_list))

        total = len(set(rec_list) & set(cry_list) & set(doc_list))
        finished = len(set(finished_list)- set(failed_list))
        failed = len(set(failed_list))

        if progress:
            return (total, finished, failed)
        else:
            return rest_list


def get_args():
    parser = get_baseparser()
    parser.add_argument('--databases',type=str, default='VDS1')
    FLAGS, unparsed = parser.parse_known_args()
    return FLAGS

def main():
    FLAGS = get_args()
    if FLAGS.db_create:
        db_create(FLAGS, db)
    if FLAGS.db_continue:
        db_continue(FLAGS, db)
    if FLAGS.db_delete:
        db_delete(FLAGS, db)
    if FLAGS.db_progress:
        db_progress(FLAGS, db)
    if FLAGS.db_param:
        db_param(FLAGS, db)


if __name__ == '__main__':
    main()
