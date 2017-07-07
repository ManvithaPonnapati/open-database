#!/usr/bin/env python123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# -*- coding: utf-8 -*-123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom six.moves import xrange123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom simpletrain4 import st4123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom utils import *123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif get_hostname() == "lebennin-vm":123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Привет!")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# Download and extract the dataset if it's missing123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFprint("Setting up dataset...")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFmaybe_download_and_extract()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFprint("Done.")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# Run some checks on the dataset to make sure it's correct123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFprint("Running tests...")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFverify_dataset()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFprint("All tests passed.")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# Clean up directories123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFprint("Cleaning up directories...")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif tf.gfile.Exists(FLAGS.train_dir):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.gfile.DeleteRecursively(FLAGS.train_dir)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtf.gfile.MakeDirs(FLAGS.train_dir)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFprint("Done.")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# Get images and labels for MSHAPES123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFprint("Setting up getting batches and labels")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFenqueues, images_batch, labels_batch = st4.inputs(eval_data=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFprint("Got two batches")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFprint("Image batch shape: ")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFprint(images_batch.get_shape())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFprint("Labels batch shape:")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFprint(labels_batch.get_shape())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFwith tf.Session(config=tf.ConfigProto(log_device_placement=False, operation_timeout_in_ms=60000)) as sess:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Actually running now")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Initializing global variables")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.set_random_seed(42)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.global_variables_initializer().run()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Finished")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Starting coordinator and queue runners")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    coord = tf.train.Coordinator()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    threads = tf.train.start_queue_runners(coord=coord, sess=sess)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Ok")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # enqueue everything as needed123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sess.run(enqueues)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for i in xrange(0, 5):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("blah")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Get an image tensor and print its value.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Getting image tensor")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        image_tensor = sess.run([images_batch])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Got image tensor")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print(image_tensor[0][0, 0, 0])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Finish off the filename queue coordinator.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    coord.request_stop()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    coord.join(threads)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF