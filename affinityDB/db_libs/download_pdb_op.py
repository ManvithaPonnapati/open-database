import os,sys

class Download_pdb_init:
    this_module = sys.modules[__name__]
    def __init__(self,db_path,download_dir):
        download_path = os.path.join(db_path,download_dir)
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        self.db_path = db_path
        self.download_dir = download_dir
        self.this_module.download_pdb_init = self


def download_pdb(pdb_id,init="download_pdb_init"):
    """

    :param pdb_id:
    :param dir_path:
    :return:
    """
    init = eval(init)
    download_link = 'https://files.rcsb.org/download/{}.pdb'.format(pdb_id)
    download_path = os.path.join(init.db_path,init.download_dir)
    cmd = 'wget --no-check-certificate -P {} {}'.format(download_path, download_link)
    os.system(cmd)
    output_file = init.download_dir + "/" + download_link.split("/")[-1]
    return [[output_file]]
