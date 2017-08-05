import tensorflow as tf 
import time, os
from glob import glob

def read_my_file_format(filename_queue):
	reader = tf.TFRecordReader()
	key, example = reader.read(filename_queue)
	features = tf.parse_single_example(example, features={'labels':tf.FixedLenFeature([], tf.float32), #[], tf.int64
	                                                        'number_of_examples':tf.FixedLenFeature([], tf.int64), #[], tf.int64
	                                                        'elements':tf.VarLenFeature(tf.int64), #tf.int64
	                                                        'multiframe_coords': tf.VarLenFeature(tf.float32)}) 

	elements = features['elements'].values
	coords = features['multiframe_coords'].values
	return  elements, coords
	# print(sess.run(tf.shape(elements)))
	# print(sess.run(tf.shape(coords)))
	
	#lig_coords = tf.reshape(coords, coordinate_shape)
	#Need to reshape
	#print(sess.run(features['elements']))

if __name__ == "__main__":
	ligand_file_list = []
	db_path = '/home/urops/ryanh/export/test_stuff_5'
	#print(glob(os.path.join(db_path,"*[_]*.tfr")))
	for ligand_file in glob(os.path.join(db_path,"*[_]*.tfr")):
		ligand_file_list.append(ligand_file)
	index_list = range(len(ligand_file_list))
	examples_in_database = len(index_list)
	if examples_in_database == 0:
		raise Exception('tfr_input: No files found in the database path:', db_path)
	print "Indexed ligands in the database:", examples_in_database
	ligand_files = tf.convert_to_tensor(ligand_file_list,dtype=tf.string) 
	filename_queue = tf.train.string_input_producer(ligand_files,
	                                               num_epochs=None,shuffle=False)
	#Start session
	with tf.Session() as sess:
		init_op = tf.global_variables_initializer()
		coord = tf.train.Coordinator()
		threads = tf.train.start_queue_runners(sess=sess, coord=coord)
		for i in range(20):
			elements, coords = read_my_file_format(filename_queue) 
			print(sess.run(elements))
			print(sess.run(tf.shape(elements)))
			print(sess.run(coords))
			print(sess.run(tf.shape(coords)))
		coord.request_stop()
		coord.join(threads)
		sess.close()
	



