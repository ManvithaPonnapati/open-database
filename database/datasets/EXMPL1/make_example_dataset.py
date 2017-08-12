import os,sys
import numpy as np
sys.path.append('../../')
#from dataset_libs import EXMPL1
import database,sqlite3


#print EXMPL1.sum_diff(1,2)

db_path = "/home/maksym/Projects/new_data/nano.db"
os.remove(db_path)
afdb = database.AffinityDB(db_path)

arg_ones = list(np.arange(10000) +7)
arg_twos = list(np.arange(10000) + 15)


afdb.run_multithread("dataset_libs.EXMPL1.sum_diff",
                     arg_types=[int,int],
                     arg_lists=[arg_ones,arg_twos],
                     out_types=[int,int],
                     out_names=['sum','difference'],
                     num_threads=10,commit_freq=500)


# afdb.run_multithread("dataset_libs.EXMPL1.string_test",
#                       arg_types=[int],
#                       arg_lists=[arg_twos],
#                       out_types=[str],
#                       out_names=['test_string'],
#                       num_threads=10,commit_freq=500)
#
# afdb.run_multithread("dataset_libs.EXMPL1.multi_out",
#                      arg_types=[int],
#                      arg_lists=[arg_ones],
#                      out_types=[int],
#                      out_names=['multi_remainder'],
#                      num_threads=10,commit_freq=500)


# Merge and Retrieve examples

db_path = "/home/maksym/Projects/new_data/nano.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
downs_table,ups_table = cursor.fetchall()
downs_table = downs_table[0]
ups_table = ups_table[0]
conn.close()


my_db = database.DatabaseGardener(db_path)
my_db.up_merge(ups_table,downs_table,["num1","num2","run_state","run_message"])
sel_vals = my_db.retrieve(ups_table,["num1","num2"],{"run_state":"{}==1 or {}==2",
                                          "sum":"{}>200"})
print sel_vals