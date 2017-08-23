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

        :param data_dir:
        :param blast_db:
        """
        self.data_dir = data_dir
        self.blast_db = blast_db
        self.this_module.blast_init = self 

def blast(rec_file, lig_file ,min_qseq_len = 100, init = 'blast_init'):
    """

    :param rec_outpath:
    :param lig_outpath:
    :param min_qseq_len:
    :param init:
    :return:
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

    rec_size = pr_rec.numAtoms()
    lig_coords = pr_lig.getCoords()

    if rec_size < min_qseq_len:
        raise Exception("Receptor's seq len {} smaller than the smallest query seq len {}".format(rec_size, min_qseq_len))

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