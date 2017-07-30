# Try Chembl API

import os,sys
from chembl_webresource_client.new_client import new_client
import prody


def run():
    # get the title of a pdb structure
    head = prody.parsePDBHeader("3EML")

     
    assay = new_client.assay
    asy = assay.search(head['title'])

    target = new_client.target
    tar = target.search(head['A'].name)

    # get the componds
    res = molecule.search(head['chemicals'][0].name)

    # searching the similar componds
    similarity = new_client.similarity
    similar_res = similarity.filter(smiles=res[0]['molecule_structures']['canonical_smiles'])

    print similar_res

if __name__ == '__main__':
    run()