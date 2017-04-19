import time,re123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport av4_input123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom av4_main import FLAGS123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport av4_networks123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport av4_utils123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef softmax_cross_entropy_with_RMSD(logits,lig_RMSDs,RMSD_threshold=3.0):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Calculates usual sparse softmax cross entropy for two class classification between 1(correct position)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    and 0(incorrect position) and multiplies the resulting cross entropy by RMSD coefficient.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    | RMSD_ligand > RMSD_threshold | RMSDcoeff = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    | RMSD_ligand < RMSD_threshold | RMSDcoeff = (RMSD_threshold - RMSD_ligand)/RMSD_threshold123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    RMSD threshold is in Angstroms.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    labels = tf.cast((lig_RMSDs < 0.01), tf.int32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=labels,logits=logits)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    cost_correct_positions = cross_entropy * tf.cast(labels,tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    cost_incorrect_positions = cross_entropy * tf.cast((lig_RMSDs > RMSD_threshold), tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    cost_semicorrect_positions = cross_entropy * tf.cast((lig_RMSDs < RMSD_threshold), tf.float32) * (lig_RMSDs/RMSD_threshold)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#    return cost_incorrect_positions + cost_semicorrect_positions + cost_correct_positions123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return cross_entropy123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass SearchAgent:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """ Search agent takes a single protein with a bound ligand, samples many possible protein-ligand conformations,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    as well as many camera views of the correct position, and outputs a single batch of images and labels for training123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    on which network makes biggest error, and gradient is highest.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Search agent also outputs a compressed form (affine transform matrices) of other conformations that would make good123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    training examples, but did not make it to the batch.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TODO: variance option for positives and negatives123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TODO: clustering123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TODO: add VDW possibilities123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TODO: RMSD + the fraction of native contacts123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TODO: add fast reject for overlapping atoms123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TODO: in the future be sure not to find poses for a similar ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TODO: leave a single binding site on the level of data preparation123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TODO:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #        # example 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #        # take all (do not remove middle) dig a hole in the landscape123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #        # batch is a training example123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # needs labels123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TODO:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #        # example 2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #        # remove semi-correct conformations123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #        # batch is a training example123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TODO:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #       # example 3123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #       # remove semi-correct conformations123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #       # take many images of positive123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #       # image is a training example123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    class EvaluationsContainer:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """" Groups together information about the evaluated positions in a form of affine transform matrices. Reduces123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        all of the evaluated poses into training batch.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # TODO: add a possibility to generate new matrices based on performed evaluations.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # (aka genetic search in AutoDock)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        preds = np.array([])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        costs = np.array([])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lig_pose_transforms = np.array([]).reshape([0, 4, 4])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cameraviews = np.array([]).reshape([0, 4, 4])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lig_RMSDs = np.array([])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        def add_batch(self, pred_batch, cost_batch, lig_pose_transform_batch, cameraview_batch, lig_RMSD_batch):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            """ Adds batch of predictions for different positions and cameraviews of the ligand.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.preds = np.append(self.preds, pred_batch, axis=0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.costs = np.append(self.costs,cost_batch,axis=0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.lig_pose_transforms = np.append(self.lig_pose_transforms, lig_pose_transform_batch, axis=0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.cameraviews = np.append(self.cameraviews, cameraview_batch, axis=0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.lig_RMSDs = np.append(self.lig_RMSDs, lig_RMSD_batch, axis=0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return len(self.preds)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # def hardest_poses_so-_far123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #"""selects new affine transformations to make one more step"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        def convert_into_training_batch(self, cameraviews_initial_pose=10, generated_poses=90, remember_poses=300):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            """ Takes predictions for which the label * prediction is highest123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            (label * prediction is equal to the cost to the network)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            constructs num_batches of bathes with a single positive example and returns a list of batches123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            [cameraviews_initial_pose] + [generated_poses] should be == to [desired batch size] for training123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # order all parameters by costs in ascending order123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            order = np.argsort(self.costs)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.preds = self.preds[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.costs = self.costs[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.lig_pose_transforms = self.lig_pose_transforms[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.cameraviews = self.cameraviews[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.lig_RMSDs = self.lig_RMSDs[order]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # Take examples for which the cost is highest.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # The arbitrary number of RMSD of 0.01 which distinguishes correct from incorrect examples should not123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # affect the results at all. Positions with small ligand_RMSDs < RMSD_threshold will only become training123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # examples after no (ligand_RMSD > RMSD_threshold) is left. It is same with sliding along the threshold.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            init_poses_idx = (np.where(self.lig_RMSDs < 0.01)[0])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            gen_poses_idx = (np.where(self.lig_RMSDs > 0.01)[0])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            sel_init_poses_idx = init_poses_idx[-cameraviews_initial_pose:]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            sel_gen_poses_idx = gen_poses_idx[-generated_poses:]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # print a lot of statistics for debugging/monitoring purposes123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "statistics sampled conformations:"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            var_list = {'lig_RMSDs':self.lig_RMSDs,'preds':self.preds,'costs':self.costs}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            av4_utils.describe_variables(var_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "statistics for selected (hardest) initial conformations"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            var_list = {'lig_RMSDs':self.lig_RMSDs[sel_init_poses_idx], 'preds':self.preds[sel_init_poses_idx],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                        'costs':self.costs[sel_init_poses_idx]}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            av4_utils.describe_variables(var_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "statistics for selected (hardest) generated conformations"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            var_list = {'lig_RMSDs':self.lig_RMSDs[sel_gen_poses_idx], 'preds':self.preds[sel_gen_poses_idx],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                        'costs':self.costs[sel_gen_poses_idx]}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            av4_utils.describe_variables(var_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            sel_idx = np.hstack([sel_init_poses_idx,sel_gen_poses_idx])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return self.preds[sel_idx],self.costs[sel_idx],self.lig_pose_transforms[sel_idx],self.cameraviews[sel_idx],self.lig_RMSDs[sel_idx]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def __init__(self,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                 side_pixels=FLAGS.side_pixels,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                 pixel_size=FLAGS.pixel_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                 batch_size=FLAGS.batch_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                 num_threads=FLAGS.num_threads,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                 sess = FLAGS.main_session):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Generate a single ligand position from initial coordinates and a given transformation matrix.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.sess = sess123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.num_threads = num_threads123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self._affine_tforms_queue = tf.FIFOQueue(capacity=80000, dtypes=tf.float32,shapes=[4, 4])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.lig_pose_tforms = tf.concat([av4_utils.generate_identity_matrices(num_frames=1000),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                          av4_utils.generate_exhaustive_affine_transform()],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                         0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.lig_elements = tf.Variable([0],trainable=False, validate_shape=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.lig_coords = tf.Variable([[0.0,0.0,0.0]], trainable=False, validate_shape=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.rec_elements = tf.Variable([0],trainable=False, validate_shape=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.rec_coords = tf.Variable([[0.0,0.0,0.0]], trainable=False, validate_shape=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tformed_lig_coords,lig_pose_tform = av4_utils.affine_transform(self.lig_coords,self._affine_tforms_queue.dequeue())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # TODO: create fast reject for overlapping atoms of the protein and ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # convert coordinates of the protein and ligand into an image123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        complex_image,_,cameraview = av4_input.convert_protein_and_ligand_to_image(self.lig_elements,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                                   tformed_lig_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                                   self.rec_elements,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                                   self.rec_coords,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                                   side_pixels,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                                                   pixel_size)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # calculate Root Mean Square Deviation for atoms of the transformed molecule compared to the initial one123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lig_RMSD = tf.reduce_mean(tf.square(tformed_lig_coords - self.lig_coords))**0.5123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # create and enqueue images in many threads, and deque and score images in a main thread123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.coord = tf.train.Coordinator()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.image_queue = tf.FIFOQueue(capacity=batch_size*5,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                         dtypes=[tf.float32,tf.float32,tf.float32,tf.float32],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                         shapes=[[side_pixels,side_pixels,side_pixels], [4,4], [4,4], []])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.image_queue_enqueue = self.image_queue.enqueue([complex_image, lig_pose_tform, cameraview, lig_RMSD])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.queue_runner = av4_utils.QueueRunner(self.image_queue, [self.image_queue_enqueue]*num_threads)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.image_batch,self.lig_pose_tform_batch,self.cameraview_batch,self.lig_RMSD_batch = self.image_queue.dequeue_many(batch_size)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.keep_prob = tf.placeholder(tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        with tf.name_scope("network"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            y_conv = av4_networks.max_net(self.image_batch, self.keep_prob, batch_size)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # calculate both predictions, and costs for every ligand position in the batch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.pred_batch = tf.nn.softmax(y_conv)[:,1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.cost_batch = softmax_cross_entropy_with_RMSD(y_conv,self.lig_RMSD_batch)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # create a pipeline to convert ligand transition matrices + cameraviews into images again123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def grid_evaluate_positions(self,my_lig_elements,my_lig_coords,my_rec_elements,my_rec_coords):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """ Puts ligand in the center of every square of the box around the ligand, performs network evaluation of123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        every conformation.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Enqueue all of the transformations for the ligand to sample.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.sess.run(self._affine_tforms_queue.enqueue_many(self.lig_pose_tforms))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Assign elements and coordinates of protein and ligand; shape of the variable will change from ligand to ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.sess.run([tf.assign(self.lig_elements,my_lig_elements, validate_shape=False, use_locking=True),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                       tf.assign(self.lig_coords,my_lig_coords, validate_shape=False, use_locking=True),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                       tf.assign(self.rec_elements,my_rec_elements, validate_shape=False, use_locking=True),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                       tf.assign(self.rec_coords,my_rec_coords, validate_shape=False, use_locking=True)])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # re-initialize the evalutions class123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.evaluated = self.EvaluationsContainer()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "shapes of the ligand and protein:"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print self.sess.run([tf.shape(self.lig_elements),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                             tf.shape(self.lig_coords),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                             tf.shape(self.rec_elements),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                             tf.shape(self.rec_coords)])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # start threads to fill the queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.enqueue_threads = self.queue_runner.create_threads(self.sess, coord=self.coord, start=False, daemon=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "print queue size -3:", self.sess.run(self.image_queue.size())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for tr in self.enqueue_threads:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            tr.start()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        time.sleep(0.3)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "print queue size -2:", self.sess.run(self.image_queue.size())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        time.sleep(0.3)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "print queue size -1:", self.sess.run(self.image_queue.size())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        time.sleep(0.3)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "start evaluations"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            while True:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                start = time.time()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                my_pred_batch, my_cost_batch, my_image_batch, my_lig_pose_tform_batch, my_cameraview_batch, my_lig_RMSD_batch = \123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    self.sess.run([self.pred_batch,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                   self.cost_batch,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                   self.image_batch,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                   self.lig_pose_tform_batch,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                   self.cameraview_batch,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                   self.lig_RMSD_batch],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                  feed_dict = {self.keep_prob:1},123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                  options=tf.RunOptions(timeout_in_ms=1000))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                # save the predictions and cameraviews from the batch into evaluations container123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                lig_poses_evaluated = self.evaluated.add_batch(my_pred_batch,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                               my_cost_batch,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                               my_lig_pose_tform_batch,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                               my_cameraview_batch,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                               my_lig_RMSD_batch)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                print "ligand_atoms:",np.sum(np.array(my_image_batch >7,dtype=np.int32)),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                print "\tpositions evaluated:",lig_poses_evaluated,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                print "\texamples per second:", "%.2f" % (FLAGS.batch_size / (time.time() - start))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        except tf.errors.DeadlineExceededError:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # create training examples for the main queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.evaluated.convert_into_training_batch(cameraviews_initial_pose=20,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                       generated_poses=200,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                       remember_poses=300)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # accurately terminate all threads without closing the queue (uses custom QueueRunner class)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.sess.run(self._affine_tforms_queue.enqueue_many(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                av4_utils.generate_identity_matrices(self.num_threads*3)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.coord.request_stop()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.coord.join()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.coord.clear_stop()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # remove all affine transform matrices from the queue to be empty before the next protein/ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                while True:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    print ".",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    self.sess.run(self._affine_tforms_queue.dequeue(),options=tf.RunOptions(timeout_in_ms=500))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            except tf.errors.DeadlineExceededError:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                print "affine transform queue size:", self.sess.run(self._affine_tforms_queue.size())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            # remove all images from the image queue to be empty before the next protein/ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                while True:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    print ".",123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    self.sess.run(self.image_queue.dequeue(),options=tf.RunOptions(timeout_in_ms=500))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            except tf.errors.DeadlineExceededError:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                print "image queue size:", self.sess.run(self.image_queue.size())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF