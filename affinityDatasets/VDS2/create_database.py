import os,sys,time 
import numpy as np 
sys.path.append('../../affinityDB')
sys.path.append('../../affinityDB/dataset_libs')
import database, sqlite3
import VDS2


db_dir = os.path.abspath(os.path.join(os.getcwd(),'database'))
data_dir = os.path.join(db_dir, 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

db_path = os.path.join(db_dir, 'database.db')

afdb = database.AffinityDB(db_path)
db_editor = database.DatabaseMaster(db_path)

with open('../VDS1/data/main_pdb_target_list.txt') as f: pdb_list = f.readline().strip().split(', ')
pdb_list = pdb_list[:2]
pdb_list = [str(p) for p in pdb_list]

VDS2.Download_init(data_dir,'download')

afdb.run_multithread(func='VDS2.download',
                     arg_types=[str],
                     arg_lists=[pdb_list],
                     out_types=[str, str],
                     out_names = ['receptor','pdb_outpath'],
                     num_threads=1, commit_sec=1)



inputs = db_editor.retrieve('out_000_VDS2.download',['receptor','pdb_outpath'],{"run_idx":"{}>=0"})

receptors = list(map(str, inputs[0]))
pdb_paths = list(map(str,inputs[1]))


VDS2.Split_init(data_dir,'receptor','ligand')


afdb.run_multithread(func='VDS2.split',
                     arg_types=[str, str],
                     arg_lists = [receptors, pdb_paths],
                     out_types=[str,str,str,str],
                     out_names = ['receptor','resname','rec_outpath','lig_outpath'],
                     num_threads=1, commit_sec=1)


inputs = db_editor.retrieve('out_001_VDS2.split',['receptor','resname','rec_outpath','lig_outpath'],{"run_idx":"{}>=0"})
receptors = list(map(str,inputs[0]))
resnames = list(map(str, inputs[1]))
rec_paths = list(map(str,inputs[2]))
lig_paths = list(map(str,inputs[3]))

VDS2.Reorder_init(data_dir,'reorder')

afdb.run_multithread(func='VDS2.reorder',
                     arg_types=[str, str,str,str],
                     arg_lists=[receptors, resnames, rec_paths, lig_paths],
                     out_types = [str, str,str,str],
                     out_names = ['receptor','resname','rec_outpath','reorder_outpath'],
                     num_threads=1, commit_sec=1)




inputs = db_editor.retrieve('out_002_VDS2.reorder',['receptor','resname','rec_outpath','reorder_outpath'],{"run_idx":"{}>=0"})

receptors = list(map(str,inputs[0]))
resnames = list(map(str, inputs[1]))
rec_paths = list(map(str,inputs[2]))
reorder_paths = list(map(str,inputs[3]))

VDS2.Dock_init(data_dir, 'dock','vinardo')


afdb.run_multithread(func='VDS2.dock',
                     arg_types=[str,str,str,str],
                     arg_lists = [receptors, resnames, rec_paths, reorder_paths],
                     out_types = [str,str,str,str,str],
                     out_names=['receptor','resname','rec_outpath','reorder_outpath','dock_outpath'],
                      num_threads=1, commit_sec=1)



