# Concat Net123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF### Experiment 1 Pixel Size/Cutoff123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFIt is an optimization of a single-layer network consisting of tf.nn.concat_nonlinear_conv3d() 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFconvolutional layer + FC + FC.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFTrying different pixel sizes and cuttoffs. The only parameters changing are:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF1) Pixel size in the first (single) convolutional layer123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF2) Cutoff for the pairlist distance123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFV1: pixel size: 0.5 pairlist distance: 5123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFV2: pixel size: 1 pairlist distance: 5123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFV3: pixel size: 0.5 pairlist distance: 2.5123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFV4: pixel size: 0.3 pairlist distance 1.5123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFV5: pixel size: 0.5 pairlist distance 5 ( I had to substitute convolution size 11x11x11 to 21x21x21 in layer 1) 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFV6: pixel size: 0.3 pairlist distance 3 ( I had to substitute convolution size 11x11x11 to 21x21x21 in layer 1)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFCross entropy: 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFV1: 0.52 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFV2: 0.45123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFV3: 0.5123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFV4: 0.43123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFV5: 0.5123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFV6: 0.44123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFFrom python notebook since fluctuations seem to be very large:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFV1: mean: 0.54 std: 0.05123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFV2: mean: 0.47 std: 0.052123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFV3: mean: 0.48 std: 0.05123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFV4: mean: 0.47 std: 0.05123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFV5: mean: 0.51 std: 0.053123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFV6: mean: 0.46 std: 0.07 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF