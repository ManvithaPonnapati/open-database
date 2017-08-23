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
lib_mod.Split_pdb_init(db_path=data_dir, split_dir='split')

afdb.run_multithread(func='split_pdb',
                     arg_types=[str],
                     arg_lists = [pdb_paths],
                     out_types=[str,str],
                     out_names = ['lig_outpath','rec_outpath'])


inputs = database_master.retrieve('out_001_split_pdb',['rec_outpath','lig_outpath'],{"run_idx":"{}>=0"})
rec_outpaths = list(map(str,inputs[0]))
lig_outpaths = list(map(str,inputs[1]))

smina_path = '/Users/Will/projects/smina/smina.osx'
fp, path, descr = imp.find_module('reorder_op')
lib_mod = imp.load_module('reorder_op', fp, path, descr)
lib_mod.Reorder_init(data_dir=data_dir, reorder_folder = 'reorder', smina_path=smina_path)

afdb.run_multithread(func='reorder',
                     arg_types=[str,str],
                     arg_lists=[rec_outpaths, lig_outpaths],
                     out_types = [str,str],
                     out_names = ['rec_outpath','reorder_outpath'])

inputs = db_editor.retrieve('out_002_reorder',['rec_outpath','reorder_outpath'],{"run_idx":"{}>=0"})


rec_outpaths = list(map(str,inputs[0]))
reorder_outpaths = list(map(str,inputs[1]))
fp, path, descr = imp.find_module('dock_op')
lib_mod = imp.load_module('dock_op', fp, path, descr)
lib_mod.Dock_init(data_dir=data_dir, dock_folder = 'dock', smina_path=smina_path)

afdb.run_multithread(func='dock',
                     arg_types=[str,str],
                     arg_lists = [rec_outpaths, reorder_outpaths],
                     out_types = [str,str,str],
                     out_names=['rec_outpath','reorder_outpath','dock_outpath'])


afdb.run_multithread(func='binding_affinity',
                    arg_types=[str, str],
                    arg_lists = [['bindingmoad'],[os.path.abspath('./data/nr.csv')]],
                    out_types = [str, str, float, float, str, str],
                    out_names = ['pdb_id','lig_name','log_affinity','norm_affinity','state','comment'])