import os,sys
import prody as pr
import numpy as np


class Split_pdb_init:
    this_module = sys.modules[__name__]
    arg_types = [str]
    out_types = [str, str, int, int]
    out_names = ["lig_file", "bindsite_file", "lig_num_atoms", "bindsite_num_atoms"]

    def __init__(self,db_root,split_dir,discard_h = True):
        """
        :param db_root: string (path to the root folder of the database)
        :param split_dir: string (where to put split pdbs)
        :param discard_h: Bool T/F (discard all hydrogens for both ligand and receptor defaults to True)
        """
        download_path = os.path.join(db_root,split_dir)
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        self.db_root = db_root
        self.split_dir = split_dir
        self.discard_h = discard_h
        self.this_module.split_pdb_init = self


def split_pdb(pdb_file, cuttoff_dist = 8, min_rec_atoms=10,
              min_lig_atoms = 5, init="split_pdb_init"):
    """ Iterates through every ligand molecule in the crystal structure (frequently there are a few). For each ligand
    selects and crops its binding site (any atom of Protein/DNA/Cofactor within the cutoff distance). Saves pairs of
    files: ligand + this ligand's binding site.

    :param pdb_file: string (relative path the the file to split)
    :param cuttoff_dist: float (distance of any atoms in the binding site from any atom of the ligand to be saved)
    :param min_rec_atoms: minimun number of atoms be saved as binding site
    :param min_lig_atoms: minumum number of atoms for ligand to be saved
    :param init: string (init function in this module)
    :return: nested list of pairs of file names of dimensions [num_pairs x [string,string,int,int]] or
    [num_pairs x [lig_file,bindsite_file,lig_num_atoms,bindsite_num_atoms]]
    """

    #FIXME: there is a bug with selection -- more stuff is selected

    init = eval(init)
    pdb_path = os.path.join(init.db_root,pdb_file)
    # parse PDB file
    pr_pdb = pr.parsePDB(pdb_path)
    assert pr_pdb.numAtoms() > (min_lig_atoms+min_rec_atoms), "the crystal structure only has"+str(pr_pdb.numAtoms())

    # parse header of the PDB file
    pr_header = pr.parsePDBHeader(pdb_path)
    pdb_id = pr_header["identifier"]
    ligs = []

    # retrieve names of the chemicals from the header of the PDB file
    for chem in pr_header['chemicals']:
        ligs.append([chem.chain, str(chem.resnum), chem.resname])
    out_filenames = []

    for lig_chain, lig_resnum, lig_resname in ligs:
        if init.discard_h:
            lig = pr_pdb.select('noh chain {} and resnum {}'.format(lig_chain, lig_resnum))
            rec = pr_pdb.select('noh and not water not (chain {} resnum {})'.format(lig_chain, lig_resnum))
        else:
            lig = pr_pdb.select('chain {} resnum {}'.format(lig_chain, lig_resnum))
            rec = pr_pdb.select('not water not (chain {} resnum {})'.format(lig_chain, lig_resnum))
        lig_coords = lig.getCoords()
        lig_atom_num = lig.numAtoms()

        # escape the loop without writing anything if the number of ligand atoms is too small
        if lig_atom_num < min_lig_atoms:
            continue

        # select residues of the binding site
        bindsite_resnums = []
        for atom_coord in lig_coords:
            around_atoms = rec.select('same residue as within {} of center'.format(cuttoff_dist), center=atom_coord)
            around_resnums = list(around_atoms.getResnums())
            bindsite_resnums = bindsite_resnums + around_resnums
        bindsite_resnums = np.unique(np.asarray(bindsite_resnums))

        # proofcheck that ligand and receptor residues do not overlap
        lig_resnums = np.unique(np.asarray(lig.getResnums()))
        assert len(np.intersect1d(lig_resnums, bindsite_resnums)) == 0, \
            "broken selection: binding site and ligand overlap"

        # select the receptor atoms to save
        prody_cmd = "resnum " + " ".join([str(resnum) for resnum in bindsite_resnums])
        binding_site = rec.select(prody_cmd)

        # write the ligand file and the receptor file
        pair_name = '_'.join([pdb_id, str(lig_chain), str(lig_resnum), str(lig_resname)])
        lig_name = pair_name + "_ligand.pdb"
        bindsite_name = pair_name + "_bindsite.pdb"
        os.makedirs(os.path.join(init.db_root, init.split_dir, pair_name))
        lig_outpath = os.path.join(init.split_dir, pair_name, lig_name)
        bindsite_outpath = os.path.join(init.split_dir, pair_name, bindsite_name)
        pr.writePDB(os.path.join(init.db_root, lig_outpath), lig)
        pr.writePDB(os.path.join(init.db_root, bindsite_outpath), binding_site)
        out_filenames.append([lig_outpath, bindsite_outpath, lig.numAtoms(), binding_site.numAtoms()])
    return out_filenames
