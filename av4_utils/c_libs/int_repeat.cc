// Define the op's interface

#include "tensorflow/core/framework/op.h"
#include "tensorflow/core/framework/shape_inference.h"

using namespace tensorflow;

REGISTER_OP("IntRepeat")
    .Input("integers: int32")
    .Input("repeats: int32")
    .Output("return_sequence: int32")
    .SetShapeFn([](::tensorflow::shape_inference::InferenceContext* c) {
        ::tensorflow::shape_inference::ShapeHandle integers_shape;
        TF_RETURN_IF_ERROR(c->WithRank(c->input(0), 1, &integers_shape));

        ::tensorflow::shape_inference::ShapeHandle repeats_shape;
        TF_RETURN_IF_ERROR(c->WithRank(c->input(1), 1, &repeats_shape));

        ::tensorflow::shape_inference::ShapeHandle output_shape = c->UnknownShapeOfRank(1);
        c->set_output(0, output_shape);
        return Status::OK();
    });


// Implement the kernel for the op

#include "tensorflow/core/framework/op_kernel.h"

class IntRepeatOp : public OpKernel {
public:
    explicit IntRepeatOp(OpKernelConstruction* context) : OpKernel(context) {}

    void Compute(OpKernelContext* context) override {
        // get the starts tensor
        const Tensor& input0 = context->input(0);
        auto integers = input0.flat<int32>();

        // get the lengths tensor
        const Tensor& input1 = context->input(1);
        auto repeats = input1.flat<int32>();

        int num_vals = 0; // size of output array 
        int num_seqs = integers.size(); // number of distinct ints
        for (int i = 0; i < num_seqs; i++) {
            num_vals += repeats(i);
        }

        // Create an output tensor
        Tensor* output_tensor = NULL;
        OP_REQUIRES_OK(context, context->allocate_output(0, {num_vals}, &output_tensor));

        auto output = output_tensor->flat<int32>();

        // create an index variable to loop through the output
        int index = 0;
        for (int i = 0; i < num_seqs; i++) {
            int curr_val = integers(i);
            for (int j = 0; j < repeats(i); j++) {
                output(index) = curr_val;
                index += 1;
            }
        }
    }
};

REGISTER_KERNEL_BUILDER(Name("IntRepeat").Device(DEVICE_CPU), IntRepeatOp);