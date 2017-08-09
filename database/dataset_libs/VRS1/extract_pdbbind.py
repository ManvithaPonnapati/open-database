import joblib
import os, time
import pickle
import numpy as np 
import pickle

from utils import DiskDataset

"""
1: H
2: C
3: N
4: O
5: Halogens
6: P
7: S, Se
8: Alkali/Alkali-earth metals
9: Metals
"""
atom_dictionary = {
	1:1, 
	6:2, 
	7:3, 
	8:4, 
	9:5, 17:5, 35:5, 53:5, 
	15:6, 
	16:7, 34:7,
	11:8, 19:8, 37:8, 55:8, 12:8, 20:8, 38:8, 56:8,
	25:9, 26:9, 27:9, 28:9, 29:9, 30:9, 48:9, 80:9
}

def process_data(coords, nbr_idx, elements):
	num_atoms = len(nbr_idx)

	# truncates off zero padding at the end and maps atomic numbers to atom types
	coords = coords[:num_atoms, :]
	elements = np.array([atom_dictionary[elements[i]] for i in range(num_atoms)], dtype=np.int32)

	# pad the neighbor indices with zeros if not enough neighbors
	elements = np.append(elements, 0)
	for i in range(num_atoms):
		if len(nbr_idx[i]) < 12:
			nbr_idx[i].extend(np.ones([12-len(nbr_idx[i])], dtype=np.int32) * num_atoms)
	nbr_idx = np.array([nbr_idx[i] for i in range(num_atoms)], dtype=np.int32)

	# creates neighboring atom type matrix - 0 = nonexistent atom
	nbr_atoms = np.take(elements, nbr_idx)
	np.place(nbr_idx, nbr_idx >= num_atoms, 0)
	elements = elements[:-1]

	return (coords.astype(np.float32), nbr_idx.astype(np.int32), 
	       elements.astype(np.int32), nbr_atoms.astype(np.int32))


base_dir = os.getcwd()
data_dir = os.path.join(base_dir, "datasets")
train_dir = os.path.join(data_dir, "random_train")
test_dir = os.path.join(data_dir, "random_test")

train_dataset = DiskDataset(train_dir)
test_dataset = DiskDataset(test_dir)


print 'Loading the training dataset...'

X = train_dataset.X
y = train_dataset.y
ids = train_dataset.ids
num_examples = len(ids)

os.mkdir('./pdbbind_refined_train')
os.chdir('./pdbbind_refined_train')

for i in range(num_examples):
	ligand_coords, ligand_nbr_idx, ligand_elements, ligand_nbr_atoms = process_data(X[i][0], X[i][1], X[i][2])
	receptor_coords, receptor_nbr_idx, receptor_elements, receptor_nbr_atoms = process_data(X[i][3], X[i][4], X[i][5])
	complex_coords, complex_nbr_idx, complex_elements, complex_nbr_atoms = process_data(X[i][6], X[i][7], X[i][8])
	label = y[i][0].astype(np.float32)

	os.makedirs(ids[i])
	os.chdir(ids[i])

	path = os.path.join(os.getcwd(), 'data')
	np.savez(path, label=label,
		ligand_coords=ligand_coords, 
		ligand_nbr_idx=ligand_nbr_idx, 
		ligand_nbr_atoms=ligand_nbr_atoms,
		ligand_elements=ligand_elements,
		receptor_coords=receptor_coords, 
		receptor_nbr_idx=receptor_nbr_idx,
		receptor_nbr_atoms=receptor_nbr_atoms, 
		receptor_elements=receptor_elements,
		complex_coords=complex_coords, 
		complex_nbr_idx=complex_nbr_idx, 
		complex_nbr_atoms=complex_nbr_atoms,
		complex_elements=complex_elements)

	os.chdir('..')
	print 'Progress %(example_num)d of %(total)d' % {'example_num': i, 'total': num_examples}

os.chdir('..')


print 'Loading the testing dataset...'

X = test_dataset.X
y = test_dataset.y
ids = test_dataset.ids
num_examples = len(ids)

os.mkdir('./pdbbind_refined_test')
os.chdir('./pdbbind_refined_test')

for i in range(num_examples): 
	ligand_coords, ligand_nbr_idx, ligand_elements, ligand_nbr_atoms = process_data(X[i][0], X[i][1], X[i][2])
	receptor_coords, receptor_nbr_idx, receptor_elements, receptor_nbr_atoms = process_data(X[i][3], X[i][4], X[i][5])
	complex_coords, complex_nbr_idx, complex_elements, complex_nbr_atoms = process_data(X[i][6], X[i][7], X[i][8])
	label = y[i][0].astype(np.float32)

	os.makedirs(ids[i])
	os.chdir(ids[i])

	path = os.path.join(os.getcwd(), 'data')
	np.savez(path, label=label,
		ligand_coords=ligand_coords, 
		ligand_nbr_idx=ligand_nbr_idx, 
		ligand_nbr_atoms=ligand_nbr_atoms,
		ligand_elements=ligand_elements,
		receptor_coords=receptor_coords, 
		receptor_nbr_idx=receptor_nbr_idx,
		receptor_nbr_atoms=receptor_nbr_atoms, 
		receptor_elements=receptor_elements,
		complex_coords=complex_coords, 
		complex_nbr_idx=complex_nbr_idx, 
		complex_nbr_atoms=complex_nbr_atoms,
		complex_elements=complex_elements)

	os.chdir('..')
	print 'Progress %(example_num)d of %(total)d' % {'example_num': i, 'total': num_examples}

print "All done"