import time, sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport affinity.geom123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport affinity.input123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport affinity.nn123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport affinity.networks123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# telling tensorflow how we want to randomly initialize weights123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef weight_variable(shape):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    initial = tf.truncated_normal(shape, stddev=0.005)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return tf.Variable(initial)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef bias_variable(shape):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    initial = tf.constant(0.01, shape=shape)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return tf.Variable(initial)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass ConcatNet(affinity.networks.AtomicNetworks):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def __init__(self,b_size):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # variables for concat Graham convolution 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conc_ll_w1 = weight_variable([21 * 21 * 21, 2, 200])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conc_lr_w1 = weight_variable([21 * 21 * 21, 2, 200])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conc_rr_w1 = weight_variable([21 * 21 * 21, 2, 100])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conc_rl_w1 = weight_variable([21 * 21 * 21, 2, 100])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conc_ll_b1 = bias_variable([200])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conc_lr_b1 = bias_variable([200])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conc_rr_b1 = bias_variable([100])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conc_rl_b1 = bias_variable([100])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.pix_size_1 = 0.5123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.fc1_w = weight_variable([300, 256])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.fc1_b = bias_variable([256])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.fc2_w = weight_variable([256, 2])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.fc2_b = bias_variable([2])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.b_size = b_size123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        super(ConcatNet, self).__init__(self.b_size)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def _single_ex_pipeline(self,input_q):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        transit pars are not required by the network123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        :param input_q:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        input_stream = input_q.dequeue()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lig_elem = input_stream[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lig_coord = input_stream[1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rec_elem = input_stream[2]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rec_coord = input_stream[3]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ll_pairs = input_stream[4]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ll_rel_coords = input_stream[5]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lr_pairs = input_stream[6]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lr_rel_coords = input_stream[7]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rr_pairs = input_stream[8]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rr_rel_coords = input_stream[9]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rl_pairs = input_stream[10]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rl_rel_coords = input_stream[11]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        transit_pars = input_stream[12:]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        l_feat_0 = tf.to_float(tf.expand_dims(lig_elem, 1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        r_feat_0 = tf.to_float(tf.expand_dims(rec_elem, 1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        l_feat_1, r_feat_1 = affinity.nn.concat_nonlinear_conv3d(s_feat=l_feat_0,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 d_feat=r_feat_0,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 ss_pairs=ll_pairs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 sd_pairs=lr_pairs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 dd_pairs=rr_pairs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 ds_pairs=rl_pairs,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 ss_rel_coords=ll_rel_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 sd_rel_coords=lr_rel_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 dd_rel_coords=rr_rel_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 ds_rel_coords=rl_rel_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 ss_w=self.conc_ll_w1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 sd_w=self.conc_lr_w1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 dd_w=self.conc_rr_w1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 ds_w=self.conc_rl_w1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 ss_b=self.conc_ll_b1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 sd_b=self.conc_lr_w1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 dd_b=self.conc_rr_b1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 ds_b=self.conc_rl_b1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                 pix_size=self.pix_size_1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        l_act_1 = tf.nn.relu(l_feat_1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        r_act_1 = tf.nn.relu(r_feat_1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        l_atomsum = tf.reduce_sum(l_act_1, reduction_indices=0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        r_atomsum = tf.reduce_sum(r_act_1, reduction_indices=0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return [l_atomsum,r_atomsum],transit_pars123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def _batch_pipeline(self,b_feat):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        :param b_feat:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_fc1 = tf.nn.relu(tf.matmul(b_feat, self.fc1_w) + self.fc1_b)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_fc2 = tf.matmul(h_fc1, self.fc2_w) + self.fc2_b123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return h_fc2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def compute_output(self,input_q):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        b_net_feats,b_transit_pars = self._make_batch(input_q)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        b_l_atomsum = b_net_feats[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        b_r_atomsum = b_net_feats[1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        b_atomsum = tf.concat([b_l_atomsum,b_r_atomsum],1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        b_logits = self._batch_pipeline(b_atomsum)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return b_logits,b_transit_pars123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF