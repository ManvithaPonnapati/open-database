# operation for Binding Site datasest
import os 
import sys
import re 
import time 
import subprocess 
from functools import partial 
from glob import glob
import scipy 
import numpy as np 
import prody  as pr 
import tempfile
import xml.dom.minidom



class Download_pdb_init:
    this_module = sys.modules[__name__]
    def __init__(self, data_dir, download_folder):
        download_dir = os.path.join(data_dir, download_folder)
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        self.data_dir = data_dir
        self.download_folder = download_folder
        self.this_module.download_pdb_init = self


def download_pdb(receptor, init='download_pdb_init'):

    init = eval(init)
    download_link = 'https://files.rcsb.org/download/{}.pdb'.format(receptor)
    download_path = os.path.join(init.data_dir,init.download_folder)
    cmd = 'wget --no-check-certificate -P {} {}'.format(download_path, download_link)
    os.system(cmd)
    output_file = os.path.join(init.download_folder, receptor+'.pdb')
    return [[output_file]]


class Split_pdb_init:
    this_module = sys.modules[__name__]
    def __init__(self, data_dir, split_folder):
        split_dir = os.path.join(data_dir, split_folder)
        if not os.path.exists(split_dir):
            os.makedirs(split_dir)

        self.data_dir = data_dir
        self.split_folder = split_folder 
        self.this_module.split_pdb_init = self 

def split_pdb(pdb_outpath, cutoff_dist = None, discard_h = True, init='split_pdb_init'):

    init  = eval(init)
    pdb_path = os.path.join(init.data_dir, pdb_outpath)

    pr_pdb = pr.parsePDB(pdb_path)
    pr_header = pr.parsePDBHeader(pdb_path)
    pdb_id = pr_header['identifier']
    ligs = []

    for chem in pr_header['chemicals']:
        ligs.append([chem.chain, str(chem.resnum), chem.resname])

    out_filenames = []
    for chain, resnum, resname in ligs:
        if discard_h:
            lig = pr_pdb.select('noh chain {} and resnum {}'.format(chain, resnum))
            rec = pr_pdb.select('noh and not water not (chain {} resnum {})'.format(chain, resnum))
        else:
            lig = pr_pdb.select('chain{} resnum {}'.format(chain, resnum))
            rec = pr_pdb.select('not water not (chain {} resnum {})'.format(chain, resnum))

        pair_name = '_'.join([pdb_id, chain, resnum, resname])
        lig_name = pair_name + '_ligand.pdb'
        rec_name = pair_name + '_receptor.pdb'
        split_dir = os.path.join(init.data_dir, init.split_folder, pair_name)
        if not os.path.exists(split_dir):
            os.makedirs(split_dir)

        lig_outpath = os.path.join(init.split_folder, pair_name, lig_name)
        rec_outpath = os.path.join(init.split_folder, pair_name, rec_name)

        pr.writePDB(os.path.join(init.data_dir, lig_outpath), lig)
        pr.writePDB(os.path.join(init.data_dir, rec_outpath), rec)
        out_filenames.append([rec_outpath, lig_outpath])

    return out_filenames

class Blast_init:
    this_module = sys.modules[__name__]
    def __init__(self, data_dir, blast_db):
        self.data_dir = data_dir 
        self.blast_db = blast_db
        self.this_module.blast_init = self 

