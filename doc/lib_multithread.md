[TOC]

# lib_multithread
## Function
### activity
```
activity(
	pair_name,
	target_id,
	init=activity_init,
)
```
Getting bioactivity result from local chembl database
query by the target_chembl_id



**Args**
- **`pair_name`** : str combined receptor id and ligand info {receptor_id}_{chain}_{resnum}_{resname}
- **`target_id`** : str chembl_target_id
- **`init`** : str init function name

**Returns**

sted list:
[pair_name, aid, tid, mid, confidence_score, type, relation, value, unit, smile]


### binding\_affinity
```
binding_affinity(
	index_path,
	init=binding_affinity_init,
)
```
Parse binding affinity record from index_path


**Args**
- **`index_path`** : record file
- **`init`** : str init function name

**Returns**

sult:
list [ pdb_name, ligand_names, log_affinities, normalized_affinities, states, comments]


### blast
```
blast(
	rec_outpath,
	lig_outpath,
	init=blast_init,
)
```
Applying protein sequence blast on the receptor


**Args**
- **`rec_outpath`** : str:: relative path of receptor
- **`lig_outpath`** : str:: relative path of ligand
- **`init`** : str:: init func name

**Returns**

sted list:
blast result contain  pair_name with receptor id and ligand name,     chembl_target_id for similar sequence in database,  ideitity number as num_match/align_length and     the sequence of selected receptor


### dock
```
dock(
	rec_outpath,
	reorder_outpath,
	init=dock_init,
)
```
Docking the ligand by smina


**Args**
- **`rec_outpath`** : str relative path for receptor
- **`reorder_outpath`** : str relative path for reorder ligand
- **`init`** : str init func naem

**Returns**

sted list:
docking result contains the relative path for receptor, reorder ligand and docked ligand


### download\_pdb
```
download_pdb(
	pdb_id,
	init=download_pdb_init,
)
```
Download PDB crystal structure from the Protein Data Bank.


**Args**
- **`pdb_id`** : string (4-letter PDB ID IE: 1QGT)
- **`dir_path`** : string (folder in which to save the pdb file)

**Returns**

sted list:
(of dimensions 1x[string] where string is the relative path to the output file)


### generate\_conformers
```
generate_conformers(
	uid,
	lig_file,
	init=generate_conformers_init,
)
```
Forgets the initial coordinates of the molecule. Looses all hydrogens. Adds all hydrogens.
Generates random conformers. Optimizes conformers with MMFF94 Force Field.
Saves multiframe PDB file of the ligand with new coordinates.

**Args**
- **`lig_file`** : string (path to the ligand file in the PDB format to read)
- **`init`** : string (init function)

**Returns**

sted list:
of dimension [1x[string]]. String is the relative path to the output file.


### num\_atoms
```
num_atoms(
	pdb_file,
	init=num_atoms_init,
)
```


### pdb2mol
```
pdb2mol(
	uid,
	lig_file,
	init=pdb2mol_init,
)
```
Convert .pdb file to .mol file

**Args**
- **`lig_file`** : string (relative path to the ligand file)
- **`init`** : string (init function)

**Returns**



### reorder
```
reorder(
	rec_outpath,
	lig_outpath,
	init=reorder_init,
)
```
Parse the ligand by smina, and then output it. So the order of the atom keeps the same as the docking result


**Args**
- **`rec_outpath`** : str relative path for receptor
- **`lig_outpath`** : str relative path for ligand
- **`init`** : str initialize module

**Returns**

sted list:
order result contains the relative path for receptor and relative path for reorder ligand


### save\_record\_tfr
```
save_record_tfr(
	filename,
	cryst_elem,
	cryst_coord,
	binders_elem,
	binders_coordsets,
	cryst_label,
	binders_labels,
	rec_elem,
	rec_coord,
)
```


**Args**
- **`filename`** : string (file path to the output file)
- **`pos_per_binder`** : integer (number of positions per binder)
- **`cryst_elem`** : np.array shape=[n_elem] type=float32 (elements of the ligand)
- **`cryst_coord`** : np.array shape=[n_elem, 3] type=float32 (coordinates of the elements of the ligand)
- **`binders_elem`** : list of np.array of shape=[n_elem] type=float32 (elements of binders)
- **`binders_coordsets`** : list of np.array [pos_per_binder, n_elem, 3 ] (coordinate sets per each of the bidners)
- **`cryst_label`** : float32 (something about the crystal pose, like binding affinity)
- **`binders_labels`** : list of np.array shape=[pos_per_binder] type=float32
- **`rec_elem`** : np.array of shape [n_elem] of float32
- **`rec_coord`** : np.array of shape [n_elem, 3]

