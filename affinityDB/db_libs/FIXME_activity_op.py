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

    :param pair_name:
    :param target_id:
    :param init:
    :return:
    """
    activities = new_client.activity
    init = eval(init)
    res = activities.filter(target_chembl_id=target_id, pchembl_value__isnull=False)

    res_size = len(res)
    activity_records = []
    for i in range(res_size):
        result = res[i]
        aid = str(result['assay_chembl_id'])
        smile= str(result['canonical_smiles'])
        mid = str(result['molecule_chembl_id'])
        measure = str(result['published_type'])
        op = str(result['published_relation'])
        value = float(result['published_value'])
        unit = str(result['standard_units'])
        activity_records.append([pair_name, target_id, aid, mid, smile, measure, op, value, unit])
    return activity_records
