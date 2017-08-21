import tensorflow as tf
import numpy as np


def decode_record_VDS1(filename_queue):
    """

    :param filename_queue:
    :return:
    """
    features = {'norm_affinity':tf.FixedLenFeature([],tf.float32),
                'dock_scores':tf.VarLenFeature(tf.float32),
                'lig_elem':tf.VarLenFeature(tf.int64),
                'lig_coord':tf.VarLenFeature(tf.float32),
                'dock_coords':tf.VarLenFeature(tf.float32),
                'rec_elem':tf.VarLenFeature(tf.int64),
                'rec_coord':tf.VarLenFeature(tf.float32)
                }

    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    example = tf.parse_single_example(serialized_example, features=features)
    norm_affinity = example['norm_affinity']
    dock_scores = example['dock_scores'].values
    lig_elem = example['lig_elem'].values
    lig_coord = example['lig_coord'].values
    dock_coords = example['dock_coords'].values
    rec_elem = example['rec_elem'].values
    rec_coord = example['rec_coord'].values

    # reshape flat tensors into tensors with dimensions
    num_lig_atm = tf.shape(lig_elem)[0]
    num_dock = tf.shape(dock_scores)[0]
    num_rec_atm = tf.shape(rec_elem)[0]
    lig_coord = tf.reshape(lig_coord,[num_lig_atm,3])
    dock_coords = tf.reshape(dock_coords,[num_dock,num_lig_atm,3])
    rec_coord = tf.reshape(rec_coord,[num_rec_atm,3])
    return norm_affinity,dock_scores,lig_elem,lig_coord,dock_coords,rec_elem,rec_coord

filename_queue = tf.train.string_input_producer(["one.tfr"], num_epochs=None, shuffle=True)
example = decode_record_VDS1(filename_queue)


sess = tf.Session()
coord = tf.train.Coordinator()
tf.train.start_queue_runners(sess,coord)


print sess.run(example)