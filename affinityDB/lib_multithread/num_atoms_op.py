import os,sys
import prody as pr
import numpy as np

class Num_atoms_init:
    this_module = sys.modules[__name__]
    def __init__(self,db_root):
        """
        Initialize num_atoms func
        :param db_root: string (path to the root of the database)
        :return:
        None
        """
        self.db_root = db_root
        self.this_module.num_atoms_init = self

def num_atoms(pdb_file,init="num_atoms_init"):
    """
    Counter the number of atom

    Example:
    ```python
    num_atoms('4_reorder/10MH/10MH_B_407_5CM_ligand.pdb')
    ```

    Output:
    ```python
    [[10]]
    ```

    :param pdb_file: relative path of the pdb file
    :return:
    nested list [[atom_num]]
    """
    init = eval(init)
    pdb_path = os.path.join(init.db_root, pdb_file)
    pr_pdb = pr.parsePDB(pdb_path)
    return [[pr_pdb.numAtoms()]]