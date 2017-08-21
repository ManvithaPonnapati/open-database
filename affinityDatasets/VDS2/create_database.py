import os,sys
import numpy as np
sys.path.append('../../')
from dataset_libs import VDS2
import database,sqlite3
import dataset_libs


flags = VDS2.FLAGS(os.path.join(os.getcwd(),'data'))

afdb = database.AffinityDB(flags.db_path)
db_editor = database.DatabaseGardener(flags.db_path)


def get_run_state(table_name):
    """
    get run_state from args table and insert into out table
    """

    db_editor.up_merge(table_name,table_name[:17]+'_arg_'+table_name[22:],["run_state"])


flags.download_init('main_pdb_target_list.txt')
"""
afdb.run_multithread(func='VDS2.download',
                     arg_types=[str],
                     arg_lists=[flags.pdb_list],
                     out_types=[str, str],
                     out_names = ['receptor','pdb_path'],
                     num_threads=1, commit_sec=1)


get_run_state('aug_17_2017_27_36_out_VDS2.download')

inputs = db_editor.retrieve('aug_17_2017_27_36_out_VDS2.download',['receptor','pdb_path'],{"run_state":"{}==1 or {}==2"})

receptors = inputs[0]
rec_paths = inputs[1]
receptors = list(map(str, receptors))
rec_paths = list(map(str, rec_paths))

flags.split_init(receptors, rec_paths)

afdb.run_multithread(func='VDS2.split',
                     arg_types=[str, str],
                     arg_lists = [flags.receptor, flags.pdb_path],
                     out_types=[str,str,str,str],
                     out_names = ['receptor','resname','rec_path','lig_path'],
                     num_threads=1, commit_sec=1)

get_run_state('aug_17_2017_46_57_out_VDS2.split')


inputs = db_editor.retrieve('aug_17_2017_46_57_out_VDS2.split',['receptor','resname','rec_path','lig_path'],{"run_state":"{}==1 or {}==2"})
receptors = list(map(str,inputs[0]))
resnames = list(map(str, inputs[1]))
rec_paths = list(map(str,inputs[2]))
lig_paths = list(map(str,inputs[3]))

flags.reorder_init(receptors, resnames, rec_paths, lig_paths)

afdb.run_multithread(func='VDS2.reorder',
                     arg_types=[str, str,str,str],
                     arg_lists=[flags.receptor, flags.resname, flags.rec_path, flags.lig_path],
                     out_types = [str, str,str,str],
                     out_names = ['receptor','resname','rec_path','reorder_path'],
                     num_threads=1, commit_sec=1)


get_run_state('aug_17_2017_55_15_out_VDS2.reorder')

inputs = db_editor.retrieve('aug_17_2017_55_15_out_VDS2.reorder',['receptor','resname','rec_path','reorder_path'],{"run_state":"{}==1 or {}==2"})

receptors = list(map(str,inputs[0]))
resnames = list(map(str, inputs[1]))
rec_paths = list(map(str,inputs[2]))
reorder_paths = list(map(str,inputs[3]))

flags.dock_init(receptors, resnames, rec_paths, reorder_paths,'vinardo')

afdb.run_multithread(func='VDS2.dock',
                     arg_types=[str,str,str,str],
                     arg_lists = [flags.receptor, flags.resname, flags.rec_path, flags.reorder_path],
                     out_types = [str,str,str,str,str],
                     out_names=['receptor','resname','rec_path','reorder_path','dock_path'],
                      num_threads=1, commit_sec=1)

"""
get_run_state('aug_17_2017_46_57_out_VDS2.split')
inputs = db_editor.retrieve('aug_17_2017_46_57_out_VDS2.split',['receptor','resname','rec_path','lig_path'],{"run_state":"{}==1 or {}==2"})
receptors = list(map(str,inputs[0]))
resnames = list(map(str, inputs[1]))
rec_paths = list(map(str,inputs[2]))
lig_paths = list(map(str,inputs[3]))

print (inputs)