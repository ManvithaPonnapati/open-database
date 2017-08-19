import os,sys
import numpy as np
sys.path.append('../../')
from dataset_libs import BS1
import database,sqlite3
import dataset_libs


blast_db_path = os.path.abspath('../../dataset_libs/BS1/blastdb/chembl_23_blast.fa')
flags = BS1.FLAGS(os.path.join(os.getcwd(),'data'))

afdb = database.AffinityDB(flags.db_path)
db_editor = database.DatabaseGardener(flags.db_path)


def get_run_state(table_name):
    """
    get run_state from args table and insert into out table
    """

    db_editor.up_merge(table_name,table_name[:17]+'_arg_'+table_name[22:],["run_state"])


flags.download_init('main_pdb_target_list.txt')

afdb.run_multithread(func='BS1.download',
                    arg_types=[str],
                    arg_lists=[flags.pdb_list],
                    out_types=[str,str],
                    out_names = ['receptor','pdb_path'],
                    num_threads=1, commit_sec=1)



get_run_state(download_out_table)



inputs = db_editor.retrieve(download_out_table,['receptor','pdb_path'],{"run_state":"{}==1 or {}==2"})

receptors = inputs[0]
pdb_paths = inputs[1]
receptors = list(map(str, receptors))
pdb_paths = list(map(str, pdb_paths))

flags.blast_init(receptors, pdb_paths,blast_db_path,0.4)

afdb.run_multithread(func='BS1.blast',
                     arg_types=[str,str],
                     arg_lists = [flags.receptor, flags.pdb_path],
                     out_types = [str, str, str, float, str, str, str],
                     out_names = ['receptor','resname','target_id','identity','rec_path','lig_path','sequence'],
                     num_threads=1, commit_sec=1)


get_run_state(blast_out_table)



inputs = db_editor.retrieve(blast_out_table,['receptor','resname', 'target_id'],{"run_state":"{}==1 or {}==2"})

flags.activity_init(*inputs)

afdb.run_multithread(func='BS1.activity',
                     arg_types=[str,str,str],
                     arg_lists=[flags.receptor, flags.resname, flags.target_id],
                     out_types=[str,str,str,str,str,str,str,str,float, str],
                     out_names=['receptor','resname','target_id','aid','mid','smile','measure','op','value','unit'])


get_run_state(activity_out_table)



inputs = db_editor.retrieve(activity_out_table,['receptor','resname','mid','smile'],{"run_state":"{}==1 or {}==2"})

flags.conf_gen_init(*inputs)

afdb.run_multithread(func='BS1.conf_gen',
                    arg_types=[str, str,str,str],
                    arg_lists=[flags.receptor, flags.resname, flags.mid, flags.smile],
                    out_types=[str, str,int],
                    out_names = ['gen_pdb_path','gen_mol_path','num_atoms'])