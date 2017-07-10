# Global constants describing the MSHAPES data set.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFIMAGE_SIZE = 100123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFNUM_CLASSES = 2123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFNUM_EXAMPLES_PER_EPOCH_FOR_TRAIN = 50000123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFNUM_EXAMPLES_PER_EPOCH_FOR_EVAL = 10000123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# How many examples to use for training in the queue123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFNUM_EXAMPLES_TO_LOAD_INTO_QUEUE = 40000123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# Constants describing the training process.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFMOVING_AVERAGE_DECAY = 0.9999  # The decay to use for the moving average.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFNUM_EPOCHS_PER_DECAY = 350.0  # Epochs after which learning rate decays.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFLEARNING_RATE_DECAY_FACTOR = 0.1  # Learning rate decay factor.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFINITIAL_LEARNING_RATE = 0.1  # Initial learning rate.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# If a model is trained with multiple GPUs, prefix all Op names with tower_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# to differentiate the operations. Note that this prefix is removed from the123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# names of the summaries when visualizing a model.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFTOWER_NAME = 'tower'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# Where to download the MSHAPES dataset from123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFDATA_URL = 'https://electronneutrino.com/affinity/shapes/datasets/MSHAPES_30DEG_ONECOLOR_SIMPLE_50k_100x100.zip'