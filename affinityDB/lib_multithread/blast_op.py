import os,sys
import tempfile 
import prody 
import subprocess
import xml.dom.minidom

# FIXME explanations
# what is blastdb
# why is input receptor file named out_path ?

class Blast_init:
    this_module = sys.modules[__name__]
    def __init__(self, data_dir, blast_db):
        """

        :param data_dir: str:: dir for the data
        :param blast_db: str:: path of the blast database
        """
        self.data_dir = data_dir
        self.blast_db = blast_db
        self.this_module.blast_init = self 

def blast(rec_outpath, lig_outpath, init = 'blast_init'):
    """
    Applying protein sequence blast on the receptor

    :param rec_outpath: str:: relative path of receptor
    :param lig_outpath: str:: relative path of ligand
    :param init: str:: init func name
    :return: nested list:: blast result contain  pair_name with receptor id and ligand name, 
    chembl_target_id for similar sequence in database,  ideitity number as num_match/align_length and
    the sequence of selected receptor
    """
    
    cdir = os.getcwd()
    tdir = tempfile.mkdtemp()
    os.chdir(tdir)

    pair_name = '_'.join(os.path.basename(rec_outpath).split('_')[:-1])

    init = eval(init)
    rec_path = os.path.join(init.data_dir, rec_outpath)
    lig_path = os.path.join(init.data_dir, lig_outpath)

    pr_rec = prody.parsePDB(rec_path)
    pr_lig = prody.parsePDB(lig_path)

    sequence = pr_rec.getHierView()['A'].getSequence()
    
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