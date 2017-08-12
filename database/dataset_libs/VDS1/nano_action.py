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
from chembl_webresource_client.new_client import new_client
activities = new_client.activity

BLASTDB = '/Users/Will/projects/reformat/uptodate/core/database/datasets/BS1/blastdb/chembl_23_blast.fa'

def _makedir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download(pdb_id,dir_path):

    pdb_id = pdb_id.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    download_address = 'https://files.rcsb.org/download/{}.pdb'.format(pdb_id)
    cmd = 'wget --no-check-certificate -P {} {}'.format(dir_path, download_address)
    print (cmd)
    os.system(cmd)

    return [[os.path.join(dir_path,pdb_id+'.pdb')]]
    

def split(pdb_path, rec_out_dir, lig_out_dir):


    parsed_pdb = prody.parsePDB(pdb_path)
    parsed_header = prody.parsePDBHeader(pdb_path)

    ligands = []
    for chem in parsed_header['chemicals']:
        ligands.append([chem.chain, str(chem.resnum), chem.resname])

    splited = []

    for chain, resnum, resname in ligands:

        lig = parsed_pdb.select('chain {} resnum {}'.format(chain, resnum))
        rec = parsed_pdb.select('not (chaint {} resnum {}'.format(chain, resnum))
        if lig is None:
            continue
        resid = lig.getHierView().iterResidues().next().getResindex()
        resid = str(resid)
        heavy_lig = lig.select('not hydrogen')
        heavy_atom = heavy_lig.numAtoms()
        heavy_coord =heavy_lig.getCoords()
        #max_size_on_axis = max(heavy_coord.max(axis=0) - heavy_coord.min(axis=0))
        #Changing max_size_on_axis to max pairwise distance between coords
        max_size_on_axis = max(scipy.spatial.distance.pdist(heavy_coord).tolist())
        lig_name = '_'.join([receptor,chain,resnum,resname,'ligand']) + '.pdb'
        if not os.path.exists(os.path.join(lig_out_dir,receptor)):
            os.makedirs(os.path.join(lig_out_dir,receptor))
        prody.writePDB(os.path.join(lig_out_dir,receptor, lig_name), lig)

        rec_name = '_'.join([receptor, chain, resnum, resname, 'receptor']) + '.pdb'
        if not os.path.exists(os.path.join(rec_out_dir,receptor)):
            os.makedirs(os.path.join(rec_out_dir,receptor))
        prody.writePDB(os.path.join(rec_out_dir,receptor, rec_name), rec)

        splited.append([os.path.join(rec_out_dir,receptor, rec_name),os.path.join(lig_out_dir,receptor, lig_name)])


    return splited


def reorder(rec_path, lig_path, reorder_out_dir):

    reo_name = os.path.basename(rec_path).replace('receptor','reorder')
    receptor = os.path.basename(os.path.dirname(rec_path))
    out_path = os.path.join(reorder_out_dir, receptor, reo_name)
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

    return [[rec_path, out_path]]

def dock(rec_path, reorder_path, dock_out_dir):

    dock_name = os.path.basename(rec_path).replace('receptor','dock')
    receptor = os.path.basename(os.path.dirname(rec_path))
    out_path = os.path.join(dock_out_dir, receptor, dock_name)
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

    return [[rec_path, reorder_path, out_path]]

def rmsd(reorder_path, dock_path):

    docked_coords = prody.parsePDB(dock_path).getCoordsets()
    crystal_coords = prody.parsePDB(reorder_path).getCoords()

    rmsd = np.sqrt(np.mean(np.sum(np.square(docked_coords - crystal_coord), axis=1), axis=-1))

    return [list(rmsd)]

def overlap(reorder_path, dock_path):

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