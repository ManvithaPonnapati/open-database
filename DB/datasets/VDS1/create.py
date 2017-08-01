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

from db_create import get_baseparser, monitering, run_multiprocess, db_creator, db_continue, db_delete, db_progress, db_param, DBManager
from db import AffinityDatabase
from db_action import DatabaseAction as db_action_dict
from action import DatabaseAction as action_dict 

action_dict.update(db_action_dict)

db = AffinityDatabase()
manager = DBManager()
manager.start()
bucket = manager.bucket() 

def db_create(db_creator):
    def __init__(self, FLAGS, db):
        super(db_create, self).__init__(FLAGS, db)
        self.run()

    def run(self):
        table_idx, table_param, data = self.run_create()
        func_name = table_param['func']
        func = action_dict[func_name]
        run_multiprocess(data, partial(func, bucket, table_idx, table_param), monitering, bucket, db)



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
