import os,sys
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdmolfiles import PDBWriter


class Generate_conformers_init:
    this_module = sys.modules[__name__]
    arg_types = [str,str]
    out_types = [str,str]
    out_names = ["uid","conformers_file"]

    def __init__(self,db_root,conformers_dir,num_conformers,out_H):
        """

        :param db_root: string (database root)
        :param conformers_dir: string (name of the directory where to put generated conformers)
        :param num_conformers: int (number of the conformers to output)
        :param out_H: bool T/F (Add hydrogen atoms to the output. All input hydorogen atoms are always lost.)
        """
        self.db_root = db_root
        self.conformers_dir = conformers_dir
        conformers_path = os.path.join(db_root,conformers_dir)
        if not os.path.exists(conformers_path):
            os.makedirs(conformers_path)
        self.conformers_path = conformers_path
        self.num_conformers = num_conformers
        self.out_H = out_H
        self.this_module.generate_conformers_init = self


def generate_conformers(uid,lig_file,init='generate_conformers_init'):
    """
    Forgets the initial coordinates of the molecule. Looses all hydrogens. Adds all hydrogens.
    Generates random conformers. Optimizes conformers with MMFF94 Force Field.
    Saves multiframe PDB file of the ligand with new coordinates.
    :param lig_file: string (path to the ligand file in the PDB format to read)
    :param init: string (init function)
    :return:
    nested list:
    of dimension [1x[string]]. String is the relative path to the output file.
    """
    # TODO: test if shape if forgotten (give an option to optimize only?)
    init = eval(init)
    conf_outpath = os.path.join(init.conformers_path,uid + ".pdb")
    mol = Chem.MolFromPDBFile(lig_file)
    mol = Chem.RemoveHs(mol)
    mol = Chem.AddHs(mol)
    conf_ids = AllChem.EmbedMultipleConfs(mol,
                                          clearConfs=True,
                                          numConfs=init.num_conformers)
    pdb_writer = PDBWriter(conf_outpath)
    for cid in conf_ids:
        AllChem.MMFFOptimizeMolecule(mol, confId=cid)
        if not init.out_H:
            mol = Chem.RemoveHs(mol)
        pdb_writer.write(mol, confId=cid)
    pdb_writer.close()
    return [[uid,os.path.join(init.conformers_dir,uid+".pdb")]]