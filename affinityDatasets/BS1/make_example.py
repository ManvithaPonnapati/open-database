import os,sys,time 
import numpy as np 
sys.path.append('../../affinityDB')
sys.path.append('../../affinityDB/db_libs')
import database, sqlite3
import imp

db_dir = os.path.join(os.path.abspath(os.getcwd()), 'database')
db_path = os.path.join(db_dir, 'database.db')
data_dir = os.path.join(db_dir, 'data')


if not os.path.exists(data_dir):
    os.makedirs(data_dir)

afdb = database.AffinityDB(db_path)
database_master = database.DatabaseMaster(db_path)



with open('../VDS1/data/main_pdb_target_list.txt') as f: pdb_list = f.readline().strip().split(', ')
pdb_list = pdb_list[:2]
pdb_list = [str(p) for p in pdb_list]


fp, path, descr = imp.find_module('download_pdb_op')
lib_mod = imp.load_module('download_pdb_op', fp, path, descr)
lib_mod.Download_pdb_init(db_path=data_dir, download_dir = 'download')


afdb.run_multithread("download_pdb",
                    arg_types=[str],
                    arg_lists=[pdb_list],
                    out_types=[str],
                    out_names=["pdb_path"])



inputs = database_master.retrieve('out_000_download_pdb',['pdb_path'],{"run_idx":"{}>=0"})
print (inputs)

pdb_paths = list(map(str,inputs[0]))

fp, path, descr = imp.find_module('split_pdb_op')
lib_mod = imp.load_module('split_pdb_op', fp, path, descr)
lib_mod.Split_pdb_init(db_root=data_dir, split_dir='split')

afdb.run_multithread(func='split_pdb',
                     arg_types=[str],
                     arg_lists = [pdb_paths],
                     out_types=[str,str],
                     out_names = ['lig_outpath','rec_outpath'])




inputs = database_master.retrieve('out_001_split_pdb',['rec_outpath','lig_outpath'],{"run_idx":"{}>=0"})
rec_outpaths = list(map(str,inputs[0]))
lig_outpaths = list(map(str,inputs[1]))

blast_db_path = os.path.abspath('./blastdb/chembl_23_blast.fa')
fp, path, descr = imp.find_module('blast_op')
lib_mod = imp.load_module('blast_op', fp, path, descr)
lib_mod.Blast_init(data_dir=data_dir, blast_db = blast_db_path)

afdb.run_multithread("blast",
                arg_types=[str, str],
                arg_lists=[rec_outpaths, lig_outpaths],
                out_types=[str, str, float, str],
                out_names = ['pair_name', 'target_id', 'identity', 'sequence'])




inputs = database_master.retrieve('out_002_blast',['pair_name','target_id'],{ "identity":"{}>=0.4"})


pair_names = [str(_) for _ in inputs[0]]
target_idx = [str(_) for _ in inputs[1]]

fp, path, descr = imp.find_module('activity_op')
lib_mod = imp.load_module('activity_op', fp, path, descr)
lib_mod.Activity_init(data_dir=data_dir, activity_folder = 'activity')

afdb.run_multithread("activity",
                    arg_types=[str, str],
                    arg_lists=[pair_names, target_idx],
                    out_types=[str, str, str, str, str, str, str, float, str, int],
                    out_names=['pair_name','target_id','aid','mid','smile','measure','op','value','unit', 'confidence'])