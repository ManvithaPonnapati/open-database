#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>

using namespace std;

//store all the desired properties in smina_type_info
struct info
{
	string smina_name; //this must be more than 2 chars long
	string adname; //this must be no longer than 2 chars
	double ad_radius;
	double ad_depth;
	double ad_solvation;
	double ad_volume;
	double covalent_radius;
	double xs_radius;
	bool xs_hydrophobe;
	bool xs_donor;
	bool xs_acceptor;
	bool ad_heteroatom;
};


const info atom_data[] = { //el, ad, xs
		{"Hydrogen",
				"H",	1.000000,	0.020000,	0.000510,	0.000000,	0.370000,	0.000000,	false,	false,	false,	false},
		{"PolarHydrogen",
				"HD",	1.000000,	0.020000,	0.000510,	0.000000,	0.370000,	0.000000,	false,	false,	false,	false},
		{"AliphaticCarbonXSHydrophobe",
				"C",	2.000000,	0.150000,	-0.001430,	33.510300,	0.770000,	1.900000,	true,	false,	false,	false},
		{"AliphaticCarbonXSNonHydrophobe",
				"C",	2.000000,	0.150000,	-0.001430,	33.510300,	0.770000,	1.900000,	false,	false,	false,	false},
		{"AromaticCarbonXSHydrophobe",
				"A",	2.000000,	0.150000,	-0.000520,	33.510300,	0.770000,	1.900000,	true,	false,	false,	false},
		{"AromaticCarbonXSNonHydrophobe",
				"A",	2.000000,	0.150000,	-0.000520,	33.510300,	0.770000,	1.900000,	false,	false,	false,	false},
		{"Nitrogen",
				"N",	1.750000,	0.160000,	-0.001620,	22.449300,	0.750000,	1.800000,	false,	false,	false,	true},
		{"NitrogenXSDonor",
				"N",	1.750000,	0.160000,	-0.001620,	22.449300,	0.750000,	1.800000,	false,	true,	false,	true},
		{"NitrogenXSDonorAcceptor",
				"NA",	1.750000,	0.160000,	-0.001620,	22.449300,	0.750000,	1.800000,	false,	true,	true,	true},
		{"NitrogenXSAcceptor",
				"NA",	1.750000,	0.160000,	-0.001620,	22.449300,	0.750000,	1.800000,	false,	false,	true,	true},
		{"Oxygen",
				"O",	1.600000,	0.200000,	-0.002510,	17.157300,	0.730000,	1.700000,	false,	false,	false,	true},
		{"OxygenXSDonor",
				"O",	1.600000,	0.200000,	-0.002510,	17.157300,	0.730000,	1.700000,	false,	true,	false,	true},
		{"OxygenXSDonorAcceptor",
				"OA",	1.600000,	0.200000,	-0.002510,	17.157300,	0.730000,	1.700000,	false,	true,	true,	true},
		{"OxygenXSAcceptor",
				"OA",	1.600000,	0.200000,	-0.002510,	17.157300,	0.730000,	1.700000,	false,	false,	true,	true},
		{"Sulfur",
				"S",	2.000000,	0.200000,	-0.002140,	33.510300,	1.020000,	2.000000,	false,	false,	false,	true},
		{"SulfurAcceptor",
				"SA",	2.000000,	0.200000,	-0.002140,	33.510300,	1.020000,	2.000000,	false,	false,	false,	true},
		{"Phosphorus",
				"P",	2.100000,	0.200000,	-0.001100,	38.792400,	1.060000,	2.100000,	false,	false,	false,	true},
		{"Fluorine",
				"F",	1.545000,	0.080000,	-0.001100,	15.448000,	0.710000,	1.500000,	true,	false,	false,	true},
		{"Chlorine",
				"Cl",	2.045000,	0.276000,	-0.001100,	35.823500,	0.990000,	1.800000,	true,	false,	false,	true},
		{"Bromine",
				"Br",	2.165000,	0.389000,	-0.001100,	42.566100,	1.140000,	2.000000,	true,	false,	false,	true},
		{"Iodine",
				"I",	2.360000,	0.550000,	-0.001100,	55.058500,	1.330000,	2.200000,	true,	false,	false,	true},
		{"Magnesium",
				"Mg",	0.650000,	0.875000,	-0.001100,	1.560000,	1.300000,	1.200000,	false,	true,	false,	true},
		{"Manganese",
				"Mn",	0.650000,	0.875000,	-0.001100,	2.140000,	1.390000,	1.200000,	false,	true,	false,	true},
		{"Zinc",
				"Zn",	0.740000,	0.550000,	-0.001100,	1.700000,	1.310000,	1.200000,	false,	true,	false,	true},
		{"Calcium",
				"Ca",	0.990000,	0.550000,	-0.001100,	2.770000,	1.740000,	1.200000,	false,	true,	false,	true},
		{"Iron",
				"Fe",	0.650000,	0.010000,	-0.001100,	1.840000,	1.250000,	1.200000,	false,	true,	false,	true},
		{"GenericMetal",
				"M",	1.200000,	0.000000,	-0.001100,	22.449300,	1.750000,	1.200000,	false,	true,	false,	true}
};

inline bool xs_is_donor(int sm) {
	return atom_data[sm].xs_donor;
}

inline bool xs_is_acceptor(int sm) {
	return atom_data[sm].xs_acceptor;
}

inline bool xs_donor_acceptor(int t1, int t2) {
	return xs_is_donor(t1) && xs_is_acceptor(t2);
}

inline bool xs_h_bond_possible(int t1, int t2) {
	return xs_donor_acceptor(t1, t2) || xs_donor_acceptor(t2, t1);
}

void strip(string & str){
	int b = str.find_first_not_of(" ");
	int e = str.find_last_not_of(" ");
	str = str.substr(b, e-b+1);
	return;
}

int elem2aid(string elem){
	int aid = 0;
	
	for(auto atom: atom_data){
		if(atom.adname == elem){
			return aid;
		}
		aid +=1;
	}
	// doesn't find the atom in table
	cout<<"doesn't find the atom in table "<<elem<<endl;
	exit(0);
}

bool is_hydrogen(int aid){
	return aid <2;
}
bool is_hydrogen(string elem){
	int aid = elem2aid(elem);
	return aid <2;
}

bool is_hetero(int aid){
	return aid>5;
}

bool is_hetero(string elem){
	int aid = elem2aid(elem);
	return aid > 5;
}



const std::string non_ad_metal_names[] = { // expand as necessary
	"Cu", "Fe", "Na", "K", "Hg", "Co", "U", "Cd", "Ni"
};
bool is_mental(string elem){
	for(string mental:non_ad_metal_names){
		if (elem == mental) return true;
	}
	return false;
}

bool ends_with(string atomname, string ending){
	
	if (ending.size() > atomname.size()) return false;
	return std::equal(ending.rbegin(), ending.rend(), atomname.rbegin());
}

int type_shift(int aid, string ending){
	string astr = atom_data[aid].adname;
	int idx = 0;
	for(auto atom: atom_data){
		if (astr == atom.adname and ends_with(atom.smina_name, ending)) return idx;
		idx ++;
	}
	//cann't find the atom
	cout<<"cann't find the atom "<<astr<<" with ending "<<ending<<endl;
	exit(0);
}

float type2elem(int atomtype){
	switch(atomtype){
		case 0: 
		case 1: return 1.0;
		case 2: 
		case 3: 
		case 4: 
		case 5: 
		case 6: return 2.0;
		case 7: 
		case 8: 
		case 9: 
		case 10:return 3.0;
		case 11:
		case 12:
		case 13:
		case 14:return 4.0;
		case 15:
		case 16:
		case 17:return 6.0;
		case 18:
		case 19:
		case 20:
		case 21:return 5.0;
		default: return 7.0;
	}

}

