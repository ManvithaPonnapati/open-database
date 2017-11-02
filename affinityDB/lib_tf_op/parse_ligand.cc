#include "tensorflow/core/framework/op_kernel.h"
#include "tensorflow/core/framework/op.h"
#include "tensorflow/core/framework/shape_inference.h"
#include <openbabel/babelconfig.h>
#include <openbabel/mol.h>
#include <openbabel/parsmart.h>
#include <openbabel/obconversion.h>
#include "../head/atom_constant.h"
using namespace tensorflow;
using namespace std;
REGISTER_OP("ParseLigand")
    .Input("lignad: string")
    .Output("coords: float32")
    .Output("energy: float32")
    .Output("atom_mask: int32")
    .Output("branch_rot_bonds: int32")
    .Output("movable_mat: int32");

class ParseLigandOp : public OpKernel {
 public:
  explicit ParseLigandOp(OpKernelConstruction* context) : OpKernel(context) {}
  // Define const value 
  vector< vector<int> > all_bonds;
  vector< vector<int> > rot_bonds;
  vector< vector<int> > branch_bonds;
  vector< vector<int> > branch_rot_bonds;
  vector< int > branch;
  vector< vector<int> > branch_mask;
  vector< vector<int> > atom_mask;
  vector< vector<int> > movable_mat;
  vector< vector<int> > bonded;

  bool find_bond(vector<int> bond, vector< vector<int> > bond_set){
      for (auto bond_in_set:bond_set){
          if (bond[0]==bond_in_set[0] and bond[1]==bond_in_set[1]){
              return true;
          }
      }
      return false;
  }

  vector<int> adj_atom(int root_idx){
    vector<int> adj;
    for (auto bond:all_bonds){
        if ( bond[0] == root_idx ){
            adj.push_back(bond[1]);
        }else if( bond[1] == root_idx){
            adj.push_back(bond[0]);
        }
    }
    return adj;
  }

  bool find(vector<int> list, int value){
    for (int val:list){
        if (val == value){
            return true; 
        }
    }
    return false;
  }

  void bond_by_degree(int root_idx,int atom_idx,int degree){
    std::cout<<"bond by degree "<<degree<<std::endl;
    if(degree > 0){
        vector<int> adj = adj_atom(atom_idx);
        for (int idx:adj){
            if (!find(bonded[root_idx], idx)){
                bonded[root_idx].push_back(idx);
                bond_by_degree(root_idx, idx, degree-1);
            }
        }
    }
  }

  void split_branch(int atom_idx, int bond_idx){
     
      branch[atom_idx] = bond_idx;
      vector<vector<int> > adj_bonds;

      
     

      for (auto bond:all_bonds){
          vector<int> branch_bond;
          int begin;
          int end;
          if (bond[0]==atom_idx){
              begin = bond[0];
              end = bond[1];
          } else if (bond[1] == atom_idx){
              begin = bond[1];
              end = bond[0];
          } else {
              continue;
          }
          
          if (branch[end] > -1){
              
              // atom has been assigned to a group
              continue;
          } else {
              if ( find_bond(bond, rot_bonds)) {
                  int n_bond_idx = -1;
                  for (int i = 0;i<branch.size();i++){
                      if (branch[i]>n_bond_idx){
                          n_bond_idx = branch[i];
                      }
                  }

                  n_bond_idx +=1;

                  if (bond_idx < n_bond_idx){
                      branch_bond.push_back(bond_idx);
                      branch_bond.push_back(n_bond_idx);
                  } else {
                      branch_bond.push_back(n_bond_idx);
                      branch_bond.push_back(bond_idx);
                  }

                  branch_bonds.push_back(branch_bond);
                  branch_rot_bonds.push_back(branch_bond);
                  split_branch(end, n_bond_idx);
              } else {
                  split_branch(end, bond_idx);
              }

          }
      }
  }

  void label_branch(int mask_idx, int bond_idx, int label, int rotbond_idx){
       branch_mask[mask_idx][bond_idx] = label;
       int begin;
       int end;

       for (auto bond:branch_bonds){
           if (bond[0] == branch_bonds[rotbond_idx][0] and bond[1] == branch_bonds[rotbond_idx][1]){
               continue;
           } else if( bond[0]== bond_idx){
                begin = bond[0];
                end = bond[1];         
           } else if( bond[1] == bond_idx){
               begin = bond[1];
               end = bond[0];
           } else {
               continue;
           }

           if (branch_mask[mask_idx][end] >=0){
               continue;
           } else {
               branch_mask[mask_idx][end] = label;
               label_branch(mask_idx, end, label, rotbond_idx);
           }


       }
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
    conv.ReadFile(&mol, lig_path.c_str());

    //get bonds
    int num_rot_bond = 0;
    int c = 0;

    FOR_BONDS_OF_MOL(bond, mol){
        vector<int> atom_pair;
        int begin_idx = bond->GetBeginAtomIdx()-1;
        int end_idx = bond->GetEndAtomIdx()-1;
        if (begin_idx>end_idx){
            atom_pair.push_back(end_idx);
            atom_pair.push_back(begin_idx);
        } else {
            atom_pair.push_back(begin_idx);
            atom_pair.push_back(end_idx);
        }
        all_bonds.push_back(atom_pair);
        if ((!bond->IsSingle())or bond->IsAmide() or bond->IsInRing()){
            c +=1;

            continue;
        } else if ( bond->GetBeginAtom()->GetValence() ==1 or bond->GetEndAtom()->GetValence() ==1){
            c +=1;
            continue;
        } else {
            rot_bonds.push_back(atom_pair);
            c +=1;
            num_rot_bond +=1;
        }

    }   
    
    //get atom groups
    for (int i = 0;i<mol.NumAtoms();i++){
        
        branch.push_back(-1);
    }

    //get branch group
    int num_branch = -1;
    for(int i = 0;i<branch.size();i++){
        if (branch[i]>num_branch){
            num_branch = branch[i];
        }
    }
    num_branch +=1;

    for (int i = 0;i<rot_bonds.size();i++){
        vector<int> temp_mask;
        for (int j= 0;j<num_branch;j++){
            temp_mask.push_back(-1);
        }
        branch_mask.push_back(temp_mask);
    }



    for (int i = 0;i<branch_bonds.size();i++){
        label_branch(i, branch_bonds[i][0], 0, i);
        label_branch(i, branch_bonds[i][1], 1, i);
    }

    // get atom mask

    for (int i = 0;i< rot_bonds.size();i++){
        vector<int> temp_mask;
        for (int j = 0; j< mol.NumAtoms();j++){
            temp_mask.push_back(-1);
        }
        atom_mask.push_back(temp_mask);
    }

    
    for(int i =0;i<branch_mask.size();i++){
        for(int j=0;j< branch_mask[i].size();j++){
            // j for bond_idx
            if (branch_mask[i][j] == 0){
                for(int k=0;k<branch.size();k++){
                    if(branch[k] == j){
                        atom_mask[i][k] = 0;
                    }
                }
            } else{
                for(int k=0;k<branch.size();k++){
                    if(branch[k] == j){
                        atom_mask[i][k] = 1;
                    }
                } 
            }
        }
    }

    // get movable bond
    for(int i=0;i<mol.NumAtoms();i++){
        vector<int> tmp;
        for(int j=0;j<mol.NumAtoms();j++){
            tmp.push_back(1);
        }
        movable_mat.push_back(tmp);
    }

    for(int i = 0;i<mol.NumAtoms();i++){
        vector<int> tmp;
        tmp.push_back(i);
        bonded.push_back(tmp);
        bond_by_degree(i,i,3);
    }

    for(int i=0;i<bonded.size();i++){
        for(int bonded_atom:bonded[i]){
            movable_mat[i][bonded_atom] = 0;
            movable_mat[bonded_atom][i] = 0;
        }
    }

    for(auto bond: rot_bonds){
        for(int i=0;i<branch.size();i++){
            if (branch[i] == branch[bond[1]]){
                movable_mat[i][bond[0]] = 0;
                movable_mat[bond[0]][i] = 0;
            } else if(branch[i] == branch[bond[0]]){
                movable_mat[i][bond[1]] = 0;
                movable_mat[bond[1]][i] = 0;
            }
        }
    }

    for(int i=0;i<mol.NumAtoms();i++){
        for(int j=0;j<mol.NumAtoms();j++){
            if (branch[i] == branch[j]){
                movable_mat[i][j] = 0;
                movable_mat[j][i] = 0;
            }
        }
    }
    //==============//

    float value = 0;
    bool read = conv.ReadFile(&mol, lig_path.c_str());

    FOR_ATOMS_OF_MOL(atom, mol)
    {
    	if(atom->GetAtomicNum() == 1){
			continue; //heavy atoms only
    	} else {
    		flexatoms.push_back(atom);
    	}
    }


    Tensor* output_coords;
    TensorShape coord_shape;
    int atom_num = flexatoms.size();
    coord_shape.AddDim(atom_num);
    coord_shape.AddDim(3);
    OP_REQUIRES_OK(context, context->allocate_output(0, coord_shape, &output_coords));

    std::vector<smina_atom_type::info> atom_type;
    for(int i=0;i<10;i++){
          atom_type.push_back(smina_atom_type::data[i]);
    }

    auto output_coords_val = output_coords->flat<float>();
    for (int i=0;i<flexatoms.size();i++){

      auto atom = flexatoms[i];
      auto element_name = etab.GetSymbol(atom->GetAtomicNum());

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

    	auto atom_v = atom->GetVector();
    	output_coords_val(i*3+0) = atom_v.x();
    	output_coords_val(i*3+1) = atom_v.y();
    	output_coords_val(i*3+2) = atom_v.z();
    }
    //


    // set ouptut tensor shape
    TensorShape output_shape;
    output_shape.AddDim(1);
    
    // create an output tensor
    Tensor* output_tensor = NULL;
    OP_REQUIRES_OK(context, context->allocate_output(1, output_shape,
                                                     &output_tensor));
    

    // Set the output value 
    auto output_flat = output_tensor->flat<float>();
    output_flat(0) = flexatoms.size();

    // set output tensor shape
    Tensor* atom_mask_tensor;
    TensorShape atom_mask_shape;
    atom_mask_shape.AddDim(rot_bonds.size());
    atom_mask_shape.AddDim(mol.NumAtoms());
    OP_REQUIRES_OK(context, context->allocate_output(2, atom_mask_shape,
        &atom_mask_tensor));       

    auto atom_mask_flat = atom_mask_tensor->flat<int>();
    for (int i = 0;i<rot_bonds.size();i++){
        for (int j = 0;j<mol.NumAtoms();j++){
            atom_mask_flat(i*mol.NumAtoms() + j) = atom_mask[i][j];
        }
    }


    //Branch rot bonds
    Tensor* branch_rot_bonds_tensor;
    TensorShape branch_rot_bonds_shape;
    branch_rot_bonds_shape.AddDim(branch_rot_bonds.size());
    branch_rot_bonds_shape.AddDim(2);
    OP_REQUIRES_OK(context, context->allocate_output(3, branch_rot_bonds_shape,
        &branch_rot_bonds_tensor));  

    auto branch_rot_bonds_flat = branch_rot_bonds_tensor->flat<int>();
    for (int i=0;i<branch_rot_bonds.size();i++){
        branch_rot_bonds_flat(i*2+0) = branch_rot_bonds[i][0];
        branch_rot_bonds_flat(i*2+1) = branch_rot_bonds[i][1];
    }

    //Movable bond
    Tensor* movable_mat_tensor;
    TensorShape movable_mat_shape;
    movable_mat_shape.AddDim(mol.NumAtoms());
    movable_mat_shape.AddDim(mol.NumAtoms());
    OP_REQUIRES_OK(context, context->allocate_output(4, movable_mat_shape,
        &movable_mat_tensor));
    
    auto movable_mat_flat = movable_mat_tensor->flat<int>();
    for (int i=0;i<mol.NumAtoms();i++){
        for (int j=0;j<mol.NumAtoms();j++){
            movable_mat_flat(i* mol.NumAtoms() + j) = movable_mat[i][j];
        }
    }

  }

};

REGISTER_KERNEL_BUILDER(Name("ParseLigand").Device(DEVICE_CPU), ParseLigandOp);