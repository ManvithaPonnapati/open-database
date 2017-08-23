import os,sys

class Split_pdb_init:
    this_module = sys.modules[__name__]
    def __init__(self,db_path,split_dir):
        download_path = os.path.join(db_path,split_dir)
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        self.db_path = db_path
        self.split_dir = split_dir
        self.this_module.split_pdb_init = self


def split_pdb(split_pdb, cuttoff_dist = None, discard_h = True,init="split_pdb_init"):
    """
    Iterates through every molecule of the ligand in the receptor. Crops atoms of the receptor (and any chemicals,
     but not water) within within the cutoff  distance of any atoms of the ligand. Saves ligand + binding site crop
     as pairs into folders.

    :param split_pdb: string (relative path the the file to split)
    :param cuttoff_dist: float (distance of any atoms in the binding site from any atom of the ligand to be saved)
    :param discard_h: Bool T/F (discard all hydrogens ?)
    :param init: string (init function in this module)
    :return:
    """
    init = eval(init)
    pdb_path = os.path.join(init.db_path,split_pdb)

    # parse header and coordinates from the PDB file
    pr_pdb = pr.parsePDB(pdb_path)
    pr_header = pr.parsePDBHeader(pdb_path)
    pdb_id = pr_header["identifier"]
    ligs = []

    # retrieve names of the chemicals from the header of the PDB file
    for chem in pr_header['chemicals']:
        ligs.append([chem.chain, str(chem.resnum), chem.resname])
    out_filenames = []
    for chain, resnum, resname in ligs:
        if discard_h:
            lig = pr_pdb.select('noh chain {} and resnum {}'.format(chain, resnum))
            rec = pr_pdb.select('noh and not water not (chain {} resnum {})'.format(chain, resnum))
        else:
            lig = pr_pdb.select('chain {} resnum {}'.format(chain, resnum))
            rec = pr_pdb.select('not water not (chain {} resnum {})'.format(chain, resnum))

        # write the ligand file and the receptor file
        pair_name = '_'.join([pdb_id, chain, resnum, resname])
        lig_name = pair_name + "_ligand.pdb"
        rec_name = pair_name + "_receptor.pdb"
        os.makedirs(os.path.join(init.db_path, init.split_dir, pair_name))
        lig_outpath = os.path.join(init.split_dir, pair_name, lig_name)
        rec_outpath = os.path.join(init.split_dir, pair_name, rec_name)
        pr.writePDB(os.path.join(init.db_path,lig_outpath), lig)
        pr.writePDB(os.path.join(init.db_path,rec_outpath), rec)
        out_filenames.append([lig_outpath,rec_outpath])
    return out_filenames
