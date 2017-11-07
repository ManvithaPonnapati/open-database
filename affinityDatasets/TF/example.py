import tensorflow as tf


def example_parse():
    parse_op = tf.load_op_library('../../affinityDB/lib_tf_op/parse.so')
    sess = tf.Session()

    pdb_path = tf.placeholder(tf.string)
    coords,atom_type,elem = parse_op.parse_pdb(pdb_path)
    sess.run(tf.initialize_all_variables())

    lig_coords, lig_atom_type, lig_elem = sess.run([coords,atom_type,elem],feed_dict={a:'lig.pdb'})

    print(lig_atom_type,lig_elem)

def example_score():
    parse_op = tf.load_op_library('../../affinityDB/lib_tf_op/parse.so')
    score_op = tf.load_op_library('../../affinityDB/lib_tf_op/score.so')
    sess = tf.Session()

    lig_path = tf.placeholder(tf.string)
    lig_coords, lig_atom_type, lig_elem = parse_op.parse_pdb(lig_path)

    rec_path = tf.placeholder(tf.string)
    rec_coords, rec_atom_type, rec_elem = parse_op.parse_pdb(rec_path)
    
    energy = score_op.score(lig_coords,lig_atom_type,rec_coords,rec_atom_type)
    sess.run(tf.initialize_all_variables())

    e = sess.run(energy,feed_dict={lig_path:'data/lig.pdb', rec_path:'data/rec.pdb'})

