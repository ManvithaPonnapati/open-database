# action for nano db

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
import tempfile
import xml.dom.minidom
import config
from smina_param import smina_param
from parse_bind_affinity import parse_bind_func
from atom_dict import atom_dictionary

BLASTDB = '/Users/Will/projects/reformat/uptodate/core/database/datasets/BS1/blastdb/chembl_23_blast.fa'

def _makedir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download(receptor,dir_path):
    """
    download receptor to dir_path

    args:
        receptor:: str
            4 letters pdb id
        dir_path:: str
            dir for output

    returns:
        receptor:: str
            4 letters pdb id
        pdb_path:: str
            path of download pdb file
    """

    receptor = receptor.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    download_address = 'https://files.rcsb.org/download/{}.pdb'.format(receptor)
    cmd = 'wget --no-check-certificate -P {} {}'.format(dir_path, download_address)
    print (cmd)
    os.system(cmd)

    return [['"'+receptor+'"' ,'"'+os.path.join(dir_path,receptor+'.pdb')+'"']]
    

def split(receptor, pdb_path, rec_dir, lig_dir):
    """
    split pdb into receptor and ligand

    args:
        receptor:: str
            4 letters pdb id

        pdb_path:: str
            path of download pdb file

        rec_dir:: str
            dir for output

        lig_dir:: str
            dir for output

    returns:
        receptor:: str
            4 letters pdb id

        resname:: str
            res id  

        rec_path:: str
            path of splited receptor

        lig_path:: str
            path of splited ligand      
    """

    parsed_pdb = prody.parsePDB(pdb_path)
    parsed_header = prody.parsePDBHeader(pdb_path)

    ligands = []
    for chem in parsed_header['chemicals']:
        ligands.append([chem.chain, str(chem.resnum), chem.resname])

    splited = []

    for chain, resnum, resname in ligands:

        lig = parsed_pdb.select('chain {} resnum {}'.format(chain, resnum))
        rec = parsed_pdb.select('not (chain {} resnum {})'.format(chain, resnum))
        if lig is None:
            continue
        resid = lig.getHierView().iterResidues().next().getResindex()
        resid = str(resid)
        heavy_lig = lig.select('not hydrogen')
        heavy_atom = heavy_lig.numAtoms()
        heavy_coord =heavy_lig.getCoords()
        #max_size_on_axis = max(heavy_coord.max(axis=0) - heavy_coord.min(axis=0))
        #Changing max_size_on_axis to max pairwise distance between coords
        #max_size_on_axis = max(scipy.spatial.distance.pdist(heavy_coord).tolist())
        lig_name = '_'.join([receptor,chain,resnum,resname,'ligand']) + '.pdb'
        if not os.path.exists(os.path.join(lig_dir,receptor)):
            os.makedirs(os.path.join(lig_dir,receptor))
        prody.writePDB(os.path.join(lig_dir,receptor, lig_name), lig)

        rec_name = '_'.join([receptor, chain, resnum, resname, 'receptor']) + '.pdb'
        if not os.path.exists(os.path.join(rec_dir,receptor)):
            os.makedirs(os.path.join(rec_dir,receptor))
        prody.writePDB(os.path.join(rec_dir,receptor, rec_name), rec)

        splited.append(['"'+receptor+'"','"'+str(resname)+'"','"'+os.path.join(rec_dir,receptor, rec_name)+'"','"'+os.path.join(lig_dir,receptor, lig_name)+'"'])


    return splited


def reorder(receptor, resname, rec_path, lig_path, reorder_dir):
    """
    reorder atom in ligand 

    args:
        receptor:: str
            4 letters pdb id

        resname:: str
            res id  

        rec_path:: str
            path of splited receptor

        lig_path:: str
            path of splited ligand   

        reorder_dir:: str
            dir for output file

    returns:
        receptor:: str
            4 letters pdb id

        resname:: str
            res id  

        rec_path:: str
            path of splited receptor

        reorder_path:: str
            path of reorder ligand           
                        

    """

    reo_name = os.path.basename(rec_path).replace('receptor','reorder')
    receptor = os.path.basename(os.path.dirname(rec_path))
    out_path = os.path.join(reorder_dir, receptor, reo_name)

    smina_pm = smina_param()
    smina_pm.param_load(config.dock_pm['reorder'])
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
    
    result =  [list(map(lambda x:'"'+str(x)+'"',[receptor, resname, rec_path, out_path]))]
    print (result)
    return result

def dock(receptor, resname, rec_path, reorder_path, dock_pm, dock_dir):
    """
    Smina docking

    args:
        receptor:: str
            4 letters pdb id

        resname:: str
            res id  

        rec_path:: str
            path of splited receptor

        reorder_path:: str
            path of reorder ligand   

        dock_pm:: str
            docking parameter

        dock_dir:: str
            dir for output 

    
    returns:
        receptor:: str
            4 letters pdb id

        resname:: str
            res id  

        rec_path:: str
            path of splited receptor

        reorder_path:: str
            path of reorder ligand   

        dock_path:: str
            path of docking result
 
    """
    dock_name = os.path.basename(rec_path).replace('receptor','dock')
    receptor = os.path.basename(os.path.dirname(rec_path))
    out_path = os.path.join(dock_dir, receptor, dock_name)

    smina_pm = smina_param()
    smina_pm.param_load(config.dock_pm[dock_pm])

    if not os.path.exists(os.path.dirname(out_path)):
        os.makedirs(os.path.dirname(out_path))

    kw = {
        'receptor': rec_path,
        'ligand': reorder_path,
        'autobox_ligand':reorder_path,
        'out':out_path
    }       

    cmd = smina_pm.make_command(**kw)
    cl = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    cl.wait()

    return [list(map(lambda x:'"'+str(x)+'"',[receptor, resname, rec_path, reorder_path, out_path]))]

