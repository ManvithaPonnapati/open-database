# database create module

from __future__ import print_function

import os
import sys
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
from utils import smina_param

import numpy as np 
import pandas as pd 
import db_config 


class Stmt_bucket(object):
    ''' 
    collect sql command from threads
    insrt them into 

    '''
    def __init__(self):
        self.bucket = []

    def size(self):
        return len(self.bucket)

    def insert(self, stmt):
        self.bucket.append(stmt)

    def commit(self, db):
        #db = AffinityDatabase()
        for stmt in self.bucket:
            db.conn.execute(stmt)

        db.conn.commit()
        self.bucket = []

class DBManager(BaseManager):
    pass

class DBProxy(NamespaceProxy):
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__', 'insert', 'commit', 'size')

    def insert(self, *args, **kwargs):
        callmethod = object.__getattribute__(self, '_callmethod')
        return callmethod(self.insert.__name__, args, kwargs)

    def commit(self, *args, **kwargs):
        callmethod = object.__getattribute__(self, '_callmethod')
        return callmethod(self.commit.__name__, args, kwargs)

    def size(self, *args, **kwargs):
        callmethod = object.__getattribute__(self, '_callmethod')
        return callmethod(self.size.__name__, args, kwargs)


DBManager.register("bucket", Stmt_bucket, DBProxy)




def get_baseparser():
    parser = argparse.ArgumentParser(description='Affinity Database')
    parser.add_argument('--create',dest='db_create', action='store_true')
    parser.add_argument('--continue',dest='db_continue', action='store_true')
    parser.add_argument('--delete',dest='db_delete', action='store_true')
    parser.add_argument('--progress', dest='db_progress', action='store_true')
    parser.add_argument('--list_param', dest='db_param',action='store_true')
    parser.add_argument('--action', type=str)
    parser.add_argument('--param', type=str)
    parser.add_argument('--retry_failed', action='store_true')
    parser.add_argument('--folder_name', type=str)
    parser.add_argument('--table_idx', type=int)
    parser.add_argument('--receptor_idx', type=int)
    parser.add_argument('--ligand_idx', type=int)
    parser.add_argument('--crystal_idx', type=int)
    parser.add_argument('--docked_idx', type=int)
    parser.add_argument('--column_name', type=str)
    parser.add_argument('--column_dtype', type=str)
    parser.add_argument('--download_idx', type=int)
    #parser.add_argument('--orchestra',action='store_true')
    parser.add_argument('--jobindex', type=int)
    parser.add_argument('--jobsize', type=int, default=1)
    parser.add_argument('--column_data', type=str)

    return parser


def monitering(bucket, db):
    while (True):
        time.sleep(60)
        if bucket.size() > 1000:
            bucket.commit(db)


def run_multiprocess(target_list, func, monitering, bucket, db):
    logging.basicConfig(level=logging.INFO)
    print(len(target_list))
    start_time = time.time()
    if len(target_list) == 0:
        return
    if type(target_list[0]).__name__ in ['unicode', 'str']:
        target_list = list(target_list)
    else:
        try:
            target_list = map(list, target_list)
        except TypeError:
            pass
    print(len(target_list))


    p = multiprocessing.Process(target=monitering, args=(bucket, db))

    pool = multiprocessing.Pool(db_config.process_num)
    pool.map_async(func, target_list)

    p.start()

    pool.close()
    pool.join()

    p.terminate()
    p.join()

    bucket.commit()


