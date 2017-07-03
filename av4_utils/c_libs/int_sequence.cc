/* TO COMPILE THIS OP:

Enter the following two lines into terminal in the same folder as this .cc file:
    TF_INC=$(python -c 'import tensorflow as tf; print(tf.sysconfig.get_include())')
    g++ -std=c++11 -shared int_sequence.cc -o int_sequence.so -fPIC -I $TF_INC -O2

NOTE: tensorflow is compiled with gcc4. If you have gcc>=5, please add:
    -D_GLIBCXX_USE_CXX11_ABI=0
to the second line. This makes the library compatible with older C++ ABI. 

TO USE THIS OP:

In the script you wish to use this op, include the line:
    int_sequence_module = tf.load_op_library('/...(filename_path)/int_sequence.so')
Once you have loaded the library, you can treat it as any other python library and call
    int_sequence.module.int_sequence(starts, lengths)
*/

// Define the op's interface

#include "tensorflow/core/framework/op.h"
#include "tensorflow/core/framework/shape_inference.h"

using namespace tensorflow;

REGISTER_OP("IntSequence")
    .Input("starts: int32")
    .Input("lengths: int32")
    .Output("return_sequence: int32")
    .SetShapeFn([](::tensorflow::shape_inference::InferenceContext* c) {
        ::tensorflow::shape_inference::ShapeHandle starts_shape;
        TF_RETURN_IF_ERROR(c->WithRank(c->input(0), 1, &starts_shape));

        ::tensorflow::shape_inference::ShapeHandle lengths_shape;
        TF_RETURN_IF_ERROR(c->WithRank(c->input(1), 1, &lengths_shape));

        ::tensorflow::shape_inference::ShapeHandle output_shape = c->UnknownShapeOfRank(1);
        c->set_output(0, output_shape);
        return Status::OK();
    });


// Implement the kernel for the op

#include "tensorflow/core/framework/op_kernel.h"

class IntSequenceOp : public OpKernel {
public:
    explicit IntSequenceOp(OpKernelConstruction* context) : OpKernel(context) {}

    void Compute(OpKernelContext* context) override {
        // get the starts tensor
        const Tensor& input0 = context->input(0);
        auto starts = input0.flat<int32>();

        // get the lengths tensor
        const Tensor& input1 = context->input(1);
        auto lengths = input1.flat<int32>();

        int num_vals = 0; // size of output array 
        int num_seqs = starts.size(); // number of distinct sequences
        for (int i = 0; i < num_seqs; i++) {
            num_vals += lengths(i);
        }

        // Create an output tensor
        Tensor* output_tensor = NULL;
        OP_REQUIRES_OK(context, context->allocate_output(0, {num_vals}, &output_tensor));

        auto output = output_tensor->flat<int32>();

        // create an index variable to loop through the output
        int index = 0;
        for (int i = 0; i < num_seqs; i++) {
            // loop through the different sequences
            int curr_val = starts(i);
            for (int j = 0; j < lengths(i); j++) {
                output(index) = curr_val;
                index += 1;
                curr_val += 1;
            }
        }
    }
};

REGISTER_KERNEL_BUILDER(Name("IntSequence").Device(DEVICE_CPU), IntSequenceOp);