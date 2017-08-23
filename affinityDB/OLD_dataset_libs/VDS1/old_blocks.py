import os
import sys 
import re 
import time
import scipy.spatial
from db_config import data_dir
from collections import namedtuple, OrderedDict
import prody
from chembl_webresource_client.new_client import new_client
import tempfile
table_tuple = namedtuple('Table',['type','columns','primary_key'])

from db_config import blast_db as BLASTDB
import subprocess

import xml.dom.minidom
from chembl_webresource_client.new_client import new_client
activities = new_client.activity

def _makedir(path):
    if not os.path.exists(path):
        os.makedirs(path)

class operation(object):
    def __init__(self):
        self.ops = {}

    def register(self, name, block):
        self.ops[name] = block

class blast(object):
    table = table_tuple(*['blast',
                    OrderedDict(
                        [
                            ('receptor','varchar(255)'),
                            ('chain','varchar(255)'),
                            ('resnum','varchar(255)'),
                            ('resname','varchar(255)'),
                            ('bitscore','real'),
                            ('score','real'),
                            ('evalue','real'),
                            ('aid','varchat(255)'),
                            ('mid','varchat(255)'),
                            ('targetid','varchar(255)'),
                            ('smile','text'),
                            ('type','text'),
                            ('op','text'),
                            ('value','real'),
                            ('unit','text'),
                            ('state','integer'),
                            ('comment','text')
                        ]
                    ),
                    ['receptor','chain','resnum','resname','targetid','aid','mid']    
                ])

    @staticmethod
    def action(db, bucket, table_idx, param, input_data):
        try:
            if type(input_data).__name__ in ['tuple', 'list']:
                input_data = input_data[0]        # do not allow x = x[0]
            
            activities = new_client.activity
            
            receptor = input_data  
            input_download_folder = param['input_download_folder']
            pdb_dir = os.path.join(data_dir, input_download_folder)      # todo (maksym) download_folder = source_folder
            pdb_path = os.path.join(pdb_dir, receptor+'.pdb')

            cdir = os.getcwd()
            tdir = tempfile.mkdtemp()
            os.chdir(tdir)    

            pdbHead = prody.parsePDBHeader(pdb_path)
            pdbFile = prody.parsePDB(pdb_path)

            ligands = []
            for chem in pdbHead['chemicals']:
                ligands.append([chem.chain, str(chem.resnum), chem.resname, chem.name])
            
            for chain, resnum, resname, name in ligands:
                
                rec = pdbFile.select('not (chain {} resnum {})'.format(chain, resnum))
                ligand = pdbFile.select('chain {} resnum {}'.format(chain, resnum))

                cen_ligand = prody.calcCenter(ligand)
                around_atoms = rece.select('within 10 of center', center=cen_ligand)
                hv = around_atoms.getHierView()
                sequence = hv['A'].getSequence()


                


                with open('sequence.fasta','w') as fout:
                    fout.write(">receptor\n" + sequence + '\n')

                cmd = 'blastp -db {} -query sequence.fasta -outfmt 5 -out result'.format(BLASTDB)
                print(os.getcwd())
            
                cl = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                cl.wait()

                print(os.listdir(os.getcwd()))

                dtree = xml.dom.minidom.parse("result")
                collection = dtree.documentElement
                hits = collection.getElementsByTagName("Hit")


                blast_result = []
                for hit in hits:
                    hit_id = hit.getElementsByTagName('Hit_id')[0].childNodes[0].data
                    hsps = hit.getElementsByTagName('Hit_hsps')[0]
                    bit_score = hsps.getElementsByTagName('Hsp_bit-score')[0].childNodes[0].data
                    score = hsps.getElementsByTagName('Hsp_score')[0].childNodes[0].data
                    evalue = hsps.getElementsByTagName('Hsp_evalue')[0].childNodes[0].data
                    blast_result.append([hit_id, bit_score, score, evalue])

                for bresult in blast_result:
                    target_id = bresult[0]
                    res = activities.filter(target_chembl_id=target_id, pchembl_value__isnull=False)

                    res_size = len(res)
                    print (res_size)
                    for i in range(res_size):
                        result = res[i]
                        aid = result['assay_chembl_id']
                        smile= result['canonical_smiles']
                        mid = result['molecule_chembl_id']
                        ptype = result['published_type']
                        op = result['published_relation']
                        value = result['published_value']
                        unit = result['standard_units']

                        entry = [aid, mid, target_id, smile, ptype, op, value, unit]

                        record = [receptor, chain, resnum, resname] + bresult[1:] + entry + [1, 'success']
                        records = [record]
                        db.insert(table_idx, records, bucket=bucket)
        except Exception as e:
            print(str(e))

    @staticmethod
    def create(FLAGS, db):

        if FLAGS.download_idx is None:
            raise Exception('download_idx required')


        download_idx = FLAGS.download_idx
        _, tp = db.get_table_info(download_idx)
        download_folder = tp['output_folder']
        table_param = {
            'func':'blast',
            'download_idx': download_idx,
            'input_download_folder': '{}_{}'.format(download_idx, download_folder),
            'depend':[download_idx]
        }
        return table_param                    

    @staticmethod
    def data(FLAGS, db, table_idx, table_param):

        download_idx = table_param['download_idx']
        download_list = db.select_from_table(download_idx, ['receptor'],[('state','=','1')])  

        finished_list = db.select_from_table(table_idx, ['receptor','chain','resnum','resname'] ,[('state','=','1')])
        finished_list = map(lambda x:(x[0],),finished_list)
        failed_list = db.select_from_table(table_idx, ['receptor','chain','resnum','resname'] ,[('state','=','0')])
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
        total = db.count_from_table(download_idx,[('state','=','1')])
        finished = db.count_from_table(table_idx,[('state','=','1')])
        failed = db.count_from_table(table_idx,[('state','=','0')])

        
        return (total, finished, failed)

