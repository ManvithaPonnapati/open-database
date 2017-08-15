import os,sys,time
import numpy as np
sys.path.append('../../')
import database,sqlite3
from dataset_libs import VDS1


db_path = "/home/maksym/Desktop/vds1/vds1_ex.db"
#os.remove(db_path)
afdb = database.AffinityDB(db_path)


VDS1.Download_pdb_init(db_path="/home/maksym/Desktop/vds1",
                       download_dir="download_pdbs1")

with open("./data/main_pdb_target_list.txt") as f: raw_pdb_list = f.readlines()
pdb_list = raw_pdb_list[0].split(", ")
print "number of pdbs to download:", len(pdb_list)

afdb.run_multithread("VDS1.download_pdb",
                     arg_types=[str],
                     arg_lists=[pdb_list],
                     out_types=[str],out_names=["filename"])
