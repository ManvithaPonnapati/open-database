import glob,os,sys,time
sys.path.append("../../affinityDB/")
import database
from ccdc import io
import ccdc

db_root = "/home/maksym/Projects/datasets/CSD1/"
pdb_folder = "pdbs"
afdb_file = "CSD1.db"
afdb = database.AffinityDB(os.path.join(db_root,afdb_file))
out_q,stop_event = afdb.open_table_with_queue(table_name="some_table",
                                              col_names=["ccdc_id","filename","SMILES"],
                                              col_types=[str,str,str])

# Creating a CSD entry reader
csd_entry_reader = io.EntryReader('CSD')

# Create a CSD entry reader including any updates
directory = ccdc.io.csd_directory()
csd_and_updates = glob.glob(os.path.join(directory, '*.inf'))
csd_and_updates_reader = io.EntryReader(csd_and_updates)


#for i in range(1000):
#    out_q.put(["srandom text"])

exceptions = []
i = 0
for mol in csd_entry_reader.molecules():
    start = time.time()
    try:
        ccdc_id = mol.identifier
        mol = mol.heaviest_component
        mol_smiles = mol.smiles
        assert len(mol_smiles) < 200
        outfile = ccdc_id + ".pdb"
        out_path = os.path.join(db_root,pdb_folder,outfile)
        assert not mol.is_polymeric
        assert mol.is_organic
        with io.MoleculeWriter(out_path) as filehandle:
            filehandle.write(mol)
            filehandle.close()
        out_q.put([ccdc_id,outfile,mol_smiles])
    except Exception as e:
        exceptions.append(e)
    print "exps:", "%.3f" % (1 / (time.time() - start)), "total:", i, "exceptions:", len(exceptions)
    i += 1

stop_event.set()
print "closing table with queue"
