import os,time,sys
import tensorflow as tf
import numpy as np
from glob import glob
sys.path.append('../../')

#from av4_utils import geom_utils
#import av4_input
import affinity as af


def convert_protein_and_ligand_to_image(ligand_elements,ligand_coords,receptor_elements,
                                        receptor_coords,side_pixels,pixel_size):
    """Take coordinates and elements of protein and ligand and convert them into an image.
    Return image with one dimension so far."""

    # FIXME abandon ligand when it does not fit into the box (it's kept now)

    # max_num_attempts - maximum number of affine transforms for the ligand to be tried
    max_num_attemts = 1000
    # affine_transform_pool_size is the first(batch) dimension of tensor of transition matrices to be returned
    # affine tranform pool is only generated once in the beginning of training and randomly sampled afterwards
    affine_transform_pool_size = 10000

    # transform center ligand around zero
    ligand_center_of_mass = tf.reduce_mean(ligand_coords, reduction_indices=0)
    centered_ligand_coords = ligand_coords - ligand_center_of_mass
    centered_receptor_coords = receptor_coords - ligand_center_of_mass

    # use TF while loop to find such an affine transform matrix that can fit the ligand so that no atoms are outside
    box_size = (tf.cast(side_pixels, tf.float32) * pixel_size)


    def generate_transition_matrix(attempt,transition_matrix,batch_of_transition_matrices):
        """Takes initial coordinates of the ligand, generates a random affine transform matrix
        and transforms coordinates.
        """
        transition_matrix= tf.gather(batch_of_transition_matrices,tf.random_uniform([],
                                                                                    minval=0,
                                                                                    maxval=affine_transform_pool_size,
                                                                                    dtype=tf.int32))
        attempt += 1
        return attempt, transition_matrix,batch_of_transition_matrices

    def not_all_in_the_box(attempt, transition_matrix,batch_of_transition_matrices,
                           ligand_coords=centered_ligand_coords,box_size=box_size,
                           max_num_attempts=max_num_attemts):
        """Takes affine transform matrix and box dimensions, performs the transformation, and checks if all atoms
        are in the box."""
        transformed_coords, transition_matrix = af.geom.affine_tform(ligand_coords, transition_matrix)
        not_all = tf.cast(tf.reduce_max(tf.cast(tf.square(box_size*0.5) - tf.square(transformed_coords) < 0,tf.int32)),
                          tf.bool)
        within_iteration_limit = tf.cast(tf.reduce_sum(tf.cast(attempt < max_num_attemts, tf.float32)), tf.bool)
        return tf.logical_and(within_iteration_limit, not_all)

    attempt = tf.Variable(tf.constant(0, shape=[1]))
    batch_of_transition_matrices = tf.Variable(af.geom.gen_affine_tform(affine_transform_pool_size))
    transition_matrix = tf.gather(batch_of_transition_matrices, tf.random_uniform([], minval=0,
                                                                                  maxval=affine_transform_pool_size-1,
                                                                                  dtype=tf.int64))

    last_attempt,final_transition_matrix,_ = tf.while_loop(not_all_in_the_box, generate_transition_matrix,
                                                           [attempt, transition_matrix,batch_of_transition_matrices],
                                                           parallel_iterations=1)

    # rotate receptor and ligand using an affine transform matrix found
    rotatated_ligand_coords,_ = af.geom.affine_tform(centered_ligand_coords,final_transition_matrix)
    rotated_receptor_coords,_ = af.geom.affine_tform(centered_receptor_coords,final_transition_matrix)

    # check if all of the atoms are in the box, if not set the ligand to 0, but do not raise an error
    def set_elements_coords_zero(): return tf.constant([0],dtype=tf.int32),tf.constant([[0,0,0]],dtype=tf.float32)
    def keep_elements_coords(): return ligand_elements, rotatated_ligand_coords
    not_all = tf.cast(tf.reduce_max(tf.cast(tf.square(box_size * 0.5) - tf.square(rotatated_ligand_coords) < 0,
                                            tf.int32)),tf.bool)
    ligand_elements,rotatated_ligand_coords = tf.case({tf.equal(not_all,tf.constant(True)): set_elements_coords_zero},
                                                      keep_elements_coords)

    # move receptor randomly
    label_transition_matrices, xyz_labels = af.geom.gen_affine_tform_with_labels(affine_transform_pool_size,
									                                          x_rot_range=tf.convert_to_tensor(np.pi),
                                                                              #y_rot_range=tf.convert_to_tensor(np.pi))#,
                                                                              #z_rot_range=tf.convert_to_tensor(np.pi),#,
                                                                              #shift_partitions=1,
                                                                              #rot_partitions = 1,
                                                                              abs=True)

    # rec_transition_matrices = tf.Variable(affine_initializer)
    random_slice = tf.random_uniform([], minval=0, maxval=affine_transform_pool_size, dtype=tf.int64)
    label_transition_matrix = tf.gather(label_transition_matrices,random_slice)
    xyz_label = tf.gather(xyz_labels, random_slice)
    twice_rotated_receptor_coords,_ = af.geom.affine_tform(rotated_receptor_coords,label_transition_matrix)

    # move coordinates of a complex to an integer number so as to put every atom on a grid
    # ceiled coords is an integer number out of real coordinates that corresponds to the index on the cell
    # epsilon - potentially, there might be very small rounding errors leading to additional indexes
    epsilon = tf.constant(0.999, dtype=tf.float32)
    ceiled_ligand_coords = tf.cast(tf.round((-0.5 + (tf.cast(side_pixels,tf.float32)*0.5) +
                                             (rotatated_ligand_coords/pixel_size))*epsilon),tf.int64)
    ceiled_receptor_coords = tf.cast(tf.round((-0.5 + (tf.cast(side_pixels, tf.float32) * 0.5) +
                                               (twice_rotated_receptor_coords/pixel_size))*epsilon),tf.int64)

    # crop atoms of the protein that do not fit inside the box
    top_filter = tf.reduce_max(ceiled_receptor_coords,reduction_indices=1)<side_pixels
    bottom_filter = tf.reduce_min(ceiled_receptor_coords,reduction_indices=1)>0
    retain_atoms = tf.logical_and(top_filter,bottom_filter)
    cropped_receptor_coords = tf.boolean_mask(ceiled_receptor_coords,retain_atoms)
    cropped_receptor_elements = tf.boolean_mask(receptor_elements,retain_atoms)

    # merge protein and ligand together. In this case an arbitrary value of 10 is added to the ligand
    lig_coords_d = tf.concat([ceiled_ligand_coords,tf.expand_dims(tf.zeros([tf.shape(ceiled_ligand_coords)[0]],
                                                                          dtype=tf.int64),1)],1)
    rec_coords_d = tf.concat([cropped_receptor_coords,tf.expand_dims(tf.ones([tf.shape(cropped_receptor_coords)[0]],
                                                                             dtype=tf.int64),1)],1)
    complex_coords_d = tf.concat([lig_coords_d,rec_coords_d],0)
    complex_elements = tf.cast(tf.concat([ligand_elements, cropped_receptor_elements],0),tf.float32)

    # in coordinates of a protein rounded to the nearest integer can be represented as indices of a sparse 3D tensor
    # values from the atom dictionary can be represented as values of a sparse tensor
    # in this case TF's sparse_tensor_to_dense can be used to generate an image out of rounded coordinates

    # move elemets to the dimension of depth
    #complex_coords_4d = tf.concat([complex_coords, tf.reshape(tf.cast(complex_elements - 1, dtype=tf.int64), [-1, 1])],1)
    sparse_image = tf.SparseTensor(indices=complex_coords_d, values=complex_elements,
                                   dense_shape=[side_pixels,side_pixels,side_pixels,2])
    dense_image = tf.sparse_tensor_to_dense(sparse_image, validate_indices=False)

    # FIXME: try to save an image and see how it looks like
    return dense_image,ligand_center_of_mass,final_transition_matrix,xyz_label

def image_and_label_queue(batch_size,pixel_size,side_pixels,num_threads,filename_queue,epoch_counter,train=True):
    """Creates shuffle queue for training the network"""

    # read one receptor and stack of ligands; choose one of the ligands from the stack according to epoch
    ligand_file,current_epoch,label,ligand_elements,ligand_coords,receptor_elements,receptor_coords = \
        af.input.read_rec_and_lig(filename_queue,epoch_counter=epoch_counter,lig_frame='ZERO')

    # convert coordinates of ligand and protein into an image
    dense_image,_,_,xyz_label = convert_protein_and_ligand_to_image(
        ligand_elements,ligand_coords,receptor_elements,receptor_coords,side_pixels,pixel_size)

    # create a batch of proteins and ligands to read them together
    multithread_batch = tf.train.batch([ligand_file, current_epoch, label,xyz_label, dense_image],
                                       batch_size,
                                       num_threads=num_threads,
                                       capacity=batch_size * 3,
                                       dynamic_pad=True,
                                       shapes=[[],[], [], [6], [side_pixels,side_pixels,side_pixels,2]])
    return multithread_batch
