# Try Chembl API

import os,sys
from chembl_webresource_client.new_client import new_client
import prody

def get_similar_compound(mol_name, threshold=90):
    """
    Given the name of a compound, search the similar structure on chembl

    args:
        mol_name ::str
            name of the compound
            e.g. STEARIC ACID

    return:
        similar_smiles ::list of string
            smiles string for the similar compunds
    """
    molecule = new_client.molecule
    res = molecule.search(mol_name)

    smiles=res[0]['molecule_structures']['canonical_smiles']

    similarity = new_client.similarity
    similar_res = similarity.filter(smiles=smiles, similarity=threshold)

    similar_smiles = map(lambda x:x['molecule_structures']['canonical_smiles'], similar_res)
    return list(similar_smiles)

def run():
    # get the title of a pdb structure
    head = prody.parsePDBHeader("3EML")

     
    assay = new_client.assay
    asy = assay.search(head['title'])

    target = new_client.target
    tar = target.search(head['A'].name)

    # get the componds
    molecule = new_client.molecule
    res = molecule.search(head['chemicals'][0].name)
    print(head['chemicals'][0].name)

    # searching the similar componds
    similarity = new_client.similarity
    similar_res = similarity.filter(smiles=res[0]['molecule_structures']['canonical_smiles'],similarity=90)

    return similar_res

if __name__ == '__main__':
    sr = run()