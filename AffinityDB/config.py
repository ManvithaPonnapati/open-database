import os123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom collections import namedtuple123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport multiprocessing123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFvariable shared between file123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFmanager = multiprocessing.Manager()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFlock = manager.Lock()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFParameter123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdb_name='affinity.db'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# only ligands' atom number above threshold will saved123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFheavy_atom_threshold = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# number of process running at the same time123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFprocess_num = 2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# RENAMES:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [ ] tanimoto_cutoff    # minimum Tanimoto similarity score to be considered 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [ ] clash_size_cutoff  # ls # no cutoff here!123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] base               # database_root123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] lig_download_path  # why ?123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] downloads          # raw_pdbs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] receptors          # raw_receptors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] raw_ligands123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [-] docked_ligand_path # SMINA_DOCKED ?? 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] docking parameters123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] target_list_file     list_of_PDBs_to_download123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] lig_target_list_file (Not needed)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] add folder for repaired ligands and proteins (with H)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [ ] add folder for minimized hydrogens on ligands and proteins (How does the hydrogen addition happen)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] think how we can deal with multiple docking parameters123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# _________________________ Review 2 _________________________________________________123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# Bugs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 0) Tanimoto similarity cutoff does not work123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 1) Fraction of native contacts does not work123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 2) similarity cutoff, fraction of native contacts, clash -- all should have a similar simple format123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 3) reorder should become a part of every docking algorithm123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 4) get_same_ligands becomes standalone123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 5) ligand_name_of becomes _ligand_name_of same for receptor_of, receptor_path_of, mkdir, run ---> run_multiptocessor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 6) calculate_clash becomes a part of detect_overlap123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 7) dock merges with VInardo_do_docking123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 8) Empty files + broken file check (have a log file to do the stop so as to be able to resume from any point )123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# broken file is unless "success is written in log"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# Enhancements123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 0) Dependencies into README.md123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 1) rename into 1_download, 2_split, 3_docking123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 2) split_structure needs medhod (IE: NMR,X-RAY)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 3) More splitting statistics123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# let's also write a number of receptor atoms when splitting123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# and the number of receptor chains when splitting123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# number of receptor residues when splitting123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 4) write a script that will gether all of the logs together and create many plots about the data in python notebook123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# Statistics about the PDB in README.md with all of the plots123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# def crystal_ligand_for_same_receptor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 5) Write the script that will do a retrieval based on 4 and write the structures in av4 format123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 6) How do we do this on Orchestra or Bridges -- how do we launch many separate jobs ?123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFoverlap detaction constant123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtanimoto_cutoff = 0.75  # an exact Tanimoto similarity score should be recorded in the file123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclash_cutoff_A = 4      # 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclash_size_cutoff = 0.3 # __ an exact value should be recorded123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFolders123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# the path for this script config.py123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFscript_path = sys.path[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#base folder for all the output123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdatabase_root = '/home/maksym/PyCharmProjects/tensorMe21_Database/AffinityDB/test'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdb_path =os.path.join(database_root, db_name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# pdb download from Protein DataBank123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFpdb_download_path = os.path.join(database_root,'data','row_pdb')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# splited receptor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsplited_receptors_path = os.path.join(database_root,'data','row_receptors')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# splited ligands123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsplited_ligands_path = os.path.join(database_root,'data','row_ligands')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# log files123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFlog_folder = os.path.join(database_root,'log')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# docked ligands123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdocked_ligand_path = os.path.join(database_root,'data','docked')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# ligands docked by smina , scoring function: default123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsmina_docked_path = os.path.join(database_root, 'data','smina')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# ligands docked by smina , scoring function: vinardo                       # will c123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFvinardo_docked_path = os.path.join(database_root, 'data','vinardo')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# ligans output by smina, keep the same atom order as docked result123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsmina_std_path = os.path.join(database_root, 'data', 'smina_std_ligands')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFile Path 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# path of smina binary file123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsmina = '/usr/local/bin/smina'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# pdb_target_list123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#target_list_file = os.path.join(sys.path[0],'target_list','main_pdb_target_list.txt')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFlist_of_PDBs_to_download = '/home/xander/affinityDB/target_list/main_pdb_target_list.txt'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# example scoring123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFscoring_terms = os.path.join(sys.path[0], 'scoring', 'smina.score')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdocking para123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFvinardo_pm = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'arg': [],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'kwarg' : {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'autobox_add':12,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'num_modes':400,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'exhaustiveness':64,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'scoring':'vinardo',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'cpu':1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsmina_pm = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'arg':[],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'kwarg':{123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'num_modes':400,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'cpu':1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF