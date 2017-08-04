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
#from utils import smina_param

import numpy as np 
import pandas as pd 
import db_config 
from db import AffinityDatabase

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

    def commit(self):
        print ('\n\n\n\n\n\n\n\ncommit\n\n\n\n\n\n\n\n')
        db = AffinityDatabase()
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


def monitering(bucket):
    while (True):
        time.sleep(60)
        #if bucket.size() > 10:
        bucket.commit()


def run_multiprocess(target_list, func, monitering, bucket):
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


    p = multiprocessing.Process(target=monitering, args=(bucket,))

    pool = multiprocessing.Pool(db_config.process_num)
    pool.map_async(func, target_list)

    p.start()

    pool.close()
    pool.join()

    p.terminate()
    p.join()

    bucket.commit()


class db_operator(object):
    def __init__(self, FLAGS, db):
        self.db = db
        self.FLAGS = FLAGS
        self.data_func_dict = {
            'download':self.data_download,
            'split_ligand':self.data_split_ligand,
            'split_receptor':self.data_split_ligand
        }

        self.create_func_dict = {
            'download':self.create_download,
            'split_ligand':self.create_split_ligand,
            'split_receptor':self.create_split_receptor
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



        
    def prepare_create(self):
        action = self.FLAGS.action
        if not action in self.create_func_dict.keys():
            raise Exception("action {} unrecognized".format(action))

        create_func = self.create_func_dict[action]
        table_param = create_func()
        func_name = table_param['func']

        table_type = func_name
        data_type = func_name

        table_idx = self.db.create_table(table_type, table_param)

        data = self.prepare_data(data_type, table_idx, table_param)

        return table_idx, table_param, data  


    def prepare_data(self, func_name, table_idx, table_param, progress=False):
        if not func_name in self.data_func_dict.keys():
            raise Exception("function name {} unrecognized ".format(func_name))


        data_func = self.data_func_dict[func_name]
        data = data_func(table_idx, table_param, progress)

        return data


    def data_download(self, table_idx, table_param, progress=False):
        
        if progress:
            total = len(open('/Users/Will/projects/reformat/new_branch/core/DB/datasets/VDS1/data/main_pdb_target_list.txt').readline().strip().split(','))
            finished = self.db.get_num_all_success(table_idx)
            failed = self.db.get_num_all_failed(table_idx)
            return (total, finished, failed)

        else:

            download_list = open('/Users/Will/projects/reformat/new_branch/core/DB/datasets/VDS1/data/main_pdb_target_list.txt').readline().strip().split(',')
            finished_list = self.db.get_all_success(table_idx)
            failed_list = self.db.get_all_failed(table_idx)

            if self.FLAGS.retry_failed:
                rest_list = list(set(download_list) - set(finished_list) | set(failed_list))
            else:
                rest_list =list(set(download_list) - set(finished_list) - set(failed_list)) 

            total = len(set(download_list))
            finished = len(set(finished_list)-set(failed_list))
            failed = len(set(failed_list))


            return rest_list   

    def data_split_ligand(self, table_idx, table_param, progress=False):

        if progress:
            download_idx = table_param['download_idx']
            total = self.db.get_num_all_success(download_idx)
            finished = self.db.get_num_all_success(table_idx)
            failed = self.db.get_num_all_failed(table_idx)
            return (total, finished, failed)

        else:

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


            return rest_list   

    def data_split_receptor(self, table_idx, table_param, progress=False):

        if progress:
            download_idx = table_param['download_idx']
            total = self.db.get_num_all_success(download_idx)
            finished = self.db.get_num_all_success(table_idx)
            failed = self.db.get_num_all_failed(table_idx)
            return (total, finished, failed)            

        else:

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

            return rest_list  

    def prepare_continue(self):
        
        if self.FLAGS.table_idx is None:
            raise Exception("table_idx required")


        table_idx = self.FLAGS.table_idx
        table_name, table_param = self.db.get_table(table_idx)

        func_name = table_param['func']
        
        table_type = func_name
        data_type = func_name

        data = self.prepare_data(data_type, table_idx, table_param)
        
        return table_idx, table_param, data

    def db_delete(self):
        if self.FLAGS.table_idx is None:
            raise Exception('table_idx required')

        table_idx = self.FLAGS.table_idx
        self.db.delete_table(table_idx)





    def db_progress(self):
        if self.FLAGS.table_idx is None:
            raise Exception('table_idx required')
        
        table_idx = self.FLAGS.table_idx

        if table_idx:
            table_idxes = [table_idx]
        else:
            table_idxes = sorted(self.db.get_all_dix())


        print("Progress\n")
        if len(table_idxes):
            print("Total jobs |  Finished  | Finished(%) |   Failed   |  Failed(%)  |   Remain   |  Remain(%)  | Table name ")
        for table_idx in table_idxes:
            table_name, table_param = self.db.get_table(table_idx)
            
            func_name = table_param['func']
            data_type = func_name

            if func_name == 'smina_dock':
                table_type = 'docked_ligand'
                data_type = 'dock'
            elif func_name == 'reorder':
                table_type = 'reorder_ligand'
                data_type = 'reorder'
            else:
                table_type = func_name
                data_type = func_name            
                
            total, finished, failed = self.prepare_data(data_type, table_idx, table_param, progress=True)
            print( "{:<13d} {:<11d} {:<15.2f} {:<11d} {:<14.2f} {:<11d} {:<12.2f} {}". \
                    format(total,
                        finished, 100.*finished/total  if total else 0,
                        failed, 100.*failed/total if total else 0,
                        total - finished - failed, 100.*(total-finished-failed)/total if total else 0,
                        table_name))

    def db_param(self):
        if self.FLAGS.table_idx is None:
            raise Exception('table_idx required')

        table_idx = self.FLAGS.table_idx

        table_name, table_param = self.b.get_table(table_idx)

        print("Parameter for Table: {}".format(table_name))
        pprint.pprint(table_param)