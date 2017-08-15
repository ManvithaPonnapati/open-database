import tensorflow as tf
import numpy as np

# class
# get coordinates; write tensorflow record (each process creates it's own class writer)
# read record; a function gives a tensor and creates an enq_op; done !


def save_record_VDS1(filename,norm_affinity,dock_scores,lig_elem,lig_coord,dock_coords,rec_elem,rec_coord):
    """

    :param filename:
    :param number_of_examples:
    :param lig_labels:
    :param lig_elements:
    :return:
    """

    lig_coord = np.reshape(lig_coord,[-1])
    dock_coords = np.reshape(dock_coords,[-1])
    rec_coord = np.reshape(rec_coord,[-1])

    writer = tf.python_io.TFRecordWriter(filename)
    example = tf.train.Example(
        features=tf.train.Features(
            feature={
                'norm_affinity': tf.train.Feature(float_list=tf.train.FloatList(value=norm_affinity)),
                'dock_scores': tf.train.Feature(float_list=tf.train.FloatList(value=dock_scores)),
                'lig_elem': tf.train.Feature(int64_list=tf.train.Int64List(value=lig_elem)),
                'lig_coord': tf.train.Feature(float_list=tf.train.FloatList(value=lig_coord)),
                'dock_coords': tf.train.Feature(float_list=tf.train.FloatList(value=dock_coords)),
                'rec_elem': tf.train.Feature(int64_list=tf.train.Int64List(value=rec_elem)),
                'rec_coord': tf.train.Feature(float_list=tf.train.FloatList(value=rec_coord))
            }
        )
    )
    serialized = example.SerializeToString()
    writer.write(serialized)
    writer.close()
    return None



norm_affinity = np.array([0.9292],np.float32)
dock_scores = np.array([9.3,9.5,3.6],np.float32)
lig_elem = np.array([1,2,3,1],np.int64)

lig_coord = np.array([[0.1,0.1,0.1],
                      [0.2,0.2,0.2],
                      [0.3,0.3,0.3],
                      [0.4,0.4,0.4]],np.float32)

dock_coords = np.array([[[1,0.1,0.1],
                           [0.2,0.2,0.2],
                           [0.3,0.3,0.3],
                           [0.4,0.4,0.4]],
                          [[2,0.1,0.1],
                           [0.2,0.2,0.2],
                           [0.3,0.3,0.3],
                           [0.4,0.4,0.4]],
                          [[3, 0.1, 0.1],
                           [0.2, 0.2, 0.2],
                           [0.3, 0.3, 0.3],
                           [0.4, 0.4, 0.4]]],np.float32)

rec_elem = np.array([1,2,3,4,5,6,7],np.int64)
rec_coord = np.array([[0,0,0],
                     [1,1,1],
                     [2,2,2],
                     [3,3,3],
                     [4,4,4],
                     [5,5,5],
                     [6,6,6]],np.float32)


save_record_VDS1(filename= "one.tfr",
                 norm_affinity=norm_affinity,
                 dock_scores=dock_scores,
                 lig_elem=lig_elem,
                 lig_coord=lig_coord,
                 dock_coords=dock_coords,
                 rec_elem=rec_elem,
                 rec_coord=rec_coord)
# Input pipe

