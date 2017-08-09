import sys
import numpy as np
sys.path.append('../../')
from dataset_libs import EXMPL1
import database

print EXMPL1.sum_diff(1,2)
db_path = "/home/maksym/Projects/new_data/nano.db"
afdb = database.AffinityDB(db_path)

arg_ones = np.arange(10000) +7
arg_twos = np.arange(10000) + 15


afdb.run_multithread("dataset_libs.EXMPL1.sum_diff",
                     arg_types=[int,int],
                     arg_lists=[arg_ones,arg_twos],
                     out_types=[int],
                     out_names=['sumqrt'],
                     num_threads=10,commit_freq=500)
