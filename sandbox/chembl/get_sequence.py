import os, sys
import prody
import tempfile
#import chembl
import subprocess
import xml.dom.minidom
from chembl_blast import chembl_blast
from get_similar_compound import get_similar_compound

def parse_PDB(PDBname):
	"""
	Parse the structure from Protein Data Bank

	args: 
		PDBname :: str
		4 letters identifier for the strcuture

	return:
		result :: list
			[ PDBname, ligand_info, similar_smiles, blast_result]
			

	"""
	cdir = os.getcwd()
	tdir = tempfile.mkdtemp()
	os.chdir(tdir)

	PDBHead = prody.parsePDBHeader(PDBname)
	PDB = prody.parsePDB(PDBname)

	ligands = []
	for chem in PDBHead['chemicals']:
		ligands.append([chem.chain, str(chem.resnum), chem.resname, chem.name])

	for chain, resnum, resname, name in ligands:
    	# select the receptor and the ligand
		receptor = PDB.select('not (chain {} resnum {})'.format(chain, resnum))
		ligand = PDB.select('chain {} resnum {}'.format(chain, resnum))
		
		# get the amino acid sequence around the ligand 
		cen_ligand = prody.calcCenter(ligand)
		around_atoms = receptor.select('within 20 of center', center=cen_ligand)
		hv = around_atoms.getHierView()
		sequence = hv['A'].getSequence()
		
		# blast 
		blast = chembl_blast(sequence)

		# get compund similar to the ligand
		similar_smiles = get_similar_compound(name)

		result = (PDBname, [chain, resnum, resname], similar_smiles, blast)
		yield result




if __name__ == '__main__':
    	
    p = parse_PDB("3eml")
    result = p.next()
    print(result)