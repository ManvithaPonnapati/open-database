import os,time,sys
import scipy as scp
import prody as pr
from config import FLAGS



class Download_pdb_init:
    this_module = sys.modules[__name__]
    def __init__(self,db_path,download_dir):
        download_path = os.path.join(db_path,download_dir)
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        self.db_path = db_path
        self.download_dir = download_dir
        self.this_module.download_init = self


def download_pdb(pdb_id,init="download_init"):
    """

    :param pdb_id:
    :param dir_path:
    :return:
    """
    init = eval(init)
    download_link = 'https://files.rcsb.org/download/{}.pdb'.format(pdb_id)
    download_path = os.path.join(init.db_path,init.download_dir)
    cmd = 'wget --no-check-certificate -P {} {}'.format(download_path, download_link)
    os.system(cmd)
    output_file = init.download_dir + "/" + download_link.split("/")[-1]
    return [[output_file]]



# def split(pdb_path, rec_out_dir, lig_out_dir):
#     # FIXME: discard hydrogens = True
#
#     parsed_pdb = pr.parsePDB(pdb_path)
#     parsed_header = pr.parsePDBHeader(pdb_path)
#
#     ligands = []
#     for chem in parsed_header['chemicals']:
#         ligands.append([chem.chain, str(chem.resnum), chem.resname])
#
#     splited = []
#
#     for chain, resnum, resname in ligands:
#
#         lig = parsed_pdb.select('chain {} resnum {}'.format(chain, resnum))
#         rec = parsed_pdb.select('not (chaint {} resnum {}'.format(chain, resnum))
#
#

#        if lig is None:
#            continue
#        resid = lig.getHierView().iterResidues().next().getResindex()
#        resid = str(resid)
#        heavy_lig = lig.select('not hydrogen')
#        heavy_atom = heavy_lig.numAtoms()
#        heavy_coord =heavy_lig.getCoords()
#        #max_size_on_axis = max(heavy_coord.max(axis=0) - heavy_coord.min(axis=0))
#        #Changing max_size_on_axis to max pairwise distance between coords
#        max_size_on_axis = max(scp.spatial.distance.pdist(heavy_coord).tolist())
#        lig_name = '_'.join([receptor,chain,resnum,resname,'ligand']) + '.pdb'
#        if not os.path.exists(os.path.join(lig_out_dir,receptor)):
#            os.makedirs(os.path.join(lig_out_dir,receptor))
#        pr.writePDB(os.path.join(lig_out_dir,receptor, lig_name), lig)
#        rec_name = '_'.join([receptor, chain, resnum, resname, 'receptor']) + '.pdb'
#       if not os.path.exists(os.path.join(rec_out_dir,receptor)):
#            os.makedirs(os.path.join(rec_out_dir,receptor))
#        pr.writePDB(os.path.join(rec_out_dir,receptor, rec_name), rec)
#
# #        splited.append([os.path.join(rec_out_dir,receptor, rec_name),os.path.join(lig_out_dir,receptor, lig_name)])
#
#     return splited
