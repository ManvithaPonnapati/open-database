import os,sys
import numpy as np
sys.path.append('../../')
from dataset_libs import BS1
import database,sqlite3
import dataset_libs



db_path = "db/nano.db"
os.remove(db_path)
afdb = database.AffinityDB(db_path)

# def download():
#     """
#     download pdb file
#     """
#     # parser pdb target list
#     d_list = open('main_pdb_target_list.txt').readline().strip().split(', ')
#     d_list = d_list[:2]
#     d_list = list(map(lambda x:'"'+str(x)+'"', d_list))
#     # dir to store download pdb
#     data_dir = '"db/download"'
#     d_paths = [data_dir]*len(d_list)
#     # downlaod the pdb file and output the path of file
#     afdb.run_multithread("dataset_libs.VDS1.download",
#                         arg_types=[str, str],
#                         arg_lists=[d_list, d_paths],
#                         out_types=[str]*2,
#                         out_names=['receptor','pdb_path'],
#                         num_threads=10,commit_sec=50)


#
# def get_run_state(table_name):
#     """
#     get run_state from args table and insert into out table
#     """
#     my_db = database.DatabaseGardener(db_path)
#     my_db.up_merge(table_name,table_name[:17]+'_arg_'+table_name[22:],["run_state"])

# def split(table_name):
#     """
#     split pdb into ligand and receptor
#     """
#     my_db = database.DatabaseGardener(db_path)
#     inputs = my_db.retrieve(table_name,['receptor','pdb_path'],{"run_state":"{}==1 or {}==2"})
#     receptors = inputs[0]
#     rec_paths = inputs[1]
#     receptors = list(map(str, receptors))
#     rec_paths = list(map(str, rec_paths))
#
#     # dir to store ligand
#     lig_dir = '"db/ligands"'
#
#     # dir to store receptor
#     rec_dir = '"db/receptors"'
#     ligs = [lig_dir] * len(receptors)
#     recs = [rec_dir] * len(receptors)
#
#
#     afdb.run_multithread("dataset_libs.VDS2.split",
#                     arg_types = [str, str, str, str],
#                     arg_lists = [receptors,rec_paths, recs, ligs],
#                     out_types = [str]*4,
#                     out_names = ['receptor','resname','rec_path', 'lig_path'],
#                     num_threads=10, commit_sec=50)



def reorder(table_name):
    """
    reorder ligand by smina
    """
    my_db = database.DatabaseGardener(db_path)
    inputs = my_db.retrieve(table_name,['receptor','resname','rec_path','lig_path'],{"run_state":"{}==1 or {}==2"})
    receptors = list(map(str,inputs[0]))
    resnames = list(map(str, inputs[1]))
    rec_paths = list(map(str,inputs[2]))
    lig_paths = list(map(str,inputs[3]))

    # dor to store reorder output
    reorder_dir = '"db/reorder"'
    reorder_dirs = [reorder_dir] * len(rec_paths)


    afdb.run_multithread("dataset_libs.VDS2.reorder",
                    arg_types = [str, str, str, str, str],
                    arg_lists = [receptors,resnames,rec_paths, lig_paths, reorder_dirs],
                    out_types = [str]*4,
                    out_names = ['receptor','resname','rec_path', 'reorder_path'],
                    num_threads=10, commit_sec=50)          


def dock(table_name):
    """
    do docking by smina
    """
    my_db = database.DatabaseGardener(db_path)
    inputs = my_db.retrieve(table_name,['receptor','resname','rec_path','reorder_path'],{"run_state":"{}==1 or {}==2"})    
    receptors = list(map(str,inputs[0]))
    resnames = list(map(str, inputs[1]))
    rec_paths = list(map(str,inputs[2]))
    reorder_paths = list(map(str,inputs[3]))

    # docking parameter
    dock_pms = ['"vinardo"']* len(receptors)

    # dir to store docking output
    dock_dirs = ['"db/vinardo"'] * len(receptors)


    afdb.run_multithread("dataset_libs.VDS2.dock",
                    arg_types = [str, str, str, str, str, str],
                    arg_lists = [receptors,resnames,rec_paths, reorder_paths, dock_pms, dock_dirs],
                    out_types = [str]*5,
                    out_names = ['receptor','resname','rec_path', 'reorder_path','dock_path'],
                    num_threads=10, commit_sec=50)             
    
def bind_affinity():
    """
    get bind affinity
    """

    # path of affinity record file
    index = ['"/core/database/datasets/VDS2/bind_affinity/INDEX_general_PL.2016"']

    # source of bindinf affinity
    source = ['"pdbbind"']

    afdb.run_multithread("dataset_libs.VDS2.binding_affinity",
                        arg_types = [str,str],
                        arg_lists=[index, source],
                        out_types=[str, str, float, float, int, str],
                        out_names = ['receptor','resname','log_affinity','norm_affinity','state','comment'],
                        num_threads=10, commit_sec=50)
    


def main():

    #download()
    #get_run_state(downlaod_out_table)
    #split(downlaod_out_table)
    #get_run_state(split_out_table)
    #reorder(split_out_table)
    #get_run_state(reorder_out_table)
    #dock(reorder_out_table)
    #get_run_state(dock_out_table)
    #bind_affinity()
    #get_run_state(affinity_out_table)
    return None

if __name__ == '__main__':
    main()