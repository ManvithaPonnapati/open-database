import os,sys
import subprocess
import json 




class Dock_init:
    this_module = sys.modules[__name__]

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


    def __init__(self, data_dir, dock_folder, smina_path, dock_param):
        """

        :param data_dir: str:: dir for the folder to save data
        :param dock_folder: str:: name of the folder to save reorder output
        :param smina_path: str:: path for teh executable smina program
        :param dock_param: dict::   docking parameter {'args':[...], 'kwargs':{...}}
        """
        dock_dir = os.path.join(data_dir, dock_folder)
        if not os.path.exists(dock_dir):
            os.makedirs(dock_dir)

        self.param_load(dock_param)
        self.data_dir = data_dir
        self.dock_folder = dock_folder
        self.smina_path = smina_path

        self.this_module.dock_init = self 

    def param_load(self, param):
        if type(param).__name__ in ['unicode','str']:
            param = json.loads(param)

        self.args = param['args']
        self.kwargs = param['kwargs']


    def make_command(self, *arg, **kw):
        cmd = self.smina_path
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
        


def dock(rec_outpath, reorder_outpath, init='dock_init'):
    """
    Docking the ligand by smina

    :param rec_outpath: str:: relative path for receptor
    :param reorder_outpath: str:: relative path for reorder ligand
    :param init: str:: init func naem
    :return: nested list:: docking result contains the relative path for receptor, reorder ligand and docked ligand
    """
    init = eval(init)
    receptor = os.path.basename(rec_outpath).split('_')[0]
    dock_dir = os.path.join(init.data_dir, init.dock_folder) 
    rec_path = os.path.join(init.data_dir, rec_outpath)
    reorder_path = os.path.join(init.data_dir, reorder_outpath)

    dock_name = os.path.basename(rec_path).replace('receptor','dock')
    out_path = os.path.join(dock_dir, receptor, dock_name)



    if not os.path.exists(os.path.dirname(out_path)):
        os.makedirs(os.path.dirname(out_path))

    kw = {
        'receptor': rec_path,
        'ligand': reorder_path,
        'autobox_ligand':reorder_path,
        'out':out_path
    }

    cmd = init.make_command(**kw)
    cl = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    cl.wait()

    return [[rec_outpath, reorder_outpath, os.path.join(init.dock_folder, receptor, dock_name)]]

