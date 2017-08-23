import sys, os, sqlite3, time
from compiler.ast import flatten
from glob import glob
from rdkit import Chem
from rdkit.Chem.rdchem import Mol
sys.path.append('../../affinityDB')
import database
sys.path.append('../../affinityDB/db_libs')
from convert_pdb_to_mol_op import convert_pdb_to_mol, ConvertPDBToMolInit
from generate_conformers_op import generate_conformers, GenerateConformersInit
from get_decoys_op import get_decoys, GetDecoysInit
from write_ars2_tfr_op import write_ars2_tfr, WriteARS2TFRInit

base_dir = '/home/cosmynx/Documents/database'

cryst_lig_dir = os.path.join(base_dir, 'labeled_pdb/crystal_ligands')
cryst_lig_files = glob(os.path.join(cryst_lig_dir + '/**/', '*[_]*.pdb'))[:]
print 'Number of ligands:', len(cryst_lig_files)
mol_files = [cryst_lig_files[i].replace('labeled_pdb/crystal_ligands', 'mol').replace('.pdb', '.mol') for i in range(len(cryst_lig_files))]
bind_lig_files = [cryst_lig_files[i].replace('labeled_pdb/crystal_ligands', 'ars2/binding_ligands') for i in range(len(cryst_lig_files))]

# Create the output file structure
rec_dir = os.path.join(base_dir, 'labeled_pdb/receptors')
mol_dir = os.path.join(base_dir, 'mol')
tfr_dir = os.path.join(base_dir, 'tfr')
ars2_dir = os.path.join(base_dir, 'ars2')
bind_lig_dir = os.path.join(base_dir, 'ars2/binding_ligands')
decoy_lig_dir = os.path.join(base_dir, 'ars2/decoy_ligands')
if os.path.exists(ars2_dir):
	os.system('rm -r ' + ars2_dir)
if os.path.exists(tfr_dir):
	os.system('rm -r ' + tfr_dir)
if os.path.exists(mol_dir):
	os.system('rm -r ' + mol_dir)
cryst_rec_dirs = glob(os.path.join(cryst_lig_dir, '**/'))
rec_names = [cryst_rec_dirs[i][-5:-1] for i in range(len(cryst_rec_dirs))]
for rec_name in rec_names:
	os.makedirs(os.path.join(mol_dir, rec_name))
	os.makedirs(os.path.join(bind_lig_dir, rec_name))
	os.makedirs(os.path.join(decoy_lig_dir, rec_name))
os.mkdir(tfr_dir)

# Initialize the database objects
db_path = os.path.join(base_dir, 'ars2.db')
if os.path.isfile(db_path):
	os.system('rm ' + db_path)
afdb = database.AffinityDB(db_path)
db_master = database.DatabaseMaster(db_path)


"""Convert the PDB files into Mol------------------------------------------------"""

start = time.time()
ConvertPDBToMolInit()

afdb.run_multithread(func='convert_pdb_to_mol',
	arg_types=[str, str],
	arg_lists=[cryst_lig_files, mol_files],
	out_types=[str],
	out_names=['mol_files'],
	num_threads=100, commit_sec=1)

print '\nConverted crystal PDB files to Mol in:', str(time.time()-start), 'seconds\n'

"""Generate ligand conformers----------------------------------------------------"""

start = time.time()
GenerateConformersInit(num_conformers=100)

afdb.run_multithread(func='generate_conformers',
	arg_types=[str, str],
	arg_lists=[cryst_lig_files, bind_lig_files],
	out_types=[str],
	out_names=['bind_lig_files'],
	num_threads=100, commit_sec=1)

print '\nGenerated ligand conformers in:', str(time.time()-start), 'seconds\n'

"""Get decoys for each of the binding ligands------------------------------------"""

start = time.time()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
_, arg_table_convert, out_table_convert, _, out_table_generate = cursor.fetchall()
arg_table_convert = arg_table_convert[0]
out_table_convert = out_table_convert[0]
out_table_generate = out_table_generate[0]
conn.close()

arg_data_convert = db_master.retrieve(arg_table_convert, ['run_idx'], {'run_idx': '{}<100000'})
table_data_convert = db_master.retrieve(out_table_convert, ['run_idx'], {'run_idx': '{}<100000'})
table_data_generate = db_master.retrieve(out_table_generate, ['run_idx'], {'run_idx': '{}<100000'})

# First merge the mol files into generate conformers table
_, _, pair_idx = db_master.list_search(search_with=table_data_generate[0], search_in=table_data_convert[0])
db_master.merge(into_table='out_001_generate_conformers', 
				from_table='out_000_convert_pdb_to_mol', 
				merge_cols=['mol_files'], 
				order=pair_idx)

# Then merge the crystal ligand files into generate conformers table
_, _, pair_idx = db_master.list_search(search_with=table_data_generate[0], search_in=arg_data_convert[0])
db_master.merge(into_table='out_001_generate_conformers',
				from_table='arg_000_convert_pdb_to_mol',
				merge_cols=['cryst_lig_file'],
				order=pair_idx)

# Extract filepaths to PDB and Mol files
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
_, _, _, _, out_table_generate = cursor.fetchall()
out_table_generate = out_table_generate[0]
conn.close()

table_data = db_master.retrieve(out_table_generate, ['bind_lig_files', 'mol_files'], {'run_idx': '{}<100000'})
all_pdb_files = [table_data[0][i].encode('ascii','ignore') for i in range(len(table_data[0]))]
all_mol_files = [table_data[1][i].encode('ascii','ignore') for i in range(len(table_data[0]))]
all_mols = [Chem.MolFromMolFile(all_mol_files[i]) for i in range(len(all_mol_files))]
all_num_atoms = [Mol.GetNumAtoms(all_mols[i]) for i in range(len(all_mols))]

GetDecoysInit(all_pdb_files, all_mol_files, all_mols, all_num_atoms,
	max_atom_dif=2, max_substruct=4, max_num_decoys=10)

afdb.run_multithread(func='get_decoys',
	arg_types=[str, str, int],
	arg_lists=[all_pdb_files, all_mol_files, all_num_atoms],
	out_types=[str, str],
	out_names=['bind_lig_files', 'decoy_ligs'],
	num_threads=100, commit_sec=1)

print '\nGot decoys for each ligand in:', str(time.time()-start), 'seconds\n'

"""Generate conformers for all the decoy ligands---------------------------------"""

start = time.time()

# Extract the filepaths to the decoy ligands
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
_, _, _, _, _, _, out_table_decoys = cursor.fetchall()
out_table_decoys = out_table_decoys[0]
conn.close()

table_data = db_master.retrieve(out_table_decoys, ['bind_lig_files', 'decoy_ligs'], {'run_idx': '{}<100000'})
bind_lig_files = [table_data[0][i].encode('ascii','ignore') for i in range(len(table_data[0]))]
decoy_ligs = [table_data[1][i].encode('ascii','ignore') for i in range(len(table_data[1]))]
decoy_lig_files = [bind_lig_files[i].replace('binding_ligands', 'decoy_ligands') for i in range(len(bind_lig_files))]

split_decoy_ligs = [decoy_ligs[i].split(',') for i in range(len(decoy_ligs))]
split_decoy_lig_files = [[decoy_lig_files[j].replace('.pdb', str(i)+'.pdb') for i in range(2)] for j in range(len(decoy_ligs))]

all_decoy_ligs = list(flatten(split_decoy_ligs))
all_decoy_lig_files = list(flatten(split_decoy_lig_files))

GenerateConformersInit(num_conformers=10)

afdb.run_multithread(func='generate_conformers',
	arg_types=[str, str],
	arg_lists=[all_decoy_ligs, all_decoy_lig_files],
	out_types=[str],
	out_names=['decoy_lig_files'],
	num_threads=100, commit_sec=1)

print '\nGenerated decoy conformers in:', str(time.time()-start), 'seconds\n'

# """Save all the data in TFR format----------------------------------------------"""

start = time.time()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
_, _, _, _, out_table_generate, _, out_table_decoys, _, _ = cursor.fetchall()
out_table_generate = out_table_generate[0]
out_table_decoys = out_table_decoys[0]
conn.close()

table_data_generate = db_master.retrieve(out_table_generate, ['bind_lig_files'], {'run_idx': '{}<100000'})
table_data_decoys = db_master.retrieve(out_table_decoys, ['bind_lig_files'], {'run_idx': '{}<100000'})

# Merge the crystal ligand files with bind lig files to match up decoys
_, _, pair_idx = db_master.list_search(search_with=table_data_decoys[0], search_in=table_data_generate[0])
db_master.merge(into_table='out_002_get_decoys', 
				from_table='out_001_generate_conformers', 
				merge_cols=['cryst_lig_file'], 
				order=pair_idx)

# Then retrieve them to get the crystal ligand files with bind lig files
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
_, _, _, _, _, _, out_table_decoys, _, _ = cursor.fetchall()
out_table_decoys = out_table_decoys[0]
conn.close()

# Generate the filepaths to the decoy ligands, receptors, and out tfr paths
table_data = db_master.retrieve(out_table_decoys, ['bind_lig_files', 'cryst_lig_file'], {'run_idx': '{}<100000'})
bind_lig_files = [table_data[0][i].encode('ascii','ignore') for i in range(len(table_data[0]))]
cryst_lig_files = [table_data[1][i].encode('ascii','ignore') for i in range(len(table_data[1]))]
decoy_lig_files = [','.join(split_decoy_lig_files[i]) for i in range(len(split_decoy_lig_files))]

cryst_lig_names = [cryst_lig_files[i][len(cryst_lig_dir)+6:] for i in range(len(cryst_lig_files))]
rec_names = [cryst_lig_files[i][len(cryst_lig_dir)+1:len(cryst_lig_dir)+5] for i in range(len(cryst_lig_files))]
out_tfr_files = [(os.path.join(tfr_dir, cryst_lig_names[i])).replace('.pdb', '.tfr') for i in range(len(cryst_lig_names))]
rec_files = [(os.path.join(rec_dir, rec_names[i]+'.pdb')) for i in range(len(rec_names))]

WriteARS2TFRInit(num_bind_confs=100, num_decoy_confs=10, num_decoys=10)

afdb.run_multithread(func='write_ars2_tfr',
	arg_types=[str, str, str, str, str],
	arg_lists=[rec_files, cryst_lig_files, bind_lig_files, decoy_lig_files, out_tfr_files],
	out_types=[str],
	out_names=['out_tfr_files'],
	num_threads=100, commit_sec=1)

print '\nSaved dataset in TFR format in:', str(time.time()-start), 'seconds\n'