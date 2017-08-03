import os
import sys
import re 

import time 
import pprint
import argparse 
import logging

import multiprocessing
from multiprocessing.managers import BaseManager, NamespaceProxy
from glob import glob 
from functools import partial

import numpy as np 
import pandas as pd 
import db_config
from db import AffinityDatabase
from blocks import download, split_ligand, operation

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
            print('stmt '+ stmt)
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
    logging.basicConfig(level=logging.DEBUG)

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
    print('Target list len %d' %len(target_list))

    p = multiprocessing.Process(target=monitering, args=(bucket,))

    pool = multiprocessing.Pool(db_config.process_num)
    # running function outside the 
    func(target_list[0])
    pool.map_async(func, target_list)
    p.start()

    pool.close()
    pool.join()

    p.terminate()
    p.join()

    bucket.commit()

class executor(object):
    def __init__(self, bucket):
        self.bucket = bucket

    def db_create(self, FLAGS, db, ops):
        action = FLAGS.action
        if not action in ops.ops.keys():
            raise Exception("action {} unrecognized".format(action))

        op = ops.ops[action]
        table_param = op.create(FLAGS, db)

        table_idx = db.create_table_with_def(table_param, op.table)
        data = op.data(FLAGS, db, table_idx, table_param)
        run_multiprocess(data, partial(op.action,db, self.bucket, table_idx, table_param), monitering, self.bucket)

    def db_continue(self, FLAGS, db, ops):
        if FLAGS.table_idx is None:
            raise Exception("table_idx required")

        table_idx = FLAGS.table_idx
        table_name, table_param = db.get_table(table_idx)
        func = table_param['func']
        op = ops.ops[func]

        data = op.data(FLAGS, db, table_idx, table_param)
        run_multiprocess(data, partial(op.action,db, self.bucket, table_idx, table_param), monitering, self.bucket)
        
    def db_progress(self, FLAGS, db, ops):
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

            op = ops.ops[func_name]
                       
            #print(dir(op))
            total, finished, failed = op.progress(FLAGS, db, table_idx, table_param)

            print( "{:<13d} {:<11d} {:<15.2f} {:<11d} {:<14.2f} {:<11d} {:<12.2f} {}". \
                    format(total,
                        finished, 100.*finished/total  if total else 0,
                        failed, 100.*failed/total if total else 0,
                        total - finished - failed, 100.*(total-finished-failed)/total if total else 0,
                        table_name))     

    def db_delete(self, FLAGS, db, ops):
        if FLAGS.table_idx is None:
            raise Exception('table_idx required')

        table_idx = FLAGS.table_idx
        db.delete_table(table_idx)

def main():
    
    parser = get_baseparser()
    db = AffinityDatabase()
    db.regist_table('download',download.table)
    db.regist_table('splited_ligand', split_ligand.table)

    manager = DBManager()
    manager.start()
    bucket = manager.bucket() 

    Ops = operation()
    Ops.register('download',download)
    Ops.register('split_ligand',split_ligand)
    ex = executor(bucket)
    FLAGS, unparsed = parser.parse_known_args()
    if FLAGS.db_create:
        ex.db_create(FLAGS, db, Ops)
    if FLAGS.db_continue:
        ex.db_continue(FLAGS, db, Ops)
    if FLAGS.db_delete:
        ex.db_delete(FLAGS, db, Ops)
    if FLAGS.db_progress:
        ex.db_progress(FLAGS, db, Ops)
    if FLAGS.db_param:
        ex.db_param(FLAGS, db, Ops)


if __name__ == '__main__':
    main()