class reorder(object):
    table = table_tuple(*['reorder',
                     OrderedDict(
                        [
                            ('receptor','varchar(255)'),
                            ('chain','varchar(255)'),
                            ('resnum','varchar(255)'),
                            ('resname','varchar(255)'),
                            ('path','text'),
                            ('state','integer'),
                            ('comment','text')
                        ]
                     ),
                     ['receptor','chain','resnum','resname']
                ])

    @staticmethod
    def action(db,bucket, table_idx, param, input_data): 
        try:
            receptor, chain, resnum, resname = input_data
            
            output_folder = param['output_folder']
            output_folder = '{}_{}'.format(table_idx, output_folder)
            input_lig_folder = param['input_ligand_folder']
            input_rec_folder = param['input_receptor_folder']
            smina_pm = smina_param()
            smina_pm.param_load(param['smina_param'])

            out_dir = os.path.join(data_dir, output_folder, receptor)
            _makedir(out_dir)
            out_name = '_'.join(input_data + ['ligand']) + '.pdb'
            out_path = os.path.join(out_dir, out_name)

            input_lig_dir = os.path.join(data_dir, input_lig_folder, receptor)       # lig_dir = input_lig_dir
            lig_name = '_'.join(input_data + ['ligand']) + '.pdb'
            input_lig_path = os.path.join(input_lig_dir, lig_name)

            input_rec_dir = os.path.join(data_dir, input_rec_folder, receptor)      # rec_dir = input_rec_dir
            rec_name = '_'.join(input_data + ['receptor']) + '.pdb'
            input_rec_path = os.path.join(input_rec_dir, rec_name)

            kw = {
                'receptor': input_rec_path,
                'ligand': input_lig_path,
                'autobox_ligand':input_lig_path,
                'out':out_path
            }

            rel_path = os.path.join(output_folder, receptor, out_name)

            cmd = smina_pm.make_command(**kw)                                       # todo(maksym) smina_cmd

            cl = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            cl.wait()
            prody.parsePDB(out_path)

            record = input_data + [rel_path, 1, 'success']
            records = [record]
            db.insert(table_idx, records,bucket=bucket)

        except Exception as e:
            record = input_data + [' ', 0, str(e)]
            records = [record]
            db.insert(table_idx, records,bucket=bucket)

    @staticmethod
    def create(FLAGS, db):
        if FLAGS.folder_name is None:
            raise Exception("folder_name required")
        if FLAGS.receptor_idx is None:
            raise Exception('receptor_idx required')
        if FLAGS.ligand_idx is None:
            raise Exception('ligand_idx required')

        folder_name = FLAGS.folder_name
        receptor_idx = FLAGS.receptor_idx
        receptor_folder = db.get_folder(receptor_idx)
        ligand_idx = FLAGS.ligand_idx
        ligand_folder = db.get_folder(ligand_idx)
        table_param = {
            'func': 'reorder',
            'output_folder': folder_name,
            'receptor_idx':receptor_idx,
            'input_receptor_folder':'{}_{}'.format(receptor_idx,receptor_folder),
            'ligand_idx': ligand_idx,
            'input_ligand_folder': '{}_{}'.format(ligand_idx, ligand_folder),
            'depend':[receptor_idx, ligand_idx],
            'smina_param':config.smina_dock_pm['reorder']
        }

        return table_param

    @staticmethod
    def data(FLAGS, db, table_idx, table_param):
        rec_idx = table_param['receptor_idx']
        rec_list = db.select_from_table(rec_idx, ['receptor','chain','resnum','resname'] ,[('state','=','1')])

        lig_idx = table_param['ligand_idx']
        lig_list = db.select_from_table(lig_idx, ['receptor','chain','resnum','resname'] ,[('state','=','1')])

        finished_list = db.select_from_table(table_idx, ['receptor','chain','resnum','resname'] ,[('state','=','1')])
        failed_list = db.select_from_table(table_idx, ['receptor','chain','resnum','resname'] ,[('state','=','0')])


        if FLAGS.retry_failed:
            rest_list = list(set(rec_list) & set(lig_list) - set(finished_list) | set(failed_list))
        else:
            rest_list = list(set(rec_list) & set(lig_list) - set(finished_list) - set(failed_list))

        return rest_list

class dock(object):
    table = table_tuple(*['dock',
                     OrderedDict(
                        [
                            ('receptor','varchar(255)'),
                            ('chain','varchar(255)'),
                            ('resnum','varchar(255)'),
                            ('resname','varchar(255)'),
                            ('path','text'),
                            ('state','integer'),
                            ('comment','text')
                        ]
                     ),
                     ['receptor','chain','resnum','resname']
                ])

    @staticmethod
    def action(db,bucket, table_idx, param, input_data):
        '''
        Use smina to docking lignad, 
        ligand can be identified by input_data, take the ligand and receptor
        from input_ligand_folder and input_receptor_folder
        docking result will be saved to ouptut_folder
        
        Docking parameter will be parsed from smina_param
        
        Args:
            table_idx: id for dock table
            param: dict
                {
                    'output_folder': '...',
                    'input_lignad_folder':'...',
                    'input_receptor_folder':'...',
                    'smina_param':
                        {
                            'args': [],
                            'kwargs' : {
                                'autobox_add':12,
                                'num_modes':400,
                                'exhaustiveness':64,
                                'scoring':'vinardo',
                                'cpu':1
                        },
                    ...
                }
            input_data: list
                        [receptor, chain, resnum, resname]

        Returns:

        '''
        try:
            receptor, chain, resnum, resname = input_data
            
            output_folder = param['output_folder']
            output_folder = '{}_{}'.format(table_idx, output_folder)
            input_lig_folder = param['input_ligand_folder']
            input_rec_folder = param['input_receptor_folder']
            smina_pm = smina_param()
            smina_pm.param_load(param['smina_param'])

            out_dir = os.path.join(data_dir, output_folder, receptor)
            _makedir(out_dir)
            out_name = '_'.join(input_data + ['ligand']) + '.pdb'
            out_path = os.path.join(out_dir, out_name)

            input_lig_dir = os.path.join(data_dir, input_lig_folder, receptor)    # lig_dir = input_lig_dir
            lig_name = '_'.join(input_data + ['ligand']) + '.pdb'
            input_lig_path = os.path.join(input_lig_dir, lig_name)

            input_rec_dir = os.path.join(data_dir, input_rec_folder, receptor)
            rec_name = '_'.join(input_data + ['receptor']) + '.pdb'
            input_rec_path = os.path.join(input_rec_dir, rec_name)

            rel_path = os.path.join(output_folder, receptor, out_name)

            kw = {
                'receptor': input_rec_path,
                'ligand': input_lig_path,
                'autobox_ligand':input_lig_path,
                'out':out_path
            }


            cmd = smina_pm.make_command(**kw)
            #print cmd
            cl = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            cl.wait()
            prody.parsePDB(out_path)                                                                    # todo (maksym) we can even do more

            record = input_data + [rel_path, 1, 'success']
            records = [record]
            db.insert(table_idx, records,bucket=bucket)

        except Exception as e:
            record = input_data + [' ', 0, str(e)]
            records = [record]
            db.insert(table_idx, records,bucket=bucket)

    @staticmethod
    def create(FLAGS, db):
        if FLAGS.folder_name is None:
            raise Exception("folder_name required")
        if FLAGS.receptor_idx is None:
            raise Exception('receptor_idx required')
        if FLAGS.ligand_idx is None:
            raise Exception('ligand_idx required')
        if FLAGS.param is None:
            raise Exception('param required')

        dock_param = FLAGS.param
        if not dock_param in config.smina_dock_pm.keys():
            raise KeyError("dock param {} doesn't exists. ".format(dock_param)\
                            + "available options are: {}".format(', '.join(config.smina_dock_pm.keys())))
        dock_param = config.smina_dock_pm[dock_param]
        folder_name = FLAGS.folder_name
        receptor_idx = FLAGS.receptor_idx
        receptor_folder = db.get_folder(receptor_idx)
        ligand_idx = FLAGS.ligand_idx
        ligand_folder = db.get_folder(ligand_idx)
        table_param = {
            'func': 'smina_dock',
            'output_folder': folder_name,
            'receptor_idx':receptor_idx,
            'input_receptor_folder': '{}_{}'.format(receptor_idx, receptor_folder),
            'ligand_idx': ligand_idx,
            'input_ligand_folder': '{}_{}'.format(ligand_idx, ligand_folder),
            'depend':[receptor_idx, ligand_idx],
            'smina_param':dock_param
        }

        return table_param       

    @staticmethod
    def data(FLAGS, db, table_idx, table_param):
        rec_idx = table_param['receptor_idx']
        rec_list = db.select_from_table(rec_idx, ['receptor','chain','resnum','resname'] ,[('state','=','1')])

        lig_idx = table_param['ligand_idx']
        lig_list = db.select_from_table(lig_idx, ['receptor','chain','resnum','resname'] ,[('state','=','1')])

        finished_list = db.select_from_table(table_idx, ['receptor','chain','resnum','resname'] ,[('state','=','1')])
        failed_list = db.select_from_table(table_idx, ['receptor','chain','resnum','resname'] ,[('state','=','0')])


        if FLAGS.retry_failed:
            rest_list = list(set(rec_list) & set(lig_list) - set(finished_list) | set(failed_list))
        else:
            rest_list = list(set(rec_list) & set(lig_list) - set(finished_list) - set(failed_list))

        return rest_list

    
