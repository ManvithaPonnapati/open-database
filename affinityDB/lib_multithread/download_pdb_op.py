import os,sys

class Download_pdb_init:
    this_module = sys.modules[__name__]
    arg_types = [str]
    out_types = [str,str]
    out_names = ["pdb_id","pdb_file"]

    def __init__(self,db_root,download_dir):
        """
        Initialize download func
        :param db_root: string (root folder directory for the files in the database)
        :param download_dir: string (name of the directory where to put downloaded PDBs)
        :return:
        None
        """
        download_path = os.path.join(db_root,download_dir)
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        self.db_path = db_root
        self.download_dir = download_dir
        self.this_module.download_pdb_init = self


def download_pdb(pdb_id,init="download_pdb_init"):
    """ Download PDB crystal structure from the Protein Data Bank.
    
    Example:
    <pre lang="python">
    download_pdb('104M')
    </pre>

    Output:
    <pre lang="python">
    [['104M','download/104M.pdb']]
    </pre>

    :param pdb_id: string (4-letter PDB ID IE: 1QGT)
    :param dir_path: string (folder in which to save the pdb file)
    :return: 
    nested list [[pdb_identifier, download_file_path]]
    """
    init = eval(init)
    download_link = 'https://files.rcsb.org/download/{}.pdb'.format(pdb_id)
    download_path = os.path.join(init.db_path,init.download_dir)
    cmd = 'wget --no-check-certificate -P {} {}'.format(download_path, download_link)
    os.system(cmd)
    output_file = os.path.join(init.download_dir,download_link.split("/")[-1])
    return [[pdb_id,output_file]]