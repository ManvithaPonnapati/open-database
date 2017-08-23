import tensorflow as tf
import numpy as np


def read_features_tfr(filename_queue):
    """
    Reads tensorflow record into features (stacked arrays of labels/elements/coordinates)

    :param filename_queue: tensorflow string input producer
    return: features
    """
    features = {'_cryst_elem':tf.VarLenFeature(tf.float32),
                '_cryst_coord': tf.VarLenFeature(tf.float32),
                '_binders_nelem': tf.VarLenFeature(tf.int64),
                '_binders_elem': tf.VarLenFeature(tf.float32),
                '_binders_nframes': tf.VarLenFeature(tf.int64),
                '_binders_coordsets': tf.VarLenFeature(tf.float32),
                '_cryst_label': tf.FixedLenFeature([],tf.float32),
                '_binders_labels': tf.VarLenFeature(tf.float32),
                '_rec_elem': tf.VarLenFeature(tf.float32),
                '_rec_coord': tf.VarLenFeature(tf.float32),
                }

    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    example = tf.parse_single_example(serialized_example, features=features)

    cryst_elem = example['_cryst_elem'].values
    cryst_coord = tf.reshape(example['_cryst_coord'].values,[-1,3])
    _binders_nelem = example['_binders_nelem'].values
    _binders_elem = example['_binders_elem'].values
    _binders_nframes = example['_binders_nframes'].values
    _binders_coordsets = example['_binders_coordsets'].values
    cryst_label = example['_cryst_label']
    _binders_labels = example['_binders_labels'].values
    rec_elem = example['_rec_elem'].values
    rec_coord = tf.reshape(example['_rec_coord'].values,[-1,3])
    return cryst_elem, cryst_coord, _binders_nelem, _binders_elem, _binders_nframes, _binders_coordsets, \
           cryst_label,_binders_labels,rec_elem, rec_coord

def adapt_features_tfr(tfr_record,lig_frame):
    """
    Unpacks stacked arrays of ligand elements/frames/coordinates into a frame and coordinate set to use.
    :param record_tfr: list of tensors (raw features from file)
    :param lig_frame string (select sampling method to choose coordinates of the ligand)
    :return: label,lig_elem,lig_coord,rec_elem,rec_coord
    """

    cryst_elem = tfr_record[0]
    cryst_coord = tfr_record[1]
    _binders_nelem = tfr_record[2]
    _binders_elem = tfr_record[3]
    _binders_nframes = tfr_record[4]
    _binders_coordsets = tfr_record[5]
    cryst_label = tfr_record[6]
    _binders_labels = tfr_record[7]
    rec_elem = tfr_record[8]
    rec_coord = tfr_record[9]

    # select a relevant frame of the ligand
    if lig_frame == "CRYSTAL":
        label = cryst_label
        lig_elem = cryst_elem
        lig_coord = cryst_coord
    elif lig_frame == "RANDOM_BINDER":
        # select/slice random binder
        num_binders = tf.shape(_binders_nelem)[0]
        rand_binder = tf.random_uniform(shape=[],minval=0,maxval=num_binders,dtype=tf.int32)
        # takes corresponding to frames labels
        num_frames = tf.to_int32(_binders_nframes[rand_binder])
        past_frames = tf.to_int32(tf.slice(tf.concat([[0],_binders_nframes],0),[0],[rand_binder+1]))
        lig_labels = tf.slice(_binders_labels,[tf.reduce_sum(past_frames)],[num_frames])
        # take corresponding elements
        num_elem = tf.to_int32(_binders_nelem[rand_binder])
        past_elem = tf.to_int32(tf.slice(tf.concat([[0], _binders_nelem], 0), [0], [rand_binder + 1]))
        lig_elem = tf.slice(_binders_elem,[tf.reduce_sum(past_elem)],[num_elem])
        # take corresponding coordset
        coordsizes = _binders_nframes * _binders_nelem * 3
        coordsize = coordsizes[rand_binder]
        past_coordsizes = tf.slice(tf.concat([[0], coordsizes], 0), [0], [rand_binder + 1])
        coordset = tf.slice(_binders_coordsets,[tf.reduce_sum(past_coordsizes)],[coordsize])

        # select a random frame
        rand_frame = tf.random_uniform(shape=[], minval=0, maxval=num_frames, dtype=tf.int32)
        label = lig_labels[rand_frame]
        past_coord = num_elem * rand_frame * 3
        lig_coord = tf.slice(coordset, [tf.reduce_sum(past_coord)], [num_elem*3])
        return label,lig_elem,lig_coord,rec_elem,rec_coord

filename_queue = tf.train.string_input_producer(["/home/maksym/Desktop/try_tfr.tfr"], num_epochs=None, shuffle=True)
tfr_record = read_features_tfr(filename_queue)
answer = adapt_features_tfr(tfr_record,'RANDOM_BINDER')

sess = tf.Session()
coord = tf.train.Coordinator()
tf.train.start_queue_runners(sess,coord)

print sess.run(answer)
