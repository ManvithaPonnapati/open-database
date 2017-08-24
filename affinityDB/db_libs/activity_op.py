import os,sys
from chembl_webresource_client.new_client import new_client


# FIXME: explanations
# FIXME: I think it needs target confidense as in AtomWise

class Activity_init:
    this_module = sys.modules[__name__]
    def __init__(self, data_dir, activity_folder):
        """

        :param data_dir:
        :param activity_folder:
        """
        activity_dir = os.path.join(data_dir, activity_folder)
        if not os.path.exists(activity_dir):
            os.makedirs(activity_dir)

        self.data_dir = data_dir 
        self.activity_folder = activity_folder 
        self.this_module.activity_init = self 
    

def activity(pair_name, target_id, init='activity_init'):
    """
    Getting bioactivity result from chbmel 
    query by the target_chembl_id

    :param pair_name:
    :param target_id:
    :param init:
    :return:
    """
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
        smile= str(result['canonical_smiles'])
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

        activity_records.append([pair_name, target_id, aid, mid, smile, measure, op, value, unit, confidence_score])

    return activity_records
