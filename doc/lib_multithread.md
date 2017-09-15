[TOC]
# Function
### activity
```python
activity(
	pair_name,
	target_id,
	init=activity_init,
)
```
Getting bioactivity result from local chembl database     query by the `target_chembl_id`

Example:
```python
activity('154L_A_188_NAG','CHEMBL2366438')
```

Output:
```python
[['154L_A_188_NAG','CHEMBL3070308','CHEMBL2366438','CHEMBL223593',9,'IC50','=',28.0,'nM','CC(Oc1ccc(Oc2ncc(cc2Cl)C(F)(F)F)cc1)C(=O)O']]
```



Args:
- **`pair_name`** : str combined receptor id and ligand info {receptor_id}_{chain}_{resnum}_{resname}
- **`target_id`** : str chembl_target_id
- **`init`** : str init function name


Returns:

nested list:
[pair_name, aid, tid, mid, confidence_score, type, relation, value, unit, smile]


### binding\_affinity
```python
binding_affinity(
	index_path,
	init=binding_affinity_init,
)
```
Parse binding affinity record from index_path

Example:
```python
binding_affinity('nr.csv','bindingmoad')
```

Output:
```
[['4CPA','GLY',-19.1138279245,0.538831666908,1,'success'],
 ['4FAB','FDS',-18.5485141155,0.552471259564,1,'success']]
```


Args:
- **`index_path`** : record file
- **`init`** : str init function name


Returns:

Nested list [ [pdb_name, ligand_names, log_affinities, normalized_affinities, states, comments] ]


### blast
```python
blast(
	rec_outpath,
	lig_outpath,
	init=blast_init,
)
```
Applying protein sequence blast on the receptor

Example:
```python
blast('split/10MH_C_427_5NC/10MH_C_427_5NC_receptor.pdb','split/10MH_C_427_5NC/10MH_C_427_5NC_ligand.pdb')
```

Output:
```python
[['10MH_C_427_5NC', 'CHEMBL2242732', 0.44, 'FFAGFPCQFSISGMENVKNFKRERIQTLSAYGKMKFGNSVV']]
```


Args:
- **`rec_outpath`** : str:: relative path of receptor
- **`lig_outpath`** : str:: relative path of ligand
- **`init`** : str:: init func name


Returns:

nested list: [ [pair_name, chembl_target_id, identity, sequence]]


### dock
```python
dock(
	rec_outpath,
	reorder_outpath,
	init=dock_init,
)
```
Docking the ligand by smina

Example:
```python
dock('3_split_receptor/10MH/10MH_B_407_5CM_receptor.pdb','4_reorder/10MH/10MH_B_407_5CM_ligand.pdb')
```

Output:
```python
[['3_split_receptor/10MH/10MH_B_407_5CM_receptor.pdb', '4_reorder/10MH/10MH_B_407_5CM_ligand.pdb', '5_vinardo/10MH/10MH_C_427_5NC_ligand.pdb']]
```


Args:
- **`rec_outpath`** : str relative path for receptor
- **`reorder_outpath`** : str relative path for reorder ligand
- **`init`** : str init func naem


Returns:

Nested list [[receptor_path, ligand_path, dock_result_path]]


### download\_pdb
```python
download_pdb(
	pdb_id,
	init=download_pdb_init,
)
```
Download PDB crystal structure from the Protein Data Bank.

Example:
```python
download_pdb('104M')
```

Output:
```python
[['104M','download/104M.pdb']]
```


Args:
- **`pdb_id`** : string (4-letter PDB ID IE: 1QGT)
- **`dir_path`** : string (folder in which to save the pdb file)


Returns:

nested list [[pdb_identifier, download_file_path]]


### generate\_conformers
```python
generate_conformers(
	uid,
	lig_file,
	init=generate_conformers_init,
)
```
Forgets the initial coordinates of the molecule. Looses all hydrogens. Adds all hydrogens.
Generates random conformers. Optimizes conformers with MMFF94 Force Field.
Saves multiframe PDB file of the ligand with new coordinates.

Args:
- **`lig_file`** : string (path to the ligand file in the PDB format to read)
- **`init`** : string (init function)


Returns:

nested list:
of dimension [1x[string]]. String is the relative path to the output file.


### num\_atoms
```python
num_atoms(
	pdb_file,
	init=num_atoms_init,
)
```
Counter the number of atom

Example:
```python
num_atoms('4_reorder/10MH/10MH_B_407_5CM_ligand.pdb')
```

Output:
```python
[[10]]
```


Args:
- **`pdb_file`** : relative path of the pdb file


Returns:

nested list [[atom_num]]


### pdb2mol
```python
pdb2mol(
	uid,
	lig_file,
	init=pdb2mol_init,
)
```
Convert .pdb file to .mol file

Args:
- **`lig_file`** : string (relative path to the ligand file)
- **`init`** : string (init function)


Returns:



### reorder
```python
reorder(
	rec_outpath,
	lig_outpath,
	init=reorder_init,
)
```
Parse the ligand by smina, and then output it. So the order of the atom keeps the same as the docking result

Example:
```python
reorder('3_split_receptor/10MH/10MH_B_407_5CM_receptor.pdb','2_split_ligand/10MH/10MH_B_407_5CM_ligand.pdb')
```

Output:
```python
[['3_split_receptor/10MH/10MH_B_407_5CM_receptor.pdb', '4_reorder/10MH/10MH_B_407_5CM_ligand.pdb']]
```


Args:
- **`rec_outpath`** : str relative path for receptor
- **`lig_outpath`** : str relative path for ligand
- **`init`** : str initialize module


Returns:
:returns:
nested list: [[receptor_output_path, reorder_ligand_output_path]]


### save\_record\_tfr
```python
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
Save input data into Tensorflow Record

Args:
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


Returns:

None


### get\_decoys
```python
get_decoys(
	pdb_file,
	mol_file,
	num_atoms,
	init=get_decoys_init,
)
```
For each binding ligand, get a list of decoy ligands. We filter by number of atoms and maximum common
substructure (MCS). Returns filepaths to all binding ligand - decoy pair.


Args:
- **`pdb_file`** : pdb format ligand
- **`mol_file`** : mol format ligand
- **`num_atoms`** : ligand's atom number
- **`init`** : 


Returns:

nested list [[pdb_file, decoy_files]]


### search\_decoys
```python
search_decoys(
	molfile_path,
)
```


### split\_pdb
```python
split_pdb(
	uid,
	pdb_file,
	init=split_pdb_init,
)
```
Iterates through every ligand molecule in the crystal structure (frequently there are a few). For each ligand
selects and crops its binding site (any atom of Protein/DNA/Cofactor within the cutoff distance). Saves pairs of
files: ligand + this ligand's binding site.

Example:
```python
split_pdb('105M','download/105M.pdb')
```

Output:
```python
[['05M_A_155_HEM','split/105M_A_155_HEM/105M_A_155_HEM_receptor.pdb','split/105M_A_155_HEM/105M_A_155_HEM_ligand.pdb',30,100]]
```


Args:
- **`pdb_file`** : string (relative path the the file to split)
- **`cutoff_dist`** : float (distance of any atoms in the binding site from any atom of the ligand to be saved)
- **`min_rec_atoms`** : minimun number of atoms be saved as binding site
- **`min_lig_atoms`** : minumum number of atoms for ligand to be saved
- **`init`** : string (init function in this module)


Returns:

nested list of pairs of file names of dimensions [num_pairs x [string,string,int,int]] or     [num_pairs x [lig_file,bindsite_file,lig_num_atoms,bindsite_num_atoms]]


### test\_multout
```python
test_multout(
	num,
	init=test_multout_init,
)
```


### test\_sum
```python
test_sum(
	num1,
	num2,
	init=test_sum_init,
)
```


### save\_record\_tfr
```python
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
Save input data into Tensorflow Record

Args:
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


Returns:

None


### write\_ars2\_tfr
```python
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


Args:
- **`rec_file`** : filepath to receptor PDB
- **`cryst_lig_file`** : filepath to crystal ligand PDB
- **`bind_lig_file`** : filepath to conformers of crystal ligand PDB
- **`decoy_files`** : comma separated filepath to decoy ligands PDB
- **`out_tfr_file`** : filepath to write tf record to


Returns:
None


# Class
## Activity_init
### \_\_init\_\_
```python
__init__(
	self,
	data_dir,
	db_path,
)
```
Initialize activity func

Args:
- **`data_dir`** : str dir for the folder to save data
- **`db_path`** : str path for the chembl database


Returns:

None


## Binidng_affinity_init
### \_\_init\_\_
```python
__init__(
	self,
	db_root,
	parse_type,
)
```
Initialize binding affinity parse func

Args:
- **`db_root`** : string (path to the root folder of the database)
- **`parse_type`** : source of binding affinity record ['pdbbind','bindingmoad','bindingdb']


Returns:

None


## Blast_init
### \_\_init\_\_
```python
__init__(
	self,
	data_dir,
	blast_db,
)
```
Initialize blast func

Args:
- **`data_dir`** : str dir for the data
- **`blast_db`** : str path of the blast database


Returns:

None


## Dock_init
### \_\_init\_\_
```python
__init__(
	self,
	data_dir,
	dock_folder,
	smina_path,
	dock_param,
)
```


Args:
- **`data_dir`** : str dir for the folder to save data
- **`dock_folder`** : str name of the folder to save reorder output
- **`smina_path`** : str path for teh executable smina program
- **`dock_param`** : dict docking parameter {'args':[...], 'kwargs':{...}}


Returns:
None


## Download_pdb_init
### \_\_init\_\_
```python
__init__(
	self,
	db_root,
	download_dir,
)
```
Initialize download func

Args:
- **`db_root`** : string (root folder directory for the files in the database)
- **`download_dir`** : string (name of the directory where to put downloaded PDBs)


Returns:

None


## Generate_conformers_init
### \_\_init\_\_
```python
__init__(
	self,
	db_root,
	conformers_dir,
	num_conformers,
	out_H,
)
```


Args:
- **`db_root`** : string (database root)
- **`conformers_dir`** : string (name of the directory where to put generated conformers)
- **`num_conformers`** : int (number of the conformers to output)
- **`out_H`** : bool T/F (Add hydrogen atoms to the output. All input hydorogen atoms are always lost.)


Returns:
None


## Num_atoms_init
### \_\_init\_\_
```python
__init__(
	self,
	db_root,
)
```
Initialize num_atoms func

Args:
- **`db_root`** : string (path to the root of the database)


Returns:

None


## Pdb2mol_init
### \_\_init\_\_
```python
__init__(
	self,
	db_root,
	molfile_dir,
)
```


Args:
- **`db_root`** : string (database root)
- **`molfile_dir`** : string (relative path where to create the output directory with .mol files)


Returns:
None


## Reorder_init
### \_\_init\_\_
```python
__init__(
	self,
	data_dir,
	reorder_folder,
	smina_path,
	dock_param,
)
```
Initialize reorder func


Args:
- **`data_dir`** : str dir for the folder to save data
- **`reorder_folder`** : str name of the folder to save reorder output
- **`smina_path`** : str path for teh executable smina program
- **`dock_param`** : dict docking parameter {'args':[...], 'kwargs':{...}}


Returns:

None


## Search_decoys_init
### \_\_init\_\_
```python
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


Args:
- **`db_root`** : 
- **`decoy_ids`** : 
- **`decoy_natoms`** : 
- **`decoy_molfiles`** : 
- **`max_decoys`** : 
- **`atom_diff`** : 
- **`max_substruct`** : 


Returns:

None


## Split_pdb_init
### \_\_init\_\_
```python
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


Args:
- **`db_root`** : string (path to the root folder of the database)
- **`split_dir`** : string (where to put split pdbs)
- **`discard_h`** : Bool T/F (discard all hydrogens for both ligand and receptor defaults to True)


Returns:
None


## Test_multout_init
### \_\_init\_\_
```python
__init__(
	self,
)
```


## Test_sum_init
### \_\_init\_\_
```python
__init__(
	self,
)
```


## WriteARS2TFRInit
### \_\_init\_\_
```python
__init__(
	self,
	num_bind_confs,
	num_decoy_confs,
	num_decoys,
)
```


