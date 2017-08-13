import os,sys
import numpy as np
sys.path.append('../../')
#from dataset_libs import BS1
import database,sqlite3




db_path = "/db/nano.db"
os.remove(db_path)
afdb = database.AffinityDB(db_path)

# parser pdb target list
d_list = open('/core/database/datasets/VDS1/main_pdb_target_list.txt').readline().strip().split(', ')

# dir to store download pdb
data_dir = '/db/download'
d_paths = [data_dir]*len(d_list)

# downlaod the pdb file and output the path of file
afdb.run_multithread("dataset_libs.BS1.download",
                     arg_types=[str],
                     arg_lists=[d_list, data_dir],
                     out_types=[str],
                     out_names=['pdb_path'],
                     num_threads=10,commit_freq=500)


# output table name 
download_table_name = None


if download_table_name is not None:

	my_db = database.DatabaseGardener(db_path)
	inputs = my_db.retrieve(download_table_name,['pdb_path'],{'run_state':"=1"})

	afdb.run_multithread("database_libs.BS1.blast",
						arg_types = [str],
						arg_lists = [inputs],
						out_tpes = [str]*8,
						out_names = ['receptor','target_id','identity','align_len','seq_len','midline','hseq','sequence'],
						num_threads=10, commit_freq=10)

