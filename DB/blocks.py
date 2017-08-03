import os
import sys 
import re 
import time 
from db_config import data_dir
from collections import namedtuple, OrderedDict
import prody

table_tuple = namedtuple('Table',['type','columns','primary_key'])

def _makedir(path):
    if not os.path.exists(path):
        os.makedirs(path)

class operation(object):
    def __init__(self):
        self.ops = {}

    def register(self, name, block):
        self.ops[name] = block

class split_ligand(object):
    table = table_tuple(*['splited_ligand',
                     OrderedDict(
                        [
                            ('receptor','text'),
                            ('chain','text'),
                            ('resnum','text'),
                            ('resname','text'),
                            ('resid','text'),
                            ('heavy_atom','integer'),
                            ('max_size_on_axis', 'real'),
                            ('state','integer'),
                            ('comment','text')
                        ]
                     ),
                     ['receptor','chain','resnum','resname']
                ])

    @staticmethod
    def action(db,bucket, table_idx, param, input_data):
        '''
        Split ligand form PDB file
        
        Parse PDB header, ligand records under key 'chemicals', get the 
        
        
        Args:
            table_idx: id for split ligand table 
            param: dict
                {
                    'output_folder':'...',
                    'input_download_folder':'...',
                }
            input_data: [str], (str) or str
                ['1a2b'] ,('3eml') ,'3eln'
                
        Returns:

        '''
        try:
            if type(input_data).__name__ in ['tuple', 'list']:
                input_data = input_data[0]        # do not allow x = x[0]
            
            receptor = input_data                                                   # todo (maksym) better representation of the input data

            #fit_box_size = param['fit_box_size']

            output_folder = param['output_folder']
            output_folder = '{}_{}'.format(table_idx, output_folder)
            input_download_folder = param['input_download_folder']
            pdb_dir = os.path.join(data_dir, input_download_folder)      # todo (maksym) download_folder = source_folder
            pdb_path = os.path.join(pdb_dir, receptor+'.pdb')
            
            parsed_pdb = prody.parsePDB(pdb_path)
            parsed_header = prody.parsePDBHeader(pdb_path)
            
            output_lig_dir = os.path.join(data_dir, output_folder, receptor)  # todo(maksym) datadir is config.data_dir
            _makedir(output_lig_dir)

            ligands = []
            for chem in parsed_header['chemicals']:
                ligands.append([chem.chain, str(chem.resnum), chem.resname])


            for chain, resnum, resname in ligands:
                try:
                    lig = parsed_pdb.select('chain {} resnum {}'.format(chain, resnum))
                    resid = lig.getHierView().iterResidues().next().getResindex()
                    resid = str(resid)
                    heavy_lig = lig.select('not hydrogen')
                    heavy_atom = heavy_lig.numAtoms()
                    heavy_coord =heavy_lig.getCoords()
                    #max_size_on_axis = max(heavy_coord.max(axis=0) - heavy_coord.min(axis=0))
                    #Changing max_size_on_axis to max pairwise distance between coords
                    max_size_on_axis = max(scipy.spatial.distance.pdist(heavy_coord).tolist())
                    lig_name = '_'.join([receptor,chain,resnum,resname,'ligand']) + '.pdb'
                    prody.writePDB(os.path.join(output_lig_dir, lig_name), lig)

                    record = [receptor, chain, resnum, resname, resid, heavy_atom, max_size_on_axis, 1, 'success']
                    records = [record]
                    db.insert(table_idx, records, bucket=bucket)
                except Exception as e:
                    record =  [receptor, chain, resnum, resname, 0, 0, 0, 0, str(e)]
                    records = [record]
                    db.insert(table_idx, records, bucket=bucket)

        except Exception as e:
            print(e)
            raise Exception(str(e))

    @staticmethod
    def create(FLAGS, db):
        if FLAGS.folder_name is None:
            raise Exception("folder_name required")
        if FLAGS.download_idx is None:
            raise Exception('download_idx required')
        
        folder_name = FLAGS.folder_name
        download_idx = FLAGS.download_idx
        download_folder = db.get_folder(download_idx)
        table_param = {
            'func':'split_ligand',
            'output_folder': folder_name,
            'download_idx': download_idx,
            'input_download_folder': '{}_{}'.format(download_idx, download_folder),
            'depend':[download_idx],
            'fit_box_size':20
        } 

        return table_param

    @staticmethod
    def data(FLAGS, db, table_idx, table_param):

        download_idx = table_param['download_idx']
        download_list = db.get_all_success(download_idx)

        finished_list = db.get_all_success(table_idx)
        finished_list = map(lambda x:(x[0],),finished_list)
        failed_list = db.get_all_failed(table_idx)
        failed_list = map(lambda x:(x[0],), failed_list)

        if FLAGS.retry_failed:
            rest_list = list(set(download_list) - set(finished_list) | set(failed_list))
        else:
            rest_list = list(set(download_list) - set(finished_list) - set(failed_list))

        total = len(set(download_list))
        finished = len(set(finished_list)-set(failed_list))
        failed = len(set(failed_list))


        return rest_list   

    @staticmethod
    def progress(FLAGS, db, table_idx, table_param):
        download_idx = table_param['download_idx']
        total = db.get_num_all_success(download_idx)
        finished = db.get_num_all_success(table_idx)
        failed = db.get_num_all_failed(table_idx)
        return (total, finished, failed)

