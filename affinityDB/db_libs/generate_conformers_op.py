import sys
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdmolfiles import PDBWriter


class GenerateConformersInit:
	this_module = sys.modules[__name__]
	def __init__(self, num_conformers):
		self.num_conformers = num_conformers
		self.this_module.generate_conformers_init = self

def generate_conformers(cryst_lig_file, out_pdb_path, init='generate_conformers_init', keepHs=False):
	"""Performs the following tasks:
		> Converts the PDB molecule in lig_file into a mol object
		> (Optional) Save single-frame file in Mol format for future use
		> Generates conformers for this mol object
		> Save multi-frame ligand to out_pdb_path in PDB format"""

	init = eval(init)

	mol = Chem.MolFromPDBFile(cryst_lig_file)
	pdb_writer = PDBWriter(out_pdb_path)
	mol = Chem.AddHs(mol)
	conf_ids = AllChem.EmbedMultipleConfs(mol, init.num_conformers)
	for cid in conf_ids:
		AllChem.MMFFOptimizeMolecule(mol, confId=cid)
		if not keepHs: 
			mol = Chem.RemoveHs(mol)
		pdb_writer.write(mol)
	pdb_writer.close()

	print 'Generated conformers for one ligand'
	return [[out_pdb_path]]