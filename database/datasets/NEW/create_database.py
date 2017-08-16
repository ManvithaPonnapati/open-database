import sys, os, sqlite3, time
from glob import glob
from rdkit import Chem
sys.path.append('../../')
import database
from dataset_libs import NEW

"""Convert all the PDB files into mol files--------------------------------------"""

flags = NEW.FLAGS()
flags.get_crystal_ligand_conformers_init(base_dir='/data/affinity/old/datasets',
										 max_atom_dif=2, 
										 max_substruct=4,
										 max_num_decoys=10,
										 decoy_conformers=10,
										 binding_conformers=100)
afdb = database.AffinityDB(flags.db_path)
db_editor = database.DatabaseGardener(flags.db_path)
start = time.time()

afdb.run_multithread(func="NEW.get_crystal_ligand_conformers", 
	arg_types=[str], 
	arg_lists=[flags.ligand_files], 
	out_types=[str, str, int], 
	out_names=['pdb_file', 'mol_file', 'num_atoms'],
	num_threads=200, commit_sec=1)

print '\nConverted PDB to MOL in:', str(time.time()-start), 'seconds'
start = time.time()

"""Extract filepaths and number of atoms from database---------------------------"""

conn = sqlite3.connect(flags.db_path)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
arg_table, out_table = cursor.fetchall()
arg_table = arg_table[0]
out_table = out_table[0]
conn.close()

table_data = db_editor.retrieve(out_table, ['pdb_file','mol_file','num_atoms'], {'num_atoms': '{}<1000'})

print '\nRetrieved data from database in:', str(time.time()-start), 'seconds'
start = time.time()

"""Compute and copy decoys into decoy_ligands folder-----------------------------"""

flags.get_ligand_decoys_init(all_pdb_files=[table_data[0][i].encode('ascii','ignore') for i in range(len(table_data[0]))],
	all_mol_files=[table_data[1][i].encode('ascii','ignore') for i in range(len(table_data[1]))],
	all_num_atoms=table_data[2])

afdb.run_multithread(func="NEW.get_ligand_decoys",
	arg_types=[str, str, int],
	arg_lists=[flags.all_pdb_files, flags.all_mol_files, flags.all_num_atoms],
	out_types=[str, str],
	out_names=['crystal_files', 'decoy_files'],
	num_threads=200, commit_sec=1)

print '\nDetermined the decoys for each ligand in:', str(time.time()-start), 'seconds\n'
start = time.time()