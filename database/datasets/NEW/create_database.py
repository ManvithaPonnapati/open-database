import sys, os, sqlite3, time
from glob import glob
from rdkit import Chem
sys.path.append('../../')
import database
from dataset_libs import NEW

base_dir = '/data/affinity/old/datasets'
db_path = os.path.join(base_dir, 'labeled_pdb.db')
out_db_path = os.path.join(base_dir, 'labeled_pdb_out.db')
# if os.path.isfile(db_path):
# 	os.system('rm ' + db_path)
if os.path.isfile(out_db_path):
	os.system('rm ' + out_db_path)
afdb = database.AffinityDB(out_db_path)
db_editor = database.DatabaseGardener(db_path)

# """Convert all the PDB files into mol files and generate ligand conformers-------"""

# start = time.time()
# ligand_files = glob(os.path.join(base_dir, 'labeled_pdb/crystal_ligands' + '/**/', '*[_]*.pdb'))[:10]
# NEW.GenerateConformersInit(base_dir=base_dir, num_conformers=10)

# afdb.run_multithread(func="NEW.generate_conformers", 
# 	arg_types=[str], 
# 	arg_lists=[ligand_files], 
# 	out_types=[str, str, int], 
# 	out_names=['pdb_file', 'mol_file', 'num_atoms'],
# 	num_threads=3, commit_sec=1)

# print '\nGenerated ligand conformers in:', str(time.time()-start), 'seconds'

# """Extract filepaths and number of atoms from database---------------------------"""

# conn = sqlite3.connect(db_path)
# cursor = conn.cursor()
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# arg_table, out_table = cursor.fetchall()
# arg_table = arg_table[0]
# out_table = out_table[0]
# conn.close()

# table_data = db_editor.retrieve(out_table, ['pdb_file','mol_file','num_atoms'], {'num_atoms': '{}<1000'})

# all_pdb_files = [table_data[0][i].encode('ascii','ignore') for i in range(len(table_data[0]))]
# all_mol_files = [table_data[1][i].encode('ascii','ignore') for i in range(len(table_data[1]))]
# all_num_atoms = table_data[2]

# """Get decoys and generate conformers in decoy_ligands folder--------------------"""

# start = time.time()
# NEW.GetDecoysInit(base_dir, all_pdb_files, all_mol_files, all_num_atoms, 
# 	max_atom_dif=100, max_substruct=100, max_num_decoys=5, num_conformers=2)

# afdb.run_multithread(func="NEW.get_decoys",
# 	arg_types=[str, str, int],
# 	arg_lists=[all_pdb_files, all_mol_files, all_num_atoms],
# 	out_types=[str, str],
# 	out_names=['crystal_files', 'decoy_files'],
# 	num_threads=3, commit_sec=1)

# print '\nGot decoys for each ligand in:', str(time.time()-start), 'seconds\n'

"""Save all the data in TFR format-----------------------------------------------"""

start = time.time()

NEW.WriteTFRInit(base_dir, num_bind_confs=100, num_decoy_confs=10)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
_, _, _, out_table = cursor.fetchall()
conn.close()

all_bind_lig_files = db_editor.retrieve(out_table[0], ['crystal_files'], {'run_idx': '{}<100000'})
all_bind_lig_files = list(set(all_bind_lig_files[0]))
all_bind_lig_files = [all_bind_lig_files[i].encode('ascii','ignore') for i in range(len(all_bind_lig_files))]

afdb.run_multithread(func='NEW.write_tfr',
	arg_types=[str],
	arg_lists=[all_bind_lig_files],
	out_types=[str],
	out_names=['tfr_files'],
	num_threads=100, commit_sec=1)

print '\nSaved dataset in TFR format in:', str(time.time()-start), 'seconds\n'