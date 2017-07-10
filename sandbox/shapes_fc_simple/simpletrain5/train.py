#!/usr/bin/env python123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# -*- coding: utf-8 -*-123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport base64123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom datetime import datetime123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport st5123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom utils import *123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef train():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Make logging very verbose123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.logging.set_verbosity(tf.logging.DEBUG)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.Session(config=tf.ConfigProto(log_device_placement=False, operation_timeout_in_ms=600000)) as sess: # Stop after 10 minutes123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Get images and labels for MSHAPES123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Setting up getting batches and labels")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        filequeue, images_batch, labels_batch = st5.inputs(eval_data=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Got two batches")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Image batch shape: ")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print(images_batch.get_shape())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Labels batch shape:")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print(labels_batch.get_shape())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        global_step = tf.contrib.framework.get_or_create_global_step()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Build a Graph that computes the logits predictions from the123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # inference model.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        logits = st5.inference(images_batch)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Calculate loss.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        loss = st5.loss(logits, labels_batch)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Build a Graph that trains the model with one batch of examples and123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # updates the model parameters.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        train_op = st5.train(loss, global_step)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Actually running now")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        saver = tf.train.Saver(var_list=(tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if FLAGS.RESTORE:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print("Restoring...")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            saver = tf.train.Saver()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            saver.restore(sess, FLAGS.RESTORE_FROM)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print("Restored.")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print("Initializing global variables")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            tf.set_random_seed(42)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            tf.global_variables_initializer().run()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print("Finished")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Starting coordinator and queue runners")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        coord = tf.train.Coordinator()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        threads = tf.train.start_queue_runners(coord=coord, sess=sess)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Ok")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # tf.group(enqueues, reenqueues)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # enqueue everything as needed123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # e = sess.run([enqueues])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # print("Enqueue result ")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # print(e)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # queue_size = sess.run(filequeue.size())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # print("Initial queue size: " + str(queue_size))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for i in xrange(0, 10000000):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # print("blah")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            _, my_loss = sess.run([train_op, loss])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # sess.run([reenqueues])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # m = tf.group(train_op, reenqueues)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # _, my_loss = sess.run([m, loss])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # queue_size = sess.run(filequeue.size())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # print("Queue size: " + str(queue_size))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ml = np.array(my_loss)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print('Step: %d     Cross entropy loss: % 6.2f' % (i, ml))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if i % 1000 == 0 and i != 0:  # Every 1000 steps, save the results and send an email123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                print("NS")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                notify("Current cross-entropy loss: " + str(ml) + ".", subject="Running stats [step " + str(i) + "]")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                saver.save(sess, "summaries/netstate/saved_state", global_step=i)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                # saver.save(sess, "summaries/netstate/saved_state/model.ckpt")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if np.isnan(ml):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                print("Oops")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                notify("Diverged :(", subject="Process ended")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                sys.exit(0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # Get an image tensor and print its value.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # print("Getting image tensor")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # image_tensor = sess.run([images_batch])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # print("Got image tensor")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # print(image_tensor[0][50, 50, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # it = np.array(image_tensor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # print(np.shape(it))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # image1 = image_tensor[0][0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # it = np.array(image1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # print(np.shape(it))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # w, h = 200, 100123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # data = np.zeros((h, w, 3), dtype=np.uint8)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # data[50, 50] = [255, 0, 0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # img = Image.fromarray(it, 'RGB')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # img.save('my.png')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # img.show()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Ok done with that")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Finish off the filename queue coordinator.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Requesting thread stop")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        coord.request_stop()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Ok")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Joining threads")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        coord.join(threads)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Ok")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Finished")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef main(argv=None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Hello, world! v5")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # notify("Running simple4train/train.py", subject="Hi!!!")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    missing_dependencies = check_dependencies_installed()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if len(missing_dependencies) > 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise Exception("Not all dependencies are installed! (Missing packages " + ' and '.join(missing_dependencies) +123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                        "). See README.md for details.")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if get_hostname() == "lebennin-vm":123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Привет!")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Download and extract the dataset if it's missing (only on Titan)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Setting up dataset...")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if get_hostname() == "titan" or FLAGS.CHECK_DATASET:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        maybe_download_and_extract()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Done.")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Run some checks on the dataset to make sure it's correct123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Running tests...")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    verify_dataset()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("All tests passed.")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Clean up directories123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Cleaning up directories...")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if tf.gfile.Exists(FLAGS.train_dir):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.gfile.DeleteRecursively(FLAGS.train_dir)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.gfile.MakeDirs(FLAGS.train_dir)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.gfile.MakeDirs("summaries/netstate")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Done.")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Get images and labels for MSHAPES123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # print("Setting up getting batches and labels")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # enqueues, reenqueues, images_batch, labels_batch = st4.inputs(eval_data=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # print("Got two batches")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # print("Image batch shape: ")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # print(images_batch.get_shape())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # print("Labels batch shape:")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # print(labels_batch.get_shape())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Train the network!!123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    train()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif __name__ == '__main__':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.app.run()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF