import os,sys
import sqlite3

# FIXME: explanations
# FIXME: I think it needs target confidense as in AtomWise

class Activity_init:
    this_module = sys.modules[__name__]
    def __init__(self, data_dir, db_path):
        """
        Initialize activity func
        :param data_dir: str dir for the folder to save data
        :param db_path: str path for the chembl database
        :return:
        None
        """

        self.data_dir = data_dir
        self.db_path = '/data/affinity/chembl/chembl_23/chembl_23_sqlite/chembl_23.db'
        self.this_module.activity_init = self


def activity(pair_name, target_id, init='activity_init'):
    """
    Getting bioactivity result from local chembl database \
    query by the `target_chembl_id`

    Example:
    <pre lang="python">
    activity('154L_A_188_NAG','CHEMBL2366438')
    </pre>

    Output:
    <pre lang="python">
    [['154L_A_188_NAG','CHEMBL3070308','CHEMBL2366438','CHEMBL223593',9,'IC50','=',28.0,'nM','CC(Oc1ccc(Oc2ncc(cc2Cl)C(F)(F)F)cc1)C(=O)O']]
    </pre>


    :param pair_name: str combined receptor id and ligand info {receptor_id}_{chain}_{resnum}_{resname}
    :param target_id: str chembl_target_id
    :param init: str init function name
    :return:
    nested list:
    [pair_name, aid, tid, mid, confidence_score, type, relation, value, unit, smile]
    """
    init = eval(init)
    conn = sqlite3.connect(init.db_path)

    tid = conn.execute('select tid from target_dictionary where chembl_id=\"{}\";'.format(target_id)).fetchone()[0]

    assay_tbinfo = conn.execute('pragma table_info (assays)').fetchall()
    assay_cols = [_[1] for _ in assay_tbinfo]


    assay_outs = conn.execute('select * from assays where tid={} and assay_type=\"B\"'.format(tid)).fetchall()
    assays = []
    for assay in assay_outs:
        # 0:assay id, 14:confidence score, 18:assay chembl id
        assays.append([assay[0], assay[14], assay[18]])

    activities = []
    for assay in assays:
        activity_outs = conn.execute('select * from activities where assay_id={}'.format(assay[0])).fetchall()
        for activity in activity_outs:
                molregno = activity[4]
                stand_value = activity[8]
                stand_unit = activity[9]
                stand_type = activity[11]
                published_type = activity[13]
                relation = activity[16]

                if stand_unit == 'nM' and relation=='=':
                        mid = conn.execute('select chembl_id from molecule_dictionary where molregno={}'.format(molregno)).fetchall()[0][0]
                        smiles = conn.execute('select canonical_smiles from compound_structures where molregno={}'.format(molregno)).fetchall()
                        if len(smiles):
                                smiles = smiles[0][0]

                                # pair_name, aid, tid, mid, confidence_score, type, relation, value, unit, smile
                                activities.append([str(pair_name), str(assay[2]), str(target_id), str(mid), int(assay[1]), str(stand_type), str(relation), float(stand_value), str(stand_unit),str(smiles)])



    return activities


