import os,sys, random
from rdkit import Chem
from rdkit.Chem import MCS
from rdkit.Chem.rdmolfiles import SDMolSupplier



# takes a list of .mol files as a source of decoys
# takes a list of number of atoms for each of the potantial decoys
# takes a list of .mol files as a molecules that need decoys

# sorts list by number of atoms
# for each of the search ligands
#     retrieve all with the approximate number of atoms
#     random shuffle
#     while num_decoys < desired:
#          mcs substructure search




class Search_decoys_init:
    this_module = sys.modules[__name__]
    arg_types = [str]
    out_types = [str]
    out_names = ["decoy_id"]

    def __init__(self,db_root,decoy_ids,decoy_natoms,decoy_molfiles,max_decoys=10,atom_diff=5,max_substruct=5):
        """

        :param db_root:
        :param decoy_ids:
        :param decoy_natoms:
        :param decoy_molfiles:
        :param max_decoys:
        :param atom_diff:
        :param max_substruct:
        """

        print decoy_ids,decoy_natoms,decoy_molfiles




def search_decoys(molfile_path):
    pass



# class GetDecoysInit:
#     this_module = sys.modules[__name__]
#     def __init__(self, all_pdb_files, all_mol_files, all_mols, all_num_atoms, max_atom_dif, max_substruct, max_num_decoys):
#         """
#
#         :param all_pdb_files:
#         :param all_mol_files:
#         :param all_mols:
#         :param all_num_atoms:
#         :param max_atom_dif:
#         :param max_substruct:
#         :param max_num_decoys:
#         """
#         self.all_pdb_files = all_pdb_files
#         self.all_mol_files = all_mol_files
#         self.all_mols = all_mols
#         self.all_num_atoms = all_num_atoms
#         self.max_atom_dif = max_atom_dif
#         self.max_substruct = max_substruct
#         self.max_num_decoys = max_num_decoys
#         self.this_module.get_decoys_init = self










def get_decoys(pdb_file, mol_file, num_atoms, init='get_decoys_init'):
    """
    For each binding ligand, get a list of decoy ligands. We filter by number of atoms and maximum common
    substructure (MCS). Returns filepaths to all binding ligand - decoy pair.

    :param pdb_file:
    :param mol_file:
    :param num_atoms:
    :param init:
    :return:
    """

    init = eval(init)
    reader = SDMolSupplier(mol_file)
    mol = reader[0]
    output = ""
    counter = 0

    # Shuffle which ligands we sample to avoid biases in decoy ligands
    iterator = range(len(init.all_mols))
    random.shuffle(iterator)
    for i in iterator:
        if (init.all_mol_files[i] == mol_file or abs(init.all_num_atoms[i] - num_atoms) > init.max_atom_dif):           # FIXME O2 time
            continue                                                                                                    # FIXME
        mcs = MCS.FindMCS([init.all_mols[i], mol],
                          minNumAtoms=init.max_substruct,
                          ringMatchesRingOnly=True,
                          completeRingsOnly=True,
                          timeout=1)
        if mcs.numAtoms == -1:
            if counter == init.max_num_decoys -1:
                output += init.all_pdb_files[i]
                counter += 1
                break                                                                                                   # FIXME
        output += init.all_pdb_files[i] + ','
        counter += 1
    # Check to make sure there are enough decoys
    if counter < init.max_num_decoys:
        raise Exception("Not enough decoys for ligand " + pdb_file)
    print 'Got the decoys for one ligand'
    return [[pdb_file, output]]