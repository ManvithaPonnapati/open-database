from __future__ import print_function

import os
import sys
import re
import logging
import tensorflow as tf
import time
import pprint
import argparse
import subprocess
import multiprocessing
from multiprocessing.managers import BaseManager, NamespaceProxy
from glob import glob
from functools import partial
from utils import smina_param
#import prody
import numpy as np
import pandas as pd
import config
from database_action import DatabaseAction, db
from db import AffinityDatabase
from ccdc import io

class Stmt_bucket(object):
    def __init__(self):
        self.bucket = []

    def size(self):
        return len(self.bucket)

    def insert(self, stmt):
        self.bucket.append(stmt)

    def commit(self):
        db = AffinityDatabase()
        for stmt in self.bucket:
            db.conn.execute(stmt)

        db.conn.commit()
        self.bucket = []

class DBManager(BaseManager):
    pass

class DBProxy(NamespaceProxy):
    _exposed_ = ('__getattribute__','__setattr__','__delattr__','insert','commit','size')

    def insert(self, *args, **kwargs):
        callmethod = object.__getattribute__(self,'_callmethod')
        return callmethod(self.insert.__name__, args, kwargs)

    def commit(self, *args, **kwargs):
        callmethod = object.__getattribute__(self,'_callmethod')
        return callmethod(self.commit.__name__, args, kwargs)

    def size(self, *args, **kwargs):
        callmethod = object.__getattribute__(self,'_callmethod')
        return callmethod(self.size.__name__, args, kwargs)

DBManager.register("bucket", Stmt_bucket, DBProxy)
manager = DBManager()
manager.start()
bucket = manager.bucket()

def monitering(bucket):
    while(True):
        time.sleep(60)
        if bucket.size()> 1000:
            bucket.commit()




FLAGS = None

def get_arguments():
    # FIXME should be auto Parse
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

    FLAGS, unparsed = parser.parse_known_args()
    if FLAGS.orchestra:
        if FLAGS.jobindex is None:
                raise Exception("Jobindex required.")
    return FLAGS

def run_multiprocess(target_list, func):
    tf.logging.set_verbosity(tf.logging.DEBUG)
    logging.basicConfig(level=logging.INFO)
    print(len(target_list))  
    start_time = time.time()
    if len(target_list) == 0:
        return
    if type(target_list[0]).__name__ in ['unicode','str']:
        target_list = list(target_list)
    else:
        try:
            target_list = map(list, target_list)
        except TypeError:
            pass
    print (len(target_list))


    p = multiprocessing.Process(target=monitering, args=(bucket,))

    pool = multiprocessing.Pool(config.process_num)
    pool.map_async(func, target_list)

    p.start()

    pool.close()
    pool.join()

    p.terminate()
    p.join()

    bucket.commit()

        
        #map(func, target_list)


    
def get_job_data(func_name, table_idx, table_param, progress=False):

    if func_name in ['download', 'local_qm9_load', 'local_csd_load']:
        if func_name == 'download':
            download_list = open(config.list_of_PDBs_to_download).readline().strip().split(',') #test with subset
        elif func_name == 'local_csd_load':
            download_list = [entry.identifier for entry in io.EntryReader('CSD')] #list of identifier names, smallsubset to begin with
        else:            
            download_list = open(config.list_of_PDBs_to_download).read().splitlines()      
        finished_list = db.get_all_success(table_idx)
        failed_list = db.get_all_failed(table_idx)

#        if FLAGS.orchestra:
#            jobindex = FLAGS.jobindex 
#            jobsize = FLAGS.jobsize
#            download_list = sorted(list(set(download_list)))[jobindex-1::jobsize]
# FIXME: flags such as this one are not acceptable in any code that is supposed to be used more than once

        if FLAGS.retry_failed:
            rest_list = list(set(download_list) - set(finished_list) | set(failed_list))
        else:
            rest_list =list(set(download_list) - set(finished_list) - set(failed_list))        
        total = len(set(download_list))
        finished = len(set(finished_list)-set(failed_list))
        failed = len(set(failed_list))

    elif func_name == 'insert_column':
        return [table_param['download_idx']]



    else:
        raise Exception("Doesn't support action {}".format(FLAGS.action))


    func_name = table_param['func']
    func = DatabaseAction[func_name]

#    elif func_name == 'insert_column':
#        table_type = db.get_table_type_by_idx(table_param['download_idx'])        
#        data_type = func_name
# FIXME this will not work
    else:
        table_type = func_name
        data_type = func_name

    table_idx = db.create_table(table_type, table_param)
    if func_name == 'insert_column':
        pass
    else:
        data = get_job_data(data_type, table_idx, table_param)    
        run_multiprocess(data, partial(func, bucket, table_idx, table_param))


def db_continue():
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

def db_delete():
    if FLAGS.table_idx is None:
        raise Exception('table_idx required')

    table_idx = FLAGS.table_idx
    db.delete_table(table_idx)

def db_progress():
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


def db_param():
    if FLAGS.table_idx is None:
        raise Exception('table_idx required')

    table_idx = FLAGS.table_idx

    table_name, table_param = db.get_table(table_idx)

    print("Parameter for Table: {}".format(table_name))
    pprint.pprint(table_param)


def main():
    if FLAGS.db_create:
        db_create()
    if FLAGS.db_continue:
        db_continue()
    if FLAGS.db_delete:
        db_delete()
    if FLAGS.db_progress:
        db_progress()
    if FLAGS.db_param:
        db_param()


if __name__ == '__main__':
    FLAGS = get_arguments()
    main()
