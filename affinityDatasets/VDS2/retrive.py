import os,sys
import numpy as np
sys.path.append('../../')
from dataset_libs import BS1
import database,sqlite3
import dataset_libs
import pandas as pd


db_path = "db/nano.db"
#os.remove(db_path)
afdb = database.AffinityDB(db_path)

def retrieve_data(dock_table, affinity_table,tfr_out_dir):
    my_db = database.DatabaseGardener(db_path)

    # get necessary columns from dock out table
    cols = ['receptor','resname','rec_path','reorder_path','dock_path']
    inputs = my_db.retrieve(dock_table,
                            cols, {"run_state":"{}==1 or {}==2"})

    
    # get norm_affintiy data
    affinity = my_db.retrieve(affinity_table,
                            ['receptor','resname','norm_affinity'],
                            {"run_state":"{}==1 or {}==2"})


                        
    dock_df = pd.DataFrame(data = zip(*inputs), columns=cols)
    aff_df = pd.DataFrame(data = zip(*affinity), columns=['receptor','resname','norm_affinity'])
    insect_df = dock_df.merge(aff_df, 'inner',['receptor','resname'])



    inputs = [list(map(lambda x:'"'+str(x)+'"',insect_df['receptor'])),
             list(map(lambda x:'"'+str(x)+'"',insect_df['resname'])),
             list(map(lambda x:'"'+str(x)+'"',insect_df['rec_path'])),
             list(map(lambda x:'"'+str(x)+'"',insect_df['reorder_path'])),
             list(map(lambda x:'"'+str(x)+'"',insect_df['dock_path'])),
             list(insect_df['norm_affinity']),
             ['"'+tfr_out_dir+'"']* len(insect_df)]


    afdb.run_multithread('dataset_libs.VDS1.retrieve_tfr',
                        arg_types=[str,str,str,str,str,float,str],
                        arg_lists=inputs,
                        out_types=[str],
                        out_names=['tfr_path'],
                        num_threads=1, commit_sec=1)

retrieve_data(dock_table, affinity_table, tfr_out_dir)