To obtain the datasets:

1) Run get_pdbbind.sh. This will download the database from the server in folder "datasets". (copied from deepchem github)
	- NOTE: This might not work - ask Brian for the dataset in joblib format

2) Run extract_pdbbind.py. This will preprocess and save the datasets in numpy arrays that contain the data necessary for the Atomic Convolutions (ligand, receptor, and complex -- coords, neighbor indices, neighbor atom types, and elements). 
	- Note that you can change the atom_dictionary if you want to change the atom type representation.
	- To train on a different dataset (currently defaults to random split for the refined dataset), simply change the path variables accordingly. 
	- utils.py contains many utility functions/classes used in extract_pdbbind.py, in particular DiskDataset accesses the joblib file and gets data using .X, .y, .ids. (edited from deepchem github)
