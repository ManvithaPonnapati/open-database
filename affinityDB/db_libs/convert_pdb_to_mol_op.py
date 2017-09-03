import sys
from rdkit import Chem
from rdkit.Chem.rdmolfiles import SDWriter


class ConvertPDBToMolInit:
    this_module = sys.modules[__name__]
    def __init__(self):
        self.this_module.convert_pdb_to_mol_init = self

def convert_pdb_to_mol(cryst_lig_file, out_mol_path, init='convert_pdb_to_mol_init'):
    init = eval(init)

    mol = Chem.MolFromPDBFile(cryst_lig_file)
    mol_writer = SDWriter(out_mol_path)
    mol_writer.write(mol)
    mol_writer.close()
    print 'Converted one PDB file to Mol'
    return [[out_mol_path]]