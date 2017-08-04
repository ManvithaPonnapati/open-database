from av4_atomdict import atom_dictionary


def _receptor(path):
    return os.path.basename(path).split('_')[0]

def atom_to_number(atomname):
    atomic_tag_number = atom_dictionary.ATM[atomname.lower()]
    return atomic_tag_number

def _int_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))

def _float_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))

def _byte_feature(value):
    return tf.train.Feature(byte_list=tf.train.BytesList(value=value))

def save_with_format(filepath,labels,elements,multiframe_coords,d_format='tfr'):
    '''
    save the labels, elemetns and coords into as d_format file
    Args:
        filepath: path for the output file
        labels:  [0] for receptor [affinity] for crystal ligand
        elements: int64::list
        multiframe_coords:  
        d_format: output format ['tfr','pkl','av4']

    Returns: None

    '''
    labels = np.asarray(labels,dtype=np.float32)
    elements = np.asarray(elements,dtype=np.int32)
    multiframe_coords = np.asarray(multiframe_coords,dtype=np.float32)

    if not (int(len(multiframe_coords[:,0]) == int(len(elements)))):
        raise Exception('Number of atom elements is not equal to the number of coordinates')

    if multiframe_coords.ndim==2:
        if not int(len(labels))==1:
            raise Exception ('Number labels is not equal to the number of coordinate frames')
            
    else:
        if not (int(len(multiframe_coords[0, 0, :]) == int(len(labels)))):
            raise Exception('Number labels is not equal to the number of coordinate frames')

    number_of_examples = np.array([len(labels)], dtype=np.int32)

    if d_format == 'av4':
        av4_record = number_of_examples.tobytes()
        av4_record += labels.tobytes()
        av4_record += elements.tobytes()
        av4_record += multiframe_coords.tobytes()
        f = open(filepath, 'w')
        f.write(av4_record)
        f.close()

    
    elif d_format == 'pkl':
        dump_cont = [number_of_examples,labels, elements, multiframe_coords]




        cPickle.dump(dump_cont,open(filepath,'w'))

    elif d_format == 'tfr':
        writer = tf.python_io.TFRecordWriter(filepath)

        example = tf.train.Example(
            features=tf.train.Features(
                feature={
                    'number_of_examples': _int_feature(number_of_examples),
                    'labels': _float_feature(labels),
                    'elements': _int_feature(elements),
                    'multiframe_coords': _float_feature(multiframe_coords.reshape(-1))
                }
            )
        )
        serialized = example.SerializeToString()
        writer.write(serialized)






def save_tfr_one(save_path, rec_labels, rec_elements, rec_coords, lig_labels, lig_elements, lig_coords):
    '''
    record receptor and ligand into one TFRecords
    
    Args:
        save_path: path for output file
        rec_labels: always [0] for receptor
        rec_elements: int64::list
        rec_coords:  numpy.array 
        lig_labels:  numpy.array
        lig_elements: numpy.array
        lig_coords: numpy.array

    Returns: None

    '''

    rec_labels = np.asarray(rec_labels, dtype=np.float32)
    rec_elements = np.asarray(rec_elements, dtype=np.int32)
    rec_coords = np.asarray(rec_coords, dtype=np.float32)

    lig_labels = np.asarray(lig_labels, dtype=np.float32)
    lig_elements = np.asarray(lig_elements, dtype=np.int32)
    lig_coords = np.asarray(lig_coords, dtype=np.float32)

    if not (int(len(rec_coords[:,0]) == int(len(rec_elements)))):
        raise Exception('Receptor: Number of atom elements is not equal to the number of coordinates')

    if rec_coords.ndim==2:
        if not int(len(rec_labels))==1:
            raise Exception ('Receptor: Number labels is not equal to the number of coordinate frames')
            
    else:
        if not (int(len(rec_coords[0, 0, :]) == int(len(rec_labels)))):
            raise Exception('Rcecpeor: Number labels is not equal to the number of coordinate frames')


    if not (int(len(lig_coords[:,0]) == int(len(lig_elements)))):
        raise Exception('Ligand: Number of atom elements is not equal to the number of coordinates')

    if lig_coords.ndim==2:
        if not int(len(lig_labels))==1:
            raise Exception ('Ligand: Number labels is not equal to the number of coordinate frames')
            
    else:
        if not (int(len(lig_coords[0, 0, :]) == int(len(lig_labels)))):
            raise Exception('Ligand: Number labels is not equal to the number of coordinate frames')

    number_of_examples = np.array([len(lig_labels)], dtype=np.int32)

    writer = tf.python_io.TFRecordWriter(save_path)

    example = tf.train.Example(
        features=tf.train.Features(
            feature={
                'number_of_examples': _int_feature(number_of_examples),
                'ligand_labels': _float_feature(lig_labels),
                'ligand_elements': _int_feature(lig_elements),
                'ligand_coords': _float_feature(lig_coords.reshape(-1)),
                'receptor_labels':_float_feature(rec_labels),
                'receptor_elements':_int_feature(rec_elements),
                'receptor_coords':_float_feature(rec_coords.reshape(-1))
                }
            )
        )
    serialized = example.SerializeToString()
    writer.write(serialized)


def convert_and_save_data(base_dir, rec_path, lig_path, doc_path, position, affinity, d_format):
    """
    convert the receptor and ligand into given format
    
    
    
    in the database position is start with 1
    but when select coordinates be care that python list start with 0
    so we need np.asarray(position).sort()-1 to make it work
    Args:
        base_dir: directory for output file
        rec_path: path for receptor
        lig_path: path for ligand
        doc_path: path for docked ligand
        position: list of position for docked liangd, start with 1
        affinity: affinity value ( log affinity or norm faffinity
        d_format: output format [ pdb, pkl, av4, tfr, tfr_one ]

    Returns: (save_rec_path, save_lig_path) path of the output file
             (None, None) when failed to parse PDB file
             (save_path, None) when output format is tfr_one

    """

    REMOVE_HYDROGENS = True
    def remove_hydrogens(parsed_pdb):
        nonHydrogens = []
        for atom in parsed_pdb.iterAtoms():
            element = atom.getElement()
            coord = atom.getCoords()
            index = atom.getIndex()
            if atom.getElement() != 'H':
                    nonHydrogens.append([element, coord, index])
        return nonHydrogens

    print('In convert func')
    dest_dir = os.path.join(base_dir,d_format, _receptor(rec_path))
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    prody_receptor = prody.parsePDB(rec_path)
    prody_ligand = prody.parsePDB(lig_path)
    #Using remove hydrogens function
    if REMOVE_HYDROGENS:
        # FIXME (looping over all elements this way would be very slow)
        #receptor_elem = np.array([val[0] for val in remove_hydrogens(prody_receptor)]) #prody_receptor.getElements()
        #ligand_elem = np.array([val[0] for val in remove_hydrogens(prody_ligand)]) #prody_ligand.getElements()
        #
        #ligand_coords = np.array([val[1] for val in remove_hydrogens(prody_ligand)]) #remove_hydrogens(prody_ligand, coords=True)#prody_ligand.getCoords()
        
    else:
        receptor_elem = prody_receptor.getElements()
        ligand_elem = prody_ligand.getElements()
        ligand_coords = prody_ligand.getCoords()    

    receptor_coords = np.array([val[1] for val in remove_hydrogens(prody.parsePDB(rec_path))])
    labels = np.array([affinity], dtype=np.float32)
    if len(position):
        # docked list not empty
        prody_docked = prody.parsePDB(doc_path)
         # FIXME (looping over all elements this way would be very slow)
#        if REMOVE_HYDROGENS:
#            docked_elem = np.array([val[0] for val in remove_hydrogens(prody_docked)]) #remove_hydrogens(prody_docked, elements=True)#prody_docked.getElements()
#            docked_indices = np.array([val[2] for val in remove_hydrogens(prody_docked)]) #indices to remove in docked coords
#            docked_coords = prody_docked.getCoordsets()[np.asarray(position).sort() -1]
#           docked_coords = np.array([docked_coords[index] for index in docked_indices.tolist()])
#        else:

            docked_elem = prody_docked.getElements()                    
            docked_coords = prody_docked.getCoordsets()[np.asarray(position).sort() -1]
        assert all(np.asarray(docked_elem) == np.asarray(ligand_elem))
        for docked_coord in docked_coords:
            ligand_coords = np.dstack((ligand_coords, docked_coord))
            labels = np.concatenate((labels, [1.]))
    else:
        ligand_coords = np.expand_dims(ligand_coords,-1)
        
    try:
        receptor_elements = map(atom_to_number,receptor_elem)
        ligand_elements = map(atom_to_number,ligand_elem)
        
    except:
        return None, None

    if d_format == 'pdb':
        save_rec_name= os.path.basename(rec_path)
        save_rec_path = os.path.join(dest_dir, save_rec_name)
        #os.system('cp {} {}'.format(rec_path, save_rec_path))

        save_lig_name = os.path.basename(lig_path)
        save_lig_path = os.path.join(dest_dir, save_lig_name)
        if len(position):
            try:
                lig = prody.parsePDB(lig_path)
                doc = prody.parsePDB(doc_path)
                lig.addCoordset(doc.getCoordsets()[np.asarray(position).sort()-1])
            except Exception as e:
                print(e)
                exit(1)

            prody.writePDB(save_lig_path, lig)
        else:
            os.system('cp {} {}'.format(lig_path, save_lig_path))
        os.system('cp {} {}'.format(rec_path, save_rec_path))

        return save_rec_path, save_lig_path



    if d_format == 'tfr_one':
        save_name = os.path.basename(rec_path).replace('_receptor.pdb','.tfr')
        save_path = os.path.join(dest_dir, save_name)
        save_tfr_one(save_path, 
                     [0], 
                     receptor_elements, 
                     receptor_coords, 
                     labels,
                     ligand_elements, 
                     ligand_coords)
        return save_path, None
    
    rec_name = os.path.basename(rec_path).replace('.pdb','.%s' % d_format)
    lig_name = os.path.basename(lig_path).replace('.pdb','.%s' % d_format)
    
    
    rec_path = os.path.join(dest_dir,rec_name)
    lig_path = os.path.join(dest_dir,lig_name)
    save_with_format(rec_path,[0], receptor_elements, receptor_coords, d_format)
    save_with_format(lig_path, labels , ligand_elements, ligand_coords, d_format)
    return rec_path, lig_path
