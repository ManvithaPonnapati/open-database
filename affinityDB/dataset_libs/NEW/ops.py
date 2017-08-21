import os, sqlite3, sys, random, time
from glob import glob 
from rdkit import Chem
from rdkit.Chem import MCS, AllChem
from rdkit.Chem.rdchem import Mol
from rdkit.Chem.rdmolfiles import SDWriter, SDMolSupplier, PDBWriter


class FLAGS:
	def __init__(self):
		pass

	def get_crystal_ligand_conformers_init(self, base_dir, max_atom_dif, 
		max_substruct, max_num_decoys, decoy_conformers, binding_conformers):
		"""Initializes all directories and constants needed for crystal ligands"""

		# base_dir is the directory in which we'll work in 
		FLAGS.base_dir = base_dir
		# lig_path contains our library of ligands
		FLAGS.lig_path = os.path.join(base_dir, 'labeled_pdb/crystal_ligands')
		FLAGS.db_path = os.path.join(base_dir, 'labeled_pdb.db')
		FLAGS.vds_pdb_path = os.path.join(base_dir, 'vds_pdb')
		FLAGS.out_lig_path = os.path.join(base_dir, 'vds_pdb/binding_ligands')
		FLAGS.out_decoy_path = os.path.join(base_dir, 'vds_pdb/decoy_ligands')
		FLAGS.out_receptor_path = os.path.join(base_dir, 'vds_pdb/receptors')
		FLAGS.mol_path = os.path.join(base_dir, 'mol') 

		# list of all the file paths to the pdb ligand files
		FLAGS.ligand_files = glob(os.path.join(FLAGS.lig_path + '/**/', '*[_]*.pdb'))[:20]

		FLAGS.max_atom_dif = max_atom_dif
		FLAGS.max_substruct = max_substruct
		FLAGS.max_num_decoys = max_num_decoys
		FLAGS.decoy_conformers = decoy_conformers
		FLAGS.binding_conformers = binding_conformers

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
		os.mkdir('decoy_ligands')
		os.mkdir('receptors')

	def get_ligand_decoys_init(self, all_pdb_files, all_mol_files, all_num_atoms):
		"""Initializes all global variables needed for get_ligand_decoys"""
		FLAGS.all_pdb_files = all_pdb_files
		FLAGS.all_mol_files = all_mol_files
		FLAGS.all_num_atoms = all_num_atoms
		FLAGS.all_mols = [Chem.MolFromMolFile(all_mol_files[i]) for i in range(len(all_mol_files))]


def get_crystal_ligand_conformers(lig_file):
	"""Performs the following tasks:
		> Creates the receptor folders within binding_ligands and decoy_ligands
		> Converts all PDB crystal ligands into mol for future use
		> Generates conformers and saves them to crystal_ligands folder"""

	# first check to make sure convert_pdb_to_mol_init() was performed
	if not hasattr(FLAGS, 'max_substruct'):
		raise Exception("FLAGS class was not initialized correctly. Please initialize global variables using convert_pdb_to_mol_init()")

	lig_name = lig_file[len(FLAGS.lig_path)+1: ]
	rec_name = lig_name[0:4]

	# create the receptor folders if it does not exist yet
	if not os.path.isdir(os.path.join(FLAGS.out_lig_path, rec_name)):
		os.mkdir(os.path.join(FLAGS.out_lig_path, rec_name))
	if not os.path.isdir(os.path.join(FLAGS.mol_path, rec_name)):
		os.mkdir(os.path.join(FLAGS.mol_path, rec_name))
	if not os.path.isdir(os.path.join(FLAGS.out_decoy_path, rec_name)):
		os.mkdir(os.path.join(FLAGS.out_decoy_path, rec_name))

	# use rdkit to get a mol object from PDB
	pdb_file = os.path.join(FLAGS.out_lig_path, lig_name)
	mol_file = os.path.join(FLAGS.mol_path, lig_name).replace('.pdb', '.sdf')
	
	# write the mol to a mol file for future use
	mol = Chem.MolFromPDBFile(lig_file)
	writer = SDWriter(mol_file)
	writer.write(mol)

	# generate conformers and get the number of atoms of the molecule
	mol2 = Chem.AddHs(mol)
	conf_ids = AllChem.EmbedMultipleConfs(mol2, FLAGS.binding_conformers)
	if len(conf_ids) < FLAGS.binding_conformers:
		raise Exception("Not enough binding conformers")
	for cid in conf_ids:
		_ = AllChem. MMFFOptimizeMolecule(mol2, confId=cid)
	mol = Chem.RemoveHs(mol2)
	num_atoms = Mol.GetNumAtoms(mol)

	# write the mol into PDB format (contains mols)
	pdb_writer = PDBWriter(pdb_file)
	for cid in conf_ids:
		pdb_writer.write(mol, confId=cid)

	print 'Got conformers for one binding ligand'

	return [[pdb_file, mol_file, num_atoms]]


def get_ligand_decoys(pdb_file, mol_file, num_atoms):
	"""For each binding ligand, gets a list of decoy ligands. We filter by 
	number of atoms and maximum common substructure (MCS). Then we generate 
	conformers for each decoy and save them to the decoy_ligands folder.
	"""

	# first check to make sure get_ligand_decoys_init() was performed
	if not hasattr(FLAGS, 'all_mols'):
		raise Exception("FLAGS class was not initialized correctly. Please initialize global variables using get_ligand_decoys_init()")

	reader = SDMolSupplier(mol_file)
	mol = reader[0]
	output = []

	iterator = range(len(FLAGS.all_mols))
	random.shuffle(iterator)
	for i in iterator:
		if FLAGS.all_mol_files[i] == mol_file:
			continue
		if abs(FLAGS.all_num_atoms[i] - num_atoms) <= FLAGS.max_atom_dif:
			mcs = MCS.FindMCS([FLAGS.all_mols[i], mol], minNumAtoms=FLAGS.max_substruct,
				ringMatchesRingOnly=True, completeRingsOnly=True, timeout=1)
			if mcs.numAtoms == -1:
				# generate the decoy and its conformers
				decoy2 = Chem.AddHs(FLAGS.all_mols[i])
				conf_ids = AllChem.EmbedMultipleConfs(decoy2, FLAGS.decoy_conformers)
				if len(conf_ids) < FLAGS.decoy_conformers:
					raise Exception("Not enough decoy conformers")
				for cid in conf_ids:
					AllChem.MMFFOptimizeMolecule(decoy2, confId=cid)
				decoy = Chem.RemoveHs(decoy2)

				# save the mol object as a PDB file in decoys folder
				decoy_file = pdb_file.replace('/binding_ligands/', '/decoy_ligands/').replace('.pdb', str(len(output))+'.pdb')
				pdb_writer = PDBWriter(decoy_file)
				pdb_writer.write(decoy)
				pdb_writer.close()

				output.append([FLAGS.all_pdb_files[i], decoy_file])

		if len(output) >= FLAGS.max_num_decoys:
			break

	print 'Got the decoys for one ligand'
	return output