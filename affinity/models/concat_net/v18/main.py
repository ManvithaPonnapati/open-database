import tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport time,sys,os,logging,threading123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport affinity as af123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom net import ConcatNet123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom config import FLAGS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtf.logging.set_verbosity(tf.logging.DEBUG)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFlogging.basicConfig(level=logging.DEBUG)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsess = tf.Session()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFcoord = tf.train.Coordinator()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFinput_pipe = af.input.InputPipeVDS1(sess,coord,pairlist_dist=0.01,bindsite_radii=8.66,db_path=FLAGS.db_path,num_threads=25)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFinput_q = input_pipe.self_assemble("lig_elem","lig_coord","rec_elem","rec_coord",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                   "ll_pairs","ll_rel_coords","lr_pairs","lr_rel_coords",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                   "rr_pairs","rr_rel_coords","rl_pairs","rl_rel_coords",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                   "lig_label","lig_file")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFnetwork = ConcatNet(b_size=FLAGS.b_size)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFkeep_prob = tf.placeholder(tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFb_logits,b_transit_pars = network.compute_output(input_q,keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# print network123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFb_lig_label = b_transit_pars[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFb_lig_file = b_transit_pars[1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFb_cost = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=b_lig_label,logits=b_logits)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFcost = tf.reduce_mean(b_cost)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtrain_step_run = tf.train.AdamOptimizer().minimize(cost)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsess.run(tf.global_variables_initializer())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtf.train.start_queue_runners(sess,coord)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFinput_pipe.start_threads()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtf.get_default_graph().finalize()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#todo while input_pipe.epoch_counter < 10:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfor b_num in range(1000000):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    start = time.time()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    my_cost,_ = sess.run([cost,train_step_run],feed_dict={keep_prob:0.5})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "batch:",b_num,"cost:",my_cost, "exps:", "%.3f" % (FLAGS.b_size / (time.time() - start))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if (b_num % 20 == 19):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        my_cost = sess.run([cost],feed_dict={keep_prob:1})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "batch:", b_num, "no dropout cost:", my_cost123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#input_pipe.stop_threads()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF