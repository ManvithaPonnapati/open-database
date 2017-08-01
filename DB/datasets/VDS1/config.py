import os
import sys 
# path of smina binary file
#smina = 'smina.static'
smina = '/Users/xander/Projects/AffDB/smina.osx'

# pdb_target_list
list_of_PDBs_to_download = os.path.join(sys.path[0],'data','main_pdb_target_list.txt')
#list_of_PDBs_to_download = '/home/maksym/ryan/AffinityDB/pdb_list/main_pdb_target_list.txt'
# list_of_PDBs_to_download = os.path.join(sys.path[0], 'pdb_list','pdb_list.txt')


# example scoring
scoring_terms = os.path.join(sys.path[0], 'lib', 'smina.score')


"""
docking para
"""
dock_pm = {
    'vinardo':{
        'args': [],
        'kwargs' : {
            'autobox_add':12,
            'num_modes':400,
            'exhaustiveness':64,
            'scoring':'vinardo',
            'cpu':1
        }
    },
    'smina_default':{
        'args':[],
        'kwargs':{
            'num_modes':400,
            'cpu':1
        }
    },
    'reorder':{
        'args':['score_only'],
        'kwargs':{
            'custom_scoring':scoring_terms 
        }
    }

}

overlap_pm = {
    'default':{
        'clash_cutoff_A':4
    }
}

native_contact_pm = {
    'default':{
        'distance_threshold':4.0
    }
}


bind_pm = {
    'pdbbind':{
        'index':os.path.join(sys.path[0],'bind_index','INDEX_general_PL.2016'),
        'parse_func':'pdbbind'
    },
    'bindmoad':{
        'index':os.path.join(sys.path[0],'bind_index','every.csv'),
        'parse_func':'bindmoad'
    },
    'bindingdb':{
        'index':os.path.join(sys.path[0],'bind_index','BindingDB_All.tsv'),
        'parse_func':'bindingdb'
    }
}


exclusion_pm = {
    'default':{
        'index':os.path.join(sys.path[0],'bind_index','exclusion.txt')
    }
}