class download(object):

    table = table_tuple(*['download',
                     OrderedDict(
                         [
                             ('receptor','text'),
                             ('experiment','text'),
                             ('resolution','real'),
                             ('state','integer'),
                             ('comment','text')
                         ]
                     ),
                     ['receptor']])


    @staticmethod
    def action(db,bucket, table_idx, param, input_data):         # todo(maksym) input_data = pdb_ids
        '''
        Download pdb file from rcsb
        
        Args:
            table_idx: id for download table 
            param: dict
                {
                    'output_folder':'...',
                    ...
                }
            input_data: str pdb id 

        Returns:

        '''
        print("download action")
        try:
            print('download start')
            receptor = input_data[1:]                                                   # todo(maksym) pdb_id
            output_folder = param['output_folder']
            output_folder_name = '{}_{}'.format(table_idx, output_folder)
            dest_dir = os.path.join(data_dir, output_folder_name)
            _makedir(dest_dir)
            pdb_path = os.path.join(dest_dir, receptor+'.pdb')

            #pdb_path = '/home/maksym/ryan/labeled_pdb/crystal_ligands/'+receptor+'/'+receptor+'.pdb'
            #print ('pdb',pdb_path)
            print (pdb_path)
            if not os.path.exists(pdb_path):
                download_address = 'https://files.rcsb.org/download/{}.pdb'.format(receptor)
                os.system('wget --no-check-certificate -P {} {}'.format(dest_dir, download_address))
            header = prody.parsePDBHeader(pdb_path)
            record = [receptor, header['experiment'], header['resolution'], 1, 'success']
            records = [record]
            print('insert')
            db.insert(table_idx, records, bucket=bucket)
            print('finished')
        except Exception as e:
            "Exception causing non success"
            print (e)
            record = [input_data, 'unk', 0, 0, str(e)]                      # todo maksym (unk) = failed
            records = [record]
            db.insert(table_idx, records, bucket=bucket)


    @staticmethod
    def create(FLAGS, db=None):
        if FLAGS.folder_name is None:
            raise Exception("folder_name required")

        folder_name = FLAGS.folder_name
        table_param = {
            'func':'download',
            'output_folder': folder_name,
        }

        return table_param

    @staticmethod
    def data(FLAGS, db, table_idx, table_param):

        download_list = open('/Users/Will/projects/reformat/new_branch/core/DB/datasets/VDS1/data/main_pdb_target_list.txt').readline().strip().split(',')
        finished_list = db.get_all_success(table_idx)
        failed_list = db.get_all_failed(table_idx)

        if FLAGS.retry_failed:
            rest_list = list(set(download_list) - set(finished_list) | set(failed_list))
        else:
            rest_list =list(set(download_list) - set(finished_list) - set(failed_list)) 

        total = len(set(download_list))
        finished = len(set(finished_list)-set(failed_list))
        failed = len(set(failed_list))


        return rest_list  


    @staticmethod
    def progress(FLAGS, db, table_idx, table_param):
        total = len(open('/Users/Will/projects/reformat/new_branch/core/DB/datasets/VDS1/data/main_pdb_target_list.txt').readline().strip().split(','))
        finished = db.get_num_all_success(table_idx)
        failed = db.get_num_all_failed(table_idx)
        return (total, finished, failed)