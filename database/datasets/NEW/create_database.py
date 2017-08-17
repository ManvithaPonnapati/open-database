import sys, os, sqlite3, time
from glob import glob
from rdkit import Chem
sys.path.append('../../')
import database
from dataset_libs import NEW

base_dir = '/data/affinity/old/datasets'
db_path = os.path.join(base_dir, 'labeled_pdb.db')
if os.path.isfile(db_path):
	os.system('rm ' + db_path)
afdb = database.AffinityDB(db_path)
db_editor = database.DatabaseGardener(db_path)

"""Convert all the PDB files into mol files and generate ligand conformers-------"""

start = time.time()
ligand_files = glob(os.path.join(base_dir, 'labeled_pdb/crystal_ligands' + '/**/', '*[_]*.pdb'))
NEW.GenerateConformersInit(base_dir=base_dir, num_conformers=100)

afdb.run_multithread(func="NEW.generate_conformers", 
	arg_types=[str], 
	arg_lists=[ligand_files], 
	out_types=[str, str, int], 
	out_names=['pdb_file', 'mol_file', 'num_atoms'],
	num_threads=100, commit_sec=1)

print '\nGenerated ligand conformers in:', str(time.time()-start), 'seconds'

"""Extract filepaths and number of atoms from database---------------------------"""

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
arg_table, out_table = cursor.fetchall()
arg_table = arg_table[0]
out_table = out_table[0]
conn.close()

table_data = db_editor.retrieve(out_table, ['pdb_file','mol_file','num_atoms'], {'num_atoms': '{}<1000'})

all_pdb_files = [table_data[0][i].encode('ascii','ignore') for i in range(len(table_data[0]))]
all_mol_files = [table_data[1][i].encode('ascii','ignore') for i in range(len(table_data[1]))]
all_num_atoms = table_data[2]

"""Get decoys and generate conformers in decoy_ligands folder--------------------"""

start = time.time()
NEW.GetDecoysInit(base_dir, all_pdb_files, all_mol_files, all_num_atoms, 
	max_atom_dif=2, max_substruct=4, max_num_decoys=10, num_conformers=10)

afdb.run_multithread(func="NEW.get_decoys",
	arg_types=[str, str, int],
	arg_lists=[all_pdb_files, all_mol_files, all_num_atoms],
	out_types=[str, str],
	out_names=['crystal_files', 'decoy_files'],
	num_threads=100, commit_sec=1)

print '\nGot decoys for each ligand in:', str(time.time()-start), 'seconds\n'