**Returns**
s: None


### get\_decoys
```
get_decoys(
	pdb_file,
	mol_file,
	num_atoms,
	init=get_decoys_init,
)
```
For each binding ligand, get a list of decoy ligands. We filter by number of atoms and maximum common
substructure (MCS). Returns filepaths to all binding ligand - decoy pair.


**Args**
- **`pdb_file`** : 
- **`mol_file`** : 
- **`num_atoms`** : 
- **`init`** : 

**Returns**



### search\_decoys
```
search_decoys(
	molfile_path,
)
```


### split\_pdb
```
split_pdb(
	uid,
	pdb_file,
	init=split_pdb_init,
)
```
Iterates through every ligand molecule in the crystal structure (frequently there are a few). For each ligand
selects and crops its binding site (any atom of Protein/DNA/Cofactor within the cutoff distance). Saves pairs of
files: ligand + this ligand's binding site.


**Args**
- **`pdb_file`** : string (relative path the the file to split)
- **`cutoff_dist`** : float (distance of any atoms in the binding site from any atom of the ligand to be saved)
- **`min_rec_atoms`** : minimun number of atoms be saved as binding site
- **`min_lig_atoms`** : minumum number of atoms for ligand to be saved
- **`init`** : string (init function in this module)

**Returns**

sted list of pairs of file names of dimensions [num_pairs x [string,string,int,int]] or     [num_pairs x [lig_file,bindsite_file,lig_num_atoms,bindsite_num_atoms]]


### test\_multout
```
test_multout(
	num,
	init=test_multout_init,
)
```


### test\_sum
```
test_sum(
	num1,
	num2,
	init=test_sum_init,
)
```


### save\_record\_tfr
```
save_record_tfr(
	filename,
	cryst_elem,
	cryst_coord,
	binders_elem,
	binders_coordsets,
	cryst_label,
	binders_labels,
	rec_elem,
	rec_coord,
)
```


**Args**
- **`filename`** : string (file path to the output file)
- **`pos_per_binder`** : integer (number of positions per binder)
- **`cryst_elem`** : np.array shape=[n_elem] type=float32 (elements of the ligand)
- **`cryst_coord`** : np.array shape=[n_elem, 3] type=float32 (coordinates of the elements of the ligand)
- **`binders_elem`** : list of np.array of shape=[n_elem] type=float32 (elements of binders)
- **`binders_coordsets`** : list of np.array [pos_per_binder, n_elem, 3 ] (coordinate sets per each of the bidners)
- **`cryst_label`** : float32 (something about the crystal pose, like binding affinity)
- **`binders_labels`** : list of np.array shape=[pos_per_binder] type=float32
- **`rec_elem`** : np.array of shape [n_elem] of float32
- **`rec_coord`** : np.array of shape [n_elem, 3]

**Returns**
s: None


### write\_ars2\_tfr
```
write_ars2_tfr(
	rec_file,
	cryst_lig_file,
	bind_lig_file,
	decoy_files,
	out_tfr_file,
	init=write_ars2_tfr_init,
)
```
For each protein/ligand crystal pair, write one tfrecord with the following:
> rec_elem, rec_coord, cryst_elem, cryst_coord
> lig_nelems, lig_elem, lig_nframes, lig_coordsets, lig_labels


**Args**
- **`rec_file`** : filepath to receptor PDB
- **`cryst_lig_file`** : filepath to crystal ligand PDB
- **`bind_lig_file`** : filepath to conformers of crystal ligand PDB
- **`decoy_files`** : comma separated filepath to decoy ligands PDB
- **`out_tfr_file`** : filepath to write tf record to

**Returns**
None


## Class
## Activity_init
### \_\_init\_\_
```
__init__(
	self,
	data_dir,
	db_path,
)
```


**Args**
- **`data_dir`** : str dir for the folder to save data
- **`db_path`** : str path for the chembl database

**Returns**
None


## Binidng_affinity_init
### \_\_init\_\_
```
__init__(
	self,
	db_root,
	parse_type,
)
```


**Args**
- **`db_root`** : string (path to the root folder of the database)
- **`parse_type`** : source of binding affinity record ['pdbbind','bindingmoad','bindingdb']

