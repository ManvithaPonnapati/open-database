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





class FLAGS:
    def __init__(self, base_dir):

        FLAGS.base_dir = base_dir
        FLAGS.data_dir = os.path.join(FLAGS.base_dir, 'data')
        FLAGS.db_path = os.path.join(FLAGS.base_dir,'database.db')
        FLAGS.download_dir = os.path.join(FLAGS.data_dir, 'download')
        FLAGS.lig_dir = os.path.join(FLAGS.data_dir, 'ligand')
        FLAGS.rec_dir = os.path.join(FLAGS.data_dir,'receptor')
        FLAGS.conf_gen_dir = os.path.join(FLAGS.data_dir,'conf_gen')

    def download_init(self, pdb_id_path):

        d_list = open(pdb_id_path).readline().strip().split(', ')
        self.pdb_list = d_list

    def blast_init(self,receptor, pdb_path,blast_db_path, threshold=0.4):
        FLAGS.receptor = list(map(str,receptor))
        FLAGS.pdb_path = list(map(str,pdb_path))
        FLAGS.BLAST_DB = blast_db_path
        FLAGS.identity_threshold = threshold

    
    def activity_init(self, receptor, resname, target_id):
        FLAGS.receptor = list(map(str,receptor))
        FLAGS.resname = list(map(str,resname))
        FLAGS.target_id = list(map(str,target_id))

    def conf_gen_init(self, receptor, resname, mid, smile, num_conformers=10):
        FLAGS.receptor = list(map(str,receptor))
        FLAGS.resname = list(map(str,resname))
        FLAGS.mid = list(map(str,mid))
        FLAGS.smile = list(map(str, smile))
        FLAGS.num_conformers = num_conformers

def download(receptor):

    receptor = receptor.strip()
    dir_path = FLAGS.download_dir

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    download_address = 'https://files.rcsb.org/download/{}.pdb'.format(receptor)
    cmd = 'wget --no-check-certificate -P {} {}'.format(dir_path, download_address)
    #print (cmd)
    os.system(cmd)   

    return [[receptor,os.path.join(dir_path,receptor+'.pdb').replace(FLAGS.base_dir,'')]]

