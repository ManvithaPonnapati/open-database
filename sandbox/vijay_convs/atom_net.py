import numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom constants import CONSTANTS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFint_repeat_module = tf.load_op_library('/home/cosmynx/Documents/neighbor_listing/int_repeat.so')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFint_sequence_module = tf.load_op_library('/home/cosmynx/Documents/neighbor_listing/int_sequence.so')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#------------------------------LAYER CONSTRUCTION----------------------------------#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""Performs one shot expansion of distance matrix using the corresponding atoms."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef atom_type_conv(distance_matrix, corr_atoms):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#distance matrix and corr_atoms are of dimensions [batch_size, N, M]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#Return tensor shape E = [batch_size, N, M, Nat]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#obtain the source atoms, and eliminate "self-neighbors"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	source_atoms = tf.squeeze(corr_atoms[:, :, 0])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	distance_matrix = distance_matrix[:, :, 1:]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	corr_atoms = corr_atoms[:, :, 1:]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	corr_atoms_mask = corr_atoms > 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	atoms_one_hot = tf.one_hot(corr_atoms, CONSTANTS.atom_types)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	distance_matrix = tf.expand_dims(distance_matrix, -1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	distances_expanded = tf.multiply(distance_matrix, atoms_one_hot)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return distances_expanded, source_atoms, corr_atoms_mask123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""Performs radial pooling and essentially "sums" all pairwise interactions between123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF   some atom i and each atom type aj"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef radial_pooling(E, source_atoms, corr_atoms_mask):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#E is tensor of dimensions [batch_size, N, M, Nat]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#return tensor shape: P = [batch_size, N, Nat, Nr]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#TODO: Get rid of 0 (null) atoms that don't exist in neighbor listing123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#initialize the filters (with two parameters each - mean and std)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	filter_means = tf.Variable(tf.random_normal(shape=[CONSTANTS.atom_types+1, CONSTANTS.radial_filters], mean=3.0, stddev=1.5))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	filter_stds = tf.Variable(tf.constant(1.0, shape=[CONSTANTS.atom_types+1, CONSTANTS.radial_filters]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#embed the correct filters for each corresponding atom type123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	embed_means = tf.nn.embedding_lookup(params=filter_means, ids=source_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	embed_means = tf.expand_dims(tf.expand_dims(embed_means, 2), 2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	embed_stds = tf.nn.embedding_lookup(params=filter_stds, ids=source_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	embed_stds = tf.expand_dims(tf.expand_dims(embed_stds, 2), 2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#apply the Gaussian filters to create the corresponding output (vectorized)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	E = tf.expand_dims(E, axis=-1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	E_filtered = tf.exp(-((E-embed_means)/embed_stds) ** 2) #removed cosine part123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	E_filtered = E_filtered * tf.expand_dims(tf.expand_dims(tf.cast(corr_atoms_mask, tf.float32), -1), -1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	E_filtered = tf.multiply(E_filtered, tf.cast(tf.logical_and(E > 0, E < CONSTANTS.R_c), tf.float32))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	output = tf.reduce_sum(E_filtered, axis=2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	output = output * tf.constant(CONSTANTS.radial_scaling) + tf.constant(CONSTANTS.radial_bias)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return output123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""Performs the FC layer individually for each atom in the molecule. 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF   Does not depend on number of atoms, only on atom_types and radial_filters"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef fc_layer(input_tensor, keep_prob, source_atoms):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#input_tensor is of shape P = [batch_size, N, Nat*Nr]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#Return tensor shape: [batch_size, N] (energy for each atom)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#initialize the weights, one set for each atom type123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	input_dim = CONSTANTS.radial_filters * CONSTANTS.atom_types123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	weights = tf.Variable(tf.random_normal([CONSTANTS.atom_types+1, input_dim], mean=0, stddev=0.1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	biases = tf.Variable(tf.zeros([CONSTANTS.atom_types+1]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#embed the correct weights for each corresponding atom type123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	embed_weights = tf.nn.embedding_lookup(params=weights, ids=source_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	embed_biases = tf.nn.embedding_lookup(params=biases, ids=source_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	output = tf.reduce_sum(tf.multiply(input_tensor, embed_weights), axis=2) + embed_biases123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return output123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#-----------------------------------NETWORK----------------------------------------#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""We call compute_energy once for each molecule - protein, ligand, or complex.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF   Returns the energy of the corresponding molecule"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef compute_energy(distance_matrix, corr_atoms, keep_prob):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#1st conv layer: atom type convolution, one-hot expansion of distance matrix R123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	E1, source_atoms, corr_atoms_mask = atom_type_conv(distance_matrix, corr_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	P1 = radial_pooling(E1, source_atoms, corr_atoms_mask)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	P_flattened1 = tf.reshape(P1, shape=[CONSTANTS.batch_size, tf.shape(P1)[1], CONSTANTS.atom_types * CONSTANTS.radial_filters])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	output_energies = fc_layer(P_flattened1, keep_prob, source_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	output_energy = tf.reduce_mean(output_energies, axis=1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return output_energy123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""Calculates the change in energy for the complex in bound vs unbound states.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF   Regression task is done in main."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef atom_net(ligand_dists, ligand_atoms, receptor_dists, receptor_atoms, complex_dists, complex_atoms, keep_prob=1):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	ligand_energy = compute_energy(ligand_dists, ligand_atoms, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	receptor_energy = compute_energy(receptor_dists, receptor_atoms, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	complex_energy = compute_energy(complex_dists, complex_atoms, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	change_energy = complex_energy - ligand_energy - receptor_energy123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	binding_out = tf.expand_dims(change_energy/2, axis=1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	nonbinding_out = tf.expand_dims(-change_energy/2, axis=1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	return tf.concat([nonbinding_out, binding_out], axis=1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# input_dim = CONSTANTS.atom_types * CONSTANTS.radial_filters123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# #first hidden layer (128 hidden units)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# weights1 = tf.Variable(tf.random_normal([input_dim, CONSTANTS.hidden_units_1], mean=0, stddev=0.01))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# bias1 = tf.Variable(tf.zeros([CONSTANTS.hidden_units_1]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# expanded_weights1 = tf.tile(tf.expand_dims(weights1, 0), [CONSTANTS.batch_size, 1, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# hidden1 = tf.matmul(input_tensor, expanded_weights1) + bias1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# hidden_drop1 = tf.nn.dropout(hidden1, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# #second hidden layer (64 hidden units)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# weights2 = tf.Variable(tf.random_normal([CONSTANTS.hidden_units_1, CONSTANTS.hidden_units_2], mean=0, stddev=0.02))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# bias2 = tf.Variable(tf.zeros([CONSTANTS.hidden_units_2]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# expanded_weights2 = tf.tile(tf.expand_dims(weights2, 0), [CONSTANTS.batch_size, 1, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# hidden2 = tf.matmul(hidden_drop1, expanded_weights2) + bias2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# hidden_drop2 = tf.nn.dropout(hidden2, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# #final output layer123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# weights = tf.Variable(tf.random_normal([1, 1, CONSTANTS.hidden_units_2], mean=0, stddev=0.02))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# bias = tf.Variable(tf.constant(0.0))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# output = tf.squeeze(tf.multiply(hidden_drop2, weights) + bias)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# return tf.reduce_sum(output, axis=2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	#NEED TO FIX THIS PART LATER123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# #2nd conv layer: feed flattened output back123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# atom_list = int_sequence_module.int_sequence([1], [CONSTANTS.atom_types])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# repeats = int_repeat_module.int_repeat([CONSTANTS.radial_filters], [CONSTANTS.atom_types])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# #corresponding atoms is neighboring atom, so we can "see" two neighbors away123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# corr_atoms2 = int_repeat_module.int_repeat(atom_list, repeats)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# corr_atoms2 = tf.expand_dims(tf.expand_dims(corr_atoms2, 0), 0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# #ok to pass in "untiled" corr atoms because it broadcasts (multiplication)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# E2, _ = atom_type_conv(P_flattened1, corr_atoms2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# P2 = radial_pooling(E2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	# P_flattened2 = tf.reshape(P2, shape=[CONSTANTS.batch_size, tf.shape(P2)[1], CONSTANTS.atom_types * CONSTANTS.radial_filters])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF