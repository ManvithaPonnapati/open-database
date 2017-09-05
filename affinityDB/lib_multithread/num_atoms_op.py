import os,sys
import prody as pr
import numpy as np

class Num_atoms_init:
    this_module = sys.modules[__name__]
    def __init__(self,db_root):
        """
        :param db_root: string (path to the root of the database)
        """
        self.db_root = db_root
        self.this_module.num_atoms_init = self

def num_atoms(pdb_file,init="num_atoms_init"):
    init = eval(init)
    pdb_path = os.path.join(init.db_root, pdb_file)
    pr_pdb = pr.parsePDB(pdb_path)
    return [[pr_pdb.numAtoms()]]