def blast(receptor, pdb_path):
    cdir = os.getcwd()
    tdir = tempfile.mkdtemp()
    os.chdir(tdir)

    rec_dir = FLAGS.rec_dir
    lig_dir = FLAGS.lig_dir

    pdb_path = os.path.join(FLAGS.base_dir, pdb_path.lstrip('/'))

    pdbHead = prody.parsePDBHeader(pdb_path)
    pdbFile = prody.parsePDB(pdb_path)

    ligands = []
    for chem in pdbHead['chemicals']:
        ligands.append([chem.chain, str(chem.resnum), chem.resname, chem.name])
    
    blast_result = []
    for chain, resnum, resname, name in ligands:
        
        lig_name = '_'.join([receptor,chain,resnum,resname,'ligand']) + '.pdb'
        lig_path = os.path.join(lig_dir, receptor, lig_name)
        rec_name = '_'.join([receptor, chain, resnum, resname, 'receptor']) + '.pdb'
        rec_path = os.path.join(rec_dir, receptor, rec_name)

        rec = pdbFile.select('not (chain {} resnum {})'.format(chain, resnum))
        ligand = pdbFile.select('chain {} resnum {}'.format(chain, resnum))
        if ligand is None:
            continue

        heavy_lig = ligand.select('not hydrogen')
        heavy_atom = heavy_lig.numAtoms()
        heavy_coord =heavy_lig.getCoords()        


        cen_ligand = prody.calcCenter(heavy_lig)

        res_coll = []

        sequence = ''
        i = 4
        while len(sequence)< 100:

            for center in heavy_coord:
                around_atoms = rec.select('same residue as within {} of center'.format(i), center=center)
                if around_atoms is None:
                    continue
                res_coll.append(around_atoms)
                #res_indices = around_atoms.getResindices()
                #print(around_atoms.getHierView()['A'].getSequence())
                #print (res_indices)
                #res_coll = res_coll | set(res_indices)
            resindices = reduce(lambda x,y: x|y, res_coll)
            sequence = resindices.getHierView()['A'].getSequence()
            print('sequence', i,len(sequence), sequence)
            i +=1


        with open('sequence.fasta','w') as fout:
            fout.write(">receptor\n" + sequence + '\n')

        cmd = 'blastp -db {} -query sequence.fasta -outfmt 5 -out result'.format(FLAGS.BLAST_DB)
        #print(os.getcwd())
    
        cl = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        cl.wait()

        #print(os.listdir(os.getcwd()))

        dtree = xml.dom.minidom.parse("result")
        collection = dtree.documentElement
        hits = collection.getElementsByTagName("Hit")

        hit_result = []
       
        for hit in hits:
            target_id = hit.getElementsByTagName('Hit_id')[0].childNodes[0].data
            hsps = hit.getElementsByTagName('Hit_hsps')[0]
            identity = hsps.getElementsByTagName('Hsp_identity')[0].childNodes[0].data
            align_len = hsps.getElementsByTagName('Hsp_align-len')[0].childNodes[0].data
            qseq = hsps.getElementsByTagName('Hsp_qseq')[0].childNodes[0].data
            hseq = hsps.getElementsByTagName('Hsp_hseq')[0].childNodes[0].data
            midline = hsps.getElementsByTagName('Hsp_midline')[0].childNodes[0].data
            identity_perc = float(identity)/float(align_len)
            if identity_perc > FLAGS.identity_threshold:

                if not os.path.exists(os.path.join(lig_dir,receptor)):
                    os.makedirs(os.path.join(lig_dir,receptor))
                prody.writePDB(os.path.join(lig_dir, lig_name), heavy_lig)  

                if not os.path.exists(os.path.join(rec_dir,receptor)):
                    os.makedirs(os.path.join(rec_dir,receptor))
                prody.writePDB(os.path.join(rec_dir, rec_name), rec)  


                blast_result.append([receptor,resname, target_id, identity_perc, rec_path.replace(FLAGS.base_dir,''), lig_path.replace(FLAGS.base_dir,'') ,sequence])

    return blast_result

def activity(receptor,resname, target_id):
    from chembl_webresource_client.new_client import new_client
    activities = new_client.activity

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
        activity_records.append([receptor,resname, target_id, aid, mid, smile, measure, op, value, unit])


    return activity_records



def conf_gen(receptor, resname, mid, smile):
    mol_name = '_'.join([receptor, resname, mid,'.sdf'])
    mol_file = os.path.join(FLAGS.conf_gen_dir,'mol',receptor, mol_name)

    pdb_name = mol_name.replace('.sdf','.pdb')
    pdb_file = os.path.join(FLAGS.conf_gen_dir,'pdb',receptor, pdb_name)



    if not os.path.exists(os.path.dirname(mol_file)):
        os.makedirs(os.path.dirname(mol_file))

    if not os.path.exists(os.path.dirname(pdb_file)):
        os.makedirs(os.path.dirname(pdb_file))

	# write the mol to a mol file for future use

    mol =  Chem.MolFromSmiles(smile)
    writer = SDWriter(mol_file)
    writer.write(mol)

	# generate conformers and get the number of atoms of the molecule
    mol2 = Chem.AddHs(mol)
    conf_ids = AllChem.EmbedMultipleConfs(mol2, FLAGS.num_conformers)
    for cid in conf_ids:
        AllChem.MMFFOptimizeMolecule(mol2, confId=cid)
    mol = Chem.RemoveHs(mol2)
    num_atoms = Mol.GetNumAtoms(mol)

    # write the mol into PDB format (contains mols)
    pdb_writer = PDBWriter(pdb_file)
    pdb_writer.write(mol)

    print('Generated conformers for one ligand')
    return [[pdb_file, mol_file, num_atoms]]