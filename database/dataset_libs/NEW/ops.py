import os, sqlite3, sys, random
from glob import glob 
from rdkit import Chem
from rdkit.Chem import MCS
from rdkit.Chem.rdchem import Mol
from rdkit.Chem.rdmolfiles import SDWriter, SDMolSupplier


class FLAGS:
	def __init__(self):
		pass

	def convert_pdb_to_mol_init(self, base_dir, max_atom_dif, max_substruct, max_num_decoys):
		# base_dir is the directory in which we'll work in 
		FLAGS.base_dir = base_dir
		# lig_path contains our library of ligands
		FLAGS.lig_path = os.path.join(base_dir, 'labeled_pdb/crystal_ligands')
		FLAGS.db_path = os.path.join(base_dir, 'labeled_pdb.db')
		FLAGS.vds_pdb_path = os.path.join(base_dir, 'vds_pdb')
		FLAGS.out_lig_path = os.path.join(base_dir, 'vds_pdb/binding_ligands')
		FLAGS.out_receptor_path = os.path.join(base_dir, 'vds_pdb/receptors')
		FLAGS.mol_path = os.path.join(base_dir, 'mol') 

		# list of all the file paths to the pdb ligand files
		FLAGS.ligand_files = glob(os.path.join(FLAGS.lig_path + '/**/', '*[_]*.pdb'))[:100]

		FLAGS.max_atom_dif = max_atom_dif
		FLAGS.max_substruct = max_substruct
		FLAGS.max_num_decoys = max_num_decoys

		print 'Number of ligands:', len(FLAGS.ligand_files)

		# initialize the output file structure
		os.chdir(FLAGS.base_dir)
		if os.path.exists(FLAGS.vds_pdb_path):
			os.system('rm -r ' + FLAGS.vds_pdb_path)
		if os.path.isfile(FLAGS.db_path):
			os.system('rm ' + FLAGS.db_path)
		if os.path.exists(FLAGS.mol_path):
			os.system('rm -r ' + FLAGS.mol_path)
		os.mkdir('vds_pdb')
		os.mkdir('mol')
		os.chdir('./vds_pdb')
		os.mkdir('binding_ligands')
		os.mkdir('receptors')

	def get_ligand_decoys_init(self, all_pdb_files, all_mol_files, all_num_atoms):
		"""Initializes all global variables needed for get_ligand_decoys"""
		FLAGS.all_pdb_files = all_pdb_files
		FLAGS.all_mol_files = all_mol_files
		FLAGS.all_num_atoms = all_num_atoms
		FLAGS.all_mols = [Chem.MolFromMolFile(all_mol_files[i]) for i in range(len(all_mol_files))]


def convert_pdb_to_mol(lig_file):
	"""Converts the pdb ligand specified by filepath lig_file and appends the
	converted mol file to m_files. Other procedures:"""

	# first check to make sure convert_pdb_to_mol_init() was performed
	if not hasattr(FLAGS, 'max_substruct'):
		raise Exception("FLAGS class was not initialized correctly. Please initialize global variables using convert_pdb_to_mol_init()")

	# create the folder to hold the binding ligand files
	lig_name = lig_file[len(FLAGS.lig_path)+1: ]
	rec_name = lig_name[0:4]
	if not os.path.isdir(os.path.join(FLAGS.out_lig_path, rec_name)):
		os.mkdir(os.path.join(FLAGS.out_lig_path, rec_name))
	if not os.path.isdir(os.path.join(FLAGS.mol_path, rec_name)):
		os.mkdir(os.path.join(FLAGS.mol_path, rec_name))

	# run obabel commands to perform the conversion
	pdb_file = os.path.join(FLAGS.out_lig_path, lig_name)
	smiles_file = pdb_file.replace('.pdb', '.smi')
	pdb_to_smiles_cmd = 'obabel ' + lig_file + ' -O ' + smiles_file
	smiles_to_pdb_cmd = 'obabel ' + smiles_file + ' -O ' + pdb_file + ' -d --gen3d'
	
	os.system(pdb_to_smiles_cmd)
	os.system(smiles_to_pdb_cmd)
	os.remove(smiles_file)

	mol = Chem.MolFromPDBFile(pdb_file)
	num_atoms = Mol.GetNumAtoms(mol)

	mol_file = os.path.join(FLAGS.mol_path, lig_name).replace('.pdb', '.sdf')
	writer = SDWriter(mol_file)
	writer.write(mol)

	return [[pdb_file, mol_file, num_atoms]]


def get_ligand_decoys(pdb_file, mol_file, num_atoms):
	"""Constructs a 'decoy listing' - for each molecule create a list of other 
	molecules which fall within the number of atoms bound and MCS. Then copy its
	decoys to the folder /vds_pdb/decoy_ligands
		> all_pdb_files: Contains all filenames to pdb files
		> all_mol_files: Contains all filenames to mol files
		> all_mols: Contains all mols (not filenames)
		> all_num_atoms: Contains all the number of atoms of the corresponding mols
	All three of these lists are ordered correctly since we pull from database"""

	# first check to make sure get_ligand_decoys_init() was performed
	if not hasattr(FLAGS, 'all_mols'):
		raise Exception("FLAGS class was not initialized correctly. Please initialize global variables using get_ligand_decoys_init()")

	reader = SDMolSupplier(mol_file)
	mol = reader[0]
	decoy_files = []

	shuffle = random.shuffle(range(len(FLAGS.all_mols)))
	for i in shuffle:
		if FLAGS.all_mol_files[i] == mol_file:
			continue
		if abs(FLAGS.all_num_atoms[i] - num_atoms) <= FLAGS.max_atom_dif:
			mcs = MCS.FindMCS([FLAGS.all_mols[i], mol], minNumAtoms=FLAGS.max_substruct).__str__()
			if mcs[4 : mcs.index('has')-1] != 'None':
				continue
			decoy_files.append([FLAGS.all_pdb_files[i]])
		if len(decoy_files) > FLAGS.max_num_decoys:
			break

	return decoy_files