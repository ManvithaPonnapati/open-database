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

BLASTDB = '/core/database/dataset_libs/BS1/blastdb/chembl_23_blast.fa'



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

        sequence = ''
        i = 4
        while len(sequence)< 100:

            for center in ligCoords:
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

        cmd = 'blastp -db {} -query sequence.fasta -outfmt 5 -out result'.format(BLASTDB)
        #print(os.getcwd())
    
        cl = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        cl.wait()

        #print(os.listdir(os.getcwd()))

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

            blast_result.append([receptor, hit_id, str(identity), str(align_len), str(len(sequence)),midline, hseq, sequence])

    return blast_result

if __name__ == '__main__':
    blast('3eml')
            
