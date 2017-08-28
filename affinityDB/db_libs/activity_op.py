import os,sys
import sqlite3

# FIXME: explanations
# FIXME: I think it needs target confidense as in AtomWise

class Activity_init:
    this_module = sys.modules[__name__]
    def __init__(self, data_dir, activity_folder, db_path):
        """

        :param data_dir:
        :param activity_folder:
        """
        activity_dir = os.path.join(data_dir, activity_folder)
        if not os.path.exists(activity_dir):
            os.makedirs(activity_dir)

        self.data_dir = data_dir
        self.activity_folder = activity_folder
        self.db_path = '/data/affinity/chembl/chembl_23/chembl_23_sqlite/chembl_23.db'
        self.this_module.activity_init = self


def activity(pair_name, target_id, init='activity_init'):
    """
    Getting bioactivity result from chbmel local database
    query by the target_chembl_id


    :param pair_name:
    :param target_id:
    :param init:
    :return:
    """
    init = eval(init)
    conn = sqlite3.connect(init.db_path)

    tid = conn.execute('select tid from target_dictionary where chembl_id=\"{}\";'.format(target_id)).fetchone()[0]

    assay_tbinfo = conn.execute('pragma table_info (assays)').fetchall()
    assay_cols = [_[1] for _ in assay_tbinfo]


    assay_outs = conn.execute('select * from assays where tid={} and assay_type=\"B\"'.format(tid)).fetchall()
    assays = []
    for assay in assay_outs:
        # 0:assay id, confidence score, assay chembl id
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

def _activity(pair_name, target_id, init='activity_init'):
    """
    Getting bioactivity result from chbmel web api
    query by the target_chembl_id

    :param pair_name:
    :param target_id:
    :param init:
    :return:
    """

    from chembl_webresource_client.new_client import new_client
    activities = new_client.activity
    assay = new_client.assay

    init = eval(init)
    
    # Get all activitvities for a specific target
    res = activities.filter(target_chembl_id=target_id, pchembl_value__isnull=False)

    res_size = len(res)
    activity_records = []
    for i in range(res_size):
        result = res[i]
        aid = str(result['assay_chembl_id'])
        smiles= str(result['canonical_smiles'])
        mid = str(result['molecule_chembl_id'])
        measure = str(result['standard_type'])
        op = str(result['standard_relation'])
        value = float(result['standard_value'])
        unit = str(result['standard_units'])

        # Get confidence score for a specific assay    
        resp = assay.filter(assay_chembl_id=aid)
        if not len(resp) == 1:
            continue
        else:
            confidence_score = int(resp[0]['confidence_score'])

        activity_records.append([str(pair_name), str(aid),str(target_id), str(mid), int(confidence_score), str(measure), str(op), float(value), str(unit), str(smiles)])

    return activity_records