def rmsd(reorder_path, dock_path):
    """
    calculate rmsd of ligand

    args:
        reorder_path:: str
            path of reorder ligand

        dock_path:: str
            path of docking result
        
    returns:
        rmsd:: float
            rmsd value
    """
    docked_coords = prody.parsePDB(dock_path).getCoordsets()
    crystal_coords = prody.parsePDB(reorder_path).getCoords()

    rmsd = np.sqrt(np.mean(np.sum(np.square(docked_coords - crystal_coord), axis=1), axis=-1))

    return [list(rmsd)]

def overlap(reorder_path, dock_path):
    """
    calculate overlap for the docking result

    args:
        reorder_path:: str
            path of reorder ligand

        dock_path:: str
            path of docking result
        
    returns:
        overlap:: float
            overlap value
    """
    docked_coords = prody.parsePDB(dock_path).getCoordsets()
    crystal_coords = prody.parsePDB(reorder_path).getCoords()

    expanded_docked = np.expand_dims(docked_coords, -2)
    diff = expanded_docked - crystal_coords
    distance = np.sqrt(np.sum(np.power(diff, 2), axis=-1))   

    all_clash = (distance < clash_cutoff_A).astype(float)  
    atom_clash = (np.sum(all_clash, axis=-1) > 0).astype(float) 
    position_clash_ratio = np.mean(atom_clash, axis=-1) 

    return [list(position_clash_ratio)]

def native_contact(rec_path, reorder_path, dock_path):
    """
    calculate native contact ratio for the docking result

    args:
        rec_path:: str
            path of splited receptor

        reorder_path:: str
            path of reorder ligand

        dock_path:: str
            path of docking result
        
    returns:
        native_contact:: float
            native contact value
    """
    parsed_docked =  prody.parsePDB(dock_path).select('not hydrogen')
    parsed_crystal = prody.parsePDB(reorder_path).select('not hydrogen')
    parsed_rec = prody.parsePDB(rec_path).select('not hydrogen')


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

    return [list(contact_ratio)]

def binding_affinity(index_path, source):
    """
    parser binding affinity info

    args:
        index_path:: str
            path of the file for binding affinity info

        sourde:: str
            type of index_path [bindingdb, bindingmoad, pdbbind]

    """
    parser = parse_bind_func[source]
    bind = parser(index_path)
    
    result = [['"'+bind.pdb_names[i].upper()+'"', 
               '"'+bind.ligand_names[i]+'"',
               float(bind.log_affinities[i]), 
               float(bind.normalized_affinities[i]),
               bind.states[i], 
               '"'+bind.comments[i]+'"']
                 for i in range(len(bind.pdb_names))]

    return result


def retrieve_tfr(receptor, resname, rec_path, reorder_path, dock_path, norm_affinity, tfr_dir):
    """

    convert the pdb into tensorflwo record


    args:
        receptor:: str
            4 letters pdb id

        resname:: str
            res id  

        rec_path:: str
            path of splited receptor

        reorder_path:: str
            path of reorder ligand   

        dock_path:: str
            path of docking result

        norm_affinity:: float
            normalized affinity value

        tfr_dir:: str
            dir for output

    returns:
        tfr_path:: str
            path of output tensorflow record file    
    """
    import prody
    import tensorflow as tf 

    tfr_name = '_'.join(os.path.basename(os.path.splitext(rec_path)[0]).split('_')[:-1])+'.tfr'
    tfr_path = os.path.join(tfr_dir, receptor, tfr_name)
    if not os.path.exists(os.path.dirname(tfr_path)):
        os.makedirs(os.path.dirname(tfr_path))

    dock_scores = []
    with open(dock_path) as fin:
        for line in fin:
            if line.startswith('REMARK minimizedAffinity'):
                dock_scores.append(float(line.strip().split(' ')[-1]))
    dock_scores = np.asarray(dock_scores)


    rec = prody.parsePDB(rec_path)
    lig = prody.parsePDB(reorder_path)
    doc = prody.parse(dock_path)

    rec_coord = rec.getCoords()
    rec_elements = rec.getElements()
    rec_elements = np.asarray(map(lambda x:atom_dictionary.ATM[x.lower()], rec_elements))
    
   
    lig_coord = lig.getCoords()
    lig_elements = lig.getElements()
    lig_elements = np.asarray(map(lambda x:atom_dictionary.ATM[x.lower()], lig_elements))

    doc_coords = doc.getCoordsets()
    doc_elements = doc.getElements()

    lig_coord = np.reshape(lig_coord,[-1])
    dock_coords = np.reshape(dock_coords,[-1])
    rec_coord = np.reshape(rec_coord,[-1])

    writer = tf.python_io.TFRecordWriter(filename)
    example = tf.train.Example(
        features=tf.train.Features(
            feature={
                'norm_affinity': tf.train.Feature(float_list=tf.train.FloatList(value=norm_affinity)),
                'dock_scores': tf.train.Feature(float_list=tf.train.FloatList(value=dock_scores)),
                'lig_elem': tf.train.Feature(int64_list=tf.train.Int64List(value=lig_elem)),
                'lig_coord': tf.train.Feature(float_list=tf.train.FloatList(value=lig_coord)),
                'dock_coords': tf.train.Feature(float_list=tf.train.FloatList(value=dock_coords)),
                'rec_elem': tf.train.Feature(int64_list=tf.train.Int64List(value=rec_elem)),
                'rec_coord': tf.train.Feature(float_list=tf.train.FloatList(value=rec_coord))
            }
        )
    )
    serialized = example.SerializeToString()
    writer.write(serialized)
    writer.close()

    return ['"'+tfr_path+'"']