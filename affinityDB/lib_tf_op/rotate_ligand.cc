#include "tensorflow/core/framework/op_kernel.h"
#include "tensorflow/core/framework/op.h"
#include "tensorflow/core/framework/shape_inference.h"
#include <cmath>
#include <openbabel/babelconfig.h>
#include <openbabel/mol.h>
#include <openbabel/parsmart.h>
#include <openbabel/obconversion.h>
#include "../head/atom_constant.h"

using namespace tensorflow;
using namespace std;
REGISTER_OP("RotateLigand")
    .Input("coords: float32")
    .Input("mask: int32")
    .Input("branch_rot_bond: int32")
    .Input("bond_idx: int32")
    .Input("rot_ang: float32")
    .Input("side: int32")
    .Output("out_coords: float32");

class RotateLigandOp : public OpKernel {
 public:
  explicit RotateLigandOp(OpKernelConstruction* context) : OpKernel(context) {}
  // Define const value 
  vector< Eigen::Vector3d > unit_vectors;
  vector< Eigen::Vector3d > starts;
  vector< vector<int> > rotate_masks;
  

  Eigen::Matrix<float, 4, 4> T;
  Eigen::Matrix<float, 4, 4> T_;
  Eigen::Matrix<float, 4, 4> Rot_mat;

  
  void get_translation_mat(Eigen::Vector3d origin){
      T << 1,0,0, -origin(0),  
           0,1,0, -origin(1), 
           0,0,1, -origin(2),
           0,0,0, 1;

      T_ << 1,0,0, origin(0),
            0,1,0, origin(1),
            0,0,1, origin(2),
            0,0,0, 1;
  }
  
  void roate_on_ori(Eigen::Vector3d vec, float theta){
      auto u = vec(0);
      auto v = vec(1);
      auto w = vec(2);
      Rot_mat << pow(u,2) + (1-pow(u,2))*cos(theta), 
                 u*v*(1-cos(theta)) - w*sin(theta), 
                 u*w*(1-cos(theta)) + v*sin(theta), 
                 0,

                 u*v*(1-cos(theta)) + w*sin(theta),
                 pow(v,2) + (1-pow(v,2))*cos(theta),
                 v*w*(1-cos(theta)) - u*sin(theta),
                 0,

                 u*w*(1-cos(theta)) - v*sin(theta),
                 v*w*(1-cos(theta)) + u*sin(theta),
                 pow(w,2) + (1-pow(w,2))*cos(theta),
                 0,

                 0,
                 0,
                 0,
                 1;
  }


  void Compute(OpKernelContext* context) override {
    // Get input tensors

    const Tensor& coords = context->input(0);
    auto coords_tensor = coords.matrix<float>();

    const Tensor& atom_mask = context->input(1);
    auto atom_mask_tensor = atom_mask.matrix<int>();

    const Tensor& branch_rot_bond = context->input(2);
    auto branch_rot_bond_tensor = branch_rot_bond.matrix<int>();
    //const TensorShape& rot_bond_shape = t2.shape();

    const Tensor& t3 = context->input(3);
    auto bond_idx_ = t3.flat<int>();
    auto bond_idx = bond_idx_(0);

    const Tensor& t4 = context->input(4);
    auto rot_ang_ = t4.flat<float>();
    auto rot_ang = rot_ang_(0);

    const Tensor& t5 = context->input(5);
    auto side_ = t5.flat<int>();
    auto side = side_(0);


    //get rot vector
    
    for(int i = 0;i<branch_rot_bond.shape().dim_size(0);i++){
        Eigen::Vector3d vec; 
        Eigen::Vector3d start;
        vec(0) =  coords_tensor(branch_rot_bond_tensor(i,0),0) - 
                  coords_tensor(branch_rot_bond_tensor(i,1),0);

        vec(1) =  coords_tensor(branch_rot_bond_tensor(i,0),1) - 
                  coords_tensor(branch_rot_bond_tensor(i,1),1);

        vec(2) = coords_tensor(branch_rot_bond_tensor(i,0),2) - 
                 coords_tensor(branch_rot_bond_tensor(i,1),2);

        auto unit_v = vec/sqrt(vec.dot(vec));
        unit_vectors.push_back(unit_v);

        start(0) =  coords_tensor(branch_rot_bond_tensor(i,0),0);
        start(1) =  coords_tensor(branch_rot_bond_tensor(i,0),1);
        start(2) =  coords_tensor(branch_rot_bond_tensor(i,0),2);
        starts.push_back(start);
    }

    get_translation_mat(starts[bond_idx]);
    roate_on_ori(unit_vectors[bond_idx], rot_ang);
    
    const int atom_num = coords.shape().dim_size(0);
    Eigen::Matrix<float, Eigen::Dynamic, 4> ext_coords;
    ext_coords.resize(atom_num,4);
    ext_coords.fill(1);
    for(int i = 0;i<coords.shape().dim_size(0);i++){
        ext_coords(i,0) = coords_tensor(i,0);
        ext_coords(i,1) = coords_tensor(i,1);
        ext_coords(i,2) = coords_tensor(i,2);
    }


    auto trans1 = (T * ext_coords.transpose()).transpose();
    auto trans2 = (Rot_mat * trans1.transpose()).transpose();
    auto trans3 = ( T_ * trans2.transpose()).topRows(3).transpose();

    // set ouptut tensor shape
    TensorShape output_shape;
    output_shape.AddDim(coords.shape().dim_size(0));
    output_shape.AddDim(coords.shape().dim_size(1));

    
    // create an output tensor
    Tensor* output_tensor = NULL;
    OP_REQUIRES_OK(context, context->allocate_output(0, output_shape,
                                                     &output_tensor));


    // Set the output value 
    auto output_flat = output_tensor->flat<float>();
    for(int i = 0;i<coords.shape().dim_size(0);i++){
        if (atom_mask_tensor(bond_idx,i)==side){
            for(int j = 0;j<coords.shape().dim_size(1);j++){
                output_flat(i*coords.shape().dim_size(1) + j) = trans3(i,j);   
            }
        } else {
            for(int j = 0;j<coords.shape().dim_size(1);j++){
                output_flat(i*coords.shape().dim_size(1) + j) = coords_tensor(i,j);   
            }
        }
        
    }



  }

};

REGISTER_KERNEL_BUILDER(Name("RotateLigand").Device(DEVICE_CPU), RotateLigandOp);