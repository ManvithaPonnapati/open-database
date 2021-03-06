#include "tensorflow/core/framework/op_kernel.h"
#include "tensorflow/core/framework/op.h"
#include "tensorflow/core/framework/shape_inference.h"
#include "include/atom_constant.h"

using namespace tensorflow;

REGISTER_OP("Score")
    .Input("lignad: float32")
    .Input("lig_elem: int32")
    .Input("receptor: float32")
    .Input("rec_elem: int32")
    .Output("energy: float32");

class ScoreOp : public OpKernel {
 public:
  explicit ScoreOp(OpKernelConstruction* context) : OpKernel(context) {}
  // Define const value 
  const float const_v = 10000;
  const float const_cap = 100;
  const float const_cutoff = 8;
  const float const_smooth = 1;
  const float const_epsilon = 2.22045e-16;

  float vdw(float dist, float opt_dist, float m, float n){

      float vds_dist = dist;
      float c_i = std::pow(opt_dist, n) * m * 1.0 / ( n - m );
      float c_j = std::pow(opt_dist, m) * n * 1.0 / ( m - n );

      if ( vds_dist > ( opt_dist + const_smooth ) ){
            vds_dist -= const_smooth;
      }else if(vds_dist < ( opt_dist - const_smooth )){
            vds_dist += const_smooth;
      } else {
            vds_dist = opt_dist;
      }

      float r_i = std::pow(vds_dist, n);
      float r_j = std::pow(vds_dist, m);
      float e = 0;
      if ( r_i > const_epsilon or r_j > const_epsilon){
            e = std::min(const_cap, c_i/ r_i + c_j/ r_j); 
      } else {
            e = const_cap;
      }
      return  e;
  }

  float guass(float dist, float opt_dist, float o, float w){
      float e = std::exp(- std::pow(( dist - opt_dist - o) / w, 2));
      return e;
  }

  float replusion(float dist, float opt_dist, float offset){
    float rep_dif = dist - opt_dist - offset;
    float e = 0;
    if ( rep_dif < 0 ) {
          e = std::pow(rep_dif, 2);
    } else {
          e = 0;
    }
    return e;
  }

  float slope_step(float sur_dist, float good, float bad){
        if (bad < good){
              if (sur_dist <= bad){
                    return 0;
              }
              if (sur_dist >= good){
                    return 1;
              }
        }else{
              if (sur_dist >= bad){
                    return 0;
              }
              if (sur_dist <= good){
                    return 1;
              }
        }
        return 1.0 * (sur_dist - bad) / (good - bad);
  }

  float hydrophobic(float dist, float opt_dist, int atom_a, int atom_b, float good, float bad){
      if (atom_data[atom_a].xs_hydrophobe and atom_data[atom_b].xs_hydrophobe){
            float sur_dist = dist - opt_dist;
            float sloped = slope_step(sur_dist,good, bad );
            return sloped;
      } else{
            return 0;
      }
  }

  float non_dir_h_bond(float dist, float opt_dist, int atom_a, int atom_b, float good, float bad){
        if( xs_h_bond_possible(atom_a,atom_b)){
              float sur_dist = dist - opt_dist;
              float sloped = slope_step(sur_dist, good, bad);
              return sloped;
        } else{
              return 0;
        }
  }

  float curl(float energy){
    float e = energy;
    float tmp = 0;
    if (energy > 0){
          tmp = 1.0 * const_v / (const_v + e);
          e *= tmp;
    }
    return e;
  }



  void Compute(OpKernelContext* context) override {
    // Get input tensors
    const Tensor& ligand = context->input(0);
    const Tensor& ligand_elem = context->input(1);
    const Tensor& receptor = context->input(2);
    const Tensor& receptor_elem = context->input(3);    


    // get value of tensor
    auto lig_coords = ligand.matrix<float>();
    auto lig_elem = ligand_elem.flat<int>();
    auto rec_coords = receptor.matrix<float>();
    auto rec_elem = receptor_elem.flat<int>();

    // set ouptut tensor shape
    TensorShape output_shape;
    output_shape.AddDim(1);
    
    // create an output tensor
    Tensor* output_tensor = NULL;
    OP_REQUIRES_OK(context, context->allocate_output(0, output_shape,
                                                     &output_tensor));
    

    // calculate inter molecular energy
    float energy = 0;
    float energy_0, energy_1, energy_2, energy_3, energy_4 =0;
    auto a = ligand.shape().dim_size(0);
    for (int i = 0; i< ligand.shape().dim_size(0); i++){
      for (int j = 0; j< receptor.shape().dim_size(0);j++){
            
            float dist = std::sqrt(std::pow(lig_coords(i,0)-rec_coords(j,0),2)+
                                   std::pow(lig_coords(i,1)-rec_coords(j,1),2)+
                                   std::pow(lig_coords(i,2)-rec_coords(j,2),2));

            if (dist <= const_cutoff){
                float opt_dist = atom_data[lig_elem(i)].xs_radius + atom_data[rec_elem(j)].xs_radius;
                
                float sur_dist = dist - opt_dist;
                
                float this_energy = 0;
                float weight_energy = 0;
                float curl_energy = 0;
                
                // guass
                this_energy = guass(dist, opt_dist, 0., 0.5);
                weight_energy = this_energy * -0.035579;
                curl_energy = curl(weight_energy);
                energy_0 += this_energy;
                energy += curl_energy;
                

                // guass 
                this_energy = guass(dist, opt_dist, 3., 2.);
                weight_energy = this_energy * -0.005156;
                curl_energy = curl(weight_energy);
                energy_1 += this_energy;
                energy += curl_energy;

                //rep
                this_energy = replusion(dist, opt_dist, 0.);
                weight_energy = this_energy * 0.840245;
                curl_energy = curl(weight_energy);
                energy_2 += this_energy;
                energy += curl_energy;

                //hydrophobic
                this_energy = hydrophobic(dist, opt_dist, lig_elem(i), rec_elem(j),0.5, 1.5);
                weight_energy = this_energy * -0.035069;
                curl_energy = curl(weight_energy);
                energy_3 += this_energy;
                energy += curl_energy;

                this_energy = non_dir_h_bond(dist, opt_dist, lig_elem(i), rec_elem(j),-0.7, 0);
                weight_energy = this_energy * -0.587439;
                curl_energy = curl(weight_energy);
                energy_4 += this_energy;
                energy += curl_energy;

            }
           
      }
    }


    // Set the output value 
    auto output_flat = output_tensor->flat<float>();
    output_flat(0) = energy;
  }

};

REGISTER_KERNEL_BUILDER(Name("Score").Device(DEVICE_CPU), ScoreOp);