# Affinity Core V3123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFAffinity core is a starting code for training deep convolutional neural networks on crystallographic images of proteins to predict drug binding. In the simplest case, training set consists of two sets of structures of complexes of proteins together with small molecules labeled either 1 or 0 (binders and decoys). Networks can be used to classify and rank unlabeled complexes.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFAfter a few hours of training network visualization in tensorboard might look [like this](http://ec2-54-244-199-10.us-west-2.compute.amazonaws.com/)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF### scripts:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF**database_master** [av3_database_master.py](./av3_database_master.py)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFcrawls and indexes directoris, parses protein and ligand structures (.pdb files) into numpy (.npy) arrays with 4 columns. The first three columns store the coordinates of all atoms, fourth column stores an atom tag (float) corresponding to a particular element. Hashtable that determines correspondence between some chemical elements a particular number is sourced from [av3_atomdict.py](./av2_atomdict.py). 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFBecause the most commonly used in crystallography .pdb format is inherently unstable, some (~0.5%) of the structures may fail to parse. Database master handles and captures errors in this case. After .npy arrays have been generated, database master creates label-ligand.npy-protein.npy trios and writes them into database_index.csv file. 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFinally, database master reads database_index.csv file, shuffles it, and safely splits the data into training and testing sets.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF***av3*** [av3.py](./av3.py)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFthe main script. Takes database index (train_set.csv), and .npy arrays as an input. Performs training and basic evaluation of the network. av3 depends on av3_input.py which fills the queue with images. By default, av3 is attempting to minimize weighted cross-entropy for a two-class sclassification problem with FP upweighted 10X compared to FN. For [more details see](https://www.tensorflow.org/versions/r0.11/api_docs/python/nn.html#weighted_cross_entropy_with_logits):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF<pre>123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtf.nn.weighted_cross_entropy_with_logits()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF</pre>123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFWhile running, the main script creates directoris with various outputs:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF<pre>123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF/summaries/x_logs       # stores logs for training error123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF/summaries/x_netstate   # stores state of the network123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF/summaries/x_test       # stores the data to visualize training with tensorboard123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF/summaries/x_train      # stores the data to visualize testing with tensorboard123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF</pre> 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF***av3_input*** [av3_input.py](./av3_input.py)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFhandles data preprocessing, starts multiple background threads to convert protein and drug coordinates into 3d images of pixels. Each of the background workers performs the following procedures:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF1. reads the ligand from .npy file123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF2. randomly initializes box nearby the center of mass of the ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF3. rotates and shifts the box until all of the ligand atoms can fit123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF4. reads the protein123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF5. crops the protein atoms that can't fit inside the cube123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF6. rounds coordinates and converts sparse tensor(atoms) to dense(pixels)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF7. enqueues image and label123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFIn order to organize reading of protein-ligand pairs in random order in such a way that each pair is only seen once by a single worker during one epoch, and also to count epchs, custom123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF<pre>123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfilename_coordinator_class()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF</pre> 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFcontrols the process. After a specified number of epochs has been reached, filename coordinator closes the main loop and orders enqueue workers to stop.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF***av3_eval*** [av3_eval.py](./av3_eval.py)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFrestores the network from the saved state and performs its evaluation. At first, it runs throught the dataset several times to accumulate predictions. After evaluations, it averages all of the predictions and ranks and reorders the dataset by prediction averages in descending order.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFinally, it calculates several prediction measures such as top_100_score(number of TP in TP_total first lines of the list), confusion matrix, Area Under the Curve and writes sorted predictions, and computed metrics correspondingly into:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF<pre>123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF/summaries/x_logs/x_predictions.txt123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF/summaries/x_logs/x_scores.txt123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF</pre>123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF### benchmark:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFWe have trained the network on a large subsample (~30K) of structures from [Protein Data Bank](http://www.rcsb.org/). We have generated 10 decoys by docking every ligand back to its target and selecting only ones with Root Mean Square Deviation > 6A. 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFApproximately 250 images/sec can be generated and enqueued by a single processor.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFOne epoch took approximately 25 minutes on a single processor and one K80 GPU.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFWith a 4-layer network we have achieved: 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtop_100_score: 73.09123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFconfusion matrix(\[\[TP FP\] \[FN TN\]\]):  \[\[2462 293\] \[ 2745 40519\]\]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFAUC: 0.92123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF