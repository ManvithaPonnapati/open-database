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
    

def blast(pdb_path):

    cdir = os.getcwd()
    tdir = tempfile.mkdtemp()
    os.chdir(tdir)

    receptor = os.path.basename(os.path.splitext(pdb_path)[0])

 
    pdbHead = prody.parsePDBHeader(pdb_path)
    pdbFile = prody.parsePDB(pdb_path)

    ligands = []
    for chem in pdbHead['chemicals']:
        ligands.append([chem.chain, str(chem.resnum), chem.resname, chem.name])
    
    blast_result = []
    for chain, resnum, resname, name in ligands:
        
        rec = pdbFile.select('not (chain {} resnum {})'.format(chain, resnum))
        ligand = pdbFile.select('chain {} resnum {}'.format(chain, resnum))

        cen_ligand = prody.calcCenter(ligand)

        res_coll = []
        ligCoords = ligand.getCoords()
        print('lig_size', len(ligCoords))
        for center in ligCoords:
            around_atoms = rec.select('same residue as within 6 of center', center=center)
            if around_atoms is None:
                continue
            res_coll.append(around_atoms)
            #res_indices = around_atoms.getResindices()
            #print(around_atoms.getHierView()['A'].getSequence())
            #print (res_indices)
            #res_coll = res_coll | set(res_indices)
        resindices = reduce(lambda x,y: x|y, res_coll)
        sequence = resindices.getHierView()['A'].getSequence()
        print('sequence', sequence)
        

   

        with open('sequence.fasta','w') as fout:
            fout.write(">receptor\n" + sequence + '\n')

        cmd = 'blastp -db {} -query sequence.fasta -outfmt 5 -out result'.format(BLASTDB)
        #print(os.getcwd())
    
        cl = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        cl.wait()

        #print(os.listdir(os.getcwd()))

        dtree = xml.dom.minidom.parse("result")
        collection = dtree.documentElement
        hits = collection.getElementsByTagName("Hit")

        hit_result = []
        
        print ('hits',len(hits))
        for hit in hits:
            hit_id = hit.getElementsByTagName('Hit_id')[0].childNodes[0].data
            hsps = hit.getElementsByTagName('Hit_hsps')[0]
            identity = hsps.getElementsByTagName('Hsp_identity')[0].childNodes[0].data
            align_len = hsps.getElementsByTagName('Hsp_align-len')[0].childNodes[0].data
            ident =  float(identity)/float(align_len)
            print(ident)
            if ident >= 0.7:
                hit_result.append([hit_id, ident])

        for result in hit_result:
            target_id = result[0]
            res = activities.filter(target_chembl_id=target_id, pchembl_value__isnull=False)

            res_size = len(res)
            print (res_size)
            for i in range(res_size):
                        result = res[i]
                        aid = result['assay_chembl_id']
                        smile= result['canonical_smiles']
                        mid = result['molecule_chembl_id']
                        measure = result['published_type']
                        op = result['published_relation']
                        value = result['published_value']
                        unit = result['standard_units']

                        blast_result.append([receptor, chain, resnum, aid, mid, target_id, smile, measure, op, value, unit])


        

    #print (len(blast_result))
    #print (blast_result)
    return blast_result
            
