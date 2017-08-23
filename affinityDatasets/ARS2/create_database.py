import sys, os, sqlite3, time
from glob import glob
from rdkit import Chem
sys.path.append('../../affinityDB')
import database
sys.path.append('../../affinityDB/dataset_libs')
import ARS2

base_dir = '/home/cosmynx/Documents/database'

cryst_lig_dir = os.path.join(base_dir, 'labeled_pdb/crystal_ligands')
cryst_lig_files = glob(os.path.join(cryst_lig_dir + '/**/', '*[_]*.pdb'))[:10]
print 'Number of ligands:', len(cryst_lig_files)
mol_files = [cryst_lig_files[i].replace('labeled_pdb/crystal_ligands', 'mol').replace('.pdb', '.mol') for i in range(len(cryst_lig_files))]
bind_lig_files = [cryst_lig_files[i].replace('labeled_pdb/crystal_ligands', 'ars2/binding_ligands') for i in range(len(cryst_lig_files))]

# Create the output file structure
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

# Initialize the database objects
db_path = os.path.join(base_dir, 'ars2.db')
if os.path.isfile(db_path):
	os.system('rm ' + db_path)
afdb = database.AffinityDB(db_path)
db_master = database.DatabaseMaster(db_path)


"""Convert the PDB files into Mol------------------------------------------------"""

start = time.time()
ARS2.ConvertPDBToMolInit()

afdb.run_multithread(func='ARS2.convert_pdb_to_mol',
	arg_types=[str, str],
	arg_lists=[cryst_lig_files, mol_files],
	out_types=[str],
	out_names=['mol_files'],
	num_threads=3, commit_sec=1)

print '\nConverted crystal PDB files to Mol in:', str(time.time()-start), 'seconds'

"""Generate ligand conformers----------------------------------------------------"""

start = time.time()
ARS2.GenerateConformersInit(num_conformers=100)

afdb.run_multithread(func='ARS2.generate_conformers',
	arg_types=[str, str],
	arg_lists=[cryst_lig_files, bind_lig_files],
	out_types=[str],
	out_names=['bind_lig_files'],
	num_threads=3, commit_sec=1)

print '\nGenerated ligand conformers in:', str(time.time()-start), 'seconds'

"""Get decoys for each of the binding ligands------------------------------------"""

start = time.time()

# TODO: Extract the filepaths to the PDB and Mol files
# TODO: get the merge action correct

# all_pdb_files = blah
# all_mol_files = blah
# all_num_atoms = blah (get this from mol files)

ARS2.GetDecoysInit(all_pdb_files, all_mol_files, all_num_atoms,
	max_atom_dif=2, max_substruct=4, max_num_decoys=10)

afdb.run_multithread(func='ARS2.get_decoys',
	arg_types=[str, str, int],
	arg_lists=[all_pdb_files, all_mol_files, all_num_atoms],
	out_types=[str, str],
	out_names=['bind_lig_files', 'decoy_files'],
	num_threads=3, commit_sec=1)

print '\nGot decoys for each ligand in:', str(time.time()-start), 'seconds\n'

"""Generate conformers for all the decoy ligands---------------------------------"""

start = time.time()

# TODO: Extract the filepaths to the decoy ligands
# Note that these decoy ligands are actually PDB files in binding_ligands folder
# decoy_ligs = blah (don't use decoy_lig_files because not in decoy_ligands folder)

# decoy_lig_files = (use the source PDB indices)
# no need to worry about determining whether or not bind ligands have enough decoys
# because it's done in the previous function

ARS2.GenerateConformersInit(num_conformers=10)

afdb.run_multithread(func='ARS2.generate_conformers',
	arg_types=[str, str],
	arg_list=[decoy_ligs, decoy_lig_files],
	out_types=[str],
	out_names=['decoy_lig_files'],
	num_threads=3, commit_sec=1)

print '\nGenerated decoy conformers in:', str(time.time()-start), 'seconds\n'

"""Save all the data in TFR format----------------------------------------------"""

start = time.time()

ARS2.WriteTFRInit(num_bind_confs=100, num_decoy_confs=10, num_decoys=10)

# TODO: Extract stuff from the database

afdb.run_multithread(func='ARS2.write_tfr',
	arg_types=[str, str, str, str, str],
	arg_lists=[rec_files, cryst_lig_files, bind_lig_files, decoy_files, out_tfr_files],
	out_types=[str],
	out_names=['out_tfr_files'],
	num_threads=3, commit_sec=1)

print '\nSaved dataset in TFR format in:', str(time.time()-start), 'seconds\n'