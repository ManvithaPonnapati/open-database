import os,sys,time
import numpy as np
sys.path.append('../../affinityDB')
sys.path.append('../../affinityDB/dataset_libs')
import database,sqlite3
import VDS1


db_path = "/home/cosmynx/Documents/database/test.db"
#os.remove(db_path)
afdb = database.AffinityDB(db_path)


database_master = database.DatabaseMaster(db_path)


with open("./data/main_pdb_target_list.txt") as f: raw_pdb_list = f.readlines()
pdb_list = raw_pdb_list[0].split(", ")
print "number of pdbs to download:", len(pdb_list)
print "will download only 100 in this experiment"
pdb_list = pdb_list[:100]




VDS1.Download_pdb_init(db_path="/home/cosmynx/Documents/database", download_dir="download_pdbs1")
# afdb.run_multithread("VDS1.download_pdb",
#                      arg_types=[str],
#                      arg_lists=[pdb_list],
#                      out_types=[str],
#                      out_names=["filename"])

# FIXME:needs empty rules
# FIXME: assert table name is string
disk_pdbs = database_master.retrieve("out_000_VDS1.download_pdb",["filename"],{"run_idx":"{}<100"})
disk_pdbs = disk_pdbs[0]
# FIXME: unicode
disk_pdbs = [str(disk_pdb) for disk_pdb in disk_pdbs]
print "downloaded:", disk_pdbs
VDS1.Split_pdb_init(db_path="/home/cosmynx/Documents/database", split_dir="split_pdbs1")
afdb.run_multithread("VDS1.split_pdb",
                     arg_types=[str],
                     arg_lists=[disk_pdbs],
                     out_types=[str,str],
                     out_names=["lig_file","rec_file"])