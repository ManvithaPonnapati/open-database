import os,sys
import prody 
import tempfile 


import subprocess 
import xml.dom.minidom
from chembl_webresource_client.new_client import new_client
activities = new_client.activity

cdir = os.getcwd()

BLASTDB = os.path.join(cdir,'blastdb/chembl_23_blast.fa')


def blast(pdb):

    cdir = os.getcwd()
    tdir = tempfile.mkdtemp()
    os.chdir(tdir)    

    pdbHead = prody.parsePDBHeader(pdb)
    pdbFile = prody.parsePDB(pdb)

    ligands = []
    for chem in pdbHead['chemicals']:
        ligands.append([chem.chain, str(chem.resnum), chem.resname, chem.name])

    for chain, resnum, resname, name in ligands:

        receptor = pdbFile.select('not (chain {} resnum {})'.format(chain, resnum))
        ligand = pdbFile.select('chain {} resnum {}'.format(chain, resnum))

        cen_ligand = prody.calcCenter(ligand)
        around_atoms = receptor.select('within 20 of center', center=cen_ligand)
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
            
            print('bit_score {}'.format(bit_score))
            print('score {}'.format(score))
            print('evalue {}'.format(evalue))

            res = activities.filter(target_chembl_id=hit_id, pchembl_value__isnull=False)
            res_size = len(res)
            print (res_size)
            for i in range(res_size):
                result = res[i]
                aid = result['assay_chembl_id']
                smile= result['canonical_smiles']
                mid = result['molecule_chembl_id']
                type = result['published_type']
                op = result['published_relation']
                value = result['published_value']
                unit = result['standard_units']   

                print(smile)
                print('{} {} {} {}'.format(type, op, value, unit))  


                   
if __name__ == '__main__':
    blast('3eml')
