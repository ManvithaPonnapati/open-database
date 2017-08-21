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

class FLAGS:
    def __init__(self, base_dir):
        FLAGS.base_dir = base_dir
        FLAGS.data_dir = os.path.join(FLAGS.base_dir, 'data')
        FLAGS.download_dir = os.path.join(FLAGS.data_dir ,'download')
        FLAGS.rec_dir = os.path.join(FLAGS.data_dir, 'receptor')
        FLAGS.lig_dir = os.path.join(FLAGS.data_dir, 'ligand')
        FLAGS.reorder_dir = os.path.join(FLAGS.data_dir, 'reorder')
        FLAGS.dock_dir = os.path.join(FLAGS.data_dir,'dock')
        FLAGS.db_path = os.path.join(FLAGS.base_dir,'database.db')
    
    def download_init(self, pdb_id_path):

        d_list = open('main_pdb_target_list.txt').readline().strip().split(', ')
        d_list = d_list[:2]
        self.pdb_list = d_list

    def split_init(self, receptor,pdb_path):
        FLAGS.receptor = receptor
        FLAGS.pdb_path = pdb_path

    def reorder_init(self,receptor, resname, rec_path, lig_path):
        FLAGS.receptor = receptor
        FLAGS.resname = resname
        FLAGS.rec_path = rec_path
        FLAGS.lig_path = lig_path

    def dock_init(self,receptor, resname, rec_path, reorder_path, dock_pm):
        FLAGS.receptor = receptor
        FLAGS.resname = resname
        FLAGS.rec_path = rec_path
        FLAGS.reorder_path = reorder_path
        FLAGS.dock_pm = dock_pm


    def rmsd_init(self,receptor, resname, reorder_path, dock_path):
        FLAGS.receptor = receptor
        FLAGS.resname = resname        
        FLAGS.reorder_path = reorder_path
        FLAGS.dock_path = dock_path

    def overlap_init(self,receptor, resname, reorder_path, dock_path, clash_cutoff_A=4.0):
        FLAGS.receptor = receptor
        FLAGS.resname = resname
        FLAGS.reorder_path = reorder_path
        FLAGS.dock_path = dock_path
        FLAGS.clash_cutoff_A = clash_cutoff_A

    def native_contact_init(self,receptor, resname, rec_path, reorder_path, dock_path, distance_threshold=1.0):
        FLAGS.receptor = receptor
        FLAGS.resname = resname
        FLAGS.rec_path = rec_path
        FLAGS.reorder_path = reorder_path
        FLAGS.dock_path = dock_path



    
def download(receptor):

    receptor = receptor.strip()
    dir_path = FLAGS.download_dir

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    download_address = 'https://files.rcsb.org/download/{}.pdb'.format(receptor)
    cmd = 'wget --no-check-certificate -P {} {}'.format(dir_path, download_address)
    #print (cmd)
    os.system(cmd)   

    return [[receptor,os.path.join(dir_path,receptor+'.pdb')]]


def split(receptor, pdb_path):

    rec_dir = FLAGS.rec_dir
    lig_dir = FLAGS.lig_dir

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

        splited.append([receptor, str(resname), os.path.join(rec_dir, receptor, rec_name), os.path.join(lig_dir, receptor, lig_name)])

    return splited

def reorder(receptor, resname, rec_path, lig_path):

    
    reorder_dir = FLAGS.reorder_dir 

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

    return [[receptor, resname, rec_path, out_path]]

def dock(receptor, resname, rec_path, reorder_path):

    dock_pm = FLAGS.dock_pm 
    dock_dir = FLAGS.dock_dir 

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

    return [[receptor, resname, rec_path, reorder_path, out_path]]

def rmsd(reorder_path, dock_path):

    docked_coords = prody.parsePDB(dock_path).getCoordsets()
    crystal_coords = prody.parsePDB(reorder_path).getCoords()

    rmsd = np.sqrt(np.mean(np.sum(np.square(docked_coords - crystal_coord), axis=1), axis=-1))

    return [list(rmsd)]

def overlap(reorder_path, dock_path):

    clash_cutoff_A = FLAGS.clash_cutoff_A

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

    distance_threshold = FLAGS.distance_threshold

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

    parser = parse_bind_func[source]
    bind = parser(index_path)

    result = [[ bind.pdb_names[i].upper(),
                bind.ligand_names[i],
                float(bind.log_affinities[i]),
                float(bind.normalized_affinities[i]),
                bind.states[i],
                bind.comments[i]]
                    for i in range(len(bind.pdb_names))]

    return result