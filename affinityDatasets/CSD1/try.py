import glob,os,sys,time
sys.path.append("../../affinityDB/")
import database
from ccdc import io
import ccdc


db_root = "/home/maksym/Projects/datasets/CSD1/"
pdb_folder = "pdbs"
#afdb_file = "CSD1.db"
#afdb = database.AffinityDB(os.path.join(db_root,afdb_file))
#sql_cmd = "create table out_001_CSD_load (ccdc_id string, smiles string, outfile string)"
#afdb.conn.execute(sql_cmd)
#sql_tmp = "insert into out_001_CSD_load values(\"{}\",\"{}\",\"{}\")"


# Creating a CSD entry reader
csd_entry_reader = io.EntryReader('CSD')

# Create a CSD entry reader including any updates
directory = ccdc.io.csd_directory()
csd_and_updates = glob.glob(os.path.join(directory, '*.inf'))
csd_and_updates_reader = io.EntryReader(csd_and_updates)

i = 0
exceptions = []
commit_sec = 1
#commit_clock = time.time()
#print csd_entry_reader.molecules()

# Loop over all the molecules
for mol in csd_entry_reader.molecules():
    start = time.time()
    try:
        ccdc_id = mol.identifier
#        mol = mol.heaviest_component
#        mol_smiles = mol.smiles
#        assert len(mol_smiles) < 60
#        outfile = ccdc_id + ".pdb"
#        out_path = os.path.join(db_root,pdb_folder,outfile)

#        with io.MoleculeWriter(out_path) as filehandle:
#            filehandle.write(mol)
#            filehandle.close()

#        sql_cmd = sql_tmp.format(ccdc_id,mol_smiles,outfile)
#        afdb.conn.execute(sql_cmd)
#        if time.time() - start > commit_sec:
#            afdb.conn.commit()
    except Exception as e:
        exceptions.append(e)
    print "exps:", "%.3f" % (1 / (time.time() - start)),"total:",i, "exceptions:", len(exceptions)
    i+=1