class rmsd(object):
    table = table_tuple(*['rmsd',
                    OrderedDict(
                        [
                            ('receptor','varchar(255)'),
                            ('chain','varchar(255)'),
                            ('resnum','varchar(255)'),
                            ('resname','varchar(255)'),
                            ('position','integer'),
                            ('rmsd','real'),
                            ('state','integer'),
                            ('comment','text')
                        ]
                    ),
                    ['receptor','chain','resnum','resname','position']])

    @staticmethod
    def action(db,bucket, table_idx, param, input_data):
        '''
            Calculate rmsd and insert the result into database
            
            
            Args:
                table_idx: int, id for native contact table
                param: dict, parameters
                        {
                            'input_docked_foler':'...',
                            'input_crystal_folder':'...',
                        }
                input_data: list  
                        [receptor, chain, resnum ,resname] 

            Returns:

        '''

        try:
            receptor, chain, resnum, resname = input_data
            input_docked_folder = param['input_docked_folder']
            input_crystal_folder = param['input_crystal_folder']
            lig_name = '_'.join([receptor, chain, resnum, resname, 'ligand']) + '.pdb'

            input_docked_dir = os.path.join(data_dir,input_docked_folder, receptor)
            input_docked_path = os.path.join(input_docked_dir, lig_name)

            input_crystal_dir = os.path.join(data_dir, input_crystal_folder, receptor)
            input_crystal_path = os.path.join(input_crystal_dir, lig_name)

            docked_coords = prody.parsePDB(input_docked_path).getCoordsets()
            crystal_coord = prody.parsePDB(input_crystal_path).getCoords()

            rmsd = np.sqrt(np.mean(np.sum(np.square(docked_coords - crystal_coord), axis=1), axis=-1))

            # todo (maksym) RMSDs not rmsd
            records = []
            for i, rd in enumerate(rmsd):
                records.append(input_data + [i + 1, rd, 1, 'success'])
            db.insert(table_idx, records, bucket=bucket)
        except Exception as e:
            record = input_data + [1, 0, 0, str(e)]
            records = [record]
            db.insert(table_idx, records, bucket=bucket)

    @staticmethod
    def create(FLAGS, db):
        if FLAGS.crystal_idx is None:
            raise Exception('crystal_idx required')
        if FLAGS.docked_idx is None:
            raise Exception('docked_idx required')

        crystal_idx = FLAGS.crystal_idx
        crystal_folder = db.get_folder(crystal_idx)
        docked_idx = FLAGS.docked_idx
        docked_folder = db.get_folder(docked_idx)
        table_param = {
            'func':'rmsd',
            'crystal_idx': crystal_idx,
            'input_crystal_folder':'{}_{}'.format(crystal_idx, crystal_folder),
            'docked_idx': docked_idx,
            'input_docked_folder':'{}_{}'.format(docked_idx, docked_folder),
            'depend':[crystal_idx, docked_idx]
        }

    @staticmethod
    def data(FLAGS, db, table_idx, table_param):
        cry_idx = table_param['crystal_idx']
        cry_list = db.select_from_table(cry_idx, ['receptor','chain','resnum','resname'] ,[('state','=','1')])

        doc_idx = table_param['docked_idx']
        doc_list = db.select_from_table(doc_idx, ['receptor','chain','resnum','resname'] ,[('state','=','1')])

        finished_list = db.select_from_table(cry_idx, ['receptor','chain','resnum','resname'] ,[('state','=','1')])
        finished_list = map(lambda x: x[:-1], finished_list)
        failed_list = db.select_from_table(table_idx, ['receptor','chain','resnum','resname'] ,[('state','=','0')])
        failed_list = map(lambda x: x[:-1], failed_list)

        if FLAGS.retry_failed:
            rest_list = list(set(cry_list) & set(doc_list) - set(finished_list) | set(failed_list))
        else:
            rest_list = list(set(cry_list) & set(doc_list) - set(finished_list) - set(failed_list))
        
        return rest_list

