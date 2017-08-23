import os,sys,time
import numpy as np
sys.path.append('../../affinityDB')
sys.path.append('../../affinityDB/dataset_libs')
sys.path.append('../../affinityDB/db_libs')
#from dataset_libs import EXMPL1
import database,sqlite3
from test_sum_op import Test_sum_init,test_sum
from test_multout_op import Test_multout_init,test_multout

db_path = "/home/maksym/Projects/new_data/nano.db"
os.remove(db_path)
afdb = database.AffinityDB(db_path)

arg_ones = list(np.arange(10000) +7)
arg_twos = list(np.arange(10000) + 15)

start = time.time()
Test_sum_init()
afdb.run_multithread("test_sum",
                     arg_types=[int,int],
                     arg_lists=[arg_ones,arg_twos],
                     out_types=[int,int],
                     out_names=['sum','difference'],
                     num_threads=20,commit_sec=1)
print "sum test took: ", time.time() - start, "seconds"


Test_multout_init()
afdb.run_multithread("test_multout",
                     arg_types=[int],
                     arg_lists=[arg_ones],
                     out_types=[int],
                     out_names=['remainder'],
                     num_threads=20,commit_sec=1)
print "multout test took: ", time.time() - start, "seconds"



my_db = database.DatabaseMaster(db_path)
start = time.time()
run_idx = my_db.retrieve("arg_001_test_multout",
                         ["run_idx"],
                         {"run_idx":"{}<100000"})[0]

print "len run idx:", len(run_idx)
out_idx = my_db.retrieve("out_001_test_multout",
                         ["run_idx"],
                         {"run_idx":"{}<100000"})[0]

print "eln out idx", len(out_idx)

idx,val,order = my_db.list_search(out_idx,run_idx)

print idx
print val
print "len order", len(order), len(order[0]),len(order[1])
my_db.merge(into_table="out_001_test_multout",
            from_table="arg_001_test_multout",
            merge_cols=["num","run_state"],
            order=order)
print "merge test took: ", time.time() - start, "seconds"




# version 3 (current)
#100K universal
#sum test took:  18.5235991478 seconds
#merge test took:  2.69516015053 seconds

# --- version 2
#@100K
# sum test took:  24.2396450043 seconds
# merge test took:  0.730545043945 seconds
# retrieve test took:  1.89089202881 seconds

# version 1 (old)
#@10K
# sum test took:  10.6198821068 seconds
# merge test took:  4.28091597557 seconds
# retrieve test took:  0.14103603363 seconds
#@100K
# sum test took:  102.724426031 seconds
# merge test took:  408.845376968 seconds
# retrieve test took:  1.41370987892 seconds


