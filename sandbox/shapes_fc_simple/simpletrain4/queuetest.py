import tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfirst_list = ["a", "b", "c", "d", "e", "f", "g"]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsecond_list = ["1", "2", "3", "4", "5", "6", "7"]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFletters = tf.convert_to_tensor(first_list, dtype=tf.string)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFnumbers = tf.convert_to_tensor(second_list, dtype=tf.string)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFqueue = tf.train.slice_input_producer([letters, numbers],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                      num_epochs=None, shuffle=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFkey_file = queue[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFlock_file = queue[1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFkey_file2 = queue[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFlock_file2 = queue[1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFwith tf.Session() as sess:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.global_variables_initializer().run()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    coord = tf.train.Coordinator()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    threads = tf.train.start_queue_runners(coord=coord, sess=sess)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    k, l, k2, l2 = sess.run([key_file, lock_file, key_file2, lock_file2])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("k : " + k)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("l : " + l)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("k2: " + k2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("l2: " + l2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF