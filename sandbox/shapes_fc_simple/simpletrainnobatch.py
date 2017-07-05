from __future__ import absolute_import123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom __future__ import division123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom __future__ import print_function123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport argparse123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport os123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom glob import glob123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom random import randint123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom shape_generation import Flags123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFLAGS = None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef index_the_database_into_queue2(image_path, shuffle):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Indexes av4 database and returns two lists of filesystem path: ligand files, and protein files.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Ligands are assumed to end with _ligand.av4, proteins should be in the same folders with ligands.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Each protein should have its own folder named similarly to the protein name (in the PDB)."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # STEP 1: GET LIST OF KEY AND LOCK FILES123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    key_file_list = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    lock_file_list = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Number of keys:", len(glob(os.path.join(image_path + '', "*[_]*L.png"))))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for key_image in glob(os.path.join(image_path + '', "*[_]*L.png")):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # print(key_image)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lock_image = key_image.replace('L', 'K')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if os.path.exists(lock_image):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            key_file_list.append(key_image)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            lock_file_list.append(lock_image)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print("Could not find lock for key ", key_image)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    index_list = range(len(key_file_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    examples_in_database = len(index_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if examples_in_database == 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise Exception('No files found in the image path:', image_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Number of indexed key-lock pairs in the database:", examples_in_database)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a filename queue (tensor) with the names of the keys and locks123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    index_tensor = tf.convert_to_tensor(index_list, dtype=tf.int32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    key_files = tf.convert_to_tensor(key_file_list, dtype=tf.string)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    lock_files = tf.convert_to_tensor(lock_file_list, dtype=tf.string)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Lengths:", index_tensor.get_shape(), ", ", key_files.get_shape(), ", ", lock_files.get_shape())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # STEP 2: MAKE LIST OF MATCHING/NOT MATCHING ISNTRUCTIONS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    probability_of_match = 0.5123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    match_or_not_list = np.random.choice([0, 1], size=(50000,), p=[1 - probability_of_match, probability_of_match])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    match_or_not = tf.convert_to_tensor(match_or_not_list, dtype=tf.bool)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    filename_queue = tf.train.slice_input_producer([index_tensor, key_files, lock_files], num_epochs=None,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                   shuffle=shuffle)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # filename_queue = [index_list, key_file_list, lock_file_list]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # rsq = tf.RandomShuffleQueue(50000, 0, [tf.int32, tf.string, tf.string, tf.bool], shapes=[[], [], [], []])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # do_enqueues = rsq.enqueue_many([index_tensor, key_files, lock_files, match_or_not])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # index, key_file, lock_file, match = rsq.dequeue()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return filename_queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef index_the_database_into_queue(image_path, shuffle):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Indexes av4 database and returns two lists of filesystem path: ligand files, and protein files.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Ligands are assumed to end with _ligand.av4, proteins should be in the same folders with ligands.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Each protein should have its own folder named similarly to the protein name (in the PDB)."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # STEP 1: GET LIST OF KEY AND LOCK FILES123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    key_file_list = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    lock_file_list = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Number of keys:", len(glob(os.path.join(image_path + '', "*[_]*L.png"))))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for key_image in glob(os.path.join(image_path + '', "*[_]*L.png")):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # print(key_image)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lock_image = key_image.replace('L', 'K')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if os.path.exists(lock_image):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            key_file_list.append(key_image)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            lock_file_list.append(lock_image)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print("Could not find lock for key ", key_image)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    index_list = range(len(key_file_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    examples_in_database = len(index_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if examples_in_database == 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise Exception('No files found in the image path:', image_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Number of indexed key-lock pairs in the database:", examples_in_database)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a filename queue (tensor) with the names of the keys and locks123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    index_tensor = tf.convert_to_tensor(index_list, dtype=tf.int32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    key_files = tf.convert_to_tensor(key_file_list, dtype=tf.string)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    lock_files = tf.convert_to_tensor(lock_file_list, dtype=tf.string)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Lengths:", index_tensor.get_shape(), ", ", key_files.get_shape(), ", ", lock_files.get_shape())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # STEP 2: MAKE LIST OF MATCHING/NOT MATCHING ISNTRUCTIONS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    probability_of_match = 0.5123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    match_or_not_list = np.random.choice([0, 1], size=(50000,), p=[1 - probability_of_match, probability_of_match])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    match_or_not = tf.convert_to_tensor(match_or_not_list, dtype=tf.bool)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # filename_queue = tf.train.slice_input_producer([index_tensor, key_files, lock_files], num_epochs=None,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #                                                shuffle=shuffle)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # filename_queue = [index_list, key_file_list, lock_file_list]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    rsq = tf.RandomShuffleQueue(50000, 0, [tf.int32, tf.string, tf.string, tf.bool], shapes=[[], [], [], []])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    do_enqueues = rsq.enqueue_many([index_tensor, key_files, lock_files, match_or_not])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    index, key_file, lock_file, match = rsq.dequeue()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return do_enqueues, index, key_file, lock_file, match, examples_in_database123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef random_but_not((min, max), avoid):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Chooses a random number in a range from min to max (inclusive), but avoiding the number avoid."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    chosen = avoid123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    while chosen == avoid:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        chosen = randint(min, max)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return chosen123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef image_and_label_queue2(lock_image_files_queue):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Creates shuffle queue for training the network"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    reader = tf.WholeFileReader()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    keyA, valueA = reader.read(lock_image_files_queue)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    my_imgA = tf.image.decode_png(valueA)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    lock_image = tf.image.decode_png(my_imgA)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return (lock_image_num, label, combined_image)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef image_and_label_queue(batch_size, num_threads, index, key_file, lock_file, match, train=True):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Creates shuffle queue for training the network"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    reader = tf.WholeFileReader()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Getting index")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    lock_image_num = index123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Got index")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Getting lock image")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    keyA, valueA = reader.read(lock_file)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    my_imgA = tf.image.decode_png(valueA)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    lock_image = tf.image.decode_png(my_imgA)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # key_image = None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Got lock image")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    match_or_not = match  # Determine whether the key should match the lock or not123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Got matchornot")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    key, value = reader.read(key_file)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    my_img = tf.image.decode_png(value)  # use png or jpg decoder based on your files.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    key_image = tf.image.decode_png(my_img, channels=0, dtype=tf.uint8)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # if match_or_not == 1:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #     print("Setting up true matchornot")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #     key_image = tf.image.decode_png(key_file, channels=0, dtype=tf.uint8)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #     print("Got matching key image")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #     print("Setting up false matchornot")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #     new_key_file = key_file  # TODO: CHOOSE RANDOM ONE INSTEAD!123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #     key_image = tf.image.decode_png(key_file, channels=0, dtype=tf.uint8)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #     print("Got non-matching key image")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Combining images")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    combined_image = tf.stack([lock_image, key_image], axis=1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Combined images")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Getting label")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    label = match_or_not  # The label says whether the lock and the key actually match123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Got label")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # print("Batching")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a batch of proteins and ligands to read them together123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # num, label_batch, image_batch = tf.train.batch([lock_image_num, label, combined_image], batch_size, num_threads=num_threads,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                       # capacity=batch_size * 3, dynamic_pad=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # print("Batch shape: ", str(tf.shape(multithread_batch)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # print("Finished batching")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return (lock_image_num, label, combined_image)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef main(_):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sess = tf.Session()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Get a filename queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    filequeue = index_the_database_into_queue(Flags.image_path, shuffle=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Gotten filename queue.")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # fq = sess.run(filename_queue)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # print("FQ: ", fq)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a custom shuffle queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    num, image_batch, label_batch = image_and_label_queue(batch_size=Flags.batch_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                          num_threads=Flags.num_threads,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                          index=index_queue,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                          key_file=key_file_queue,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                          lock_file=lock_file_queue,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                          match=match)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Obtained batch")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Import data123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    x = tf.placeholder(tf.float32, [None, None])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    W = tf.Variable(tf.zeros([100, 2]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    b = tf.Variable(tf.zeros([2]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    y = tf.matmul(x, W) + b123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Define loss and optimizer123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    y_ = tf.placeholder(tf.float32, [None, 2])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cross_entropy = tf.reduce_mean(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                            tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    train_step = tf.train.AdamOptimizer(0.05).minimize(cross_entropy)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sess.run(tf.local_variables_initializer())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sess.run(tf.global_variables_initializer())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    coord = tf.train.Coordinator()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    threads = tf.train.start_queue_runners(sess=sess, coord=coord)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Starting training!")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Train123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for _ in range(1000):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("In training loop.")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Running do_enqueues")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sess.run(do_enqueues)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Finished running do_enqueues")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Evaluating image batches")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_xs, batch_ys = sess.run([image_batch, label_batch])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("image: ", batch_xs)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Finished evaluating image batches")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Gettting shape of x batch")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        shape = tf.shape(batch_xs)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Got shape of x batch")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Evaluating shape of x batch")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        k = sess.run(shape)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Evaluated shape of x batch")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print("Shape: ", k)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Test trained model123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # print(sess.run(accuracy, feed_dict={x: mnist.test.images,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #                                     y_: mnist.test.labels}))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    coord.request_stop()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    coord.join(threads)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif __name__ == '__main__':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parser = argparse.ArgumentParser()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parser.add_argument('--data_dir', type=str, default='/tmp/tensorflow/mnist/input_data',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                        help='Directory for storing input data')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    FLAGS, unparsed = parser.parse_known_args()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtf.app.run(main=main, argv=[sys.argv[0]] + unparsed)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF