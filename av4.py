import time,os123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom av4_input import image_and_label_queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# telling tensorflow how we want to randomly initialize weights123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef weight_variable(shape):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    initial = tf.truncated_normal(shape, stddev=0.005)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return tf.Variable(initial)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef bias_variable(shape):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    initial = tf.constant(0.01, shape=shape)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return tf.Variable(initial)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef variable_summaries(var, name):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  """Attach a lot of summaries to a Tensor."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  with tf.name_scope('summaries'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    mean = tf.reduce_mean(var)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.scalar_summary('mean/' + name, mean)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope('stddev'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.scalar_summary('stddev/' + name, stddev)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.scalar_summary('max/' + name, tf.reduce_max(var))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.scalar_summary('min/' + name, tf.reduce_min(var))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.histogram_summary(name, var)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef conv_layer(layer_name, input_tensor, filter_size, strides=[1, 1, 1, 1, 1], padding='SAME'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  """makes a simple convolutional layer"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  input_depth = filter_size[3]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  output_depth = filter_size[4]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  with tf.name_scope(layer_name):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope('weights'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      W_conv = weight_variable(filter_size)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      variable_summaries(W_conv, layer_name + '/weights')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope('biases'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      b_conv = bias_variable([output_depth])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      variable_summaries(b_conv, layer_name + '/biases')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv = tf.nn.conv3d(input_tensor, W_conv, strides=strides, padding=padding) + b_conv123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.histogram_summary(layer_name + '/pooling_output', h_conv)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print layer_name,"output dimensions:", h_conv.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return h_conv123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef relu_layer(layer_name,input_tensor,act=tf.nn.relu):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  """makes a simple relu layer"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  with tf.name_scope(layer_name):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu = act(input_tensor, name='activation')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.histogram_summary(layer_name + '/relu_output', h_relu)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.scalar_summary(layer_name + '/sparsity', tf.nn.zero_fraction(h_relu))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  print layer_name, "output dimensions:", h_relu.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  return h_relu123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef pool_layer(layer_name,input_tensor,ksize,strides=[1, 1, 1, 1, 1],padding='SAME'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  """makes a simple pooling layer"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  with tf.name_scope(layer_name):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool = tf.nn.max_pool3d(input_tensor,ksize=ksize,strides=strides,padding=padding)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.histogram_summary(layer_name + '/pooling_output', h_pool)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print layer_name, "output dimensions:", h_pool.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return h_pool123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef fc_layer(layer_name,input_tensor,output_dim):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  """makes a simple fully connected layer"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  input_dim = int((input_tensor.get_shape())[1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF  with tf.name_scope(layer_name):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    weights = weight_variable([input_dim, output_dim])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    variable_summaries(weights, layer_name + '/weights')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope('biases'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      biases = bias_variable([output_dim])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      variable_summaries(biases, layer_name + '/biases')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope('Wx_plus_b'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      h_fc = tf.matmul(input_tensor, weights) + biases123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      tf.histogram_summary(layer_name + '/fc_output', h_fc)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print layer_name, "output dimensions:", h_fc.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return h_fc123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef max_net(x_image_batch,keep_prob):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "making a simple network that can receive 20x20x20 input images. And output 2 classes"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope('input'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        pass123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope("input_reshape"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "image batch dimensions", x_image_batch.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # formally adding one depth dimension to the input123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        x_image_with_depth = tf.reshape(x_image_batch, [-1, 20, 20, 20, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "input to the first layer dimensions", x_image_with_depth.get_shape()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv1 = conv_layer(layer_name='conv1_5x5x5', input_tensor=x_image_with_depth, filter_size=[5, 5, 5, 1, 20])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu1 = relu_layer(layer_name='relu1', input_tensor=h_conv1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool1 = pool_layer(layer_name='pool1_2x2x2', input_tensor=h_relu1, ksize=[1, 2, 2, 2, 1], strides=[1, 2, 2, 2, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv2 = conv_layer(layer_name="conv2_3x3x3", input_tensor=h_pool1, filter_size=[3, 3, 3, 20, 30])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu2 = relu_layer(layer_name="relu2", input_tensor=h_conv2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool2 = pool_layer(layer_name="pool2_2x2x2", input_tensor=h_relu2, ksize=[1, 2, 2, 2, 1], strides=[1, 2, 2, 2, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv3 = conv_layer(layer_name="conv3_2x2x2", input_tensor=h_pool2, filter_size=[2, 2, 2, 30, 40])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu3 = relu_layer(layer_name="relu3", input_tensor=h_conv3)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool3 = pool_layer(layer_name="pool3_2x2x2", input_tensor=h_relu3, ksize=[1, 2, 2, 2, 1], strides=[1, 1, 1, 1, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv4 = conv_layer(layer_name="conv4_2x2x2", input_tensor=h_pool3, filter_size=[2, 2, 2, 40, 50])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu4 = relu_layer(layer_name="relu4", input_tensor=h_conv4)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool4 = pool_layer(layer_name="pool4_2x2x2", input_tensor=h_relu4, ksize=[1, 2, 2, 2, 1], strides=[1, 1, 1, 1, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_conv5 = conv_layer(layer_name="conv5_2x2x2", input_tensor=h_pool4, filter_size=[2, 2, 2, 50, 60])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_relu5 = relu_layer(layer_name="relu5", input_tensor=h_conv5)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_pool5 = pool_layer(layer_name="pool5_2x2x2", input_tensor=h_relu5, ksize=[1, 2, 2, 2, 1], strides=[1, 1, 1, 1, 1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope("flatten_layer"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_pool2_flat = tf.reshape(h_pool5, [-1, 5 * 5 * 5 * 60])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_fc1 = fc_layer(layer_name="fc1", input_tensor=h_pool2_flat, output_dim=1024)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_fc1_relu = relu_layer(layer_name="fc1_relu", input_tensor=h_fc1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope("dropout"):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.scalar_summary('dropout_keep_probability', keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        h_fc1_drop = tf.nn.dropout(h_fc1_relu, keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_fc2 = fc_layer(layer_name="fc2", input_tensor=h_fc1_drop, output_dim=256)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    h_fc2_relu = relu_layer(layer_name="fc2_relu", input_tensor=h_fc2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    y_conv = fc_layer(layer_name="out_neuron", input_tensor=h_fc2_relu, output_dim=2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return y_conv123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef train():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    "train a network"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create session since everything is happening in one123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sess = tf.Session()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TODO: write atoms in layers of depth123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    _,y_,x_image_batch = image_and_label_queue(sess=sess,batch_size=FLAGS.batch_size,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                pixel_size=FLAGS.pixel_size,side_pixels=FLAGS.side_pixels,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                                num_threads=FLAGS.num_threads,database_path=FLAGS.database_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    float_image_batch = tf.cast(x_image_batch,tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    keep_prob = tf.placeholder(tf.float32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    y_conv = max_net(float_image_batch,keep_prob)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(y_conv,y_)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cross_entropy_mean = tf.reduce_mean(cross_entropy)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.name_scope('train'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.scalar_summary('weighted cross entropy mean', cross_entropy_mean)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        train_step_run = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    coord = tf.train.Coordinator()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    threads = tf.train.start_queue_runners(sess=sess, coord=coord)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create saver123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    saver = tf.train.Saver(tf.all_variables())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # merge all summaries123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    merged_summaries = tf.merge_all_summaries()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a _log writer object123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    train_writer = tf.train.SummaryWriter((FLAGS.summaries_dir + '/' + str(FLAGS.run_index) + "_train"), sess.graph)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # test_writer = tf.train.SummaryWriter(FLAGS.summaries_dir + '/test' + str(FLAGS.run_index))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # re-initialize all variables (two thread veriables were initialized before)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    sess.run(tf.initialize_all_variables())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    batch_num = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    while True:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        start = time.time()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #sess.run([y_, x_image_batch], feed_dict={keep_prob: 0.5})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        training_error,_ = sess.run([cross_entropy_mean,train_step_run], feed_dict={keep_prob: 0.5})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "batch ",batch_num,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "\ttraining error:",training_error,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "\texamples per second:", "%.2f" % (50 / (time.time() - start))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        assert not np.isnan(training_error), 'Model diverged with loss = NaN'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        batch_num+=1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # save network status every 1000 batch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if batch_num%1000 == 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            train_error,train_summary = sess.run([cross_entropy_mean,merged_summaries],feed_dict={keep_prob:1})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            train_writer.add_summary(train_summary, batch_num)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            saver.save(sess,FLAGS.summaries_dir + '/' + str(FLAGS.run_index) + "_netstate/saved_state", global_step=batch_num)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass FLAGS:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # important model parameters123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # size of one pixel generated from protein in Angstroms (float)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pixel_size = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # size of the box around the ligand in pixels123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    side_pixels = 20123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # weights for each class for the scoring function123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # number of times each example in the dataset will be read123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    num_epochs = 20123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # parameters to optimize runs on different machines for speed/performance123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # number of vectors(images) in one batch123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    batch_size = 50123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # number of background processes to fill the queue with images123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    num_threads = 16123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # data directories123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # path to the csv file with names of images selected for training123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    database_path = "/home/ubuntu/common/data/new_kaggle/train_small/labeled_av4/**/"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # path for the test set123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    test_set_path = "/home/ubuntu/common/data/new_kaggle/test/unlabeled_av4"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # directory where to write variable summaries123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    summaries_dir = './summaries'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # optional saved session: network from which to load variable states123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    saved_session = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef main(_):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """gracefully creates directories for the log files and for the network state launches. After that orders network training to start"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    summaries_dir = os.path.join(FLAGS.summaries_dir)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # FLAGS.run_index defines when123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    FLAGS.run_index = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    while ((tf.gfile.Exists(summaries_dir + "/"+ str(FLAGS.run_index) +'_train' ) or tf.gfile.Exists(summaries_dir + "/" + str(FLAGS.run_index)+'_test' ))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF           or tf.gfile.Exists(summaries_dir + "/" + str(FLAGS.run_index) +'_netstate') or tf.gfile.Exists(summaries_dir + "/" + str(FLAGS.run_index)+'_logs')) and FLAGS.run_index < 1000:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        FLAGS.run_index += 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.gfile.MakeDirs(summaries_dir + "/" + str(FLAGS.run_index) + '_train' )123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.gfile.MakeDirs(summaries_dir + "/" + str(FLAGS.run_index) + '_test')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.gfile.MakeDirs(summaries_dir + "/" + str(FLAGS.run_index) + '_netstate')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.gfile.MakeDirs(summaries_dir + "/" + str(FLAGS.run_index) + '_logs')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    train()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif __name__ == '__main__':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.app.run()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF