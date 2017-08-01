import os
import sys
import re 
import time
import subprocess
from functools import partial
from glob import glob
from utils import log, smina_param, timeit, count_lines, hydrogen_bond_count, rotatable_bond_count
import numpy as np 
import scipy.spatial.distance
#import openbabel
import prody
import config
from config import data_dir                                                                 # todo(maksym) import config
from db import AffinityDatabase
from parse_binding_DB import parse_bind_func
from ccdc import io
import ast

db = AffinityDatabase()

def _makedir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def insert_column(bucket, table_idx, param, input_data):
    try:
        download_idx = input_data
        column_name = param['column_name']
        column_dtype = param['column_dtype']
        # = db.get_table(download_idx)        
        table = db.get_table_name_by_idx(table_idx)
        download = db.get_table_name_by_idx(download_idx)
        db.copy_table(table, download)
        db.insert_column(table, column_name, column_dtype)
        print(db.get_table(table_idx))
    except:
        print("Error Found")
        pass

DatabaseAction = {}
"""
DatabaseAction={
    'local_qm9_load':local_qm9_load,
    'insert_column':insert_column,
    'download':download,
    'split_ligand':split_ligand,
    'split_receptor':split_receptor,
    'reorder':reorder,
    'smina_dock':smina_dock,
    'overlap':overlap,
    'rmsd':rmsd,
    'native_contact':native_contact,
    'binding_affinity':binding_affinity,
    'local_csd_load':local_csd_load,
    'exclusion':exclusion
}
"""