def blast(rec_outpath, lig_outpath,min_qseq_len = 100, init = 'blast_init'):

    
    cdir = os.getcwd()
    tdir = tempfile.mkdtemp()
    os.chdir(tdir)

    pair_name = '_'.join(os.path.basename(rec_outpath).split('_')[:-1])

    init = eval(init)
    rec_path = os.path.join(init.data_dir, rec_outpath)
    lig_path = os.path.join(init.data_dir, lig_outpath)

    pr_rec = pr.parsePDB(rec_path)
    pr_lig = pr.parsePDB(lig_path)

    rec_size = pr_rec.numAtoms()
    lig_coords = pr_lig.getCoords()

    if rec_size < min_qseq_len:
        raise Exception("Receptor's seq len {} smaller than the smallest qurey seq len {}".format(rec_size, min_qseq_len))

    sequence = ''
    r = 4 
    while len(sequence) < min_qseq_len:
        res_coll = []
        for center in lig_coords:
            around_atoms = pr_rec.select('same residue as within {} of center'.format(r), center = center)
            if around_atoms is None:
                continue
            res_coll.append(around_atoms)

        resindices = reduce(lambda x,y : x|y, res_coll)
        sequence = resindices.getHierView()['A'].getSequence()
        print('sequence ', r, len(sequence))
        r +=1 

    with open('sequence.fasta','w') as fout: fout.write(">receptor\n" + sequence + '\n')

    cmd = 'blastp -db {} -query sequence.fasta -outfmt 5 -out result'.format(init.blast_db)

    cl = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    cl.wait()

    dtree = xml.dom.minidom.parse("result")
    collection = dtree.documentElement
    hits = collection.getElementsByTagName("Hit")

    hit_result = []

    for hit in hits:
        hit_id = hit.getElementsByTagName('Hit_id')[0].childNodes[0].data
        hsps = hit.getElementsByTagName('Hit_hsps')[0]
        identity = hsps.getElementsByTagName('Hsp_identity')[0].childNodes[0].data
        align_len = hsps.getElementsByTagName('Hsp_align-len')[0].childNodes[0].data
        qseq = hsps.getElementsByTagName('Hsp_qseq')[0].childNodes[0].data
        hseq = hsps.getElementsByTagName('Hsp_hseq')[0].childNodes[0].data
        midline = hsps.getElementsByTagName('Hsp_midline')[0].childNodes[0].data

        hit_result.append([pair_name, hit_id, float(identity)/float(align_len), sequence])

    return hit_result 


class Activity_init:
    this_module = sys.modules[__name__]
    def __init__(self, data_dir, activity_folder):
        activity_dir = os.path.join(data_dir, activity_folder)
        if not os.path.exists(activity_dir):
            os.makedirs(activity_dir)

        self.data_dir = data_dir 
        self.activity_folder = activity_folder 
        self.this_module.activity_init = self 
    

def activity(pair_name, target_id, init='activity_init'):
    from chembl_webresource_client.new_client import new_client
    activities = new_client.activity

    init = eval(init)

    res = activities.filter(target_chembl_id=target_id, pchembl_value__isnull=False)



    res_size = len(res)
    #print (res_size)
    activity_records = []
    for i in range(res_size):
        result = res[i]
        aid = str(result['assay_chembl_id'])
        smile= str(result['canonical_smiles'])
        mid = str(result['molecule_chembl_id'])
        measure = str(result['published_type'])
        op = str(result['published_relation'])
        value = float(result['published_value'])
        unit = str(result['standard_units'])
        activity_records.append([pair_name, target_id, aid, mid, smile, measure, op, value, unit])


    return activity_records


class Conf_gen_init:
    this_module = sys.modules[__name__]
    def __init__(self, data_dir,  conf_dir):
        self.conf_dir = conf_dir 
        self.data_dir = data_dir 
        self.this_module.conf_gen_init = self 

def conf_gen(pair_name, mid, smile, init = 'conf_gen_init'):


    init = eval(init)
    mol_name = '_'.join([pair_name, mid+'.sdf'])
    mol_dir = os.path.join(init.data_dir, init.conf_dir, 'mol',pairname)
    if not os.path.exists(mol_dir):
        os.makedirs(mol_dir)
    mol_path = os.path.join(mol_dirr, mol_name)

    pdb_name = '_'.join([pair_name, mid+'.pdb'])
    pdb_dir = os.path.join(init.data_dir, init.conf_dir,'pdb',pair_name)
    if not os.path.exists(pdb_dir):
        os.makedirs(pdb_dir)
    pdb_path = os.path.join(pdb_dir, pdb_name)


        # write the mol to a mol file for future use

    mol =  Chem.MolFromSmiles(smile)
    writer = SDWriter(mol_path)
    writer.write(mol)

        # generate conformers and get the number of atoms of the molecule
    mol2 = Chem.AddHs(mol)
    conf_ids = AllChem.EmbedMultipleConfs(mol2, FLAGS.num_conformers)
    for cid in conf_ids:
        AllChem.MMFFOptimizeMolecule(mol2, confId=cid)
    mol = Chem.RemoveHs(mol2)
    num_atoms = Mol.GetNumAtoms(mol)

    # write the mol into PDB format (contains mols)
    pdb_writer = PDBWriter(pdb_path)
    pdb_writer.write(mol)

    print('Generated conformers for one ligand')
    return [[os.path.join(init.conf_dir, 'pdb',pair_name, pdb_name), os.path.join(init.conf_dir, 'mol',pair_name, mol_name), num_atoms]]
