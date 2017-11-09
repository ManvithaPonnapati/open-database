import tensorflow as tf 
import numpy as np 
from glob import glob
parse_pdb = tf.load_op_library("parsePdb.so").parse_pdb
score = tf.load_op_library("score.so").score

def read_tfr(fname_queue, decode_dict):
    """
    parse Tensorflow Record
    fname_queue : queue of filename
    decode_dict : key word for content to parse
    """
    _decoder = {}
    if "coords" in decode_dict:
        _decoder['_coords'] = tf.VarLenFeature(tf.float32)
    
    if "atom_type" in decode_dict:
        _decoder['_atom_type'] = tf.VarLenFeature(tf.int64)

    if "atom_elem" in decode_dict:
        _decoder['_atom_elem'] = tf.VarLenFeature(tf.float32)
    
    if "bonds" in decode_dict:
        _decoder['_bonds'] = tf.VarLenFeature(tf.int64)

    reader = tf.TFRecordReader()
    filename, serialized_example = reader.read(fname_queue)
    record_proto = tf.parse_single_example(serialized_example, features=_decoder)

    decoded = {}
    decoded['filename'] = filename
    if "coords" in decode_dict:
        decoded["coords"] = record_proto["_coords"].values
    if "atom_type" in decode_dict:
        decoded["atom_type"] = record_proto["_atom_type"].values
    if "atom_elem" in decode_dict:
        decoded["atom_elem"] = record_proto["_atom_elem"].values
    if "bonds" in decode_dict:
        decoded["bonds"] = record_proto["_bonds"].values
    return decoded

def parsePDB(fname_queue, parse_dict):
    """
    parse PDB file
    fname_queue : queue of filenqme
    parse_dict : key word for content to parse
    """
    fname = fname_queue.dequeue()
    coords, atom_type, atom_elem, bonds = parse_pdb(fname)

    data = {"filename":fname}
    if "coords" in parse_dict:
        data["coords"] = coords
    if "atom_type" in parse_dict:
        data["atom_type"] = atom_type
    if "atom_elem" in parse_dict:
        data["atom_elem"] = atom_elem
    if "bonds" in parse_dict:
        data["bonds"] = bonds
    return data

def writeTFR(data,ofile):
    """
    save parsed data into Tensorflow Record
    data: tuple (coords, atom_type, atom_elem, bonds)
    ofile: path of TFR file

    """
    if "coords" in data:
        coords = data['coords']
    if "atom_type" in data:
        atom_type = data['atom_type']
    if "atom_elem" in data:
        atom_elem = data['atom_elem']
    if "bonds" in data:
        bonds = data['bonds']
    record_proto = {}

    # check atom num
    if "coords" in data and "atom_type" in data:
        assert coords.shape[0] == atom_type.shape[0], "Atom number conflict in coords and atom type"
    
    if "atom_type" in data and "atom_elem" in data:
        assert atom_type.shape[0] == atom_elem.shape[0], "Atom number conflict in atom type and atom elem"

    if "coords" in data:
        # check coords
        assert type(coords) == np.ndarray, "expected coords to be ndarray"
        assert len(coords.shape) == 2, "expected coords is 2d array"
        assert coords.shape[1] == 3, "expected coords.shape[1] to be 3: [x,y,z]"
        assert coords.dtype == np.float32, "expected coords to be float 32"
        _coords = coords.reshape([-1])
        record_proto['_coords'] = tf.train.Feature(float_list=tf.train.FloatList(value=_coords))
        
    if "atom_type" in data:
        # check atom type
        assert type(atom_type) == np.ndarray, "expected atom type to be ndarray"
        assert len(atom_type.shape) == 1, "expected atom type to be 1d array"
        assert atom_type.dtype==np.int32, "expected atom type to be int 32"
        _atom_type = atom_type.reshape([-1])
        record_proto['_atom_type'] = tf.train.Feature(int64_list=tf.train.Int64List(value=_atom_type))

    if "atom_elem" in data:
        # check atom elem
        assert type(atom_elem) == np.ndarray, "expected atom elem to be ndarray"
        assert len(atom_elem.shape) == 1, "expected atom elem to be 1d array"
        assert atom_elem.dtype==np.float32, "expected atom elem to be float 32"
        _atom_elem = atom_elem.reshape([-1])
        record_proto['_atom_elem'] = tf.train.Feature(float_list=tf.train.FloatList(value=_atom_elem))

    if "bonds" in data:
    # check bonds
        assert type(bonds) == np.ndarray, "expected bonds to be ndarray"
        assert bonds.shape[1] == 2, "expected bonds.shape[1] to be 2 [atom_a, atom_b]"
        assert bonds.dtype == np.int32, "expected bonds to be int 32"
        _bonds = bonds.reshape([-1])
        record_proto['_bonds'] = tf.train.Feature(int64_list=tf.train.Int64List(value=_bonds))

    writer = tf.python_io.TFRecordWriter(ofile)
    example = tf.train.Example(features=tf.train.Features(feature=record_proto))
    serialized = example.SerializeToString()
    writer.write(serialized)
    writer.close()
    return True

def make_queue(path, pattern):
    """
    create filename queue
    path: root dir of data
    pattern: e.g. "*.pdb" for all pdb file under path
    """
    flist = glob(os.path.join(path, pattenr))
    flist_tensor = tf.convert_to_tensor(flist,tf.string)
    queue = tf.train.string_input_producer(flist_tensor)
    return queue


def eg_read():
    """
    example of reading TensorFlow Record
    """
    sess = tf.Session()
    fname_queue = make_queue('data','*.tfr')
    decoded = read_tfr(fname_queue,{"coords":None, "atom_type":None})
    sess.run(tf.global_variables_initializer())

    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)

    d = sess.run(decoded)
    print d

def eg_parse():
    """
    example of parsing PDB file
    """
    sess = tf.Session()
    fname_queue = make_queue('data','*.pdb')
    data = parsePDB(fname_queue,{"coords":[], "atom_type":[],"atom_elem":[], "bonds":[]})

    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)

    d = sess.run(data)
    ofile = d['filename'].replace('.pdb','.tfr')
    writeTFR(d, ofile)
    

def eg_score():
    """
    example of intermolecula energy scoring
    """
    sess = tf.Session()
    fname_queue = make_queue('data','*.tfr')

    data = parsePDB(fname_queue,{"coords":[], "atom_type":[]})
    data2 = parsePDB(fname_queue,{"coords":[], "atom_type":[]})

    energy = score(data['coords'], data['atom_type'], data2['coords'], data2['atom_type'])

    coord = tf.train.Coordinator()
    threadds = tf.train.start_queue_runners(sess=sess, coord=coord)

    e = sess.run(energy)
    print e
