import os123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom collections import namedtuple123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport multiprocessing123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFvariable shared between file123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFmanager = multiprocessing.Manager()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFlock = manager.Lock()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFParameter123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdb_name='affinity.db'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# number of process running at the same time123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFprocess_num = 8123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# RENAMES:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [ ] tanimoto_cutoff    # minimum Tanimoto similarity score to be considered 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [ ] clash_size_cutoff  # ls # no cutoff here!123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] base               # database_root123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] lig_download_path  # why ?123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] downloads          # raw_pdbs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] receptors          # raw_receptors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] raw_ligands123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] docked_ligand_path # SMINA_DOCKED ?? 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] docking parameters123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] target_list_file     list_of_PDBs_to_download123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] lig_target_list_file (Not needed)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] add folder for repaired ligands and proteins (with H)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] add folder for minimized hydrogens on ligands and proteins (How does the hydrogen addition happen)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] think how we can deal with multiple docking parameters123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# _________________________ Review 2 _________________________________________________123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# Bugs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [ ] 0) Tanimoto similarity cutoff does not work123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] 1) Fraction of native contacts does not work123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [ ] 2) similarity cutoff, fraction of native contacts, clash -- all should have a similar simple format123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] 3) reorder should become a part of every docking algorithm123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] 4) get_same_ligands becomes standalone123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] 5) ligand_name_of becomes _ligand_name_of same for receptor_of, receptor_path_of, mkdir, run ---> run_multiptocessor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [-] 6) calculate_clash becomes a part of detect_overlap123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] 7) dock merges with VInardo_do_docking123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] 8) Empty files + broken file check (have a log file to do the stop so as to be able to resume from any point )123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] broken file is unless "success is written in log"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# Enhancements123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [ ] 0) Dependencies into README.md123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] 1) rename into 1_download, 2_split, 3_docking123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] 2) split_structure needs medhod (IE: NMR,X-RAY)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 3) More splitting statistics123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] let's also write a number of receptor atoms when splitting123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] and the number of receptor chains when splitting123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# [x] number of receptor residues when splitting123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 4) write a script that will aether all of the logs together and create many plots about the data in python notebook123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# Statistics about the PDB in README.md with all of the plots123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# def crystal_ligand_for_same_receptor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 5) Write the script that will do a retrieval based on 4 and write the structures in av4 format123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 6) How do we do this on Orchestra or Bridges -- how do we launch many separate jobs ?123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# __________________________________ Review 3 ___________________________________________________123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# todo(maksym) - split we should be able to allow peptides as well123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# todo(maksym) - test how many ligands in the initial123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# raviables to rename/describe123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# tanimoto_cutoff = 0.75123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# clash_cutoff_A = 4123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# clash_size_cutoff = 0.3123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# reorder_pm123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# remove duplicate default parameters123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# datum = [table_name, table_type, table_sn, create_time, encoded_param]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# data = [datum]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFoverlap detaction constant123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtanimoto_cutoff = 0.75  # an exact Tanimoto similarity score should be recorded in the file123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclash_cutoff_A = 4      # 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclash_size_cutoff = 0.3 # __ an exact value should be recorded123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFolders123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# the path for this script config.py123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFscript_path = sys.path[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#base folder for all the output123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#database_root = os.path.join(script_path, '..', 'AffinityDB')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF<<<<<<< HEAD123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdatabase_root = '/home/xander/affinityDB/aff_test'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF=======123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdatabase_root = '/home/maksym/PyCharmProjects/datasets/affinity_DB_v2'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF>>>>>>> b6605cfc14ff3e8a471015122c700962e3ecb04d123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdb_path =os.path.join(database_root, db_name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdata_dir = os.path.join(database_root,'data')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# log files123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#log_dir = os.path.join(database_root, 'log')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# csv files123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#table_dir = os.path.join(database_root, 'table')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFile Path 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# path of smina binary file123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#smina = 'smina.static'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsmina = '/usr/local/bin/smina'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# pdb_target_list123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#list_of_PDBs_to_download = os.path.join(sys.path[0],'target_list','main_pdb_target_list.txt')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFlist_of_PDBs_to_download = '/home/xander/affinityDB/aff_test/affinity_test.txt'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# example scoring123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFscoring_terms = os.path.join(sys.path[0], 'scoring', 'smina.score')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdocking para123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsmina_dock_pm = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'vinardo':{123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        'args': [],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        'kwargs' : {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'autobox_add':12,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'num_modes':400,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'exhaustiveness':64,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'scoring':'vinardo',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'cpu':1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    },123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'smina_default':{123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        'args':[],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        'kwargs':{123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'num_modes':400,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'cpu':1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    },123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'reorder':{123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        'args':['score_only'],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        'kwargs':{123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            'custom_scoring':scoring_terms 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFvinardo_pm = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'args': [],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'kwargs' : {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'autobox_add':12,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'num_modes':400,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'exhaustiveness':64,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'scoring':'vinardo',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'cpu':1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsmina_pm = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'args':[],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'kwargs':{123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'num_modes':400,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'cpu':1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFreorder_pm = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'args':['score_only'],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'kwargs':{123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'custom_scoring':scoring_terms 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFoverlap_pm = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'default':{123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        'clash_cutoff_A':4,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        'clash_size_cutoff':0.3123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFoverlap_default = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'clash_cutoff_A':4,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'clash_size_cutoff':0.3123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFnative_contact_pm = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'default':{123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        'distance_threshold':4.0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    }123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFnative_contace_default = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'distance_threshold':4.0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFbinding_affinity_files = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'pdbbind':'/home/xander/data/PDBbind/indexs/index/INDEX_general_PL.2016'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF