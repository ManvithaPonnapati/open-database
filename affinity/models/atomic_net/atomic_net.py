import tensorflow as tf 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport time, sys, os, logging, threading123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport affinity as af 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom config import FLAGS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtf.logging.set_verbosity(tf.logging.DEBUG)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFlogging.basicConfig(level=logging.DEBUG)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsess = tf.Session(config=tf.ConfigProto(intra_op_parallelism_threads=8,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF										inter_op_parallelism_threads=8))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFcoord = tf.train.Coordinator()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFinput_pipe = af.input.InputPipePDBBind(sess, coord, db_path=FLAGS.database_path, num_threads=FLAGS.num_threads)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFinput_q = input_pipe.self_assemble("lig_coords", "lig_nbr_idx", "lig_nbr_atoms",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	"lig_elem", "rec_coords", "rec_nbr_idx", "rec_nbr_atoms", "rec_elem",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	"comp_coords", "comp_nbr_idx", "comp_nbr_atoms", "comp_elem", "epoch", "label")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFnetwork = af.networks.AtomicNet(b_size=FLAGS.batch_size, keep_prob=FLAGS.keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFpredicted_energies, b_transit_pars = network.compute_output(input_q)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFepoch = b_transit_pars[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFlabels = tf.cast(b_transit_pars[1], tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFl2_loss = (predicted_energies - labels) ** 2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFl2_loss_mean = tf.reduce_mean(l2_loss)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtrain_step_run = tf.train.AdamOptimizer(learning_rate=FLAGS.learning_rate).minimize(l2_loss_mean)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsess.run(tf.global_variables_initializer())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtf.train.start_queue_runners(sess, coord)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFinput_pipe.start_threads()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtf.get_default_graph().finalize()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#while epoch < 100:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFwhile True:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	start = time.time()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	print sess.run([l2_loss_mean, train_step_run])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF	print 'exps:', '%.2f' % (FLAGS.batch_size / (time.time() - start))