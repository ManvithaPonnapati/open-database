# api_docs



[TOC]

***
## database
### database.AffinityDB
#### \_\_init\_\_

#### coninue
Continue the interrupted run_multithread function.

**args**
:param arg_table: string (name of the sqlite table with arguments of the function to run)
:param num_threads: integer (number of processes)
:param commit_sec: integer (write outputs to the database every number of tasks)

**returns**
:return: None

#### open\_table\_with\_queue
Creates an output table, and a queue to feed this table. Creates a background thread to take results
from the queue and insert into the table.


**args**
:param table_name: string (name of the table prefix out_xxx_ will be appended)
:param col_names: list of strings (names of the columns)
:param col_types: list of python types (column types)

**returns**
:return: multiprocessing queue, event to close the table and terminate thread.

Exaple usage:
out_q,stop_event = afdb.open_table_with_queue(table_name="some_table",col_names=["num"],col_types=[int])
for i in range(1000):
    out_q.put([i])
stop_event.set()

#### run\_multithread
Run any function in lib_multithread in multiple threads.
Writes all arguments to arg_xxx_func table, record outputs to out_xxx_table. Record state of the function's
initializer to cron table.

If the task is interrupted in the process of execution, it is possible to resume with AffinityDB.continue(*)


**args**
:param func: string (a name of the function to execute)
:param arg_sets: lits of tuples (every tuple is an argument set for a single run of a function)
:param num_threads: integer (number of independent processes)
:param commit_sec: integer (time delay in flushing outputs to the arg_ and out_ tables)

**returns**
:return: None

### database.DatabaseMaster
#### \_\_init\_\_

#### list\_search
Search with each element of the "search_with" in the list "search_in".


**args**
:param search_with: list of [str/float/int]
:param search_in: list of [str/float/int]

**returns**
:return:
hits_idx:
A list of length len(search_with) of lists. Internal list is indexes [j1,j2,j3,j4] such that values
search_with[i] == search_in[j1], search_with[i] == search_in[j2], ...
hits_val:
Same as hits_idx but lists with values instead of indexes
pairs_idx:
Two lists of the same length. search_with[pairs_idx[0][i]] == search_in[pairs_idx[1][i]]

#### merge
Merges any table into the output table

**args**
:param into_table: string (table to merge into)
:param from_table: string (table to merge from)
:param merge_cols: list of strings (names of the columns in merge_from to merge)
:param order: Two lists of the same length. into_table_idx <-- from_table_idx

**returns**
First list: idx of the "into_table",  second list: idx of the "from table" to merge.

Suggestion:
When providing order, please, use run_idx for the argument table, and out_idx for the output table.
Also, it the arg_table it is a good idea to select run_idx ==1

:return: None

#### retrieve
Retrieves column values from a single table based on a given filtering rule.
example:
my_db.retrieve(some_table_table,["num1","num2"],{"remainder_div_3":"{}==1 or {}==2", "sum":"{}<200"})
will retrieve:
columns called "num1" and "num2" from some table. That have value 1 or 2 in the ramainder_div_3 column. Column
named "sum" of which would be less than 200. All columns are combined with an "AND" statement.

**args**
:param table: string (name of the table to retrieve from)
:param columns: list of strings (names of the columns to retrieve)
:param column_rules: dictionary of rules that will be evaluated

**returns**
:return: nested list in which is entry in a list a a column with filtered requested values

## lib_multithread
### lib\_multithread.activity\_op
#### activity
Getting bioactivity result from local chembl database
query by the target_chembl_id



**args**
:param pair_name: str:: combined receptor id and ligand info {receptor_id}_{chain}_{resnum}_{resname}
:param target_id: str:: chembl_target_id
:param init: str:: init function name

**returns**
:return: nested list:: [pair_name, aid, tid, mid, confidence_score, type, relation, value, unit, smile]

### lib\_multithread.activity\_op.Activity\_init
#### \_\_init\_\_


**args**
:param data_dir: str:: dir for the folder to save data
:param db_path: str:: path for the chembl database

**returns**


### lib\_multithread.binidng\_affinity\_op
#### binding\_affinity
Parse binding affinity record from index_path


**args**
:param index_path: record file 
:param init:

**returns**


### lib\_multithread.binidng\_affinity\_op.Binidng\_affinity\_init
#### \_\_init\_\_


**args**
:param db_root: string (path to the root folder of the database)
:param parse_type: source of binding affinity record ['pdbbind','bindingmoad','bindingdb']

**returns**


#### parse\_bindingdb

#### parse\_bindingmoad

#### parse\_bindingmoad\_entry

#### parse\_pdbbind

### lib\_multithread.blast\_op
#### blast
Applying protein sequence blast on the receptor


**args**
:param rec_outpath: str:: relative path of receptor
:param lig_outpath: str:: relative path of ligand
:param init: str:: init func name

**returns**
:return: nested list:: blast result contain  pair_name with receptor id and ligand name, 
chembl_target_id for similar sequence in database,  ideitity number as num_match/align_length and
the sequence of selected receptor

### lib\_multithread.blast\_op.Blast\_init
#### \_\_init\_\_


**args**
:param data_dir: str:: dir for the data
:param blast_db: str:: path of the blast database

**returns**


### lib\_multithread.dock\_op
#### dock
Docking the ligand by smina


**args**
:param rec_outpath: str:: relative path for receptor
:param reorder_outpath: str:: relative path for reorder ligand
:param init: str:: init func naem

**returns**
:return: nested list:: docking result contains the relative path for receptor, reorder ligand and docked ligand

### lib\_multithread.dock\_op.Dock\_init
#### \_\_init\_\_


**args**
:param data_dir: str:: dir for the folder to save data
:param dock_folder: str:: name of the folder to save reorder output
:param smina_path: str:: path for teh executable smina program
:param dock_param: dict::   docking parameter {'args':[...], 'kwargs':{...}}

**returns**


#### make\_command

#### param\_load

### lib\_multithread.download\_pdb\_op
#### download\_pdb
Download PDB crystal structure from the Protein Data Bank.


**args**
:param pdb_id: string (4-letter PDB ID IE: 1QGT)
:param dir_path: string (folder in which to save the pdb file)

**returns**
:return: nested list (of dimensions 1x[string] where string is the relative path to the output file)

### lib\_multithread.download\_pdb\_op.Download\_pdb\_init
#### \_\_init\_\_


**args**
:param db_root: string (root folder directory for the files in the database)
:param download_dir: string (name of the directory where to put downloaded PDBs)

**returns**


### lib\_multithread.generate\_conformers\_op
#### generate\_conformers
Forgets the initial coordinates of the molecule. Looses all hydrogens. Adds all hydrogens.
Generates random conformers. Optimizes conformers with MMFF94 Force Field.
Saves multiframe PDB file of the ligand with new coordinates.

**args**
:param lig_file: string (path to the ligand file in the PDB format to read)
:param init: string (init function)

**returns**
:return: nested list of dimension [1x[string]]. String is the relative path to the output file.

### lib\_multithread.generate\_conformers\_op.Generate\_conformers\_init
#### \_\_init\_\_


**args**
:param db_root: string (database root)
:param conformers_dir: string (name of the directory where to put generated conformers)
:param num_conformers: int (number of the conformers to output)
:param out_H: bool T/F (Add hydrogen atoms to the output. All input hydorogen atoms are always lost.)

**returns**


### lib\_multithread.num\_atoms\_op
#### num\_atoms

### lib\_multithread.num\_atoms\_op.Num\_atoms\_init
#### \_\_init\_\_


**args**
:param db_root: string (path to the root of the database)

**returns**


### lib\_multithread.pdb2mol\_op
#### pdb2mol
Convert .pdb file to .mol file

**args**
:param lig_file: string (relative path to the ligand file)
:param init: string (init function)

**returns**
:return:

### lib\_multithread.pdb2mol\_op.Pdb2mol\_init
#### \_\_init\_\_


**args**
:param db_root: string (database root)
:param molfile_dir: string (relative path where to create the output directory with .mol files)

**returns**


### lib\_multithread.reorder\_op
#### reorder
Parse the ligand by smina, and then output it. So the order of the atom keeps the same as the docking result


**args**
:param rec_outpath: str:: relative path for receptor
:param lig_outpath: str:: relative path for ligand
:param init: str:: initialize module 

**returns**
:return: nested list:: reorder result contains the relative path for receptor and relative path for reorder ligand

### lib\_multithread.reorder\_op.Reorder\_init
#### \_\_init\_\_


**args**
:param data_dir: str:: dir for the folder to save data
:param reorder_folder: str:: name of the folder to save reorder output
:param smina_path: str:: path for teh executable smina program
:param dock_param: dict:: docking parameter {'args':[...], 'kwargs':{...}}

**returns**


#### make\_command

#### param\_load

### lib\_multithread.save\_record\_tfr\_op
#### save\_record\_tfr
Params:
    filename: string (file path to the output file)
    pos_per_binder:  integer (number of positions per binder)
    cryst_elem: np.array shape=[n_elem] type=float32 (elements of the ligand)
    cryst_coord: np.array shape=[n_elem, 3] type=float32 (coordinates of the elements of the ligand)
    binders_elem: list of np.array of shape=[n_elem] type=float32 (elements of binders)
    binders_coordsets: list of np.array [pos_per_binder, n_elem, 3 ] (coordinate sets per each of the bidners)
    cryst_label: float32 (something about the crystal pose, like binding affinity)
    binders_labels: list of np.array shape=[pos_per_binder] type=float32
    rec_elem: np.array of shape [n_elem] of float32
    rec_coord: np.array of shape [n_elem, 3]
Returns: None

**args**


**returns**


### lib\_multithread.search\_decoys\_op
#### get\_decoys
For each binding ligand, get a list of decoy ligands. We filter by number of atoms and maximum common
substructure (MCS). Returns filepaths to all binding ligand - decoy pair.


**args**
:param pdb_file:
:param mol_file:
:param num_atoms:
:param init:

**returns**
:return:

#### search\_decoys

### lib\_multithread.search\_decoys\_op.Search\_decoys\_init
#### \_\_init\_\_


**args**
:param db_root:
:param decoy_ids:
:param decoy_natoms:
:param decoy_molfiles:
:param max_decoys:
:param atom_diff:
:param max_substruct:

**returns**


### lib\_multithread.split\_pdb\_op
#### split\_pdb
Iterates through every ligand molecule in the crystal structure (frequently there are a few). For each ligand
selects and crops its binding site (any atom of Protein/DNA/Cofactor within the cutoff distance). Saves pairs of
files: ligand + this ligand's binding site.


**args**
:param pdb_file: string (relative path the the file to split)
:param cutoff_dist: float (distance of any atoms in the binding site from any atom of the ligand to be saved)
:param min_rec_atoms: minimun number of atoms be saved as binding site
:param min_lig_atoms: minumum number of atoms for ligand to be saved
:param init: string (init function in this module)

**returns**
:return: nested list of pairs of file names of dimensions [num_pairs x [string,string,int,int]] or
[num_pairs x [lig_file,bindsite_file,lig_num_atoms,bindsite_num_atoms]]

### lib\_multithread.split\_pdb\_op.Split\_pdb\_init
#### \_\_init\_\_


**args**
:param db_root: string (path to the root folder of the database)
:param split_dir: string (where to put split pdbs)
:param discard_h: Bool T/F (discard all hydrogens for both ligand and receptor defaults to True)

**returns**


### lib\_multithread.test\_multout\_op
#### test\_multout

### lib\_multithread.test\_multout\_op.Test\_multout\_init
#### \_\_init\_\_

### lib\_multithread.test\_sum\_op
#### test\_sum

### lib\_multithread.test\_sum\_op.Test\_sum\_init
#### \_\_init\_\_

### lib\_multithread.write\_ars2\_tfr\_op
#### save\_record\_tfr
Params:
    filename: string (file path to the output file)
    pos_per_binder:  integer (number of positions per binder)
    cryst_elem: np.array shape=[n_elem] type=float32 (elements of the ligand)
    cryst_coord: np.array shape=[n_elem, 3] type=float32 (coordinates of the elements of the ligand)
    binders_elem: list of np.array of shape=[n_elem] type=float32 (elements of binders)
    binders_coordsets: list of np.array [pos_per_binder, n_elem, 3 ] (coordinate sets per each of the bidners)
    cryst_label: float32 (something about the crystal pose, like binding affinity)
    binders_labels: list of np.array shape=[pos_per_binder] type=float32
    rec_elem: np.array of shape [n_elem] of float32
    rec_coord: np.array of shape [n_elem, 3]
Returns: None

**args**


**returns**


#### write\_ars2\_tfr
For each protein/ligand crystal pair, write one tfrecord with the following:
> rec_elem, rec_coord, cryst_elem, cryst_coord
> lig_nelems, lig_elem, lig_nframes, lig_coordsets, lig_labels
> Params:
    rec_file: filepath to receptor PDB
    cryst_lig_file: filepath to crystal ligand PDB
    bind_lig_file: filepath to conformers of crystal ligand PDB
    decoy_files: comma separated filepath to decoy ligands PDB
    out_tfr_file: filepath to write tf record to


**args**


**returns**


### lib\_multithread.write\_ars2\_tfr\_op.WriteARS2TFRInit
#### \_\_init\_\_

## lib_singlethread
### lib\_singlethread.binding\_affinity\_op
#### binding\_affinity


**args**
:param index_path:
:param source:

**returns**
:return:

#### read\_PDB\_bind


**args**
:param pdb_bind_index:

**returns**
:return:

#### read\_binding\_db


**args**
:param binding_db_index:

**returns**
:return:

#### read\_binding\_moad


**args**
:param binding_moad_index:

**returns**
:return:

