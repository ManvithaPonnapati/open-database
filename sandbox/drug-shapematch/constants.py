class CONSTANTS:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """Put hyperparameters here."""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """general network structure"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    num_training_epochs = 100123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    batch_size = 200123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    learning_rate = 1e-4123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """specifics for network"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # dropout123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    keep_probability = 0.6123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """rotation-specific stuff"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    max_angle_degrees = 360123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """computation/IO stuff"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    num_threads = 255123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    database_path = '../../../../../maksym/datasets/large_labeled_av4'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # directory where to write variable summaries123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    summaries_dir = './summaries'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # optional saved session: network from which to load variable states123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    saved_session = './summaries/1_max_angle_10_main_netstate/saved_state-25199'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # saved_session = None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # run name to use for variable/network saving123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    run_name = "max_angle_" + str(max_angle_degrees) + "_loaded_from_10"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """protein/ligand input info"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pixel_size = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    side_pixels = 20123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    nickname = "Andrew"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Logging123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print_info = True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # Info emailing123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    notification_email = 'andrew2000g@gmail.com'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    email_info = True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    email_and_save_every_n_steps = 300123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF