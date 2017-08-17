import os, sqlite3, sys, random, time
from glob import glob 
from rdkit import Chem
from rdkit.Chem import MCS, AllChem
from rdkit.Chem.rdchem import Mol
from rdkit.Chem.rdmolfiles import SDWriter, SDMolSupplier, PDBWriter


class GenerateConformersInit:

	this_module = sys.modules[__name__]
	def __init__(self, base_dir, num_conformers):
		"""Initializes all the directories and filepaths needed for conformers"""
		
		self.base_dir = base_dir
		self.lig_path = os.path.join(base_dir, 'labeled_pdb/crystal_ligands')
		self.vds_pdb_path = os.path.join(base_dir, 'vds_pdb')
		self.out_lig_path = os.path.join(base_dir, 'vds_pdb/binding_ligands')
		self.out_decoy_path = os.path.join(base_dir, 'vds_pdb/decoy_ligands')
		self.mol_path = os.path.join(base_dir, 'mol')
		self.ligand_files = glob(os.path.join(self.lig_path + '/**/', '*[_]*.pdb'))[:20]
		print 'Number of ligands:', len(self.ligand_files)

		self.num_conformers = num_conformers

		# initialize the output file structure
		if os.path.exists(self.vds_pdb_path):
			os.system('rm -r ' + self.vds_pdb_path)
		if os.path.exists(self.mol_path):
			os.system('rm -r ' + self.mol_path)
		os.mkdir(self.vds_pdb_path)
		os.mkdir(self.mol_path)
		os.mkdir(self.out_lig_path)
		os.mkdir(self.out_decoy_path)

		for lig_file in self.ligand_files:
			lig_name = lig_file[len(self.lig_path)+1: ]
			rec_name = lig_name[0:4]
			if not os.path.isdir(os.path.join(self.out_lig_path, rec_name)):
				os.mkdir(os.path.join(self.out_lig_path, rec_name))
			if not os.path.isdir(os.path.join(self.mol_path, rec_name)):
				os.mkdir(os.path.join(self.mol_path, rec_name))
			if not os.path.isdir(os.path.join(self.out_decoy_path, rec_name)):
				os.mkdir(os.path.join(self.out_decoy_path, rec_name))

		self.this_module.generate_conformers_init = self


def generate_conformers(lig_file, init='generate_conformers_init'):
	"""Performs the following tasks:
		> Creates the receptor folders within binding_ligands and decoy_ligands
		> Converts all PDB crystal ligands into mol for future use
		> Generates conformers and saves them to crystal_ligands folder"""

	init = eval(init)

	lig_name = lig_file[len(init.lig_path)+1: ]

	# use rdkit to get a mol object from the PDB
	pdb_file = os.path.join(init.out_lig_path, lig_name)
	mol_file = os.path.join(init.mol_path, lig_name).replace('.pdb', '.sdf')

	# write the mol to a mol file for future use
	mol = Chem.MolFromPDBFile(lig_file)
	writer = SDWriter(mol_file)
	writer.write(mol)

	# generate conformers and get the number of atoms of the molecule
	mol2 = Chem.AddHs(mol)
	conf_ids = AllChem.EmbedMultipleConfs(mol2, init.num_conformers)
	for cid in conf_ids:
		AllChem.MMFFOptimizeMolecule(mol2, confId=cid)
	mol = Chem.RemoveHs(mol2)
	num_atoms = Mol.GetNumAtoms(mol)

	# write the mol into PDB format (contains mols)
	pdb_writer = PDBWriter(pdb_file)
	pdb_writer.write(mol)

	print 'Generated conformers for one ligand'
	return [[pdb_file, mol_file, num_atoms]]


class GetDecoysInit:

	this_module = sys.modules[__name__]

	def __init__(self, base_dir, all_pdb_files, all_mol_files, all_num_atoms,
		max_atom_dif, max_substruct, max_num_decoys, num_conformers):
		"""Initializes all directories and constants needed for getting decoys"""

		self.base_dir = base_dir
		self.out_decoy_path = os.path.join(base_dir, 'vds_pdb/decoy_ligands')

		self.all_pdb_files = all_pdb_files
		self.all_mol_files = all_mol_files
		self.all_num_atoms = all_num_atoms
		self.all_mols = [Chem.MolFromMolFile(all_mol_files[i]) for i in range(len(all_mol_files))]
		self.max_atom_dif = max_atom_dif
		self.max_substruct = max_substruct
		self.max_num_decoys = max_num_decoys
		self.num_conformers = num_conformers

		self.this_module.get_decoys_init = self


def get_decoys(pdb_file, mol_file, num_atoms, init='get_decoys_init'):
	"""For each binding ligand, gets a list of decoy ligands. We filter by number
	of atoms and maximum common substructure (MCS). Then we generate conformers
	for each decoy and save them to the decoy_ligands folder"""

	init = eval(init)

	reader = SDMolSupplier(mol_file)
	mol = reader[0]
	output = []

	iterator = range(len(init.all_mols))
	random.shuffle(iterator)
	for i in iterator:
		if (init.all_mol_files[i] == mol_file or \
			abs(init.all_num_atoms[i] - num_atoms) > init.max_atom_dif):
			continue
		mcs = MCS.FindMCS([init.all_mols[i], mol], minNumAtoms=init.max_substruct,
				ringMatchesRingOnly=True, completeRingsOnly=True, timeout=1)
		if mcs.numAtoms == -1:
			# generate the decoy and its conformers
			decoy2 = Chem.AddHs(init.all_mols[i])
			conf_ids = AllChem.EmbedMultipleConfs(decoy2, init.num_conformers)
			for cid in conf_ids:
				AllChem.MMFFOptimizeMolecule(decoy2, confId=cid)
			decoy = Chem.RemoveHs(decoy2)

			#save the mol object as a PDB file in the decoys folder
			decoy_file = pdb_file.replace('/binding_ligands/', '/decoy_ligands/').replace('.pdb', str(len(output))+'.pdb')
			pdb_writer = PDBWriter(decoy_file)
			pdb_writer.write(decoy)
			pdb_writer.close()

			output.append([init.all_pdb_files[i], decoy_file])

		if len(output) >= init.max_num_decoys:
			break

	print 'Got the decoys for one ligand'
	return output