**Returns**
None


### parse\_bindingdb
```
parse_bindingdb(
	self,
	binding_db_index,
)
```


### parse\_bindingmoad
```
parse_bindingmoad(
	self,
	binding_moad_index,
)
```


### parse\_bindingmoad\_entry
```
parse_bindingmoad_entry(
	self,
	entry,
)
```


### parse\_pdbbind
```
parse_pdbbind(
	self,
	pdb_bind_index,
)
```


## Blast_init
### \_\_init\_\_
```
__init__(
	self,
	data_dir,
	blast_db,
)
```


**Args**
- **`data_dir`** : str dir for the data
- **`blast_db`** : str path of the blast database

**Returns**
None


## Dock_init
### \_\_init\_\_
```
__init__(
	self,
	data_dir,
	dock_folder,
	smina_path,
	dock_param,
)
```


**Args**
- **`data_dir`** : str dir for the folder to save data
- **`dock_folder`** : str name of the folder to save reorder output
- **`smina_path`** : str path for teh executable smina program
- **`dock_param`** : dict docking parameter {'args':[...], 'kwargs':{...}}

**Returns**
None


### make\_command
```
make_command(
	self,
)
```


### param\_load
```
param_load(
	self,
	param,
)
```


## Download_pdb_init
### \_\_init\_\_
```
__init__(
	self,
	db_root,
	download_dir,
)
```


**Args**
- **`db_root`** : string (root folder directory for the files in the database)
- **`download_dir`** : string (name of the directory where to put downloaded PDBs)

**Returns**
None


## Generate_conformers_init
### \_\_init\_\_
```
__init__(
	self,
	db_root,
	conformers_dir,
	num_conformers,
	out_H,
)
```


**Args**
- **`db_root`** : string (database root)
- **`conformers_dir`** : string (name of the directory where to put generated conformers)
- **`num_conformers`** : int (number of the conformers to output)
- **`out_H`** : bool T/F (Add hydrogen atoms to the output. All input hydorogen atoms are always lost.)

**Returns**
None


## Num_atoms_init
### \_\_init\_\_
```
__init__(
	self,
	db_root,
)
```


**Args**
- **`db_root`** : string (path to the root of the database)

**Returns**
None


## Pdb2mol_init
### \_\_init\_\_
```
__init__(
	self,
	db_root,
	molfile_dir,
)
```


**Args**
- **`db_root`** : string (database root)
- **`molfile_dir`** : string (relative path where to create the output directory with .mol files)

**Returns**
None


## Reorder_init
### \_\_init\_\_
```
__init__(
	self,
	data_dir,
	reorder_folder,
	smina_path,
	dock_param,
)
```


**Args**
- **`data_dir`** : str dir for the folder to save data
- **`reorder_folder`** : str name of the folder to save reorder output
- **`smina_path`** : str path for teh executable smina program
- **`dock_param`** : dict docking parameter {'args':[...], 'kwargs':{...}}

**Returns**
None


### make\_command
```
make_command(
	self,
)
```


### param\_load
```
param_load(
	self,
	param,
)
```


## Search_decoys_init
### \_\_init\_\_
```
__init__(
	self,
	db_root,
	decoy_ids,
	decoy_natoms,
	decoy_molfiles,
	max_decoys=10,
	atom_diff=5,
	max_substruct=5,
)
```


**Args**
- **`db_root`** : 
- **`decoy_ids`** : 
- **`decoy_natoms`** : 
- **`decoy_molfiles`** : 
- **`max_decoys`** : 
- **`atom_diff`** : 
- **`max_substruct`** : 

**Returns**
None


## Split_pdb_init
### \_\_init\_\_
```
__init__(
	self,
	db_root,
	split_dir,
	discard_h=True,
	cutoff_dist=10,
	min_rec_atoms=10,
	min_lig_atoms=5,
)
```


**Args**
- **`db_root`** : string (path to the root folder of the database)
- **`split_dir`** : string (where to put split pdbs)
- **`discard_h`** : Bool T/F (discard all hydrogens for both ligand and receptor defaults to True)

**Returns**
None


## Test_multout_init
### \_\_init\_\_
```
__init__(
	self,
)
```


## Test_sum_init
### \_\_init\_\_
```
__init__(
	self,
)
```


## WriteARS2TFRInit
### \_\_init\_\_
```
__init__(
	self,
	num_bind_confs,
	num_decoy_confs,
	num_decoys,
)
```