class overlap(object):
    table = table_tuple(*['overlap',
                        OrderedDict(
                            [
                                ('receptor','varchar(255)'),
                                ('chain','varchar(255)'),
                                ('resnum','varchar(255)'),
                                ('resname','varchar(255)'),
                                ('position','integer'),
                                ('overlap_ratio','real'),
                                ('state','integer'),
                                ('comment','text')
                            ]
                        ),
                        ['receptor','chain','resnum','resname','position']])

    @staticmethod
    def action(db,bucket, table_idx, param, input_data):
        '''
        Calculate overlap ratio and insert the result into database
        
        The overlap ratio meansure how many atoms from ligand_A are
        close to the atoms from ligand_B
        
        Args:
            table_idx:  id for overlap table
            param: dict
                {
                    'input_docked_folder':'...',
                    'input_crystal_folder':'...',
                    'overlap_param':
                        {
                            'clash_cutoff_A':'...'
                            'clash_size_cutoff':'...'
                        }
                    ...
                }
            input_data: list  
                        [receptor, chain, resnum ,resname] 

        Returns:

        '''
        # todo (MAKSYM) overlap = per_atom_rmsd_with_cutoff
        try:
            receptor, chain, resnum, resname = input_data
            input_docked_folder = param['input_docked_folder']
            input_crystal_folder = param['input_crystal_folder']
            overlap_pm = param['overlap_param']
            clash_cutoff_A = overlap_pm['clash_cutoff_A']


            lig_name = '_'.join([receptor, chain, resnum, resname, 'ligand']) + '.pdb'
            input_docked_dir = os.path.join(data_dir, input_docked_folder, receptor)
            input_docked_path = os.path.join(input_docked_dir, lig_name)

            input_crystal_dir = os.path.join(data_dir, input_crystal_folder, receptor)
            input_crystal_path = os.path.join(input_crystal_dir, lig_name)

            docked_coords = prody.parsePDB(input_docked_path).getCoordsets()
            crystal_coords = prody.parsePDB(input_crystal_path).getCoords()
            # todo (maksym) next scripts have a specific way to use words coord and coords

            expanded_docked = np.expand_dims(docked_coords, -2) #1
            diff = expanded_docked - crystal_coords #2
            distance = np.sqrt(np.sum(np.power(diff, 2), axis=-1))   # 3

            all_clash = (distance < clash_cutoff_A).astype(float)  # 4
            atom_clash = (np.sum(all_clash, axis=-1) > 0).astype(float) # 5
            position_clash_ratio = np.mean(atom_clash, axis=-1) # 6
            # todo (maksym) 1-6 in one line

            records = []
            for i, ratio in enumerate(position_clash_ratio):
                records.append(input_data + [i + 1, ratio, 1, 'success'])

            db.insert(table_idx, records, bucket=bucket)

        except Exception as e:
            record = input_data + [1, 0, 0, str(e)]
            records = [record]
            db.insert(table_idx, records, bucket=bucket)

    @staticmethod
    def create(FLAGS, db):
        if FLAGS.crystal_idx is None:
            raise Exception('crystal_idx require')
        if FLAGS.docked_idx is None:
            raise Exception('docked_idx required')
        if FLAGS.param is None:
            raise Exception('param required')
        overlap_param = FLAGS.param
        if not overlap_param in config.overlap_pm.keys():
            raise KeyError("dock param {} doesn't exists. ".format(overlap_param) \
                           + "available options are: {}".format(', '.join(config.overlap_pm.keys())))

        crystal_idx = FLAGS.crystal_idx
        crystal_folder = db.get_folder(crystal_idx)
        docked_idx = FLAGS.docked_idx
        docked_folder = db.get_folder(docked_idx)
        
        
        table_param = {
            'func':'overlap',
            'crystal_idx': crystal_idx,
            'input_crystal_folder':'{}_{}'.format(crystal_idx, crystal_folder),
            'docked_idx': docked_idx,
            'input_docked_folder':'{}_{}'.format(docked_idx, docked_folder),
            'depend':[crystal_idx, docked_idx],
            'overlap_param':config.overlap_pm[overlap_param]
        }

        return table_param        

    @staticmethod
    def data(FLAGS, db, table_idx, table_param):
        cry_idx = table_param['crystal_idx']
        cry_list = db.select_from_table(cry_idx, ['receptor','chain','resnum','resname'] ,[('state','=','1')])

        doc_idx = table_param['docked_idx']
        doc_list = db.select_from_table(doc_idx, ['receptor','chain','resnum','resname'] ,[('state','=','1')])

        finished_list = db.select_from_table(cry_idx, ['receptor','chain','resnum','resname'] ,[('state','=','1')])
        finished_list = map(lambda x: x[:-1], finished_list)
        failed_list = db.select_from_table(table_idx, ['receptor','chain','resnum','resname'] ,[('state','=','0')])
        failed_list = map(lambda x: x[:-1], failed_list)

        if FLAGS.retry_failed:
            rest_list = list(set(cry_list) & set(doc_list) - set(finished_list) | set(failed_list))
        else:
            rest_list = list(set(cry_list) & set(doc_list) - set(finished_list) - set(failed_list))
        
        return rest_list

