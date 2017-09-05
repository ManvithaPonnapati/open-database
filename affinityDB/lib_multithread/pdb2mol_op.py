import os,sys
from rdkit import Chem
from rdkit.Chem.rdmolfiles import SDWriter


class Pdb2mol_init:
    this_module = sys.modules[__name__]
    arg_types = [str,str]
    out_types = [str,str]
    out_names = ["uid", "mol_file"]

    def __init__(self,db_root,molfile_dir):
        """

        :param db_root: string (database root)
        :param molfile_dir: string (relative path where to create the output directory with .mol files)
        """
        self.db_root = db_root
        self.molfile_dir = molfile_dir
        molfile_path = os.path.join(db_root,molfile_dir)
        if not os.path.exists(molfile_path):
            os.makedirs(molfile_path)
        self.molfile_path = molfile_path
        self.this_module.pdb2mol_init = self

def pdb2mol(uid, lig_file, init='pdb2mol_init'):
    """
    Convert .pdb file to .mol file
    :param lig_file: string (relative path to the ligand file)
    :param init: string (init function)
    :return:
    """
    init = eval(init)
    mol = Chem.MolFromPDBFile(os.path.join(init.db_root,lig_file))
    mol_writer = SDWriter(os.path.join(init.molfile_path,uid + ".mol"))
    mol_writer.write(mol)
    mol_writer.close()
    return [[uid,os.path.join(init.molfile_dir,uid + ".mol")]]