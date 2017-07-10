from __future__ import print_function123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport os123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom glob import glob123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom shape_generation import Flags123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef database_to_filename_queue(images_path, shuffle=True):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Creates a RandomShuffleQueue of filenames based on the directory for images.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          images_path: The directory containing all123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    of the images to be placed into123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    the filename queue.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          shuffle: (Optional.) Whether the order of123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    files should be shuffled.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    Defaults to True (shuffle)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # First, we get a list of lock files and key files.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    key_file_list = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    lock_file_list = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # All key image paths are in the form {images_path}/[n]_K.png123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # where [n] is some integer representing the ID of the image.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    key_image_path = os.path.join(images_path + '', "*[_]*K.png")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Number of keys:", len(glob(key_image_path)))  # TODO: Implement a better logging system123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Cycle through all files in the key_image_path form123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for key_image in glob(key_image_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Get the corresponding lock image for the key image.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Lock images are in the form {images_path}/[n]_L.png;123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # that is, the only difference from the key image path123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # is the K->L substitution.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lock_image = key_image.replace('K', 'L')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Append the lock and key files to their respective lists (if the files exist)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if os.path.exists(lock_image):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            key_file_list.append(key_image)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            lock_file_list.append(lock_image)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print("Could not find lock for key ", key_image)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print("(Skipping both)")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # index_list is just a list of integers from 0 to the number of images minus one123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    index_list = range(len(key_file_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    examples_in_database = len(index_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # If there are no images found, say so123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if examples_in_database == 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise Exception('No files found in the image path:', images_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Number of indexed key-lock pairs in the database:", examples_in_database)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Now, we create a list of booleans, which will tell us whether123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # we should match the lock to its key or not. This is used in123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # later methods, which actually read and combine the images.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    probability_of_match = 0.5  # The probability that we will match the key to its lock correctly (for training)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    match_or_not_list = np.random.choice([0, 1],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                         size=(len(key_file_list),),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                         p=[1 - probability_of_match, probability_of_match])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Now, create tensors from the index, key file, lock file, and matching lists123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    index_tensor = tf.convert_to_tensor(index_list, dtype=tf.int32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    key_files = tf.convert_to_tensor(key_file_list, dtype=tf.string)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    lock_files = tf.convert_to_tensor(lock_file_list, dtype=tf.string)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    match_or_not = tf.convert_to_tensor(match_or_not_list, dtype=tf.bool)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("index tensor", index_tensor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print(key_files)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print(lock_files)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print(match_or_not)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Now, we generate a queue based on the four tensors we made from the lists above123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    filename_queue = tf.train.slice_input_producer([index_tensor, key_files, lock_files, match_or_not], num_epochs=None,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                   shuffle=shuffle)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return filename_queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef filename_queue_to_image_and_label_queue(filename_queue, batch_size=Flags.batch_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                            num_threads=Flags.num_threads):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Creates a queue of images and labels based on the filename/matching queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          filename_queue: The filename/matching queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                        that images will be taken from.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          batch_size: (Optional). The size of the batches123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                        to be generated. Defaults to123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                        number listed in Flags.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          num_threads: (Optional). The number of threads123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                        to be used. Defaults to number123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                        listed in Flags.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        Returns:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            A multithread batch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Get the key image and lock image, as well as the label that says whether they match or not123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    key_image, lock_image, label = read_receptor_and_ligand(filename_queue)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # key_image = tf.reshape(key_image, [30000, ])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # lock_image = tf.reshape(lock_image, [30000, ])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TODO: Use tf.read_file() to avoid reading everything into memory123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Key image shape:", key_image.get_shape())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Lock image shape:", lock_image.get_shape())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Combine (stack) the lock and key into one image123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    combined_image = tf.concat([lock_image, key_image], axis=0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print("Combined image shape:", combined_image.get_shape())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a batch of locks and keys to read them together123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    multithread_batch = tf.train.batch([key_image, label], batch_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                       num_threads=num_threads,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                       capacity=batch_size * 3, dynamic_pad=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return multithread_batch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef read_receptor_and_ligand(filename_queue):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Creates a queue of images and labels based on the filename/matching queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF              filename_queue: The filename/matching queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                            where images and matching data123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                            will be taken from123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            Returns:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                A triplet containing a tensor of the key image, a tensor of the lock image,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                and a label recording whether the key and the lock match or not.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Get id, key file, lock file, and label123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # values from the filename queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    id_value  = filename_queue[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    key_file  = filename_queue[1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    lock_file = filename_queue[2]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    label     = filename_queue[3]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Decode the images into tensors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    key_image = decode_image(key_file)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    lock_image = decode_image(lock_file)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return key_image, lock_image, label123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef decode_image(file_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Given an image filepath, reads in the image and returns a tensor of the image.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF              file_path: The filename of the image.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            Credits:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                This function includes code adapted from the following sources:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    -https://stackoverflow.com/a/33862534/123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return tf.read_file(file_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Create a small filename queue, containing just the image123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # we're going to read (This is probably quite inefficient,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #   especially given the large number of images we're123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #   dealing with. Improvements welcome)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # filename_queue = tf.train.string_input_producer([file_path])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Read in the file123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # reader = tf.WholeFileReader()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # key, value = reader.read(filename_queue)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Decode the image into a tensor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # image_tensor = tf.image.decode_png(value)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # print("Image tensor shape:", image_tensor.get_shape())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # return image_tensor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF