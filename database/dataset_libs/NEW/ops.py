import os, sqlite3, sys, random, time
import numpy as np
import tensorflow as tf
from collections import defaultdict
from glob import glob 
from rdkit import Chem
from rdkit.Chem import MCS, AllChem
from rdkit.Chem.rdchem import Mol
from rdkit.Chem.rdmolfiles import SDWriter, SDMolSupplier, PDBWriter
from prody import *


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
		self.ligand_files = glob(os.path.join(self.lig_path + '/**/', '*[_]*.pdb'))[:10]
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


class WriteTFRInit:

	this_module = sys.modules[__name__]

	def __init__(self, base_dir, num_bind_confs, num_decoy_confs, num_decoys):
		"""Initializes all the directories and filepaths needed to write to TFR"""

		self.base_dir = base_dir
		self.receptor_path = os.path.join(base_dir, 'labeled_pdb/receptors')
		self.crystal_lig_path = os.path.join(base_dir, 'labeled_pdb/crystal_ligands')
		self.conformer_path = os.path.join(base_dir, 'vds_pdb/binding_ligands')
		self.decoy_path = os.path.join(base_dir, 'vds_pdb/decoy_ligands')
		self.out_tfr_path = os.path.join(base_dir, 'tfr')
		self.num_bind_confs = num_bind_confs
		self.num_decoy_confs = num_decoy_confs
		self.num_decoys = num_decoys

		if os.path.exists(self.out_tfr_path):
			os.system('rm -r ' + self.out_tfr_path)
		os.mkdir(self.out_tfr_path)

		mapping = [('H', 1), ('C', 2), ('N', 3), ('O', 4), ('F', 5), ('Cl', 5),
			('I', 5), ('Br', 5), ('P', 6), ('S', 6)]
		self.atom_dict = defaultdict(lambda: 7)
		for (k, v) in mapping:
			self.atom_dict[k] = v

		self.this_module.write_tfr_init = self


