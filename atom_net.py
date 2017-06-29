import numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom atom_main import CONSTANTS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#------------------------------LAYER CONSTRUCTION----------------------------------#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""Constructs a "neighbor" adjacency matrix and returns the interatomic distances123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF   between the atoms and its nearest neighbors, along with the corresponding123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF   atom types. Remember to check the paper to make sure this is done efficiently."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef preprocess(atoms, coords):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#atoms is of dimensions [batch_size, 1, N], coords [batch_size, 1, N, 3]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#TODO: MAKE THIS WORK - fix complexity, don't include atom itself in neighbors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#Return tensor shape R = [batch_size, N, M], Z123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	num_max_atoms = tf.size(tf.slice(atoms, begin=[0, 0], size=[1, -1]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	neighbor_dist = tf.ones(shape=[CONSTANTS.batch_size, num_max_atoms, CONSTANTS.neighbors], dtype=tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	neighbor_atoms = tf.ones(shape=[CONSTANTS.batch_size, num_max_atoms, CONSTANTS.neighbors], dtype=tf.int32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return neighbor_dist, neighbor_atoms123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef batched_preprocess(atoms, coords):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#get a matrix of distances between the atoms (tensor of shape [batch, N, N])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	coords_copy = tf.transpose(tf.expand_dims(coords, 0), perm=[0,2,1,3])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	distances = tf.sqrt(tf.reduce_sum(tf.square(coords-coords_copy), reduction_indices=[3]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#get the nearest neighbors using tf.nn.top_k, and the corresponding atoms123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	negative_distances = tf.multiply(distances, tf.constant(-1.0))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	neighbor_dist, neighbor_atom_indices = tf.nn.top_k(negative_distances, CONSTANTS.neighbors)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	neighbor_atoms = tf.gather(atoms, neighbor_atom_indices)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return neighbor_dist, neighbor_atoms123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""Performs one shot expansion of distance matrix using the corresponding atoms."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef atom_type_conv(distance_matrix, corr_atoms):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#distance matrix and corr_atoms are of dimensions [batch_size, N, M]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#Return tensor shape E = [batch_size, N, M, Nat]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	atoms_one_hot = tf.one_hot(corr_atoms, CONSTANTS.atom_types)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	distance_matrix = tf.expand_dims(distance_matrix, -1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	distances_expanded = tf.multiply(distance_matrix, atoms_one_hot)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return distances_expanded123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""Performs radial pooling and essentially "sums" all pairwise interactions between123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF   some atom i and each atom type aj"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef radial_pooling(E):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#E is tensor of dimensions [batch_size, N, M, Nat]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#return tensor shape: P = [batch_size, N, Nat, Nr]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#initialize the filters (with two parameters each - mean and std)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	filter_means = tf.Variable(tf.random_normal(shape=[CONSTANTS.radial_filters], mean=3.0, stddev=1.5))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	filter_stds = tf.Variable(tf.constant(1.0, shape=[CONSTANTS.radial_filters]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#for each filter, create the corresponding output (vectorized)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	E = tf.expand_dims(E, axis=-1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	E_filtered = tf.exp(tf.multiply(-tf.divide(tf.square(E-filter_means), tf.square(filter_stds)), 1.0/2 * tf.cos(np.pi * E/CONSTANTS.R_c)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	E_filtered = tf.multiply(E_filtered, tf.cast(tf.logical_and(E > 0, E < 12), tf.float32))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	output = tf.reduce_sum(E_filtered, axis=2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	output = tf.add(tf.multiply(output, tf.constant(CONSTANTS.radial_scaling)), tf.constant(CONSTANTS.radial_bias))	123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return output123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""Performs the FC layer individually for each atom in the molecule. 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF   Does not depend on number of atoms, only on atom_types and radial_filters"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef fc_layer(input_tensor):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#input_tensor is of shape P = [batch_size, N, Nat*Nr]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#Return tensor shape: [batch_size, N] (energy for each atom)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	input_dim = CONSTANTS.atom_types * CONSTANTS.radial_filters123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# initialize the bias to be 0.5 for random guessing and weights to not go "out of range" too much123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	weights = tf.Variable(tf.random_normal([1, 1, input_dim], stddev=1.0/input_dim))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	bias = tf.Variable(tf.constant(0.5))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	output = tf.squeeze(tf.multiply(input_tensor, weights) + bias)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return tf.reduce_sum(output, axis=2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#-----------------------------------NETWORK----------------------------------------#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""We call compute_energy once for each molecule - protein, ligand, or complex.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF   Returns the energy of the corresponding molecule"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef compute_energy(atoms, coords, keep_prob):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#preprocess: construct a neighbor adjacency matrix123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	R, Z = preprocess(atoms, coords)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#atom type convolution: one-hot expansion of distance matrix R123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	E = atom_type_conv(R, Z)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#radial pooling layer123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	P = radial_pooling(E)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#flatten the results for each atom in P123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	P_flattened = tf.reshape(P, shape=[CONSTANTS.batch_size, tf.shape(P)[1], CONSTANTS.atom_types * CONSTANTS.radial_filters])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#dropout123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	P_drop = tf.nn.dropout(P_flattened, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	output_energies = fc_layer(P_flattened)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	output_energy = tf.reduce_mean(output_energies, axis=1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return output_energy123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""Calculates the change in energy for the complex in bound vs unbound states.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF   Regression task is done in main."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef atom_net(ligand_atoms, ligand_coords, receptor_atoms, receptor_coords, complex_atoms, complex_coords, keep_prob=1):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	ligand_energy = compute_energy(ligand_atoms, ligand_coords, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	receptor_energy = compute_energy(receptor_atoms, receptor_coords, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	complex_energy = compute_energy(complex_atoms, complex_coords, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	change_energy = complex_energy - ligand_energy - receptor_energy123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#apply a negative sigmoid to final energy to get "probability the stuff binds"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	softmax_energy = tf.sigmoid(-change_energy)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return softmax_energy