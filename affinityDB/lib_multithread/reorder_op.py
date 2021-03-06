import os,sys
import subprocess
import json 


# FIXME: this option can only run with Vina_dock (and never can be used separately)
# please, make it an integral part of dock

class Reorder_init:
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

    def __init__(self, data_dir, reorder_folder, smina_path,dock_param):
        """
        Initialize reorder func

        :param data_dir: str dir for the folder to save data
        :param reorder_folder: str name of the folder to save reorder output
        :param smina_path: str path for teh executable smina program
        :param dock_param: dict docking parameter {'args':[...], 'kwargs':{...}}
        :return:
        None
        """
        reorder_dir = os.path.join(data_dir, reorder_folder)
        if not os.path.exists(reorder_dir):
            os.makedirs(reorder_dir)

        self.data_dir = data_dir
        self.reorder_folder = reorder_folder
        self.smina_path = smina_path
        self._param_load(dock_param)        
        self.this_module.reorder_init = self

    def _param_load(self, param):
        if type(param).__name__ in ['unicode','str']:
            param = json.loads(param)                                                                                   # FIXME: I don't like json here

        self.args = param['args']
        self.kwargs = param['kwargs']


    def _make_command(self, *arg, **kw):
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

def reorder(rec_outpath, lig_outpath, init='reorder_init'):
    """
    Parse the ligand by smina, and then output it. So the order of the atom keeps the same as the docking result

    Example:
    <pre lang="python">
    reorder('3_split_receptor/10MH/10MH_B_407_5CM_receptor.pdb','2_split_ligand/10MH/10MH_B_407_5CM_ligand.pdb')
    </pre>

    Output:
    <pre lang="python">
    [['3_split_receptor/10MH/10MH_B_407_5CM_receptor.pdb', '4_reorder/10MH/10MH_B_407_5CM_ligand.pdb']]
    </pre>

    :param rec_outpath: str relative path for receptor
    :param lig_outpath: str relative path for ligand
    :param init: str initialize module 
    :returns: 
    nested list: [[receptor_output_path, reorder_ligand_output_path]]
    """

    init = eval(init)
    reorder_dir = os.path.join(init.data_dir, init.reorder_folder) 
    rec_path = os.path.join(init.data_dir, rec_outpath)
    lig_path = os.path.join(init.data_dir, lig_outpath)

    reo_name = os.path.basename(rec_path).replace('receptor','reorder')
    receptor = os.path.basename(rec_outpath).split('_')[0]
    out_path = os.path.join(reorder_dir, receptor, reo_name)

    if not os.path.exists(os.path.dirname(out_path)):
        os.makedirs(os.path.dirname(out_path))

    kw = {
        'receptor': rec_path,
        'ligand': lig_path,
        'autobox_ligand':lig_path,
        'out':out_path
    }       

    cmd = init._make_command(**kw)
    cl = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    cl.wait()

    return [[rec_outpath, os.path.join(init.reorder_folder, receptor, reo_name)]]
