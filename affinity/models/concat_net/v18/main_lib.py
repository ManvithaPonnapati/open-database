import tensorflow as tf123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom glob import glob123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport os,sys,re123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef index_ars_database_into_q(db_path, shuffle):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """ Indexes the PDBBind database using the same method as for the av4 database,123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    but with different naming conventions. The ligand file ends in _ligand.av4123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    and the protein file ends in _receptor.av4123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param db_path:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :param shuffle:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    :return:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # TODO logging for debug123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    lig_files = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    rec_files = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "number of (folders) crystal structures:", len(glob(os.path.join(db_path+'/**/')))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for PDB_folder in glob(os.path.join(db_path+'/**/')):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lig_files_ondisk = glob(os.path.join(PDB_folder,"*_ligand.av4"))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        rec_files_ondisk = np.asarray(glob(os.path.join(PDB_folder,"*_receptor.av4")))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for lig_file in lig_files_ondisk:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            rec_file = re.sub("_ligand.av4","_receptor.av4",lig_file)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            num_rec_files = np.where(rec_files_ondisk==rec_file)[0].size123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if num_rec_files is not 1:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                raise Exception('a single receptor for ligand ',lig_file,'is expected',num_rec_files,'found')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                lig_files.append(lig_file)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                rec_files.append(rec_file)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    num_rec_lig_pairs = len(lig_files)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if num_rec_lig_pairs ==0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        raise Exception('av4_input: No files found in the database:',db_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "number of receptor-ligand pairs in the database:",num_rec_lig_pairs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        index_list = range(num_rec_lig_pairs)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # create a filename queue (tensor) with the names of the ligand and receptors123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    index_list = tf.convert_to_tensor(index_list,dtype=tf.int32)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    lig_files = tf.convert_to_tensor(lig_files,dtype=tf.string)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    rec_files = tf.convert_to_tensor(rec_files,dtype=tf.string)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    filename_queue = tf.train.slice_input_producer([index_list,lig_files,rec_files],num_epochs=None,shuffle=shuffle)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return filename_queue,num_rec_lig_pairs123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF