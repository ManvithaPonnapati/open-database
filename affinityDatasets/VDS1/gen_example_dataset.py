import os,sys,time
import numpy as np
sys.path.append('../../affinityDB')
sys.path.append('../../affinityDB/lib_multithread')
import database,sqlite3
#import VDS1
from download_pdb_op import Download_pdb_init,download_pdb
from split_pdb_op import Split_pdb_init,split_pdb
from generate_conformers_op import Generate_conformers_init,generate_conformers
from pdb2mol_op import Pdb2mol_init,pdb2mol
from search_decoys_op import Search_decoys_init,search_decoys


db_root = "/home/maksym/Desktop/vds1/"
#os.remove(db_path)
afdb = database.AffinityDB(db_root,"test")
database_master = database.DatabaseMaster(os.path.join(db_root,"test.db"))

with open("./data/main_pdb_target_list.txt") as f: raw_pdb_list = f.readlines()
pdb_list = raw_pdb_list[0].split(", ")
print "number of pdbs to download:", len(pdb_list), "will download only 20"

pdb_id_set = [(pdb_name,) for pdb_name in pdb_list[:20]]


# download 20 pdbs
Download_pdb_init(db_root=db_root,
                  download_dir="download_pdbs1")
afdb.run_multithread("download_pdb",arg_sets=pdb_id_set)


# # split 20 PDBs
disk_pdbs = database_master.retrieve("out_000_download_pdb",["pdb_file"],{})
Split_pdb_init(db_root=db_root, split_dir="split_pdbs1")
afdb.run_multithread("split_pdb",arg_sets=disk_pdbs)


# convert all 20 ligands to mol files
disk_ligs = database_master.retrieve("out_001_split_pdb",["lig_file"],{})
Pdb2mol_init(db_root=db_root,molfile_dir="lig_molf")
afdb.run_multithread("pdb2mol", arg_sets=disk_ligs)

# # find decoys
disk_molfiles = database_master.retrieve("out_002_pdb2mol",["mol_file"],{})
disk_molfiles = [disk_molfile[0] for disk_molfile in disk_molfiles]

#
# mol_pairs = [molfile.split("/")[-1].split("_ligand.mol")[0] for molfile in disk_molfiles]
# pdb_pairs = [pdbfile.split("/")[-1].split("_ligand.pdb")[0] for pdbfile in disk_ligs]
# _,_,order = database_master.list_search(pdb_pairs,mol_pairs)
#
# database_master.merge(into_table="out_002_pdb2mol",
#                       from_table="out_001_split_pdb",
#                       merge_cols=["lig_num_atoms","lig_file"],
#                       order=order)
#
# mol_pairs = database_master.retrieve("out_002_pdb2mol",["mol_file","lig_num_atoms"],{})
# print mol_pairs
#
# Search_decoys_init(db_root=db_root,
#                    decoy_molfiles=disk_molfiles,
#                    num_decoys=10,
#                    atom_diff=3,
#                    max_substruct=5)



# Generate_conformers_init(db_root="/home/maksym/Desktop/vds1",
#                          conformers_dir="gen_conformers",
#                          num_conformers=10,
#                          out_H=False)
#
# afdb.run_multithread("generate_conformers", arg_lists=[disk_ligs])
#