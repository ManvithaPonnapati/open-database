# AffinityDB

## Requirements

numpy==1.12.1
pandas==0.19.2
ProDy==1.8.2
scipy==0.19.0

## Edit config

- `database_root` : dir to store the generated data of AffinityDB
- `smina` : path of (smina)[https://sourceforge.net/projects/smina/] executable file
- `list_of_PDBs_to_download` : path of txt file, the PDB is is written in one line and split by ', '
- `bindb_pm` : index is the path for the binding affinity record
## Operation

### create

Create a new task. It will generate an unique sn number, create table and folder for this task.

```shell
# create a task to download pdb files
# they're stored under the folder named by
# [sn]_[folder_name] e.g. 1_download
python database_create.py --create --action=download --folder_name=download

# create a tak to calculate native contact
python database_create.py --create --action=native_contact --receptor_sn=[int] --crystal_sn=[int] --docked_sn=[int]
```

### continue

Continue a task.

```shell
# [int] is an unique sn number for a task
python database_create.py --continue --table_sn=[int]
```

### delete

Delete all the relative data for a task. Including the table and folder for this task and all the other task depend on it.

```shell
# [int] is an unique sn number for a task
python database_create.py --continue --table_sn=[int]
```

### progress

Monitor the statue of the job by idx.

```shell
# Statue of one table by table_idx
python databser_create_v2.py --progress --tabie_idx=[idx]

# Statue of all table
python database_create.py --progress --table_idx=0
```

## Args

Arguments for different kinds of task

**action** : type of task. `download, split_receptor, split_ligand, reorder, smina_dock, rmsd, overlap, native_contact`

**folder_name** : name of folder to store the generated data. ( When create the folder the sn number for the task will be the prefix ) . Required when action in `doanlowd, split_receptor, split_ligand, reorder, smina_dock`

**table_sn** : sn number for a task. Required when `continue, delete` task

**download_sn** : sn for the task which download pdb. Required when action in `split_receptor, split_ligand`

**receptor_sn** : sn for the task which generate receptor. Required when action in `smina_dock, reorder, native_contact`

**ligand_sn** : sn for the task which generate ligand. Required when action in `reorder, smina_dock`

**crystal_sn** : sn for the task which generate ligand. Required when action in `rmsd, overlap, native_contact`

**docked_sn** : sn for the task which docking ligand. Required when action in `rmsd, overlap, native_contact`

**dock_param** : parameter used for docking

**column_name**: name of column to be inserted

**column_dtype**: data type of the column to be inserted

**column_data**: name of .npy file to be loaded into column

## Example

```bash
# download pdb
python database_create.py --create --action=download --folder_name=download

# split the receptor from pdb
python database_create.py --create --action=split_receptor --folder_name=splite_receptor --download_idx=1

# split the ligand from pdb
python database_create.py --create --action=split_ligand --folder_name=splite_ligand --download_idx=1

# reorder the ligand
python database_create.py --create --action=reorder --folder_name=reorder --ligand_idx=3 --receptor_idx=2

# docking
python database_create.py --create --action=smina_dock --folder_name=vinardo --ligand_idx=4 --receptor_idx=2 --param=vinardo

# calculate rmsd
python database_create.py --create --action=rmsd --crystal_idx=4 --docked_idx=5

# calculate overlap
python database_create.py --create --action=overlap --crystal_idx=4 --docked_idx=5 --param=default

# calculate native_contact
python database_create.py --create --action=native_contact --receptor_idx=2 --crystal_idx=4 --docked_idx=5 --param=default

# load binidng affinity info
python database_create.py --create --action=binding_affinity  --param=pdbbind


```

##Inserting Column
You may insert a new column into an existing table. This will create a duplicate table with the new column added. The new table will have its own unique table ID.

```shell
#Insert column into table specified by download_idx
python database_create.py --create --action=insert_column --column_name=test_column_name --column_dtype=integer --download_idx=1 --folder_name=test_insert_column_folder
```

You may also add data into this new column. Data should be a saved Numpy array "e.g. testArray.npy" that is located in the DB directory. The Numpy array should be an array of [receptor, data_val] pairs, where "receptor" is the name of the molecule sample associate with the data_val being inserted.

After mounting the .npy file onto the DB directory, you can insert the data at the time of column creation
```shell
#Insert data at time of column creation
python database_create.py --create --action=insert_column --column_name=test_column_name --column_dtype=integer --column_data=numpyArrayName --download_idx=1 --folder_name=test_insert_column_folder
```
Or after the column has been created
```shell
#Insert data into existing column
python database_create.py --create --action=insert_column --column_name=test_column_name --column_data=numpyArrayName --download_idx=2 --folder_name=test_insert_column_folder_2
```

## Get av4

### Install requirement
Install using `pip install -r requirements.txt`

### Edit config.py
- database_root : dir to store the generated data of AffinityDB
- smina : path of (smina)[https://sourceforge.net/projects/smina/] executable file

### Run code

```bash
# download pdb
python database_create.py --create --action=download --folder_name=download

# split the receptor from pdb
python database_create.py --create --action=split_receptor --folder_name=splite_receptor --download_idx=1

# split the ligand from pdb
python database_create.py --create --action=split_ligand --folder_name=splite_ligand --download_idx=1

# parse binding affinity
python database_create.py --create --binding_affinity --param=pdbbind

```

## Access Database

You may access the Affinity Regression Set (ARS1) dataset in av4 format at the path /data/affinity/ars1_v1 on Titan.