class native_contact(object):
    table = table_tuple(*['native_contact',
                    OrderedDict(
                        [
                            ('receptor','varchar(255)text'),
                            ('chain','varchar(255)'),
                            ('resnum','varchar(255)'),
                            ('resname','varchar(255)'),
                            ('position','integer'),
                            ('native_contact','real'),
                            ('state','integer'),
                            ('comment','text')
                        ]
                    ),
                   ['receptor','chain','resnum','resname','position']])

    @staticmethod
    def action(db,bucket, table_idx, param, input_data):
        '''
        Calculate native contact and insert the result into database
        Args:
            table_idx: int, id for native contact table
            param: dict, parameters
                    {
                        'input_docked_foler':'...',
                        'input_crystal_folder':'...',
                        'input_receptor_folder':'...',
                        'distance_threshold':'...',
                    }
            input_data: list  
                    [receptor, chain, resnum ,resname] 

        Returns:

        '''
        try:
            receptor, chain, resnum, resname = input_data
            input_docked_folder = param['input_docked_folder']
            input_crystal_folder = param['input_crystal_folder']
            input_rec_folder = param['input_receptor_folder']
            distance_threshold = param['distance_threshold']
            lig_name = '_'.join([receptor, chain, resnum, resname, 'ligand']) + '.pdb'
            rec_name = '_'.join([receptor, chain, resnum, resname, 'receptor']) + '.pdb'

            input_docked_dir = os.path.join(data_dir, input_docked_folder, receptor)
            input_docked_path = os.path.join(input_docked_dir, lig_name)

            input_crystal_dir = os.path.join(data_dir, input_crystal_folder, receptor)
            input_crystal_path = os.path.join(input_crystal_dir, lig_name)

            input_rec_dir = os.path.join(data_dir, input_rec_folder, receptor)
            input_rec_path = os.path.join(input_rec_dir, rec_name)

            parsed_docked =  prody.parsePDB(input_docked_path).select('not hydrogen')
            parsed_crystal = prody.parsePDB(input_crystal_path).select('not hydrogen')
            parsed_rec = prody.parsePDB(input_rec_path).select('not hydrogen')

            cry_atom_num = parsed_crystal.numAtoms()
            lig_atom_num = parsed_docked.numAtoms()

            assert cry_atom_num == lig_atom_num

            docked_coords = parsed_docked.getCoordsets()
            crystal_coord = parsed_crystal.getCoords()
            rec_coord = parsed_rec.getCoords()

            exp_crystal_coord = np.expand_dims(crystal_coord, -2)
            cry_diff = exp_crystal_coord - rec_coord
            cry_distance = np.sqrt(np.sum(np.square(cry_diff), axis=-1))

            exp_docked_coords = np.expand_dims(docked_coords, -2)
            docked_diff = exp_docked_coords - rec_coord
            docked_distance = np.sqrt(np.sum(np.square(docked_diff),axis=-1))

            cry_contact = (cry_distance < distance_threshold).astype(int)
            
            num_contact = np.sum(cry_contact).astype(float)

            lig_contact = (docked_distance < distance_threshold).astype(int)

            contact_ratio = np.sum(cry_contact * lig_contact, axis=(-1,-2)) / num_contact

            records = []
            for i , nt in enumerate(contact_ratio):
                records.append(input_data + [i + 1, nt, 1, 'success'])

            db.insert(table_idx, records, bucket=bucket)
        except Exception as e:
            record = input_data + [0, 0, 0, str(e)]
            records = [record]
            db.insert(table_idx, records, bucket=bucket)


    @staticmethod
    def create(FLAGS, db):
        if FLAGS.receptor_idx is None:
            raise Exception('receptor_idx required')
        if FLAGS.crystal_idx is None:
            raise Exception('crystal_idx require')
        if FLAGS.docked_idx is None:
            raise Exception('docked_idx required')
        if FLAGS.param is None:
            raise Exception('param required')
        native_contact_param = FLAGS.param
        if not native_contact_param in config.native_contact_pm.keys():
            raise KeyError("dock param {} doesn't exists. ".format(native_contact_param) \
                           + "available options are: {}".format(', '.join(config.native_contact_pm.keys())))

        native_contact_param = config.native_contact_pm[native_contact_param]

        receptor_idx = FLAGS.receptor_idx
        receptor_folder = db.get_folder(receptor_idx)
        crystal_idx = FLAGS.crystal_idx
        crystal_folder = db.get_folder(crystal_idx)
        docked_idx = FLAGS.docked_idx
        docked_folder = db.get_folder(docked_idx)
        table_param = {
            'func':'native_contact',
            'receptor_idx': receptor_idx,
            'input_receptor_folder':'{}_{}'.format(receptor_idx, receptor_folder),
            'crystal_idx': crystal_idx,
            'input_crystal_folder':'{}_{}'.format(crystal_idx, crystal_folder),
            'docked_idx': docked_idx,
            'input_docked_folder':'{}_{}'.format(docked_idx, docked_folder),
            'depend': [receptor_idx, crystal_idx, docked_idx],
        }

        table_param.update(native_contact_param)

        return table_param

    @staticmethod
    def data(FLAGS, db, table_idx, table_param):
        rec_idx = table_param['receptor_idx']
        rec_list = db.select_from_table(rec_idx, ['receptor','chain','resnum','resname'] ,[('state','=','1')])

        cry_idx = table_param['crystal_idx']
        cry_list = db.select_from_table(cry_idx, ['receptor','chain','resnum','resname'] ,[('state','=','1')])

        doc_idx = table_param['docked_idx']
        doc_list = db.select_from_table(doc_idx, ['receptor','chain','resnum','resname'] ,[('state','=','1')])

        finished_list = db.select_from_table(table_idx, ['receptor','chain','resnum','resname'] ,[('state','=','1')])
        finished_list = map(lambda x: x[:-1], finished_list)
        failed_list = db.select_from_table(table_idx, ['receptor','chain','resnum','resname'] ,[('state','=','0')])
        failed_list = map(lambda x: x[:-1], failed_list)

        if FLAGS.retry_failed:
            rest_list = list(set(rec_list) & set(cry_list) & set(doc_list) - set(finished_list) | set(failed_list))
        else:
            rest_list = list(set(rec_list) & set(cry_list) & set(doc_list) - set(finished_list) - set(failed_list))

        return rest_list

class split_ligand(object):
    table = table_tuple(*['splited_ligand',
                     OrderedDict(
                        [
                            ('receptor','varchar(255)'),
                            ('chain','varchar(255)'),
                            ('resnum','varchar(255)'),
                            ('resname','varchar(255)'),
                            ('resid','text'),
                            ('heavy_atom','integer'),
                            ('max_size_on_axis', 'real'),
                            ('path','text'),
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

                    rel_path = os.path.join(output_folder, receptor, lig_name)

                    record = [receptor, chain, resnum, resname, resid, heavy_atom, max_size_on_axis,rel_path, 1, 'success']
                    records = [record]
                    db.insert(table_idx, records, bucket=bucket)
                except Exception as e:
                    record =  [receptor, chain, resnum, resname, 0, 0, 0, '', 0, str(e)]
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
        _, tp = db.get_table_info(download_idx)
        download_folder = tp['output_folder']
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
        download_list = db.select_from_table(download_idx, ['receptor'],[('state','=','1')])
  

        finished_list = db.select_from_table(table_idx, ['receptor','chain','resnum','resname'] ,[('state','=','1')])
        finished_list = map(lambda x:(x[0],),finished_list)
        failed_list = db.select_from_table(table_idx, ['receptor','chain','resnum','resname'] ,[('state','=','0')])
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
        total = db.count_from_table(download_idx,[('state','=','1')])
        finished = db.count_from_table(table_idx,[('state','=','1')])
        failed = db.count_from_table(table_idx,[('state','=','0')])

        
        return (total, finished, failed)

class split_receptor(object):
    table = table_tuple(*['splited_receptor',
                        OrderedDict(
                            [
                                ('receptor','varchar(255)'),
                                ('chain','varchar(255)'),
                                ('resnum','varchar(255)'),
                                ('resname','varchar(255)'),
                                ('heavy_atom','integer'),
                                ('experiment','text'),
                                ('resolution','real'),
                                ('path','text'),
                                ('state','integer'),
                                ('comment','text')
                            ]
                        ),
                        ['receptor','chain','resnum','resname']
                ])

    @staticmethod
    def action(db, bucket, table_idx, param, input_data):
        try:                                             # todo (maksym) datum = pdb_name
            if type(input_data).__name__ in ['tuple','list']:
                input_data = input_data[0]

            receptor = input_data                                                                        # todo receptor = pdb_name !!!!!
            output_folder = param['output_folder']
            output_folder = '{}_{}'.format(table_idx, output_folder)
            input_download_folder = param['input_download_folder']
            
            input_pdb_dir = os.path.join(data_dir,input_download_folder)
            input_pdb_path = os.path.join(input_pdb_dir, receptor+'.pdb')
            
            parsed_pdb = prody.parsePDB(input_pdb_path)
            parsed_header = prody.parsePDBHeader(input_pdb_path)

            
            output_rec_dir = os.path.join(data_dir, output_folder, receptor)
            _makedir(output_rec_dir)

            ligands = []
            for chem in parsed_header['chemicals']:
                chain, resnum, resname = chem.chain, chem.resnum, chem.resname
                ligands.append([chain, str(resnum), resname])
            
            for chain, resnum, resname in ligands:
                try:
                    rec = parsed_pdb.select('not (chain {} resnum {})'.format(chain, resnum))
                    rec = rec.select('not water')
                    heavy_atom = rec.select('not hydrogen').numAtoms()
                    rec_name = '_'.join([receptor, chain, resnum, resname, 'receptor']) + '.pdb'
                    prody.writePDB(os.path.join(output_rec_dir, rec_name), rec)
                    rel_path = os.path.join(output_folder, receptor, rec_name)

                    record = [receptor, chain, resnum, resname, heavy_atom, parsed_header['experiment'], parsed_header['resolution'], rel_path , 1 , 'success']
                    records = [record]
                    db.insert(table_idx, records, bucket=bucket)
                except Exception as e:
                    record = [receptor, chain, resnum, resname, 0, 0, 0, '', 0, str(e)]      # datum = failure_message
                    records = [record]
                    print(records)
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
        _, tp = db.get_table_info(download_idx)
        download_folder = tp['output_folder']
        table_param = {
            'func':'split_receptor',
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
        download_list = db.select_from_table(download_idx, ['receptor'],[('state','=','1')])
  

        finished_list = db.select_from_table(table_idx, ['receptor','chain','resnum','resname'] ,[('state','=','1')])
        finished_list = map(lambda x:(x[0],),finished_list)
        failed_list = db.select_from_table(table_idx, ['receptor','chain','resnum','resname'] ,[('state','=','0')])
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
        total = db.count_from_table(download_idx,[('state','=','1')])
        finished = db.count_from_table(table_idx,[('state','=','1')])
        failed = db.count_from_table(table_idx,[('state','=','0')])

        
        return (total, finished, failed)
   

class download(object):

    table = table_tuple(*['download',
                     OrderedDict(
                         [
                             ('receptor','varchar(255)'),
                             ('experiment','text'),
                             ('resolution','real'),
                             ('path','text'),
                             ('state','integer'),
                             ('comment','text'),
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
            rel_path = os.path.join(output_folder_name, receptor+'.pdb')
            #pdb_path = '/home/maksym/ryan/labeled_pdb/crystal_ligands/'+receptor+'/'+receptor+'.pdb'
            #print ('pdb',pdb_path)
            print (pdb_path)
            if not os.path.exists(pdb_path):
                download_address = 'https://files.rcsb.org/download/{}.pdb'.format(receptor)
                os.system('wget --no-check-certificate -P {} {}'.format(dest_dir, download_address))
            header = prody.parsePDBHeader(pdb_path)
            record = [receptor, header['experiment'], header['resolution'],rel_path, 1, 'success']
            records = [record]
            print('insert')
            db.insert(table_idx, records, bucket=bucket)
            print('finished')
        except Exception as e:
            "Exception causing non success"
            print (e)
            record = [input_data, 'unk', 0,rel_path, 0, str(e)]                      # todo maksym (unk) = failed
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

        download_list = open('/Users/Will/projects/reformat/core/DB/datasets/VDS1/data/main_pdb_target_list.txt').readline().strip().split(',')
        finished_list = db.select_from_table(table_idx, ['receptor'] ,[('state','=','1')])
        failed_list = db.select_from_table(table_idx, ['receptor'] ,[('state','=','0')])

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
        total = len(open('/Users/Will/projects/reformat/core/DB/datasets/VDS1/data/main_pdb_target_list.txt').readline().strip().split(','))
        finished = db.count_from_table(table_idx,[('state','=','1')])
        failed = db.count_from_table(table_idx,[('state','=','0')])
        return (total, finished, failed)