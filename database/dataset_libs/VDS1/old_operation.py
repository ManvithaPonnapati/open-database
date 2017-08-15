import sys
import time
import argparse 
import logging
import multiprocessing
import threading
from multiprocessing.managers import BaseManager
from glob import glob 
from functools import partial

import numpy as np 
import pandas as pd 
import db_config

sys.path.append('../')


from mini_db import AffinityDatabase
from blocks_4_mini_db import download, split_ligand, operation, split_receptor, blast

class Bucket(object):
    '''
    collect sql command from threads
    insrt them into

    '''
    def __init__(self):
        self.bucket = []
        tr = threading.Thread(target=self._autocommit)
        tr.daemon = True
        tr.start()

    def size(self):
        return len(self.bucket)

    def insert(self, stmt):
        self.bucket.append(stmt)

    def commit(self):
        db = AffinityDatabase()
        for stmt in self.bucket:
            logging.debug("executing sql command from bucket:",stmt)
            cursor = db.conn.cursor()
            cursor.execute(stmt)
        db.conn.commit()
        self.bucket = []
        logging.info('commited')


    # start dropping data to the database with a background thread
    def _autocommit(self):
        while True:
            self.commit()
            time.sleep(10)
            logging.info('autocommited')



class DBManager(BaseManager):
    pass




DBManager.register("bucket", Bucket)

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




def run_multiprocess(target_list, func, bucket):
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

    pool = multiprocessing.Pool(db_config.process_num)
    # running function outside the
    # run in a single thread
    for i in range(len(target_list)):
        func(target_list[i])
    #print "target list",target_list
    func(target_list[0])
    pool.map_async(func, target_list)
    pool.close()
    pool.join()
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

        table_idx = db.create_table(table_param=table_param, table_def=op.table)
        data = op.data(FLAGS, db, table_idx, table_param)
        run_multiprocess(data, partial(op.action,db, self.bucket, table_idx, table_param), self.bucket)

    def db_continue(self, FLAGS, db, ops):
        if FLAGS.table_idx is None:
            raise Exception("table_idx required")

        table_idx = FLAGS.table_idx
        table_name, table_param = db.get_table_info(table_idx)
        func = table_param['func']
        op = ops.ops[func]

        data = op.data(FLAGS, db, table_idx, table_param)
        run_multiprocess(data, partial(op.action,db, self.bucket, table_idx, table_param), self.bucket)


def main():
    
    parser = get_baseparser()
    db = AffinityDatabase()
    db.regist_table('download',download.table)
    db.regist_table('splited_ligand', split_ligand.table)
    db.regist_table('splited_receptor',split_receptor.table)
    db.regist_table('blast',blast.table)

    #manager = DBManager()
    #manager.start()
    #bucket = manager.bucket() 
    bucket = Bucket()

    Ops = operation()
    Ops.register('download',download)
    Ops.register('split_ligand',split_ligand)
    Ops.register('split_receptor', split_receptor)
    Ops.register('blast', blast)
    ex = executor(bucket)
    FLAGS, unparsed = parser.parse_known_args()
    if FLAGS.db_create:
        ex.db_create(FLAGS, db, Ops)
    if FLAGS.db_continue:
        ex.db_continue(FLAGS, db, Ops)


if __name__ == '__main__':
    main()
