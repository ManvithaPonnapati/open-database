import os,sys
import prody as pr
import numpy as np


class Split_pdb_init:
    this_module = sys.modules[__name__]
    arg_types = [str,str]
    out_types = [str,str, str, int, int]
    out_names = ["pair_id", "lig_file", "bindsite_file", "lig_num_atoms", "bindsite_num_atoms"]

    def __init__(self,db_root,split_dir, discard_h=True, cutoff_dist=10, min_rec_atoms=10, min_lig_atoms=5):
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
        self.cutoff_dist = cutoff_dist
        self.min_rec_atoms = min_rec_atoms
        self.min_lig_atoms = min_lig_atoms
        self.this_module.split_pdb_init = self


def split_pdb(uid, pdb_file, init="split_pdb_init"):
    """ Iterates through every ligand molecule in the crystal structure (frequently there are a few). For each ligand
    selects and crops its binding site (any atom of Protein/DNA/Cofactor within the cutoff distance). Saves pairs of
    files: ligand + this ligand's binding site.

    Example:
    <pre lang="python">
    split_pdb('105M','download/105M.pdb')
    </pre>

    Output:
    <pre lang="python">
    [['05M_A_155_HEM','split/105M_A_155_HEM/105M_A_155_HEM_receptor.pdb','split/105M_A_155_HEM/105M_A_155_HEM_ligand.pdb',30,100]]
    </pre>

    :param pdb_file: string (relative path the the file to split)
    :param cutoff_dist: float (distance of any atoms in the binding site from any atom of the ligand to be saved)
    :param min_rec_atoms: minimun number of atoms be saved as binding site
    :param min_lig_atoms: minumum number of atoms for ligand to be saved
    :param init: string (init function in this module)
    :return: 
    nested list of pairs of file names of dimensions [num_pairs x [string,string,int,int]] or \
    [num_pairs x [lig_file,bindsite_file,lig_num_atoms,bindsite_num_atoms]]
    """

    init = eval(init)
    pdb_path = os.path.join(init.db_root,pdb_file)
    # parse PDB file
    pr_pdb = pr.parsePDB(pdb_path)
    assert pr_pdb.numAtoms() > (init.min_lig_atoms+init.min_rec_atoms), \
        "not enough atoms in this pdb" + str(pr_pdb.numAtoms())

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
        if lig_atom_num < init.min_lig_atoms:
            continue

        # select residues of the binding site
        bindsite_Segindices = []
        bindsite_Chids = []
        bindsite_Resnums = []
        for atom_coord in lig_coords:
            around_atoms = rec.select('same residue as within {} of center'.format(init.cutoff_dist),center=atom_coord)
            bindsite_Segindices = bindsite_Segindices + list(around_atoms.getSegindices())
            bindsite_Chids = bindsite_Chids + list(around_atoms.getChids())
            bindsite_Resnums = bindsite_Resnums + list(around_atoms.getResnums())

        # select only unique atoms
        bindsite_names = [str(bindsite_Segindices[i]) + str(bindsite_Chids[i])+str(bindsite_Resnums[i])
                          for i in range(len(bindsite_Segindices))]
        bindsite_names,unq_idx = np.unique(np.asarray(bindsite_names),return_index=True)
        segindices = np.asarray(bindsite_Segindices)[unq_idx]
        chids = np.asarray(bindsite_Chids)[unq_idx]
        resnums = np.asarray(bindsite_Resnums)[unq_idx]

        # proofcheck that ligand and receptor residues do not overlap
        lig_names = np.unique(np.asarray([str(lig.getSegindices()[i]) + str(lig.getChids()[i])
                                          + str(lig.getResnums()[i]) for i in range(lig_atom_num)]))
        assert len(np.intersect1d(bindsite_names,lig_names)) == 0, "broken selection: binding site and ligand overlap"

        # select the receptor atoms to save
        bindsite_resid = len(unq_idx)
        prody_cmd = " or ".join(["(segindex {} chid {} resnum {})".format(segindices[i],chids[i],resnums[i])
                                 for i in range(bindsite_resid)])
        binding_site = rec.select(prody_cmd)

        # write the ligand file and the receptor file
        pair_name = '_'.join([uid, str(lig_chain), str(lig_resnum), str(lig_resname)])
        lig_name = pair_name + "_ligand.pdb"
        bindsite_name = pair_name + "_bindsite.pdb"
        os.makedirs(os.path.join(init.db_root, init.split_dir, pair_name))
        lig_outpath = os.path.join(init.split_dir, pair_name, lig_name)
        bindsite_outpath = os.path.join(init.split_dir, pair_name, bindsite_name)
        pr.writePDB(os.path.join(init.db_root, lig_outpath), lig)
        pr.writePDB(os.path.join(init.db_root, bindsite_outpath), binding_site)
        out_filenames.append([pair_name, lig_outpath, bindsite_outpath, lig.numAtoms(), binding_site.numAtoms()])
    return out_filenames
