import os,sys
from rdkit import Chem
from rdkit.Chem.rdmolfiles import SDWriter


class Pdb2mol_init:
    this_module = sys.modules[__name__]
    arg_types = [str]
    out_types = [str]
    out_names = ["mol_file"]

    def __init__(self,db_root,molfile_dir):
        """

        :param db_root: string (database root)
        :param molfile_dir: string (relative path where to create the output directory with .mol files)
        """
        self.molfile_dir = molfile_dir
        molfile_path = os.path.join(db_root,molfile_dir)
        if not os.path.exists(molfile_path):
            os.makedirs(molfile_path)
        self.molfile_path = molfile_path
        self.this_module.pdb2mol_init = self

def pdb2mol(lig_file, init='pdb2mol_init'):
    """

    :param lig_file:
    :param init:
    :return:
    """
    init = eval(init)
    lig_name = lig_file.split("/")[-1].split(".")[0] + ".mol"
    mol = Chem.MolFromPDBFile(lig_file)
    mol_writer = SDWriter(os.path.join(init.molfile_path,lig_name))
    mol_writer.write(mol)
    mol_writer.close()
    return [[os.path.join(init.molfile_dir,lig_name)]]