class db_creator(object):
    def __init__(self, FLAGS, db):
        self.db = db
        self.FALGS = FLAGS
        self.data_func_dict{
            'download':self.data_download,
            'split_ligand':self.data_split_ligand,
            'split_receptor':self.data_split_ligand,
            'reorder':self.data_reorder,
            'dock':self.data_dock,
            'rmsd':self.data_rmsd,
            'overlap':self.data_overlap,
            'native_contact':self.data_native_contact
        }

        self.create_func_dict{
            'download':self.create_download,
            'split_ligand':self.create_split_ligand,
            'split_receptor':self.create_split_receptor,
            'reorder':self.create_reorder,
            'dock':self.create_dock,
            'rmsd':self.create_rmsd,
            'overlap':self.create_overlap,
            'native_contact':self.create_native_contact
        }

        
        

    def create_download(self):
        if self.FLAGS.folder_name is None:
            raise Exception("folder_name required")

        folder_name = self.FLAGS.folder_name
        table_param = {
            'func':'download',
            'output_folder': folder_name,
        }

        return table_param

    def create_split_receptor(self):
        if self.FLAGS.folder_name is None:
            raise Exception("folder_name required")
        if self.FLAGS.download_idx is None:
            raise Exception('download_idx required')

        folder_name = self.FLAGS.folder_name
        download_idx = self.FLAGS.download_idx
        download_folder = self.db.get_folder(download_idx)
        table_param = {
            'func':'split_receptor',
            'output_folder':folder_name,
            'download_idx':download_idx,
            'input_download_folder':'{}_{}'.format(download_idx, download_folder),
            'depend':[download_idx]
        }

        return table_param

    def create_split_ligand(self):
        if self.FLAGS.folder_name is None:
            raise Exception("folder_name required")
        if self.FLAGS.download_idx is None:
            raise Exception('download_idx required')
        
        folder_name = self.FLAGS.folder_name
        download_idx = self.FLAGS.download_idx
        download_folder = self.db.get_folder(download_idx)
        table_param = {
            'func':'split_ligand',
            'output_folder': folder_name,
            'download_idx': download_idx,
            'input_download_folder': '{}_{}'.format(download_idx, download_folder),
            'depend':[download_idx],
            'fit_box_size':20
        } 

        return table_param

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
            'smina_param':db_config.smina_dock_pm['reorder']
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
        if not dock_param in db_config.smina_dock_pm.keys():
            raise KeyError("dock param {} doesn't exists. ".format(dock_param)\
                            + "available options are: {}".format(', '.join(db_config.smina_dock_pm.keys())))
        dock_param = db_config.smina_dock_pm[dock_param]
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
        if not overlap_param in db_config.overlap_pm.keys():
            raise KeyError("dock param {} doesn't exists. ".format(overlap_param) \
                           + "available options are: {}".format(', '.join(db_config.overlap_pm.keys())))

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
            'overlap_param':db_config.overlap_pm[overlap_param]
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
        if not native_contact_param in db_config.native_contact_pm.keys():
            raise KeyError("dock param {} doesn't exists. ".format(native_contact_param) \
                           + "available options are: {}".format(', '.join(db_config.native_contact_pm.keys())))

        native_contact_param = db_config.native_contact_pm[native_contact_param]

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

        
    def run_create(self):
        action = self.FLAGS.action
        if not action in self.create_func_dict.keys():
            riase Exception("action {} unrecognized".format(action))

        create_func = self.create_func_dict[action]
        table_param = create_func()
        func_name = table_param['func']

        table_type = func_name
        data_type = func_name

        table_idx = self.db.create_table(table_type, table_param)

        data = self.run_data(data_type, table_idx, table_param)

        return table_idx, table_param, data  


    def run_data(self, data_type, table_idx, table_param, progress=False):
        if not func_name in self.data_func_dict.keys():
            raise Exception("function name {} unrecognized ".format(func_name))

        data_func = self.data_func_dict[func_name]
        data = data_func(table_idx, table_param, progress)

        return data


    def data_download(self, table_idx, table_param, progress=False):

        download_list = open(db_config.list_of_PDBs_to_download).readline().strip().split(',')
        finished_list = self.db.get_all_success(table_idx)
        failed_list = self.db.get_all_failed(table_idx)

        if self.FLAGS.retry_failed:
            rest_list = list(set(download_list) - set(finished_list) | set(failed_list))
        else:
            rest_list =list(set(download_list) - set(finished_list) - set(failed_list)) 

        total = len(set(download_list))
        finished = len(set(finished_list)-set(failed_list))
        failed = len(set(failed_list))

        if progress:
            return (total, finished, failed)
        else:
            return rest_list   

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

def db_continue(FLAGS, db):
    if FLAGS.table_idx is None:
        raise Exception("table_idx required")


    table_idx = FLAGS.table_idx
    table_name, table_param = db.get_table(table_idx)

    func_name = table_param['func']
    func = DatabaseAction[func_name]
    if func_name == 'smina_dock':
        table_type = 'docked_ligand'
        data_type = 'dock'
    elif func_name == 'reorder':
        table_type = 'reorder_ligand'
        data_type = 'reorder'
    else:
        table_type = func_name
        data_type = func_name

    data = get_job_data(data_type, table_idx, table_param)
    run_multiprocess(data, partial(func, bucket,table_idx, table_param))

def db_delete(FLAGS, db):
    if FLAGS.table_idx is None:
        raise Exception('table_idx required')

    table_idx = FLAGS.table_idx
    db.delete_table(table_idx)


def db_progress(FLAGS, db):
    if FLAGS.table_idx is None:
        raise Exception('table_idx required')
    
    table_idx = FLAGS.table_idx

    if table_idx:
        table_idxes = [table_idx]
    else:
        table_idxes = sorted(db.get_all_dix())


    print("Progress\n")
    if len(table_idxes):
        print("Total jobs |  Finished  | Finished(%) |   Failed   |  Failed(%)  |   Remain   |  Remain(%)  | Table name ")
    for table_idx in table_idxes:
        table_name, table_param = db.get_table(table_idx)
        
        func_name = table_param['func']
        if func_name == 'smina_dock':
            data_type = 'dock'
        elif func_name == 'reorder':
            data_type='reorder'
        else:
            data_type = func_name

        
        
        total, finished, failed = get_job_data(data_type, table_idx, table_param, progress=True)
        print( "{:<13d} {:<11d} {:<15.2f} {:<11d} {:<14.2f} {:<11d} {:<12.2f} {}". \
                format(total,
                       finished, 100.*finished/total  if total else 0,
                       failed, 100.*failed/total if total else 0,
                       total - finished - failed, 100.*(total-finished-failed)/total if total else 0,
                       table_name))

def db_param(FLAGS, db):
    if FLAGS.table_idx is None:
        raise Exception('table_idx required')

    table_idx = FLAGS.table_idx

    table_name, table_param = db.get_table(table_idx)

    print("Parameter for Table: {}".format(table_name))
    pprint.pprint(table_param)