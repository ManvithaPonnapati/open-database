import tensorflow as tf 
import time, os
from glob import glob

def read_my_file_format(myFile):
	reader = tf.TFRecordReader()
	_, example = reader.read(myFile)
	return example
	#features = tf.parse_example(example, features={'labels':tf.FixedLenFeature([], tf.float32), #[], tf.int64
	                                                        # 'number_of_examples':tf.FixedLenFeature([], tf.int64), #[], tf.int64
	                                                        # 'elements':tf.VarLenFeature(tf.int64), #tf.int64
	                                                        # 'multiframe_coords': tf.VarLenFeature(tf.float32)}) 

	elements = features['elements'].values
	coords = features['multiframe_coords'].values
	return  elements, coords

def big_read(batch):
	features = tf.parse_example(batch, features={'labels':tf.FixedLenFeature([], tf.float32), #[], tf.int64
	                                                        'number_of_examples':tf.FixedLenFeature([], tf.int64), #[], tf.int64
	                                                        'elements':tf.VarLenFeature(tf.int64), #tf.int64
	                                                        'multiframe_coords': tf.VarLenFeature(tf.float32)})

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
		example_list = [read_my_file_format(filename_queue) for myFile in ligand_file_list]
		print(example_list)
		batch_size = 5
		min_after_dequeue = 10000
		capacity = min_after_dequeue + 3 * batch_size
		example_batch, label_batch = tf.train.shuffle_batch_join(example_list, batch_size=batch_size, capacity=capacity,
				min_after_dequeue=min_after_dequeue)
		#for i in range(5):
		elements, coords = big_read(example_batch) 
		print(sess.run(elements))
		print(sess.run(tf.shape(elements)))
		print(sess.run(coords))
		print(sess.run(tf.shape(coords)))
		coord.request_stop()
		coord.join(threads)
		sess.close()
	



