import time,os,sys
import tensorflow as tf
import numpy as np


sys.path.append('../../')
import affinity as af

import one_shot_input
from config import FLAGS
#import av4_networks
#import av4_input

# telling tensorflow how we want to randomly initialize weights

def train():
    "train a network"
    # it's better if all of the computations use a single session
    sess = tf.Session()

    # create a filename queue first
    filename_queue, examples_in_database = af.input.index_database_into_q(FLAGS.database_path, shuffle=True)

    # create an epoch counter
    batch_counter = tf.Variable(0)
    batch_counter_increment = tf.assign(batch_counter,tf.Variable(0).count_up_to(
        np.round((examples_in_database*FLAGS.num_training_epochs)/FLAGS.batch_size)))
    epoch_counter = tf.div(batch_counter*FLAGS.batch_size,examples_in_database)

    # create a custom shuffle queue
    _,current_epoch,_,xyz_label,image_batch = one_shot_input.image_and_label_queue(batch_size=FLAGS.batch_size,
                                                                    pixel_size=FLAGS.pixel_size,
                                                                    side_pixels=FLAGS.side_pixels,
                                                                    num_threads=FLAGS.num_threads,
                                                                    filename_queue=filename_queue,
                                                                    epoch_counter=epoch_counter)

    keep_prob = tf.placeholder(tf.float32)
    with tf.name_scope("network"):
        #ag_net = af.networks.ag_net()
        logits = af.networks.ag_net_2(image_batch,keep_prob,FLAGS.batch_size)

    raw_labels = xyz_label[:,3]
    norm_labels = raw_labels/(np.pi)
    shuffled_labels = tf.random_shuffle(norm_labels)

    norm_preds = tf.nn.softmax(tf.reshape(logits, [FLAGS.batch_size, 1, 2]))[:, 0, 1]

    cost = tf.abs(norm_labels - norm_preds)
    cost_mean = tf.reduce_mean(cost)
    shuffled_cost_mean = tf.reduce_mean(tf.abs(shuffled_labels-norm_preds))

    # optimize the cost of interest
    with tf.name_scope("optimizer"):
        train_step_run = tf.train.AdamOptimizer().minimize(cost_mean)

    # merge all summaries and create a file writer object
    merged_summaries = tf.summary.merge_all()
    train_writer = tf.summary.FileWriter((FLAGS.summaries_dir + '/' + str(FLAGS.run_index) + "_train"), sess.graph)

    # create saver to save and load the network state
    saver = tf.train.Saver(var_list=(tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope="optimizer")
                                     + tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope="network")))

    if FLAGS.saved_session is None:
        sess.run(tf.global_variables_initializer())
    else:
        sess.run(tf.global_variables_initializer())
        print "Restoring variables from sleep. This may take a while..."
        saver.restore(sess,FLAGS.saved_session)

    # visualization of certain parameters for debugging
    exmpl_lig_atoms = tf.reduce_sum(tf.cast(image_batch[0,:,:,:,0] >0, tf.float32))
    exmpl_rec_atoms = tf.reduce_sum(tf.cast((image_batch[0,:,:,:,1] >0), tf.float32))
    exmpl_label = raw_labels[0]
    exmpl_norm_label = norm_labels[0]
    exmpl_logit = logits[0]
    exmpl_norm_pred = norm_preds[0]
    exmpl_cost = cost[0]

    # launch all threads
    coord = tf.train.Coordinator()
    tf.get_default_graph().finalize()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)

    np.set_printoptions(precision=3)



    while True:
        # training block of the loop
        start = time.time()
        batch_num = sess.run(batch_counter_increment)
        epo,my_cost,_ = sess.run([current_epoch,cost_mean,train_step_run],
                     feed_dict={keep_prob: 0.5})
        print "epoch:",epo[0], "step:", batch_num,
        print "\tcost:", "%.2f" % my_cost,
        print "\texps:", "%.2f" % (FLAGS.batch_size / (time.time() - start))


        # visualization block of the loop
        if (batch_num % 20 == 19):
            my_lig_atoms, my_rec_atoms, my_label,my_norm_label,my_logit,my_norm_pred,my_cost \
                = sess.run([exmpl_lig_atoms,exmpl_rec_atoms,exmpl_label,exmpl_norm_label, exmpl_logit,
                            exmpl_norm_pred, exmpl_cost],
            feed_dict={keep_prob:0.5})
            print "lig atoms:", my_lig_atoms,
            print "rec atoms:", my_rec_atoms,
            print "raw labels:", my_label,
            print "norm label:", my_norm_label,
            print "raw logit:", my_logit,
            print "norm pred:", my_norm_pred,
            print "cos cost:", my_cost

            my_cost,my_shuffled_cost = sess.run([cost_mean,shuffled_cost_mean],feed_dict={keep_prob:1})
            print "cost:",my_cost,
            print "shuffled cost:", my_shuffled_cost


        # network saving block of the loop
        if (batch_num % 1000 == 999):
            # once in a while save the network state and write variable summaries to disk
            summaries = sess.run(merged_summaries, feed_dict={keep_prob: 1})
            train_writer.add_summary(summaries, batch_num)
            saver.save(sess, FLAGS.summaries_dir + '/' + str(FLAGS.run_index)
                       + "_netstate/saved_state", global_step=batch_num)


#class FLAGS:
#    """important model parameters"""
#
#    # size of one pixel generated from protein in Angstroms (float)
#    pixel_size = 1
#    # size of the box around the ligand in pixels
#    side_pixels = 20
#    # weights for each class for the scoring function
#    # number of times each example in the dataset will be read
#    num_epochs = 50000 # epochs are counted based on the number of the protein examples
#    # usually the dataset would have multiples frames of ligand binding to the same protein
#    # av4_input also has an oversampling algorithm.
#    # Example: if the dataset has 50 frames with 0 labels and 1 frame with 1 label, and we want to run it for 50 epochs,
#    # 50 * 2(oversampling) * 50(negative samples) = 50 * 100 = 5000
#    # num_classes = 2
#    # parameters to optimize runs on different machines for speed/performance
#    # number of vectors(images) in one batch
#    batch_size = 100
#    # number of background processes to fill the queue with images
#    num_threads = 512
#    # data directories#
#
#    # path to the csv file with names of images selected for training
#    database_path = "../../../datasets/labeled_av4"
#    # directory where to write variable summaries
#    summaries_dir = './summaries'
#    # optional saved session: network from which to load variable states
#    saved_session = None#'./summaries/2_netstate/saved_state-9999'


def main(_):
    """Create directoris two directories: one for the logs, one for the network state. Start the script.
    """
    summaries_dir = os.path.join(FLAGS.summaries_dir)
    # FLAGS.run_index defines when
    FLAGS.run_index = 1
    FLAGS.run_name = FLAGS.run_name + "_one_shot"
    while tf.gfile.Exists(summaries_dir + "/" + str(FLAGS.run_index) +'_netstate') \
            or tf.gfile.Exists(summaries_dir + "/" + str(FLAGS.run_index)+'_logs'):
        FLAGS.run_index += 1
    FLAGS.run_name = str(FLAGS.run_index) + "_" + FLAGS.run_name
    tf.gfile.MakeDirs(summaries_dir + "/" + FLAGS.run_name +'_netstate')
    tf.gfile.MakeDirs(summaries_dir + "/" + FLAGS.run_name +'_logs')
    train()

if __name__ == '__main__':
    tf.app.run()

