#include "tensorflow/core/framework/op_kernel.h"
#include "tensorflow/core/framework/op.h"
#include "tensorflow/core/framework/shape_inference.h"
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include "include/atom_constant.h"

using namespace tensorflow;
using namespace std;
REGISTER_OP("ParsePdb")
    .Input("path: string")
    .Output("coords: float32")
    .Output("atom_type: int32")
    .Output("atom_elem: float32")
    .Output("bonds: int32");

class ParsePdbOp : public OpKernel {
 public:
  explicit ParsePdbOp(OpKernelConstruction* context) : OpKernel(context) {}
  // Define const value 

  void Compute(OpKernelContext* context) override {

	vector<vector<int> > bonds;
	vector<vector<float> > coords;
	vector<string> elements;
	vector<vector<int> > bonds_to;
	vector<int> atom_type;
    vector<float> atom_elem;
    
    // Get input tensors
    const Tensor& infile = context->input(0);
    auto infile_str = infile.flat<string>();
    auto fpath = infile_str(0);

    // Read pdb
	ifstream fin(fpath, ios::in);
	string line;

	// parse coordinates and bonds
	while(getline(fin, line)){
        if (line.find("HETATM") == 0 or line.find("ATOM") == 0){
            //parse coordinate
            float x = atof(line.substr(30,8).c_str());
            float y = atof(line.substr(38,8).c_str());
            float z = atof(line.substr(46,8).c_str());
            
            vector<float> coord;
            coord.push_back(x);
            coord.push_back(y);
            coord.push_back(z);
            coords.push_back(coord);
            
            //parse atom type
            string elem = line.substr(76,2);
            strip(elem);
            elements.push_back(elem);
        }
            
        if (line.find("CONECT") == 0){
            // parse bond
            istringstream iss(line);
            string cont;
            int bond_atom;
            int bond_atom_;
            
            iss>>cont; // read CONECT
            iss>>cont;
            // in pdb atom starts with 1
            bond_atom = atoi(cont.c_str())-1;
            
            vector<int> bond_to;
            while(iss){
                iss>>cont;
                bond_atom_ = atoi(cont.c_str())-1;
                bond_to.push_back(bond_atom_);
                
                if (bond_atom<bond_atom_){
                    vector<int> bond;
                    bond.push_back(bond_atom);
                    bond.push_back(bond_atom_);
                    bonds.push_back(bond);
                }
            }
            bonds_to.push_back(bond_to);
        }
    }

	// adjust atom type
	for(int i = 0;i < elements.size();i++){
		string elem = elements[i];
		int aid = elem2aid(elem);
		
		bool bond2h=false;
		bool bond2hetero=false;
		
		for(int atom:bonds_to[i]){
			
			if (is_hydrogen(elements[atom])) bond2h = true;
			if (is_hetero(elements[atom])) bond2hetero = false;
		}
		
		if(elem == "A" or elem == "C"){
			if(bond2hetero) aid = type_shift(aid,"XSNonHydrophobe");
			else aid = type_shift(aid,"XSHydrophobe");
		} else if( elem == "N") {
			if (bond2h) aid = type_shift(aid, "XSDonor");
			else aid = type_shift(aid, "Nitrogen");
		} else if( elem == "NA"){
			if (bond2h) aid = type_shift(aid, "XSDonorAcceptor");
			else aid = type_shift(aid, "XSAcceptor");
		} else if( elem == "O"){
			if (bond2h) aid = type_shift(aid, "XSDonor");
			else aid = type_shift(aid, "Oxygen");
		} else if( elem == "OA"){
			if (bond2h) aid = type_shift(aid, "XSDonorAcceptor");
			else aid = type_shift(aid, "XSAcceptor");
		}
		
		atom_type.push_back(aid);
		
    }
    
	// map to elem
	for(int at:atom_type) atom_elem.push_back(type2elem(at));
        
    
    //==============//

    int atom_num = atom_type.size();

    // output coords
    Tensor* output_coords;
    TensorShape coord_shape;
    coord_shape.AddDim(atom_num);
    coord_shape.AddDim(3);
    OP_REQUIRES_OK(context, context->allocate_output(0, coord_shape, &output_coords));

    auto output_coords_val = output_coords->flat<float>();
    for(int i=0;i<atom_num;i++){
        output_coords_val(i*3+0) = coords[i][0];
        output_coords_val(i*3+1) = coords[i][1];
        output_coords_val(i*3+2) = coords[i][2];
    }

    // output atom type
    Tensor* output_atom_type;
    TensorShape atom_type_shape;
    atom_type_shape.AddDim(atom_num);
    OP_REQUIRES_OK(context, context->allocate_output(1, atom_type_shape, &output_atom_type));
    
    auto output_atom_type_val = output_atom_type->flat<int>();
    for(int i = 0; i< atom_num ;i++) output_atom_type_val(i) = atom_type[i];


    // output atom elem
    Tensor* output_atom_elem;
    TensorShape atom_elem_shape;
    atom_elem_shape.AddDim(atom_num);
    OP_REQUIRES_OK(context, context->allocate_output(2, atom_elem_shape, &output_atom_elem));
    
    auto output_atom_elem_val = output_atom_elem->flat<float>();
    for(int i = 0; i< atom_num ;i++) output_atom_elem_val(i) = atom_elem[i];
    


    // output bonds
    Tensor* output_bonds;
    TensorShape bonds_shape;
    bonds_shape.AddDim(bonds.size());
    bonds_shape.AddDim(2);
    OP_REQUIRES_OK(context, context->allocate_output(3, bonds_shape, &output_bonds));
    
    auto output_bonds_val = output_bonds->flat<int>();
    for(int i=0;i<bonds.size();i++){
        output_bonds_val(i*2+0) = bonds[i][0];
        output_bonds_val(i*2+1) = bonds[i][1];
    }


  }

};

REGISTER_KERNEL_BUILDER(Name("ParsePdb").Device(DEVICE_CPU), ParsePdbOp);