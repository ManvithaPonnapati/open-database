import tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom glob import glob123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport os,time123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom av4_utils import generate_deep_affine_transform,affine_transform123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef index_the_database(database_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Indexes av4 database and returns two lists of filesystem path: ligand files, and protein files.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Ligands are assumed to end with _ligand.av4, proteins should be in the same folders with ligands.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Each protein should have its own folder named similarly to the protein name (in the PDB)."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_file_list = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    receptor_file_list = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for ligand_file in glob(os.path.join(database_path, "*_ligand.av4")):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        receptor_file = "/".join(ligand_file.split("/")[:-1]) + "/" + ligand_file.split("/")[-1][:4] + '.av4'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if os.path.exists(receptor_file):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ligand_file_list.append(ligand_file)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            receptor_file_list.append(receptor_file)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    index_list = range(len(ligand_file_list))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if len(index_list) ==0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise Exception('av4_input: No files found in the database path:',database_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "Indexed ligand-protein pairs in the database:",index_list[-1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return index_list,ligand_file_list, receptor_file_list123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef read_receptor_and_ligand(filename_queue):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Reads ligand and protein raw bytes based on the names in the filename queue. Returns tensors with coordinates123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    and atoms of ligand and protein for future processing.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Important: by default it does oversampling of the positive examples based on training epoch."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # FIXME: epoch counter may not increment unless sess.run() is called on it explicitly123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def decode_av4(serialized_record):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # decode everything into int32123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tmp_decoded_record = tf.decode_raw(serialized_record, tf.int32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # first four bytes describe the number of frames in a record123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        number_of_frames = tf.slice(tmp_decoded_record, [0], [1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # labels are saved as int32 * number of frames in the record123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        labels = tf.slice(tmp_decoded_record, [1], number_of_frames)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # elements are saved as int32 and their number is == to the number of atoms123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        number_of_atoms = ((tf.shape(tmp_decoded_record) - number_of_frames - 1) / (3 * number_of_frames + 1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        elements = tf.slice(tmp_decoded_record, number_of_frames + 1, number_of_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # coordinates are saved as a stack of X,Y,Z where the first(vertical) dimension123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # corresponds to the number of atoms123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # second (horizontal dimension) is x,y,z coordinate of every atom and is always 3123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # third (depth) dimension corresponds to the number of frames123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        coords_shape = tf.concat(0, [number_of_atoms, [3], number_of_frames])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tmp_coords = tf.slice(tmp_decoded_record, number_of_frames + number_of_atoms + 1,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                              tf.shape(tmp_decoded_record) - number_of_frames - number_of_atoms - 1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        multiframe_coords = tf.bitcast(tf.reshape(tmp_coords, coords_shape), type=tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return labels,elements,multiframe_coords123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # read raw bytes of the ligand and receptor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    idx = filename_queue[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    serialized_ligand = tf.read_file(filename_queue[1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    serialized_receptor = tf.read_file(filename_queue[2])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create an epoch counter123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TODO: break on certain epoch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    epoch_counter = tf.Variable(0,tf.int32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def incr_epoch(): return epoch_counter+1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def keep_epoch(): return epoch_counter123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    epoch_counter = epoch_counter.assign(tf.cond(tf.equal(idx,0),incr_epoch,keep_epoch))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # decode bytes into meaningful tensors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_labels, ligand_elements, multiframe_ligand_coords = decode_av4(serialized_ligand)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    receptor_labels, receptor_elements, multiframe_receptor_coords = decode_av4(serialized_receptor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def count_frame_from_epoch(epoch_counter,ligand_labels):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """Some simple arithmetics is used to sample all of the available frames123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if the index of the examle is even, positive label is taken every even epoch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if the index of the example is odd, positive label is taken every odd epoch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        current negative example increments once every two epochs, and slides along all of the negative examples"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        def select_pos_frame(): return tf.constant(0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        def select_neg_frame(): return tf.mod(tf.div(1+epoch_counter,2), tf.shape(ligand_labels) - 1) +1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        current_frame = tf.cond(tf.equal(tf.mod(epoch_counter+idx+1,2),1),select_pos_frame,select_neg_frame)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return current_frame123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    current_frame = count_frame_from_epoch(epoch_counter,ligand_labels)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # FIXME: why would gather sometimes return 3d and sometimes 2d array (?)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_coords = tf.squeeze(tf.gather(tf.transpose(multiframe_ligand_coords, perm=[2, 0, 1]),current_frame))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    label = tf.gather(ligand_labels,current_frame)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    receptor_coords = tf.squeeze(multiframe_receptor_coords)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return tf.squeeze(current_frame),tf.squeeze(label),ligand_elements, ligand_coords, receptor_elements, receptor_coords123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef convert_protein_and_ligand_to_image(ligand_elements,ligand_coords,receptor_elements,receptor_coords,side_pixels,pixel_size):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Take coordinates and elements of protein and ligand and convert them into an image.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Return image with one dimension so far."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # FIXME abandon ligand when it does not fit into the box (it's kept now)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TODO check if indeed it breaks in the last iteration cycle when a good affine transform is found123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # max_num_attempts - maximum number of affine transforms for the ligand to be tried123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    max_num_attemts = 1000123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # affine_transform_pool_size is the first(batch) dimension of tensor of transition matrices to be returned123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # affine tranform pool is only generated once in the beginning of training and randomly sampled afterwards123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    affine_transform_pool_size = 10000123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # transform center ligand around zero123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_center_of_mass = tf.reduce_mean(ligand_coords, reduction_indices=0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    centered_ligand_coords = ligand_coords - ligand_center_of_mass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    centered_receptor_coords = receptor_coords - ligand_center_of_mass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def generate_transition_matrix(attempt, transition_matrix,batch_of_transition_matrices):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """Takes initial coordinates of the ligand, generates a random affine transform matrix and transforms coordinates."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        transition_matrix= tf.gather(batch_of_transition_matrices,tf.random_uniform([], minval=0, maxval=affine_transform_pool_size, dtype=tf.int32))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        attempt += 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return attempt, transition_matrix,batch_of_transition_matrices123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def not_all_in_the_box(attempt, transition_matrix,batch_of_transition_matrices,ligand_coords=centered_ligand_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                           box_size=(tf.cast(side_pixels,tf.float32)*pixel_size),max_num_attempts=max_num_attemts):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """Takes affine transform matrix and box dimensions, performs the transformation, and checks if all atoms123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        are in the box."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        transformed_coords, transition_matrix = affine_transform(ligand_coords, transition_matrix)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        not_all = tf.cast(tf.reduce_max(tf.cast(tf.square(box_size*0.5) - tf.square(transformed_coords) < 0,tf.int32)),tf.bool)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        within_iteration_limit = tf.cast(tf.reduce_sum(tf.cast(attempt < max_num_attemts, tf.float32)), tf.bool)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return tf.logical_and(within_iteration_limit, not_all)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    attempt = tf.Variable(tf.constant(0, shape=[1]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    batch_of_transition_matrices = tf.Variable(generate_deep_affine_transform(affine_transform_pool_size))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    transition_matrix = tf.gather(batch_of_transition_matrices, tf.random_uniform([], minval=0, maxval=affine_transform_pool_size, dtype=tf.int32))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    last_attempt,final_transition_matrix,_ = tf.while_loop(not_all_in_the_box, generate_transition_matrix, [attempt, transition_matrix,batch_of_transition_matrices],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                           parallel_iterations=1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # rotate receptor and ligand using affine transform found123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    rotatated_ligand_coords,_ = affine_transform(centered_ligand_coords,final_transition_matrix)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    rotated_receptor_coords,_ = affine_transform(centered_receptor_coords,final_transition_matrix)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # move coordinates of a complex to an integer number so as to put every atom on a grid123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # ceiled coords is an integer number out of real coordinates that corresponds to the index on the cell123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ceiled_ligand_coords = tf.cast(tf.round(-0.5 + (tf.cast(side_pixels,tf.float32)*0.5) + rotatated_ligand_coords),tf.int64)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ceiled_receptor_coords = tf.cast(tf.round(-0.5 + (tf.cast(side_pixels, tf.float32) * 0.5) + rotated_receptor_coords),tf.int64)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # crop atoms of the protein that do not fit inside the box123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    top_filter = tf.reduce_max(ceiled_receptor_coords,reduction_indices=1)<side_pixels123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    bottom_filter = tf.reduce_min(ceiled_receptor_coords,reduction_indices=1)>0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    retain_atoms = tf.logical_and(top_filter,bottom_filter)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cropped_receptor_coords = tf.boolean_mask(ceiled_receptor_coords,retain_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cropped_receptor_elements = tf.boolean_mask(receptor_elements,retain_atoms)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # merge protein and ligand together. In this case an arbitrary value of 10 is added to the ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    complex_coords = tf.concat(0,[ceiled_ligand_coords,cropped_receptor_coords])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    complex_elements = tf.concat(0,[ligand_elements+10,cropped_receptor_elements])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sparse_complex = tf.SparseTensor(indices=complex_coords, values=complex_elements,shape=[side_pixels,side_pixels,side_pixels])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    dense_complex = tf.sparse_tensor_to_dense(sparse_complex, validate_indices=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # FIXME: sparse_tensor_to_dense has not been properly tested.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # FIXME: I may need to sort indices according to TF's manual on the function123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # FIXME: try to save an image and see how it looks like123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return dense_complex123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef image_and_label_queue(sess,batch_size,pixel_size,side_pixels,num_threads,database_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TODO: add epoch counter123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a list of files in the database123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    index_list,ligand_file_list,receptor_file_list = index_the_database(database_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a filename queue (tensor) with the names of the ligand and receptors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    index_tensor = tf.convert_to_tensor(index_list,dtype=tf.int32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_files = tf.convert_to_tensor(ligand_file_list,dtype=tf.string)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    receptor_files = tf.convert_to_tensor(receptor_file_list,dtype=tf.string)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    filename_queue = tf.train.slice_input_producer([index_tensor,ligand_files,receptor_files],num_epochs=None,shuffle=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # read one receptor and stack of ligands; choose one of the ligands from the stack according to epoch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    current_frame,label,ligand_elements,ligand_coords,receptor_elements,receptor_coords = read_receptor_and_ligand(filename_queue)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # convert coordinates of ligand and protein into an image123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    dense_image = convert_protein_and_ligand_to_image(ligand_elements,ligand_coords,receptor_elements,receptor_coords,side_pixels,pixel_size)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # selectively initialize some of the variables123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    uninitialized_vars = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for var in tf.global_variables():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            sess.run(var)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        except tf.errors.FailedPreconditionError:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            uninitialized_vars.append(var)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    init_new_vars_op = tf.variables_initializer(uninitialized_vars)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sess.run(init_new_vars_op)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a batch of proteins and ligands to read them together123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    multithread_batch = tf.train.batch([current_frame, label, dense_image], batch_size, num_threads=num_threads,capacity=batch_size * 3,shapes=[[], [], [side_pixels, side_pixels, side_pixels]])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return multithread_batch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF