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
pdb_list = pdb_list[:20]

# download 20 pdbs
Download_pdb_init(db_root=db_root,
                  download_dir="download_pdbs1")
afdb.run_multithread("download_pdb",arg_lists=[pdb_list])


# split 20 PDBs
disk_pdbs = database_master.retrieve("out_000_download_pdb",["pdb_file"],{})
disk_pdbs = [disk_pdb[0] for disk_pdb in disk_pdbs]
Split_pdb_init(db_root=db_root, split_dir="split_pdbs1")
afdb.run_multithread("split_pdb",arg_lists=[disk_pdbs])


# generate confomers for 20 ligands
disk_ligs = database_master.retrieve("out_001_split_pdb",["lig_file"],{})
disk_ligs = ["/home/maksym/Desktop/vds1/" + disk_lig[0] for disk_lig in disk_ligs]

Generate_conformers_init(db_root="/home/maksym/Desktop/vds1",
                         conformers_dir="gen_conformers",
                         num_conformers=10,
                         out_H=False)

afdb.run_multithread("generate_conformers", arg_lists=[disk_ligs])

# convert all 20 ligands to mol files
Pdb2mol_init(db_root=db_root,molfile_dir="lig_molf")
afdb.run_multithread("pdb2mol", arg_lists=[disk_ligs])



# #def __init__(self,db_root,decoy_molfiles,num_decoys,atom_diff,max_substruct):
#
# Search_decoys_init(db_root=db_root,
#                    decoy_molfiles=disk_molfiles,
#                    num_decoys=10,
#                    atom_diff=3,
#                    max_substruct=5)
#