def write_tfr(bind_lig_file, init='write_tfr_init'):
	"""For each protein/ligand crystal pair, write one tfrecord with the following:
		> rec_elem, rec_coord, cryst_elem, cryst_coord (np.array)
		> num_confs (int): The number of binding/decoy conformers
		> filename (str): File path to the output file
		> cryst_label (float32): Binding affinity of the crystal pose
		> lig_elems (list of np.array)
		> lig_coordsets (list of np.array)
		> lig_labels (list of np.array): 1 if binding ligand and 0 if decoy"""

	init = eval(init)

	# parse the binding ligand
	bind_lig = parsePDB(bind_lig_file)
	# parse the receptor
	rec_name = bind_lig_file[len(init.conformer_path)+1: len(init.conformer_path)+5]
	rec_file = os.path.join(init.receptor_path, rec_name+'.pdb')
	rec = parsePDB(rec_file)
	# parse the crystal ligand
	crystal_lig_file = bind_lig_file.replace('/vds_pdb/binding_ligands/', '/labeled_pdb/crystal_ligands/')
	crystal_lig = parsePDB(crystal_lig_file)
	# get the decoy ligand filepaths
	decoy_files = glob(bind_lig_file.replace('/binding_ligands/', '/decoy_ligands/').replace('.pdb', '*.pdb'))

	# check to make sure that there are enough decoys 
	if len(decoy_files) < init.num_decoys:
		raise Exception("Not enough decoys")

	# extract all relevant information
	rec_atoms = rec.getElements()
	rec_elem = [init.atom_dict[rec_atoms[i]] for i in range(len(rec_atoms))]
	rec_coord = rec.getCoords()
	cryst_atoms = crystal_lig.getElements()
	cryst_elem = [init.atom_dict[cryst_atoms[i]] for i in range(len(cryst_atoms))]
	cryst_coord = crystal_lig.getCoords()
	# TODO: get the crystal label

	lig_elems = []
	lig_coordsets = []
	lig_labels = []

	for i in range(init.num_bind_confs):
		bind_lig.setACSIndex(i)
		lig_atoms = bind_lig.getElements()
		lig_elems.append([init.atom_dict[lig_atoms[j]] for j in range(len(lig_atoms))])
		lig_coordsets.append(bind_lig.getCoords())
		lig_labels.append(np.array(1))

	for decoy_file in decoy_files:
		decoy_lig = parsePDB(decoy_file)
		for i in range(init.num_decoy_confs):
			decoy_lig.setACSIndex(i)
			lig_atoms = decoy_lig.getElements()
			lig_elems.append([init.atom_dict[lig_atoms[j]] for j in range(len(lig_atoms))])
			lig_coordsets.append(decoy_lig.getCoords())
			lig_labels.append(np.array(0))

	assert type(cryst_elem) == np.ndarray
	assert cryst_elem.dtype == np.float32
	assert len(cryst_elem.shape) == 1

	assert type(cryst_coord) == np.ndarray
	assert cryst_coord.dtype == np.float32
	assert len(cryst_coord.shape) == 2
	assert cryst_coord.shape[1] == 3
	assert cryst_coord.shape[0] == cryst_elem.shape[0]

	assert type(lig_elems) == list
	num_ligs = len(lig_elems)
	for i in range(num_ligs):
		assert type(lig_elems[i]) == np.ndarray
		assert str(lig_elems[i].dtype) in {'float32', 'np.float32'}
		assert len(lig_elems[i].shape) == 1

	assert type(lig_coordsets) == list
	assert len(lig_coordsets) == num_ligs
	for i in range(num_ligs):
		assert type(lig_coordsets[i]) == np.ndarray
		assert str(lig_coordsets[i].dtype) in {"float32", "np.float32"}
		assert len(lig_coordsets[i].shape) == 3
		assert lig_coordsets[i].shape[2] == 3
		assert lig_coordsets[i].shape[1] == lig_elems[i].shape[0]

	assert type(lig_labels) == list
	assert len(lig_labels) == num_ligs
	for i in range(num_ligs):
		assert type(lig_labels[i]) == np.ndarray
		assert str(lig_labels[i].dtype) in {'float32', 'np.float32'}
		assert len(lig_labels[i].shape) == 1
		assert lig_labels[i].shape[0] == lig_coordsets[i].shape[0]

	assert type(rec_elem) == np.ndarray
	assert rec_elem.dtype == np.float32
	assert len(rec_elem.shape) == 1

	assert type(rec_coord) == np.ndarray
	assert rec_coord.dtype == np.float32
	assert len(rec_coord.shape) == 2
	assert rec_coord.shape[1] == 3
	assert rec_coord.shape[0] == rec_elem.shape[0]

	rec_elem = rec_elem
	rec_coord = rec_coord.reshape([-1])
	cryst_elem = cryst_elem
	cryst_coord = cryst_coord.reshape([-1])
	lig_nelems = [lig_elems[i].shape[0] for i in range(num_ligs)]
	lig_elems = np.concatenate([lig_elems[i] for i in range(num_ligs)], axis=0)
	lig_nframes = [lig_coordsets[i].shape[0] for i in range(num_ligs)]
	lig_coordsets = np.concatenate([lig_coordsets[i].reshape([-1]) for i in range(num_ligs)])
	lig_labels = np.concatenate([lig_labels[i].reshape([-1]) for i in range(num_ligs)])

	filename = os.path.join(init.out_tfr_path, bind_lig_file[len(init.conformer_path)+6:].replace('.pdb', '.tfr'))
	writer = tf.python_io.TFRecordWriter(filename)
	example = tf.train.Example(
		features=tf.train.Features(
		feature={
			'_rec_elem': tf.train.Feature(float_list=tf.train.FloatList(value=rec_elem)),
			'_rec_coord': tf.train.Feature(float_list=tf.train.FloatList(value=rec_coord)),
			'_cryst_elem': tf.train.Feature(float_list=tf.train.FloatList(value=cryst_elem)),
			'_cryst_coord': tf.train.Feature(float_list=tf.train.FloatList(value=cryst_coord)),
			# '_cryst_label': tf.train.Feature(float_list=tf.train.FloatList(value=cryst_label)),
			'_lig_nelems': tf.train.Feature(int64_list=tf.train.Int64List(value=lig_nelems)),
			'_lig_elems': tf.train.Feature(float_list=tf.train.FloatList(value=lig_elems)),
			'_lig_nframes': tf.train.Feature(int64_list=tf.train.Int64List(value=lig_nframes)),
			'_lig_coordsets': tf.train.Feature(float_list=tf.train.FloatList(value=lig_coordsets)),
			'_lig_labels': tf.train.Feature(float_list=tf.train.FloatList(value=lig_labels))
		})
	)
	serialized = example.SerializeToString()
	writer.write(serialized)
	writer.close()
	return [[filename]]