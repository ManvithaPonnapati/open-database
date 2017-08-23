import os,sys
import subprocess
import json 


# FIXME: this option can only run with Vina_dock (and never can be used separately)
# please, make it an integral part of dock

class Reorder_init:
    this_module = sys.modules[__name__]
    def __init__(self, data_dir, reorder_folder, smina_path):
        """

        :param data_dir:
        :param reorder_folder:
        :param smina_path:
        """
        reorder_dir = os.path.join(data_dir, reorder_folder)
        if not os.path.exists(reorder_dir):
            os.makedirs(reorder_dir)

        self.data_dir = data_dir
        self.reorder_folder = reorder_folder
        self.smina_path = smina_path
        self.this_module.reorder_init = self

def reorder(rec_outpath, lig_outpath, init='reorder_init'):
    """

    :param rec_outpath:
    :param lig_outpath:
    :param init:
    :return:
    """

    init = eval(init)
    reorder_dir = os.path.join(init.data_dir, init.reorder_folder) 
    rec_path = os.path.join(init.data_dir, rec_outpath)
    lig_path = os.path.join(init.data_dir, lig_outpath)

    reo_name = os.path.basename(rec_path).replace('receptor','reorder')
    receptor = os.path.basename(rec_outpath).split('_')[0]
    out_path = os.path.join(reorder_dir, receptor, reo_name)

    smina_pm = smina_param(init.smina_path)
    smina_pm.param_load({
        'args':['score_only']})
    if not os.path.exists(os.path.dirname(out_path)):
        os.makedirs(os.path.dirname(out_path))

    kw = {
        'receptor': rec_path,
        'ligand': lig_path,
        'autobox_ligand':lig_path,
        'out':out_path
    }       

    cmd = smina_pm.make_command(**kw)
    cl = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    cl.wait()

    return [[rec_outpath, os.path.join(init.reorder_folder, receptor, reo_name)]]

# class smina_param:
#
#     kw_options = [
#         'receptor',
#         'ligand',
#         'out',
#         'flex',
#         'flexres',
#         'flexdist_ligand',
#         'flexdist',
#         'center_x',
#         'center_y',
#         'center_z',
#         'size_x',
#         'size_y',
#         'size_z',
#         'autobox_ligand',
#         'autobox_add',
#         'scoring',
#         'custom_scoring',
#         'minimize_iters',
#         'approximation',
#         'factor',
#         'force_cap',
#         'user_grid',
#         'user_grid_lambda',
#         'out_flex',
#         'log',
#         'atom_terms',
#         'cpu',
#         'seed',
#         'exhaustiveness',
#         'num_modes',
#         'energy_range',
#         'min_rmsd_filter',
#         'addH',
#         'config'
#     ]
#
#     arg_options = [
#         'no_lig',
#         'score_only',
#         'local_only',
#         'minimize',
#         'randomize_only',
#         'accurate_line',
#         'print_terms',
#         'print_atom_types',
#         'atom_term_data',
#         'quiet',
#         'flex_hydrogen',
#         'help',
#         'help_hidden',
#         'version'
#     ]
#
#     def __init__(self, smina_path, name=None):
#         self.smina = smina_path
#
#         if not name is None:
#             self.name = name
#
#     def set_smina(self, smina):
#         self.smina = smina
#
#     def set_name(self, name):
#         self.name = name
#
#     def load_param(self, *arg, **kw):
#         self.args = arg
#         self.kwargs = kw
#
#     def param_dump(self):
#         param = {
#             'args':self.args,
#             'kwargs':self.kwargs
#         }
#
#         return param
#
#     def param_load(self, param):
#         if type(param).__name__ in ['unicode','str']:
#             param = json.loads(param)
#
#         self.args = param['args']
#         self.kwargs = param['kwargs']
#
#
#     def make_command(self, *arg, **kw):
#         cmd = self.smina
#         for a in self.arg_options:
#             if arg and a in arg:
#                 cmd += ' --'
#                 cmd += a
#             elif a in self.args:
#                 cmd += ' --'
#                 cmd += a
#
#         for key in self.kw_options:
#             if kw and key in kw.keys():
#                 cmd += ' --'
#                 cmd += key
#                 cmd += ' '
#                 cmd += str(kw[key])
#             elif key in self.kwargs.keys():
#                 cmd += ' --'
#                 cmd += key
#                 cmd += ' '
#                 cmd += str(self.kwargs[key])
#
#         return cmd
