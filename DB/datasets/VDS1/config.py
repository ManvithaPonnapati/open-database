import os
import sys 
import json
# path of smina binary file
#smina = 'smina.static'

smina = '/Users/Will/projects/smina/smina.osx'

# pdb_target_list
list_of_PDBs_to_download = os.path.join(sys.path[0],'data','main_pdb_target_list.txt')
#list_of_PDBs_to_download = '/home/maksym/ryan/AffinityDB/pdb_list/main_pdb_target_list.txt'
# list_of_PDBs_to_download = os.path.join(sys.path[0], 'pdb_list','pdb_list.txt')


# example scoring
scoring_terms = os.path.join(sys.path[0], 'data', 'smina.score')


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

class smina_param:

    kw_options = [
        'receptor',
        'ligand',
        'out',
        'flex',
        'flexres',
        'flexdist_ligand',
        'flexdist',
        'center_x',
        'center_y',
        'center_z',
        'size_x',
        'size_y',
        'size_z',
        'autobox_ligand',
        'autobox_add',
        'scoring',
        'custom_scoring',
        'minimize_iters',
        'approximation',
        'factor',
        'force_cap',
        'user_grid',
        'user_grid_lambda',
        'out_flex',
        'log',
        'atom_terms',
        'cpu',
        'seed',
        'exhaustiveness',
        'num_modes',
        'energy_range',
        'min_rmsd_filter',
        'addH',
        'config'
    ]

    arg_options = [
        'no_lig',
        'score_only',
        'local_only',
        'minimize',
        'randomize_only',
        'accurate_line',
        'print_terms',
        'print_atom_types',
        'atom_term_data',
        'quiet',
        'flex_hydrogen',
        'help',
        'help_hidden',
        'version'
    ]

    def __init__(self, name=None):
        self.smina = smina

        if not name is None:
            self.name = name
        
    def set_smina(self, smina):
        self.smina = smina

    def set_name(self, name):
        self.name = name

    def load_param(self, *arg, **kw):
        self.args = arg
        self.kwargs = kw

    def param_dump(self):
        param = {
            'args':self.args,
            'kwargs':self.kwargs
        }
        
        return param
        
    def param_load(self, param):
        if type(param).__name__ in ['unicode','str']:
            param = json.loads(param)
        
        self.args = param['args']
        self.kwargs = param['kwargs']
        

    def make_command(self, *arg, **kw):
        cmd = self.smina
        for a in self.arg_options:
            if arg and a in arg:
                cmd += ' --'
                cmd += a
            elif a in self.args:
                cmd += ' --'
                cmd += a

        for key in self.kw_options:
            if kw and key in kw.keys():
                cmd += ' --'
                cmd += key
                cmd += ' '
                cmd += str(kw[key])
            elif key in self.kwargs.keys():
                cmd += ' --'
                cmd += key
                cmd += ' '
                cmd += str(self.kwargs[key])

        return cmd
    
    