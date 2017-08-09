# database action

import os
import sys 
import re 
import time 
import subprocess 
from functools import partial 
from glob import glob 
import scipy
import numpy as np 
import prody 

sys.path.append('../..')
from db import AffinityDatabase
from db_config import data_dir
from lib.smina_param import smina_param
db = AffinityDatabase()

def _makedir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download(bucket, table_idx, param, input_data):         # todo(maksym) input_data = pdb_ids
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
    try:
        receptor = input_data[1:]                                                   # todo(maksym) pdb_id
        output_folder = param['output_folder']
        output_folder_name = '{}_{}'.format(table_idx, output_folder)
        dest_dir = os.path.join(data_dir, output_folder_name)
        _makedir(dest_dir)
        pdb_path = os.path.join(dest_dir, receptor+'.pdb')

        #pdb_path = '/home/maksym/ryan/labeled_pdb/crystal_ligands/'+receptor+'/'+receptor+'.pdb'
        #print ('pdb',pdb_path)
        if not os.path.exists(pdb_path):
            download_address = 'https://files.rcsb.org/download/{}.pdb'.format(receptor)
            os.system('wget --no-check-certificate -P {} {}'.format(dest_dir, download_address))
        header = prody.parsePDBHeader(pdb_path)
        record = [receptor, header['experiment'], header['resolution'], 1, 'success']
        records = [record]
        db.insert(table_idx, records, bucket=bucket)
    except Exception as e:
        "Exception causing non success"
        print e
        record = [input_data, 'unk', 0, 0, str(e)]                      # todo maksym (unk) = failed
        records = [record]
        db.insert(table_idx, records, bucket=bucket)


def split_ligand(bucket, table_idx, param, input_data):
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

def split_receptor(bucket,table_idx, param, datum):         # todo (maksym) param = params;
    try:                                             # todo (maksym) datum = pdb_name
        if type(datum).__name__ in ['tuple','list']:
            datum = datum[0]

        receptor = datum                                                                        # todo receptor = pdb_name !!!!!
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


                record = [receptor, chain, resnum, resname, heavy_atom, parsed_header['experiment'], parsed_header['resolution'] , 1 , 'success']
                records = [record]
                db.insert(table_idx, records, bucket=bucket)
            except Exception as e:
                record = [receptor, chain, resnum, resname, 0, 0, 0, 0, str(e)]      # datum = failure_message
                records = [record]
                print(records)
                db.insert(table_idx, records, bucket=bucket) 

    # TODO: (maksym) I believe this is controllable with logging
    except Exception as e:
        print(e)
        raise Exception(str(e))


def reorder(bucket, table_idx, param, input_data):                                                      # todo(maksym) smina_reorder
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

        cmd = smina_pm.make_command(**kw)                                       # todo(maksym) smina_cmd

        cl = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        cl.wait()
        prody.parsePDB(out_path)

        record = input_data + [1, 'success']
        records = [record]
        db.insert(table_idx, records, bucket=bucket)

    except Exception as e:
        record = input_data + [0, str(e)]
        records = [record]
        db.insert(table_idx, records, bucket=bucket)

def dock(bucket, table_idx, param, input_data):
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

        record = input_data + [1, 'success']
        records = [record]
        db.insert(table_idx, records, bucket=bucket)

    except Exception as e:
        record = input_data + [0, str(e)]
        records = [record]
        db.insert(table_idx, records, bucket=bucket)

def overlap(bucket, table_idx, param, input_data):
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

def rmsd(bucket, table_idx, param, input_data):
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





def native_contact(bucket, table_idx, param, input_data):
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

DatabaseAction={
    'download':download,
    'split_ligand':split_ligand,
    'split_receptor':split_receptor,
    'reorder':reorder,
    'smina_dock':dock,
    'overlap':overlap,
    'rmsd':rmsd,
    'native_contact':native_contact
    }
    