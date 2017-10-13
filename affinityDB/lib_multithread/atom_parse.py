import os, sys
import numpy as np
from collections import namedtuple
from openbabel import OBAtom, OBElementTable
import openbabel

Atom = namedtuple('Atom',
                  ['smina_name', 'adname'])

Atom_dict = [
    Atom(*["Hydrogen", "H"]),
    Atom(*["PolarHydrogen", "HD"]),
    Atom(*["AliphaticCarbonXSHydrophobe", "C"]),
    Atom(*["AliphaticCarbonXSNonHydrophobe", "C"]),
    Atom(*["AromaticCarbonXSHydrophobe", "A"]),
    Atom(*["AromaticCarbonXSNonHydrophobe", "A"]),
    Atom(*["Nitrogen", "N"]),
    Atom(*["NitrogenXSDonor", "N"]),
    Atom(*["NitrogenXSDonorAcceptor", "NA"]),
    Atom(*["NitrogenXSAcceptor", "NA"]),
    Atom(*["Oxygen", "O"]),
    Atom(*["OxygenXSDonor", "O"]),
    Atom(*["OxygenXSDonorAcceptor", "OA"]),
    Atom(*["OxygenXSAcceptor", "OA"]),
    Atom(*["Sulfur", "S"]),
    Atom(*["SulfurAcceptor", "SA"]),
    Atom(*["Phosphorus", "P"]),
    Atom(*["Fluorine", "F"]),
    Atom(*["Chlorine", "Cl"]),
    Atom(*["Bromine", "Br"]),
    Atom(*["Iodine", "I"]),
    Atom(*["Magnesium", "Mg"]),
    Atom(*["Manganese", "Mn"]),
    Atom(*["Zinc", "Zn"]),
    Atom(*["Calcium", "Ca"]),
    Atom(*["Iron", "Fe"]),
    Atom(*["GenericMetal", "M"])
]

Mental = ["Cu", "Fe", "Na", "k", "Hg", "Co", "U", "Cd", "Ni"]
etab = OBElementTable()

class atom_parser:
    def __init__(self):
        pass

    def parse_file(self,file_name):
        print (file_name)
        print ("parse file")
        obConversion = openbabel.OBConversion()
        OBligand = openbabel.OBMol()

        if not obConversion.ReadFile(OBligand, file_name):
            message = 'Cannot parse {}'.format(file_name)
            raise Exception(message)

        real_atom_type = []
        
        for obatom in openbabel.OBMolAtomIter(OBligand):
            real_atom_type.append(self.parse_atom(obatom))

        return real_atom_type
        


    
    def type_shift(self, origin_idx, suffix):

        adname = Atom_dict[origin_idx].adname
        for idx, atom in enumerate(Atom_dict):
            if atom.adname == adname and atom.smina_name.endswith(suffix):
                return idx
        raise Exception("Cannot find {} {}.".format(suffix, adname))
    
    def adjust_info(self, obatom):
        '''
        If a atom is bonded to polarhydrogen or heteroatom
        :param obatom: openbabel OBAtom istance
        :return: bond_2_hd, bond_2_hetero : boolean
        '''
        bonds = list(openbabel.OBAtomBondIter(obatom))
        atom_id = obatom.GetId()

        bond_2_hd = False
        bond_2_hetero = False
        for bond in bonds:
            begin = bond.GetBeginAtom().GetId()
            end = bond.GetEndAtom().GetId()
            if atom_id == begin:
                link_atom = bond.GetEndAtom()
            elif atom_id == end:
                link_atom = bond.GetBeginAtom()
            else:
                raise Exception("Wrong bond")

            if link_atom.IsHydrogen():
                # all the remained hydrogen is polarhydrogen
                bond_2_hd = True
            if link_atom.IsHeteroatom():
                bond_2_hetero = True

        return bond_2_hd, bond_2_hetero
    
    def getAtomIdxByName(self, element_name):

        for idx, atom in enumerate(Atom_dict):
            if atom.adname == element_name:
                return idx
        raise Exception('Atom name {} can not find in collection'.format(element_name))
 
    def parse_atom(self, obatom):
        # parse basic atom type from obatom
        element_name = etab.GetSymbol(obatom.GetAtomicNum());
        if obatom.IsHydrogen():
            element_name = 'HD'
        elif obatom.IsCarbon() and obatom.IsAromatic():
            element_name = 'A'
        elif obatom.IsOxygen():
            element_name = 'OA'
        elif obatom.IsNitrogen() and obatom.IsHbondAcceptor():
            element_name = 'NA'
        elif obatom.IsSulfur() and obatom.IsHbondAcceptor():
            element_name = 'SA'

        if element_name in Mental:
            element_name = 'M'

        idx = self.getAtomIdxByName(element_name)

        # typ shift if a atom is bonded to specific type of atom
        bond_2_hd, bond_2_hetero = self.adjust_info(obatom)

        if element_name == 'A' or element_name == 'C':
            if bond_2_hetero:
                idx = self.type_shift(idx, 'XSNonHydrophobe')
            else:
                idx = self.type_shift(idx, 'XSHydrophobe')
        elif element_name == 'N':
            if bond_2_hd:
                idx = self.type_shift(idx, 'XSDonor')
            else:
                idx = self.type_shift(idx, 'Nitrogen')
        elif element_name == 'NA':
            if bond_2_hd:
                idx = self.type_shift(idx, 'XSDonorAcceptor')
            else:
                idx = self.type_shift(idx, 'XSAcceptor')
        elif element_name == 'O':
            if bond_2_hd:
                idx = self.type_shift(idx, 'XSDonor')
            else:
                idx = self.type_shift(idx, 'Oxygen')
        elif element_name == 'OA':
            if bond_2_hd:
                idx = self.type_shift(idx, 'XSDonorAcceptor')
            else:
                idx = self.type_shift(idx, 'XSAcceptor')

        return idx