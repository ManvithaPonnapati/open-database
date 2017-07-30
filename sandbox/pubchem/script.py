"run.py" 14L, 249C written                                                                                                              9,39          All
# Try Pubchem API

import os,sys
import pubchempy as pcp
import prody

def run():
    # get the title of a pdb structure
    head = prody.parsePDBHeader("3EML")

    # get the assays by the protein name
    as = pcp.get_assays(head['title'])

    # get the componds
    comp = pcp.get_compounds(head['chemicals'][0].name,'name')

    # searching the similar componds
    comps = pcp.get_compounds(comp[0].isomeric_smiles, 'smiles',searchtype='similarity',Threshold=90, listkey_count=30)

if __name__ == '__main__':
    run()