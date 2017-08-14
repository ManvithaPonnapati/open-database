import sys, os
from glob import glob
sys.path.append('../../')
import database
import dataset_libs

flags = dataset_libs.NEW.FLAGS()
afdb = database.AffinityDB(flags.db_path)

afdb.run_multithread(func="dataset_libs.NEW.convert_pdb_to_mol", 
	arg_types=[str], 
	arg_lists=[flags.ligand_files], 
	out_types=[str, str, int], 
	out_names=['pdb_file', 'mol_file', 'num_atoms'],
	num_threads=1)

print '\nFinished converting pdb to mol\n'

"""Do the following database actions:
	> extract pdb_file, mol_file, num_atoms from database
	> save all_mol_file and all_num_atoms to FLAGS for direct usage
	> DON'T FORGET to actually convert mol files to mols
	> Then, run a multithreaded get_ligand_decoys"""

# flags.all_pdb_files = []
# flags.all_mol_files = []
# flags.all_mols = []
# flags.all_num_atoms = []


# afdb.run_multithread(func="dataset_libs.NEW.get_ligand_decoys",
# 	arg_types=[str, str, int],
# 	arg_lists=[flags.all_pdb_files, flags.all_mol_files, flags.all_num_atoms],
# 	# arg_lists=[[],[],[]],
# 	out_types=[int],
# 	out_names=['num_decoys'],
# 	num_threads=10, commit_freq=500)

# print '\nFinished copying decoys to decoy_ligands folder\n'