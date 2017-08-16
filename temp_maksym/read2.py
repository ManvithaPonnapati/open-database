import tensorflow as tf
import numpy as np

# '_cryst_elem': tf.train.Feature(float_list=tf.train.FloatList(value=_cryst_elem)),
# '_cryst_coord': tf.train.Feature(float_list=tf.train.FloatList(value=_cryst_coord)),
# '_binders_nelem': tf.train.Feature(int64_list=tf.train.Int64List(value=_binders_nelem)),
# '_binders_elem': tf.train.Feature(float_list=tf.train.FloatList(value=_binders_elem)),
# '_binders_nframes': tf.train.Feature(int64_list=tf.train.Int64List(value=_binders_nframes)),
# '_binders_coordsets': tf.train.Feature(float_list=tf.train.FloatList(value=_binders_coordsets)),
# '_cryst_label': tf.train.Feature(float_list=tf.train.FloatList(value=_cryst_label)),
# '_binders_labels': tf.train.Feature(float_list=tf.train.FloatList(value=_binders_labels)),
# '_rec_elem': tf.train.Feature(float_list=tf.train.FloatList(value=_rec_elem)),
# '_rec_coord': tf.train.Feature(float_list=tf.train.FloatList(value=_rec_coord)),


def read_record_tfr(filename_queue):
    """
    Read into multiple frames

    :param filename_queue:
    :param lig_frame:
    :return:
    """
    features = {'_cryst_elem':tf.VarLenFeature(tf.float32),
                '_cryst_coord': tf.VarLenFeature(tf.float32),
                '_binders_elemslices': tf.VarLenFeature(tf.int64),
                '_binders_elem': tf.VarLenFeature(tf.float32),
                '_binders_coordslices': tf.VarLenFeature(tf.int64),
                '_binders_coordsets': tf.VarLenFeature(tf.float32),
                '_cryst_label': tf.FixedLenFeature([],tf.float32),
                '_binders_labels': tf.VarLenFeature(tf.float32),
                '_rec_elem': tf.VarLenFeature(tf.float32),
                '_rec_coord': tf.VarLenFeature(tf.float32),
                }

    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    example = tf.parse_single_example(serialized_example, features=features)

    _cryst_elem = example['_cryst_elem'].values
    _cryst_coord = example['_cryst_coord'].values
    _binders_elemslices = example['_binders_elemslices'].values
    _binders_elem = example['binders_elem'].values
    _binders_coordslices = example['_binders_coordslices'].values
    _binders_coordsets = example['_binders_coordsets'].values
    _cryst_label = example['_cryst_label']
    _binders_labels = example['_binders_labels'].values
    rec_elem = example['_rec_elem'].values
    rec_coord = example['_rec_coord'].values
    return None

def adapt_record_tfr(record_tfr,lig_frame):
    """
    Selects frame from otherwise unusable record
    :param record_tfr:
    :return:
    """
    _cryst_elem = record_tfr[0]
    _cryst_coord = record_tfr[1]
    _binders_nelem = record_tfr[2]
    _binders_nframes = record_tfr[3]
    _binders_coordsets = record_tfr[4]
    _cryst_label = record_tfr[5]
    _binders_labels = record_tfr[6]
    rec_elem = record_tfr[7]
    rec_coord = record_tfr[8]

    # select a relevant frame of the ligand
    if lig_frame == "CRYSTAL":
        lig_elem = _cryst_elem
        lig_coord = _cryst_coord
        label = _cryst_label
    elif lig_frame == "RANDOM_BINDER":
        # select/slice random binder
        num_binders = tf.shape(_binders_nframes)[0]
        rand_binder = tf.random_uniform(shape=[],minval=0,maxval=num_binders,dtype=tf.int32)
        start = (_binders_nelem - _binders_nelem[0])[rand_binder]


#        start = (_binders_nelem * _binders_nframes - (_binders_nelem[0] * _binders_nframes[0]))[rand_binder]
#        end = (_binders_nframes * _binders_nelem)[rand_binder] + start
        # select random frame

        return start


        #lig_elem = _cryst_elem
        #lig_coord = _cryst_coord
        #label = _cryst_label
#    else:
#        raise ValueError("not implemented")
    # # "RANDOM_BINDER"

    #return lig_elem,lig_coord,label,rec_elem,rec_coord


filename_queue = tf.train.string_input_producer(["/home/maksym/Desktop/try_tfr.tfr"], num_epochs=None, shuffle=True)
record_tfr = read_record_tfr(filename_queue)
answer = adapt_record_tfr(record_tfr,'RANDOM_BINDER')

sess = tf.Session()
coord = tf.train.Coordinator()
tf.train.start_queue_runners(sess,coord)

print sess.run(answer)
