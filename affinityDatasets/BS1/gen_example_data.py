import os,sys,time 
import numpy as np 
sys.path.append('../../affinityDB')
sys.path.append('../../affinityDB/dataset_libs')
import database, sqlite3
import BS1

db_dir = os.path.join(os.path.abspath(os.getcwd()), 'database')
data_dir = os.path.join(db_dir, 'data')
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

db_path = os.path.join(db_dir, 'database.db')

afdb = database.AffinityDB(db_path)

database_master = database.DatabaseMaster(db_path)


def get_run_state(table_name):
    """
    get run_state from args table and insert into out table
    """

    database_master.up_merge(table_name,'arg'+table_name[3:],["run_state"])

"""
"""
with open('../VDS1/data/main_pdb_target_list.txt') as f: pdb_list = f.readline().strip().split(', ')
pdb_list = pdb_list[:2]
pdb_list = [str(p) for p in pdb_list]


print (pdb_list)
BS1.Download_pdb_init(data_dir=data_dir, download_folder='download')

afdb.run_multithread("BS1.download_pdb",
                    arg_types=[str],
                    arg_lists=[pdb_list],
                    out_types=[str],
                    out_names=["pdb_path"],
                    num_threads=1, commit_sec=1)




get_run_state('out_000_BS1.download_pdb')



BS1.Split_pdb_init(data_dir=data_dir, split_folder='split')

inputs = database_master.retrieve('out_000_BS1.download_pdb', ['pdb_path'], {"run_state":"{}==1 or {}==2"})
pdb_paths = [str(_) for _ in inputs[0]]

afdb.run_multithread("BS1.split_pdb",
                    arg_types=[str],
                    arg_lists=[pdb_paths],
                    out_types=[str, str],
                    out_names=['rec_outpath','lig_outpath'],
                    num_threads=1, commit_sec=1)




get_run_state('out_001_BS1.split_pdb')


blast_db_path = os.path.abspath('../../affinityDB/dataset_libs/BS1/blastdb/chembl_23_blast.fa')
BS1.Blast_init(data_dir = data_dir, blast_db = blast_db_path)

inputs = database_master.retrieve('out_001_BS1.split_pdb', ['rec_outpath','lig_outpath'],  {"run_state":"{}==1 or {}==2"})

rec_outpaths = [str(_) for _ in inputs[0]]
lig_outpaths = [str(_) for _ in inputs[1]]

afdb.run_multithread("BS1.blast",
                arg_types=[str, str],
                arg_lists=[rec_outpaths, lig_outpaths],
                out_types=[str, str, float, str],
                out_names = ['pair_name', 'target_id', 'identity', 'sequence'],
                num_threads=1, commit_sec=1)


get_run_state('out_002_BS1.blast')


BS1.Activity_init(data_dir = data_dir, activity_folder='activity')

inputs = database_master.retrieve('out_002_BS1.blast',['pair_name','target_id'],{"run_state":"{}==1 or {}==2", "identity":"{}>=0.4"})

pair_names = [str(_) for _ in inputs[0]]
target_idx = [str(_) for _ in inputs[1]]

afdb.run_multithread("BS1.activity",
                    arg_types=[str, str],
                    arg_lists=[pair_names, target_idx],
                    out_types=[str, str, str, str, str, str, str, float, str],
                    out_names=['pair_name','target_id','aid','mid','smile','measure','op','value','unit'],
                    num_threads=1, commit_sec=1)

get_run_state('out_003_BS1.activity')
BS1.Conf_gen_init(data_dir = data_dir, conf_dir = 'conformation')

inputs = database_master.retrieve('out_003_BS1.activity',['pair_name','mid','smile'],{"run_state":"{}==1 or {}==2"})

pair_names = [str(_) for _ in inputs[0]]
midx = [str(_) for _ in inputs[1]]
smiles = [str(_) for _ in inputs[2]]

afdb.run_multithread("BS1.conf_gen",
                    arg_types=[str, str,str],
                    arg_lists=[pair_names, midx, smiles],
                    out_types=[str, str,int],
                    out_names=["conf_pdb_outpath","conf_mol_outpath","num_atoms"])

