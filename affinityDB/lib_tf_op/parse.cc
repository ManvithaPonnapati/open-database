#include "tensorflow/core/framework/op_kernel.h"
#include "tensorflow/core/framework/op.h"
#include "tensorflow/core/framework/shape_inference.h"
#include <openbabel/babelconfig.h>
#include <openbabel/mol.h>
#include <openbabel/parsmart.h>
#include <openbabel/obconversion.h>
#include "atom_constant.h"
using namespace tensorflow;
using namespace std;



REGISTER_OP("ParsePdb")
    .Input("lignad: string")
    .Output("coords: float32")
    .Output("atom_type: int32")
    .Output("elem: float32");

class ParsePdbOp : public OpKernel {
 public:
  explicit ParsePdbOp(OpKernelConstruction* context) : OpKernel(context) {}


    bool ends_with(const char * atomname, std::string ending){
        std::string astr(atomname);
        if (ending.size() > astr.size()) return false;
        return std::equal(ending.rbegin(), ending.rend(), astr.rbegin());
    }

    int type_shift(int ori_idx, std::string ending){
        std::string astr(smina_atom_type::data[ori_idx].adname);
        int idx = 0;
        for(auto atom: smina_atom_type::data){
            std::string atomname(atom.adname);
            if (astr == atomname and ends_with(atom.smina_name, ending)) return idx;
            idx ++;
        }
        exit(0);
    }

    bool is_mental(std::string atomname){
        //std::string astr(atomname);
        for (std::string mental:non_ad_metal_names){
            if (mental==atomname){
                return true;
            }
        }
        return false;
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

    int get_typeidx(std::string astr){
        int i = 0;
        const char* atomname = astr.c_str();
        for (auto atom:smina_atom_type::data){
            if (strcmp(atomname, atom.adname) == 0) return i;
            i++;
        }
        exit(0);
    }
    
    bool is_bond_2_hd(OpenBabel::OBMolAtomIter obatom, OpenBabel::OBMol mol){
        auto atom_id = obatom->GetId();
        
        bool bond_2_hd = false;
        FOR_BONDS_OF_MOL(bond, mol){
            auto begin = bond->GetBeginAtom()->GetId();
            auto end = bond->GetEndAtom()->GetId();
            
            
            if (atom_id == begin){
                auto link_atom = bond->GetEndAtom();
                if (link_atom->IsHydrogen()) bond_2_hd = true;
            } else if(atom_id == end) {
                auto link_atom = bond->GetBeginAtom();
                if (link_atom->IsHydrogen()) bond_2_hd = true;
            } else {
                continue;
            } 
        }
        return bond_2_hd;
    }

    bool is_bond_2_hetero(OpenBabel::OBMolAtomIter obatom,OpenBabel::OBMol mol){
        auto atom_id = obatom->GetId();
        bool bond_2_hetero = false;
        FOR_BONDS_OF_MOL(bond, mol){
            auto begin = bond->GetBeginAtom()->GetId();
            auto end = bond->GetEndAtom()->GetId();
            if (atom_id == begin){
                auto link_atom = bond->GetEndAtom();
                if (link_atom->IsHeteroatom()) bond_2_hetero = true;
            } else if (atom_id == end) {
                auto link_atom = bond->GetBeginAtom();
                if (link_atom->IsHeteroatom()) bond_2_hetero = true;
            } else{
                continue;
            }
        }
        return bond_2_hetero;
    }

  void Compute(OpKernelContext* context) override {
    // Get input tensors
    const Tensor& ligand = context->input(0);

    auto ligand_str = ligand.flat<string>();
    auto lig_path = ligand_str(0);
    using namespace OpenBabel;
    // Read ligand
    OBConversion conv;
    conv.SetInFormat("pdb");
    OpenBabel::OBMol mol;
    OpenBabel::OBElementTable etab;
    std::vector<OBMolAtomIter> flexatoms;
    std::vector<int> atom_type;
    std::vector<float> atom_elem;
    conv.ReadFile(&mol, lig_path.c_str());

    //==============//

    int atom_count = 0;
    float value = 0;
    bool read = conv.ReadFile(&mol, lig_path.c_str());

    FOR_ATOMS_OF_MOL(atom, mol)
    {
    	if(atom->GetAtomicNum() == 1){
			continue; //heavy atoms only
    	} else {
            flexatoms.push_back(atom);
            std::string element_name(etab.GetSymbol(atom->GetAtomicNum()));

            if (atom->IsHydrogen()){
                    element_name = "HD";
            } else if( atom->IsCarbon() and atom->IsAromatic()){
                    element_name = "A";
            } else if( atom->IsOxygen()){
                    element_name = "OA";
            } else if ( atom->IsNitrogen() and atom->IsHbondAcceptor()){
                    element_name = "NA";
            } else if ( atom->IsSulfur() and atom->IsHbondAcceptor()){
                    element_name = "SA";
            }

            if (is_mental(element_name)){
                element_name = 'M';
            }
      
            auto aidx = get_typeidx(element_name);


            bool bond_2_hd = is_bond_2_hd(atom, mol);
            bool bond_2_hetero = is_bond_2_hetero(atom, mol);

            if (element_name == "A" or element_name == "C"){
                if (bond_2_hetero) aidx = type_shift(aidx,"XSNonHydrophobe");
                else aidx = type_shift(aidx, "XSHydrophobe");
            } else if( element_name == "N"){
                if(bond_2_hd) aidx = type_shift(aidx, "XSDonor");
                else aidx = type_shift(aidx, "Nitrogen");
            } else if ( element_name == "NA"){
                if(bond_2_hd) aidx = type_shift(aidx,"XSDonorAcceptor");
                else aidx = type_shift(aidx, "XSAcceptor"); 
            } else if (element_name == "O"){
                if (bond_2_hd) aidx = type_shift(aidx, "XSDonor");
                else aidx =type_shift(aidx,"Oxygen");
            } else if(element_name == "OA"){
                if (bond_2_hd) aidx = type_shift(aidx, "XSDonorAcceptor");
                else aidx = type_shift(aidx, "XSAcceptor");
            }

            atom_type.push_back(aidx);
            atom_count++;
            
    	}
    }

    for(int at:atom_type){
        atom_elem.push_back(type2elem(at));
    }

    int atom_num = flexatoms.size();

    Tensor* output_coords;
    TensorShape coord_shape;

    coord_shape.AddDim(atom_num);
    coord_shape.AddDim(3);
    OP_REQUIRES_OK(context, context->allocate_output(0, coord_shape, &output_coords));

    auto output_coords_val = output_coords->flat<float>();
    for (int i=0;i<flexatoms.size();i++){

        auto atom = flexatoms[i];
        auto atom_v = atom->GetVector();
        output_coords_val(i*3+0) = atom_v.x();
        output_coords_val(i*3+1) = atom_v.y();
        output_coords_val(i*3+2) = atom_v.z();
    }

    Tensor* output_atom_type;
    TensorShape atom_type_shape;
    
    atom_type_shape.AddDim(atom_num);
    OP_REQUIRES_OK(context, context->allocate_output(1, atom_type_shape, &output_atom_type));

    auto output_atom_type_val = output_atom_type->flat<int>();
    for(int i = 0;i<atom_num;i++){
        output_atom_type_val(i) = atom_type[i];
    }

    Tensor* output_atom_elem;
    TensorShape atom_elem_shape;

    atom_elem_shape.AddDim(atom_num);
    OP_REQUIRES_OK(context, context->allocate_output(2, atom_elem_shape, &output_atom_elem));

    auto output_atom_elem_val = output_atom_elem->flat<float>();
    for (int i = 0;i<atom_num;i++){
        output_atom_elem_val(i) = atom_elem[i];
    }


  }

};

REGISTER_KERNEL_BUILDER(Name("ParsePdb").Device(DEVICE_CPU), ParsePdbOp);