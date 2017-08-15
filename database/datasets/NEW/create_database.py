import sys, os, sqlite3
from glob import glob
sys.path.append('../../')
import database
import dataset_libs

flags = dataset_libs.NEW.FLAGS()
afdb = database.AffinityDB(flags.db_path)
db_retriever = database.DatabaseGardener(flags.db_path)

afdb.run_multithread(func="dataset_libs.NEW.convert_pdb_to_mol", 
	arg_types=[str], 
	arg_lists=[flags.ligand_files], 
	out_types=[str, str, int], 
	out_names=['pdb_file', 'mol_file', 'num_atoms'],
	num_threads=10, commit_sec=1)

print '\nFinished converting pdb to mol\n'

"""Do the following database actions:
	> extract pdb_file, mol_file, num_atoms from database
	> save all_mol_file and all_num_atoms to FLAGS for direct usage
	> DON'T FORGET to actually convert mol files to mols
	> Then, run a multithreaded get_ligand_decoys"""

conn = sqlite3.connect(flags.db_path)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
arg_table, out_table = cursor.fetchall()
arg_table = arg_table[0]
out_table = out_table[0]
# conn.close()
print db_retriever.retrieve(out_table, ['pdb_file','mol_file','num_atoms'], {'num_atoms':'{}<50'})

# flags.all_pdb_files = []
# flags.all_mol_files = []
# flags.all_mols = []
# flags.all_num_atoms = []


# afdb.run_multithread(func="dataset_libs.NEW.get_ligand_decoys",
# 	arg_types=[str, str, int],
# 	arg_lists=[flags.all_pdb_files, flags.all_mol_files, flags.all_num_atoms],
# 	out_types=[int],
# 	out_names=['num_decoys'],
# 	num_threads=10, commit_sec=1)

# print '\nFinished copying decoys to decoy_ligands folder\n'