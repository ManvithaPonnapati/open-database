import time, sys, os123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport affinity.geom123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport affinity.input123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport affinity.nn123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport affinity.networks123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass AtomicNet(affinity.networks.AtomicNetworks):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def __init__(self, b_size, keep_prob):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.batch_size = b_size123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.keep_prob = keep_prob123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.atom_types = 9123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.radial_filters = 5123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.filter_means = tf.Variable(tf.random_normal(shape=[ 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            (self.atom_types+1)**2, self.radial_filters], mean=3.0, stddev=1.5))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.filter_stds = tf.Variable(tf.constant(1.0,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            shape=[(self.atom_types+1)**2, self.radial_filters]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.radial_cutoff = 12 # maximum interaction distance123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.radial_scaling = 1.0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.radial_bias = 0.0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.hidden_units1 = 128123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.fc1_w = tf.Variable(tf.random_normal(shape=[self.atom_types+1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.atom_types * self.radial_filters, self.hidden_units1], 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            mean=0.0, stddev=0.1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.fc1_b = tf.Variable(tf.zeros([self.atom_types+1, self.hidden_units1]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.hidden_units2 = 128123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.fc2_w = tf.Variable(tf.random_normal(shape=[self.atom_types+1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.hidden_units1, self.hidden_units2], mean=0.0, stddev=0.1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.fc2_b = tf.Variable(tf.zeros([self.atom_types+1, self.hidden_units2]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.hidden_units3 = 64123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.fc3_w = tf.Variable(tf.random_normal(shape=[self.atom_types+1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.hidden_units2, self.hidden_units3], mean=0.0, stddev=0.1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.fc3_b = tf.Variable(tf.zeros([self.atom_types+1, self.hidden_units3]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.out_w = tf.Variable(tf.random_normal(shape=[self.atom_types+1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.hidden_units3, 1], mean=0.0, stddev=0.1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.out_b = tf.Variable(tf.zeros([self.atom_types+1, 1]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        super(AtomicNet, self).__init__(self.batch_size)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def _single_ex_pipeline(self, input_q):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_stream = input_q.dequeue()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lig_coords = input_stream[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lig_nbr_idx = input_stream[1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lig_nbr_atoms = input_stream[2]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lig_elem = input_stream[3]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rec_coords = input_stream[4]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rec_nbr_idx = input_stream[5]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rec_nbr_atoms = input_stream[6]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rec_elem = input_stream[7]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        comp_coords = input_stream[8]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        comp_nbr_idx = input_stream[9]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        comp_nbr_atoms = input_stream[10]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        comp_elem = input_stream[11]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        transit_pars = input_stream[12:] #12: epoch, 13: label123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        def compute_energy(coords, nbr_idx, nbr_atoms, source_atoms, keep_prob):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            nbr_atoms_mask = nbr_atoms > 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            feature_matrix = affinity.nn.atomic_convolution_layer(self.filter_means,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                self.filter_stds, self.radial_filters, coords, source_atoms, 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                nbr_idx, nbr_atoms, nbr_atoms_mask, atom_types=self.atom_types,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                batch_size=1, radial_cutoff=self.radial_cutoff, neighbors=12, 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                radial_scaling=self.radial_scaling, radial_bias=self.radial_bias)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            feature_matrix = affinity.nn.atomistic_fc_layer(self.fc1_w, self.fc1_b,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                feature_matrix, source_atoms, self.atom_types*self.radial_filters,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                self.hidden_units1, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            feature_matrix = affinity.nn.atomistic_fc_layer(self.fc2_w, self.fc2_b,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                feature_matrix, source_atoms, self.hidden_units1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                self.hidden_units2, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            feature_matrix = affinity.nn.atomistic_fc_layer(self.fc3_w, self.fc3_b,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                feature_matrix, source_atoms, self.hidden_units2,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                self.hidden_units3, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            molecule_energy = affinity.nn.atomistic_output_layer(self.out_w, 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                self.out_b, feature_matrix, source_atoms, sum_atoms=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return molecule_energy123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lig_energy = compute_energy(lig_coords, lig_nbr_idx, lig_nbr_atoms, lig_elem, self.keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rec_energy = compute_energy(rec_coords, rec_nbr_idx, rec_nbr_atoms, rec_elem, self.keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        comp_energy = compute_energy(comp_coords, comp_nbr_idx, comp_nbr_atoms, comp_elem, self.keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        change_energy = comp_energy - lig_energy - rec_energy123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return [change_energy], transit_pars123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def _batch_pipeline(self, b_feat):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return b_feat123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def compute_output(self, input_q):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        predicted_energies, b_transit_pars = self._make_batch(input_q)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        predicted_energies = self._batch_pipeline(predicted_energies)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return predicted_energies, b_transit_pars123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF