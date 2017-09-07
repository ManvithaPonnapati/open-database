# api_docs
 ***
## database
### database.AffinityDB
#### \_\_init\_\_
```
__init__(
	self,
	db_root,
	db_name,
)
```

#### coninue
```
coninue(
	self,
	arg_table,
	num_threads,
	commit_sec,
)
```
Continue the interrupted run_multithread function.

**Args**
- **`arg_table`** : string (name of the sqlite table with arguments of the function to run)
- **`num_threads`** : integer (number of processes)
- **`commit_sec`** : integer (write outputs to the database every number of tasks)

**Returns**
None

#### open\_table\_with\_queue
```
open_table_with_queue(
	self,
	table_name,
	col_names,
	col_types,
	commit_sec=1,
)
```
Creates an output table, and a queue to feed this table. Creates a background thread to take results
from the queue and insert into the table.

Exaple usage:
```python
out_q,stop_event = afdb.open_table_with_queue(table_name="some_table",col_names=["num"],col_types=[int])
for i in range(1000):
    out_q.put([i])
stop_event.set()
```


**Args**
- **`table_name`** : string (name of the table prefix out_xxx_ will be appended)
- **`col_names`** : list of strings (names of the columns)
- **`col_types`** : list of python types (column types)

**Returns**
multiprocessing queue: event to close the table and terminate thread.

#### run\_multithread
```
run_multithread(
	self,
	func,
	arg_sets,
	num_threads=10,
	commit_sec=1,
)
```
Run any function in lib_multithread in multiple threads.
Writes all arguments to arg_xxx_func table, record outputs to out_xxx_table. Record state of the function's
initializer to cron table.

If the task is interrupted in the process of execution, it is possible to resume with `AffinityDB.continue(*)`


**Args**
- **`func`** : string (a name of the function to execute)
- **`arg_sets`** : lits of tuples (every tuple is an argument set for a single run of a function)
- **`num_threads`** : integer (number of independent processes)
- **`commit_sec`** : integer (time delay in flushing outputs to the arg_ and out_ tables)

**Returns**
None

### database.DatabaseMaster
#### \_\_init\_\_
```
__init__(
	self,
	db_path,
)
```

#### list\_search
```
list_search(
	self,
	search_with,
	search_in,
)
```
Search with each element of the "search_with" in the list "search_in".


**Args**
- **`search_with`** : list of [str/float/int]
- **`search_in`** : list of [str/float/int]

**Returns**

hits_idx:
A list of length len(search_with) of lists. Internal list is indexes [j1,j2,j3,j4] such that values         search_with[i] == search_in[j1], search_with[i] == search_in[j2], ...
hits_val:
Same as hits_idx but lists with values instead of indexes
pairs_idx:
Two lists of the same length. search_with[pairs_idx[0][i]] == search_in[pairs_idx[1][i]]

#### merge
```
merge(
	self,
	into_table,
	from_table,
	merge_cols,
	order,
)
```
Merges any table into the output table

Suggestion:
When providing order, please, use `run_idx` for the argument table, and `out_idx` for the output table.
Also, it the `arg_table` it is a good idea to select `run_idx ==1`


**Args**
- **`into_table`** : string (table to merge into)
- **`from_table`** : string (table to merge from)
- **`merge_cols`** : list of strings (names of the columns in merge_from to merge)
- **`order`** : Two lists of the same length. into_table_idx <-- from_table_idx         First list: idx of the "into_table",  second list: idx of the "from table" to merge.

**Returns**

None

#### retrieve
```
retrieve(
	self,
	table,
	cols,
	col_rules,
)
```
Retrieves column values from a single table based on a given filtering rule.
example:
```python
my_db.retrieve(some_table_table,["num1","num2"],{"remainder_div_3":"{}==1 or {}==2", "sum":"{}<200"})
```
will retrieve:
columns called "num1" and "num2" from some table. That have value 1 or 2 in the ramainder_div_3 column. Column
named "sum" of which would be less than 200. All columns are combined with an "AND" statement.


**Args**
- **`table`** : string (name of the table to retrieve from)
- **`columns`** : list of strings (names of the columns to retrieve)
- **`column_rules`** : dictionary of rules that will be evaluated

**Returns**
nested list in which is entry in a list a a column with filtered requested values

## lib_multithread
### lib\_multithread.activity\_op
#### activity
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

### lib\_multithread.activity\_op.Activity\_init
#### \_\_init\_\_
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

### lib\_multithread.binidng\_affinity\_op
#### binding\_affinity
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

### lib\_multithread.binidng\_affinity\_op.Binidng\_affinity\_init
#### \_\_init\_\_
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

#### parse\_bindingdb
```
parse_bindingdb(
	self,
	binding_db_index,
)
```

#### parse\_bindingmoad
```
parse_bindingmoad(
	self,
	binding_moad_index,
)
```

#### parse\_bindingmoad\_entry
```
parse_bindingmoad_entry(
	self,
	entry,
)
```

#### parse\_pdbbind
```
parse_pdbbind(
	self,
	pdb_bind_index,
)
```

### lib\_multithread.blast\_op
#### blast
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

### lib\_multithread.blast\_op.Blast\_init
#### \_\_init\_\_
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

### lib\_multithread.dock\_op
#### dock
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

### lib\_multithread.dock\_op.Dock\_init
#### \_\_init\_\_
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

#### make\_command
```
make_command(
	self,
)
```

#### param\_load
```
param_load(
	self,
	param,
)
```

### lib\_multithread.download\_pdb\_op
#### download\_pdb
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

### lib\_multithread.download\_pdb\_op.Download\_pdb\_init
#### \_\_init\_\_
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

### lib\_multithread.generate\_conformers\_op
#### generate\_conformers
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

### lib\_multithread.generate\_conformers\_op.Generate\_conformers\_init
#### \_\_init\_\_
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

### lib\_multithread.num\_atoms\_op
#### num\_atoms
```
num_atoms(
	pdb_file,
	init=num_atoms_init,
)
```

### lib\_multithread.num\_atoms\_op.Num\_atoms\_init
#### \_\_init\_\_
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

### lib\_multithread.pdb2mol\_op
#### pdb2mol
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


### lib\_multithread.pdb2mol\_op.Pdb2mol\_init
#### \_\_init\_\_
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

### lib\_multithread.reorder\_op
#### reorder
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

### lib\_multithread.reorder\_op.Reorder\_init
#### \_\_init\_\_
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

#### make\_command
```
make_command(
	self,
)
```

#### param\_load
```
param_load(
	self,
	param,
)
```

### lib\_multithread.save\_record\_tfr\_op
#### save\_record\_tfr
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

### lib\_multithread.search\_decoys\_op
#### get\_decoys
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


#### search\_decoys
```
search_decoys(
	molfile_path,
)
```

### lib\_multithread.search\_decoys\_op.Search\_decoys\_init
#### \_\_init\_\_
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

### lib\_multithread.split\_pdb\_op
#### split\_pdb
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

### lib\_multithread.split\_pdb\_op.Split\_pdb\_init
#### \_\_init\_\_
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

### lib\_multithread.test\_multout\_op
#### test\_multout
```
test_multout(
	num,
	init=test_multout_init,
)
```

### lib\_multithread.test\_multout\_op.Test\_multout\_init
#### \_\_init\_\_
```
__init__(
	self,
)
```

### lib\_multithread.test\_sum\_op
#### test\_sum
```
test_sum(
	num1,
	num2,
	init=test_sum_init,
)
```

### lib\_multithread.test\_sum\_op.Test\_sum\_init
#### \_\_init\_\_
```
__init__(
	self,
)
```

### lib\_multithread.write\_ars2\_tfr\_op
#### save\_record\_tfr
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

#### write\_ars2\_tfr
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

### lib\_multithread.write\_ars2\_tfr\_op.WriteARS2TFRInit
#### \_\_init\_\_
```
__init__(
	self,
	num_bind_confs,
	num_decoy_confs,
	num_decoys,
)
```

## lib_singlethread
### lib\_singlethread.binding\_affinity\_op
#### binding\_affinity
```
binding_affinity(
	index_path,
	source,
)
```


**Args**
- **`index_path`** : path of the input file
- **`source`** : type of file ['pdbbind', 'bindingmoad', 'bindingdb']

**Returns**

parse result [ pdb_names, ligand_names, log_affinities, normalized_affinities, states, comments]

