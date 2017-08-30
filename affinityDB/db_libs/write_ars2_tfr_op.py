import sys
import numpy as np 
import tensorflow as tf
from collections import defaultdict
from prody import *
from save_record_tfr_op import save_record_tfr

class WriteARS2TFRInit:
    this_module = sys.modules[__name__]
    def __init__(self, num_bind_confs, num_decoy_confs, num_decoys):
        self.num_bind_confs = num_bind_confs
        self.num_decoy_confs = num_decoy_confs
        self.num_decoys = num_decoys

        atom_mapping = [('H', 1.0), ('C', 2.0), ('N', 3.0), ('O', 4.0), ('F', 5.0),
                        ('Cl', 5.0), ('I', 5.0), ('Br', 5.0), ('P', 6.0), ('S', 6.0)]
        self.atom_dict = defaultdict(lambda: 7.0)
        for (k, v) in atom_mapping:
            self.atom_dict[k] = v

        self.this_module.write_ars2_tfr_init = self

def write_ars2_tfr(rec_file, cryst_lig_file, bind_lig_file, decoy_files, out_tfr_file, init='write_ars2_tfr_init'):
	"""For each protein/ligand crystal pair, write one tfrecord with the following:
		> rec_elem, rec_coord, cryst_elem, cryst_coord
		> lig_nelems, lig_elem, lig_nframes, lig_coordsets, lig_labels
	Params:
		rec_file: filepath to receptor PDB
		cryst_lig_file: filepath to crystal ligand PDB
		bind_lig_file: filepath to conformers of crystal ligand PDB
		decoy_files: comma separated filepath to decoy ligands PDB
		out_tfr_file: filepath to write tf record to"""

	init = eval(init)
	rec = parsePDB(rec_file)
	cryst_lig = parsePDB(cryst_lig_file)
	bind_lig = parsePDB(bind_lig_file)

	decoy_files = decoy_files.split(',')
	if len(decoy_files) != init.num_decoys:
		raise Exception("Incorrect number of decoys")

	# Extract all relevant information
	rec_atoms = rec.getElements()
	rec_elem = np.array([init.atom_dict[rec_atoms[i]] for i in range(len(rec_atoms))], dtype=np.float32)
	rec_coord = rec.getCoords().astype(np.float32)
	cryst_atoms = cryst_lig.getElements()
	cryst_elem = np.array([init.atom_dict[cryst_atoms[i]] for i in range(len(cryst_atoms))], dtype=np.float32)
	cryst_coord = cryst_lig.getCoords().astype(np.float32)

	lig_elems = []
	lig_coordsets = []
	lig_labels = []

	bind_lig_coordsets = []
	bind_lig_labels = []
	for i in range(init.num_bind_confs):
		bind_lig.setACSIndex(i)
		if i == 0:
			lig_atoms = bind_lig.getElements()
			lig_elems.append(np.array([init.atom_dict[lig_atoms[j]] for j in range(len(lig_atoms))], dtype=np.float32))
		bind_lig_coordsets.append(bind_lig.getCoords().astype(np.float32))
		bind_lig_labels.append(np.array(1.0, dtype=np.float32))
	lig_coordsets.append(np.array(bind_lig_coordsets))
	lig_labels.append(np.array(bind_lig_labels))

	for decoy_file in decoy_files:
		decoy_lig = parsePDB(decoy_file)
		decoy_lig_coordsets = []
		decoy_lig_labels = []
		for i in range(init.num_decoy_confs):
			decoy_lig.setACSIndex(i)
			if i == 0:
				lig_atoms = decoy_lig.getElements()
				lig_elems.append(np.array([init.atom_dict[lig_atoms[j]] for j in range(len(lig_atoms))], dtype=np.float32))
			decoy_lig_coordsets.append(decoy_lig.getCoords().astype(np.float32))
			decoy_lig_labels.append(np.array(0.0, dtype=np.float32))
		lig_coordsets.append(np.array(decoy_lig_coordsets))
		lig_labels.append(np.array(decoy_lig_labels))

	save_record_tfr(out_tfr_file, cryst_elem, cryst_coord, lig_elems, 
		lig_coordsets, 0.0, lig_labels, rec_elem, rec_coord)

	return [[out_tfr_file]]