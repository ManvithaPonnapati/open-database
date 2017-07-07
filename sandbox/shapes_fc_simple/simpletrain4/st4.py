import os123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport FLAGS, st4input, PARAMS, re123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# Global constants describing the MSHAPES data set.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFIMAGE_SIZE = PARAMS.IMAGE_SIZE123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFNUM_CLASSES = PARAMS.NUM_CLASSES123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFNUM_EXAMPLES_PER_EPOCH_FOR_TRAIN = PARAMS.NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFNUM_EXAMPLES_PER_EPOCH_FOR_EVAL = PARAMS.NUM_EXAMPLES_PER_EPOCH_FOR_EVAL123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFTOWER_NAME = PARAMS.TOWER_NAME123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# Constants describing the training process.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFMOVING_AVERAGE_DECAY = PARAMS.MOVING_AVERAGE_DECAY  # The decay to use for the moving average.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFNUM_EPOCHS_PER_DECAY = PARAMS.NUM_EPOCHS_PER_DECAY  # Epochs after which learning rate decays.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFLEARNING_RATE_DECAY_FACTOR = PARAMS.LEARNING_RATE_DECAY_FACTOR  # Learning rate decay factor.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFINITIAL_LEARNING_RATE = PARAMS.LEARNING_RATE_DECAY_FACTOR  # Initial learning rate.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef inputs(eval_data):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Construct input for CIFAR evaluation using the Reader ops.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      eval_data: bool, indicating if one should use the train or eval data set.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      images: Images. 4D tensor of [batch_size, IMAGE_SIZE, IMAGE_SIZE, 3] size.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      labels: Labels. 1D tensor of [batch_size] size.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Raises:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      ValueError: If no data_dir123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if not FLAGS.data_dir:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise ValueError('Please supply a data_dir')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    data_dir = os.path.join(FLAGS.data_dir, '')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    (enqueues, (images, labels)) = st4input.inputs(eval_data=eval_data,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                     data_dir=data_dir,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                     batch_size=FLAGS.batch_size)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if FLAGS.use_fp16:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        images = tf.cast(images, tf.float16)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        labels = tf.cast(labels, tf.float16)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return enqueues, images, labels123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef train(total_loss, global_step):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Train CIFAR-10 model.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Create an optimizer and apply to all trainable variables. Add moving123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    average for all trainable variables.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      total_loss: Total loss from loss().123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      global_step: Integer Variable counting the number of training steps123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        processed.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      train_op: op for training.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Variables that affect learning rate.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    num_batches_per_epoch = NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN / FLAGS.batch_size123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    decay_steps = int(num_batches_per_epoch * NUM_EPOCHS_PER_DECAY)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Decay the learning rate exponentially based on the number of steps.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    lr = tf.train.exponential_decay(INITIAL_LEARNING_RATE,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                    global_step,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                    decay_steps,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                    LEARNING_RATE_DECAY_FACTOR,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                    staircase=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.summary.scalar('learning_rate', lr)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Generate moving averages of all losses and associated summaries.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    loss_averages_op = _add_loss_summaries(total_loss)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Compute gradients.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.control_dependencies([loss_averages_op]):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        opt = tf.train.GradientDescentOptimizer(lr)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        grads = opt.compute_gradients(total_loss)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Apply gradients.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    apply_gradient_op = opt.apply_gradients(grads, global_step=global_step)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Add histograms for trainable variables.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for var in tf.trainable_variables():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.histogram(var.op.name, var)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Add histograms for gradients.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for grad, var in grads:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if grad is not None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            tf.summary.histogram(var.op.name + '/gradients', grad)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Track the moving averages of all trainable variables.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    variable_averages = tf.train.ExponentialMovingAverage(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        MOVING_AVERAGE_DECAY, global_step)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    variables_averages_op = variable_averages.apply(tf.trainable_variables())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.control_dependencies([apply_gradient_op, variables_averages_op]):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        train_op = tf.no_op(name='train')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return train_op123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef inference(images):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Build the CIFAR-10 model.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      images: Images returned from distorted_inputs() or inputs().123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      Logits.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # We instantiate all variables using tf.get_variable() instead of123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # tf.Variable() in order to share variables across multiple GPU training runs.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # If we only ran this model on a single GPU, we could simplify this function123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # by replacing all instances of tf.get_variable() with tf.Variable().123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # conv1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.variable_scope('conv1') as scope:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        kernel = _variable_with_weight_decay('weights',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             shape=[5, 5, 3, 64],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             stddev=5e-2,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             wd=0.0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        conv = tf.nn.conv2d(images, kernel, [1, 1, 1, 1], padding='SAME')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        biases = _variable_on_cpu('biases', [64], tf.constant_initializer(0.0))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        pre_activation = tf.nn.bias_add(conv, biases)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        conv1 = tf.nn.relu(pre_activation, name=scope.name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        _activation_summary(conv1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # pool1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pool1 = tf.nn.max_pool(conv1, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                           padding='SAME', name='pool1')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # norm1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    norm1 = tf.nn.lrn(pool1, 4, bias=1.0, alpha=0.001 / 9.0, beta=0.75,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                      name='norm1')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # conv2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.variable_scope('conv2') as scope:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        kernel = _variable_with_weight_decay('weights',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             shape=[5, 5, 64, 64],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             stddev=5e-2,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                             wd=0.0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        conv = tf.nn.conv2d(norm1, kernel, [1, 1, 1, 1], padding='SAME')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        biases = _variable_on_cpu('biases', [64], tf.constant_initializer(0.1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        pre_activation = tf.nn.bias_add(conv, biases)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        conv2 = tf.nn.relu(pre_activation, name=scope.name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        _activation_summary(conv2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # norm2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    norm2 = tf.nn.lrn(conv2, 4, bias=1.0, alpha=0.001 / 9.0, beta=0.75,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                      name='norm2')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # pool2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pool2 = tf.nn.max_pool(norm2, ksize=[1, 3, 3, 1],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                           strides=[1, 2, 2, 1], padding='SAME', name='pool2')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # local3123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.variable_scope('local3') as scope:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Move everything into depth so we can perform a single matrix multiply.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        reshape = tf.reshape(pool2, [FLAGS.batch_size, -1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        dim = reshape.get_shape()[1].value123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        weights = _variable_with_weight_decay('weights', shape=[dim, 384],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                              stddev=0.04, wd=0.004)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        biases = _variable_on_cpu('biases', [384], tf.constant_initializer(0.1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        local3 = tf.nn.relu(tf.matmul(reshape, weights) + biases, name=scope.name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        _activation_summary(local3)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # local4123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.variable_scope('local4') as scope:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        weights = _variable_with_weight_decay('weights', shape=[384, 192],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                              stddev=0.04, wd=0.004)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        biases = _variable_on_cpu('biases', [192], tf.constant_initializer(0.1))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        local4 = tf.nn.relu(tf.matmul(local3, weights) + biases, name=scope.name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        _activation_summary(local4)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # linear layer(WX + b),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # We don't apply softmax here because123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # tf.nn.sparse_softmax_cross_entropy_with_logits accepts the unscaled logits123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # and performs the softmax internally for efficiency.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.variable_scope('softmax_linear') as scope:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        weights = _variable_with_weight_decay('weights', [192, NUM_CLASSES],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                              stddev=1 / 192.0, wd=0.0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        biases = _variable_on_cpu('biases', [NUM_CLASSES],123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                                  tf.constant_initializer(0.0))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        softmax_linear = tf.add(tf.matmul(local4, weights), biases, name=scope.name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        _activation_summary(softmax_linear)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return softmax_linear123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef loss(logits, labels):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Add L2Loss to all the trainable variables.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Add summary for "Loss" and "Loss/avg".123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      logits: Logits from inference().123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      labels: Labels from distorted_inputs or inputs(). 1-D tensor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF              of shape [batch_size]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      Loss tensor of type float.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Calculate the average cross entropy loss across the batch.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    labels = tf.cast(labels, tf.int64)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        labels=labels, logits=logits, name='cross_entropy_per_example')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    cross_entropy_mean = tf.reduce_mean(cross_entropy, name='cross_entropy')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.add_to_collection('losses', cross_entropy_mean)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # The total loss is defined as the cross entropy loss plus all of the weight123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # decay terms (L2 loss).123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return tf.add_n(tf.get_collection('losses'), name='total_loss')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef _add_loss_summaries(total_loss):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Add summaries for losses in CIFAR-10 model.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Generates moving average for all losses and associated summaries for123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    visualizing the performance of the network.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      total_loss: Total loss from loss().123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      loss_averages_op: op for generating moving averages of losses.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Compute the moving average of all individual losses and the total loss.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    loss_averages = tf.train.ExponentialMovingAverage(0.9, name='avg')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    losses = tf.get_collection('losses')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    loss_averages_op = loss_averages.apply(losses + [total_loss])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Attach a scalar summary to all individual losses and the total loss; do the123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # same for the averaged version of the losses.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for l in losses + [total_loss]:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # Name each loss as '(raw)' and name the moving average version of the loss123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # as the original loss name.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.scalar(l.op.name + ' (raw)', l)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.summary.scalar(l.op.name, loss_averages.average(l))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return loss_averages_op123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef _activation_summary(x):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Helper to create summaries for activations.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Creates a summary that provides a histogram of activations.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Creates a summary that measures the sparsity of activations.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      x: Tensor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      nothing123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    author: The TensorFlow Authors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Remove 'tower_[0-9]/' from the name in case this is a multi-GPU training123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # session. This helps the clarity of presentation on tensorboard.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tensor_name = re.sub('%s_[0-9]*/' % TOWER_NAME, '', x.op.name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.summary.histogram(tensor_name + '/activations', x)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    tf.summary.scalar(tensor_name + '/sparsity',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                      tf.nn.zero_fraction(x))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef _variable_on_cpu(name, shape, initializer):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Helper to create a Variable stored on CPU memory.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      name: name of the variable123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      shape: list of ints123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      initializer: initializer for Variable123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      Variable Tensor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with tf.device('/cpu:0'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        dtype = tf.float16 if FLAGS.use_fp16 else tf.float32123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        var = tf.get_variable(name, shape, initializer=initializer, dtype=dtype)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return var123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef _variable_with_weight_decay(name, shape, stddev, wd):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Helper to create an initialized Variable with weight decay.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Note that the Variable is initialized with a truncated normal distribution.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    A weight decay is added only if one is specified.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Args:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      name: name of the variable123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      shape: list of ints123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      stddev: standard deviation of a truncated Gaussian123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      wd: add L2Loss weight decay multiplied by this float. If None, weight123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF          decay is not added for this Variable.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Returns:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF      Variable Tensor123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    dtype = tf.float16 if FLAGS.use_fp16 else tf.float32123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    var = _variable_on_cpu(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        name,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        shape,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.truncated_normal_initializer(stddev=stddev, dtype=dtype))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if wd is not None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        weight_decay = tf.multiply(tf.nn.l2_loss(var), wd, name='weight_loss')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tf.add_to_collection('losses', weight_decay)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return var123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF