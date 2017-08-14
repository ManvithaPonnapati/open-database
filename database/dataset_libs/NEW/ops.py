import os, time, sys, sqlite3, multiprocessing
import numpy as np  
from glob import glob 
from rdkit import Chem
from rdkit.Chem import MCS
from rdkit.Chem.rdchem import Mol
from rdkit.Chem.rdmolfiles import SDWriter, SDMolSupplier
from shutil import copyfile


class FLAGS:
	# directory which contains our library of ligands
	lig_path = '/home/cosmynx/Documents/database_old/labeled_pdb/crystal_ligands'

	# base_dir is the directory in which we'll work in 
	base_dir = '/home/cosmynx/Documents/database'
	db_path = os.path.join(base_dir, 'affinity.db')
	vds_pdb_path = os.path.join(base_dir, 'vds_pdb')
	out_lig_path = os.path.join(base_dir, 'vds_pdb/binding_ligands')
	out_decoy_path = os.path.join(base_dir, 'vds_pdb/decoy_ligands')
	out_receptor_path = os.path.join(base_dir, 'vds_pdb/receptors')
	mol_path = os.path.join(base_dir, 'mol')

	# list of all the file paths to the pdb ligand files
	ligand_files = glob(os.path.join(lig_path + '/**/', '*[_]*.pdb'))[:5]

	all_pdb_files = []
	all_mol_files = []
	all_mols = []
	all_num_atoms = []

	"""Define constants here"""
	max_atom_dif = 2
	max_substruct = 4

	def __init__(self):
		print 'Number of ligands:', len(FLAGS.ligand_files)

		# create the output file structure
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
		os.mkdir('decoy_ligands')
		os.mkdir('receptors')


def convert_pdb_to_mol(lig_file):
	"""Converts the pdb ligand specified by filepath lig_file and appends the
	converted mol file to m_files. Other procedures:"""

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
	reader = SDMolSupplier(mol_file)
	mol = reader[0]

	# counter for the number of decoys a molecule has
	decoy_num = 0

	for i in range(len(FLAGS.all_mols)):
		if FLAGS.all_mol_files[i] == mol_file:
			continue
		if abs(FLAGS.all_num_atoms[i] - num_atoms) <= FLAGS.max_atom_dif:
			mcs = MCS.FindMCS([all_mols[i], mol], minNumAtoms=FLAGS.max_substruct).__str__()
			if mcs[4 : mcs.index('has')-1] != 'None':
				continue
			receptor_name = all_pdb_files[len(FLAGS.out_lig_path)+1 : len(FLAGS.out_lig_path)+5]
			extension = all_pdb_files[len(FLAGS.out_lig_path)+6 : -4] + '_' + str(decoy_num) + '.pdb'
			dest = os.path.join(FLAGS.out_decoy_path, receptor_name, extension)
			copyfile(FLAGS.all_pdb_files[i], dest)
			decoy_num += 1

	return decoy_num