### Vina Docking Set (VDS1)
all receptor-ligand pairs in the PDB
1) Original ligands docked back
2) 50? property-matching decoys per original ligand docked with noisy Vina/Vinardo
3) Binding affinity information pulled from 3 databases for 20,000 of the ligands

Experiments: 
1*) Predict Vina correct/incorrect position (Vina energy minima)
2) Predict true correct/incorrect position
3*) Predict binders/non-binders with Vina score
4) Predict true binders/non-binders from docking 

### Binding Set (BS1)
all receptor-ligand pairs in PubChem/CHEMBL with protein structure (not co-crystal) docked
1) Predict binders/non-binders with Vina score
2) Predict true binders/non-binders

6A -> and see the numbers of amino acids -> 156, 157, 158 ,212,15,16 -> QEDFRQEEEDPRPPP (amino acid sequence) -> search EDFRQE -> hits 90% identity -> save into DB -> (optional) 

Vina docking and binding sets go together.


### Cambridge Structural Database (Molecule Structure Set) CSD1
0.5M structures of the molecules from Cambridge Crystallographic Database
1) Predict correct structure

### Affinity Regression Set (ARS1)
ARS1 contains protein-ligand complexes and their binding affinites from three databases: PDBBind, BindingMOAD, and BindingDB. PDBBind contains 10483 samples, BindingMOAD contains 8869 samples, and BindingDB contains 7337 samples. A list of 69357 protein-ligand structures was collected, and all of the structures available as PDB files were downloaded. The functions "split_ligand" and "split_receptor" were used to seperate ligands from protein structures. Ligands were filtered by selecting those that have a maximum pairwise atom distance less than or equal to 20 angstroms. Only complexes that have binding affinities listed in one or more of the databases were selected. This left 21071 unique samples. The samples were exported in TFRecords file format. 

You can access this dataset by going to /data/affinity/ars1_v2 on CBA Titan.

### Vijay Regression Set 1
These files are used to obtain the PDBBind data from deepchem's AWS. This dataset reports labels in the form log(Kd/Ki), and is used in deepchem's Atomic Convolutions. 
### lINK

To obtain the datasets:

1) Run get_pdbbind.sh. This will download the database from the server in folder "datasets". (copied from deepchem github)
	- NOTE: This might not work - ask Brian for the dataset in joblib format

2) Run extract_pdbbind.py. This will preprocess and save the datasets in numpy arrays that contain the data necessary for the Atomic Convolutions (ligand, receptor, and complex -- coords, neighbor indices, neighbor atom types, and elements). 
	- Note that you can change the atom_dictionary if you want to change the atom type representation.
	- To train on a different dataset (currently defaults to random split for the refined dataset), simply change the path variables accordingly. 
	- utils.py contains many utility functions/classes used in extract_pdbbind.py, in particular DiskDataset accesses the joblib file and gets data using .X, .y, .ids. (edited from deepchem github)

### Affinity Regression Set (ARS2)
Same thing but all molecules with some filter.

### Affinity Directory of Useful Decoys (ARS1_DUD)
ARS1 dataset with structures (From Smiles or confomers) from ARS1. Every ligand will have mathing decoys with +/- same number of atoms and verified not to be a substructure). 
May Potentially integrate with BS1

### Affinity Directory of Useful Decoys (ARS2_DUD)

### Vijay Regression Set (VRS1)
Is a subset of AffinityRegression Set (Refined Structures from PDBBind)


### Rosetta Folding Set (RFS1)
all small peptydes from the pdb folding attempts with 
1*) Predict Rosetta Energy score/Energy minima
2) Predict real folding energy minima

### Quantum Set (QM9)
QM9 with different properties calculated with precise methods
1) predict Energy of atomization and other properties


<br />
<br />
<br />

## 2D Datasets

### MSHAPES Dataset
Shapes cut in half, with each half rotated by a random amount.

Each dataset is in the format `MSHAPES_{max degrees}DEG_{one color or random color (whether pairs are colored uniquely)}_SIMPLE_{number of example pairs}_{image dimensions}`, stored at `/data/affinity/2d/MSHAPES/` on Titan, or [here](https://electronneutrino.com/affinity/shapes/datasets/) on νe.


### JSHAPES_HARD Dataset
Cut-out shapes, rotated and translated randomly. Images are 200 by 200 pixels. 50k pairs. Stored at `/data/affinity/2d/JSHAPES_HARD`; download from νe [here](https://electronneutrino.com/affinity/shapes/datasets/JSHAPES_360DEG_HARD_50k_200x200.zip).

