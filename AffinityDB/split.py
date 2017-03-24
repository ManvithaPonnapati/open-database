'''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFload PDB download from RCSB123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsplit it into receptor and hetero123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif hetero's heavy atom more than threshold123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFsave the receptor and hetero ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF'''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport os,sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport prody123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport getopt123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport multiprocessing123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom glob import glob123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport config123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom utils import log,mkdir123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef split_structure(pdb_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pdb_name = os.path.basename(pdb_path).split('.')[0].lower()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        parsed = prody.parsePDB(pdb_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    except Exception as e:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        log('parse_failed.log','{},{}'.format(pdb_name,str(e)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        header = prody.parsePDBHeader(pdb_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        log('resolution.txt','{},{}'.format(pdb_name,header['resolution']))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    except Exception as e:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        log('parse_header_failed.log','{},{}',format(pdb_name, str(e)))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    hetero = parsed.select(123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '(hetero and not water) or resname ATP or resname ADP or resname AMP or resname GTP or resname GDP or resname GMP')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF   123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    receptor = parsed.select('protein or nucleic')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if receptor is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        log("select_failed.log","{},doesn't have receptor.\n".format(pdb_name))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if hetero is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        log("select_failed.log","{},doesn't have ligand.\n".format(pdb_name))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    # write ligand into file123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for each in prody.HierView(hetero).iterResidues():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ResId = each.getResindex()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ResName = each.getResname()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ligand_path = os.path.join(config.splited_ligands_path, pdb_name, "{}_{}_{}_ligand.pdb".format(pdb_name, ResName, ResId))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        mkdir(os.path.dirname(ligand_path))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        prody.writePDB(ligand_path, each) 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    receptor_path = os.path.join(config.splited_receptors_path, pdb_name + '.pdb')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    prody.writePDB(receptor_path, receptor)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    log('success_ligand.log','{} success'.format(pdb_name))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef split(target_list):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    mkdir(config.splited_receptors_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pool = multiprocessing.Pool(config.process_num)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pool.map_async(split_structure,target_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pool.close() 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    pool.join()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF   123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #map(split_structure,target_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif __name__ == '__main__':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    target_list = glob(os.path.join(config.pdb_download_path,'*.pdb'))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "target ",len(target_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    args = sys.argv123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if len(args)>2:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        a = int(args[1])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        b = int(args[2])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        parts = np.linspace(0,len(target_list),int(a)+1).astype(int)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        target_list = target_list[parts[b-1]:parts[b]]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    split(target_list)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF