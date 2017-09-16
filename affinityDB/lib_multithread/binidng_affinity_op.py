import os,sys
import numpy as np
import time
import re,math
import csv
from collections import Counter

class Binidng_affinity_init:
    this_module = sys.modules[__name__]
    def __init__(self,db_root, parse_type):
        """
        Initialize binding affinity parse func
        :param db_root: string (path to the root folder of the database)
        :param parse_type: source of binding affinity record ['pdbbind','bindingmoad','bindingdb']
        :return:
        None
        """

        self.db_root = db_root

        self.num_records = 0
        self.num_exception = 0
        self.pdb_names = []
        self.ligand_names = []
        self.binding_affinityes = []
        self.log_affinities = []
        self.normalized_affinities = []
        self.exceptions = []
        self.states = []
        self.comments = []

        self.parse_bind_func = {
            'pdbbind':self._parse_pdbbind,
            'bindingmoad':self._parse_bindingmoad,
            'bindingdb':self._parse_bindingdb
        }
        self.parse_func = self.parse_bind_func[parse_type]

        self.this_module.binding_affinity_init = self


    def _parse_bindingmoad_entry(self, entry):
        receptor, res, attr, measure, op, value, unit = entry
        if not attr == 'valid':
            return
        if not measure in ['Kd', 'Ki', 'ic50']:
            return
        if not op in ['=','~']:
            return

        resnames, chain, resnum = res.split(':')
        resnames = resnames.split(' ')

        try:
            value = float(value)
        

            if unit.lower() == 'fm':
                log_affinity = np.log(value) - np.log(10.0**15)
            elif unit.lower() == 'pm':
                log_affinity = np.log(value) - np.log(10.0**12)
            elif unit.lower() == 'nm':
                log_affinity = np.log(value) - np.log(10.0**9)
            elif unit.lower() == 'um':
                log_affinity = np.log(value) - np.log(10.0**6)
            elif unit.lower() == 'mm':
                log_affinity = np.log(value) - np.log(10.0**3)
            elif unit.lower() == 'm':
                log_affinity = np.log(value)
            else:
                raise Exception("unexpected unit {}".format(ligand))

            state = 1
            comment = 'success'
        
        except Exception as e:
            #PDB_moad.exceptions.append(e)
            log_affinity = 0
            state = 0
            comment = str(e)


       

        for resname in resnames:
            self.pdb_names.append(receptor.upper())
            self.ligand_names.append(resname.upper())
            self.log_affinities.append(log_affinity)
            self.states.append(state)
            self.comments.append(comment)
            self.num_records +=1
            if state ==0:
                self.num_exception +=1
                self.exceptions.append(e)

    def _parse_bindingmoad(self, binding_moad_index):
        with open(binding_moad_index) as fin:
            while(not fin.readline() == '"========================="\n'):
                continue
        
            csv_reader = csv.reader(fin)
            receptor = []
            for row in csv_reader:

                if len(row) == 2:
                    # smile string and rest
                    pass
                elif not row[0]== '':
                    # first columns like '2.6.1.62'
                    pass
                elif not row[2] == '':
                    # get receptor
                    receptor = row[2]
                else:
                    try:
                        self._parse_bindingmoad_entry([receptor.upper()] + row[3:9])
                    except Exception as e:
                        self.num_exception +=1
                        self.exceptions.append(e)
                    self.num_records +=1

        max_log_affinity = np.log(10.**0)
        min_log_affinity = np.log(10.**-18)

        self.normalized_affinities = (self.log_affinities - min_log_affinity)\
        /(max_log_affinity - min_log_affinity)   

    def _parse_pdbbind(self, pdb_bind_index):
        with open(pdb_bind_index) as f:
            [f.readline() for _ in range(6)]
            file_text = f.readlines()

        for line in file_text:
            pdb_name = re.split("[\s]+", line)[0]
            ligand_name = re.split("[\s]+", line)[6]
            
            try:

                # sanity check
                if re.compile(".*incomplete ligand.*").match(line):
                    raise Exception('missing atoms in ligand')

                if re.compile(".*covalent complex.*").match(line):
                    raise Exception('forms covalent complex')

                if re.compile(".*Nonstandard assay.*").match(line):
                    raise Exception('not standard assay')

                

                if not re.compile("^[a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9]$").match(pdb_name):
                    raise Exception('PDB name in the record is impossible')

                
                if not re.compile("\([a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9]\)").match(ligand_name):
                    if not re.compile("\([a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9]-[a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9]\)").match(ligand_name):
                        raise Exception('ligand name is impossible')


                
                affinity_record = re.split("[\s]+", line)[3]

                # split the lines of the PDB bind file record
                molar_affinity_record = re.sub(re.compile('(IC50=|Ki=|Kd=|IC50~|Ki~|Kd~)'), "", affinity_record)
                affinity_number_and_molarity = re.split(re.compile("([0-9]+\.[0-9]+|[0-9]+)"), molar_affinity_record)

                if len(affinity_number_and_molarity) != 3:
                    raise Exception('can not split record'), len(affinity_number_and_molarity)

                affinity_number = affinity_number_and_molarity[1]
                if not re.compile("[0-9]").match(affinity_number):
                    raise Exception('can not split record')

                molarity = affinity_number_and_molarity[2]
                if not re.compile("(fM|pM|nM|uM|mM)").match(molarity):
                    raise Exception('can not split record')

                # convert affinities into normalized affinities
                # fm = -15; pm = -12, nm = -9; uM = -6; mM = -3;
                
                if re.compile("fm|fM|Fm").match(molarity):
                    log_affinity = np.log(float(affinity_number)) - np.log(10.0 ** 15)
                elif re.compile("pm|Pm|pM").match(molarity):
                    log_affinity = np.log(float(affinity_number)) - np.log(10.0 ** 12)
                elif re.compile("nm|Nm|nM").match(molarity):
                    log_affinity = np.log(float(affinity_number)) - np.log(10.0 ** 9)
                elif re.compile("um|uM|Um"):
                    log_affinity = np.log(float(affinity_number)) - np.log(10.0 ** 6)
                elif re.compile("mM|Mm|mm"):
                    log_affinity = np.log(float(affinity_number)) - np.log(10.0 ** 3)
                
                state = 1
                comment = 'success'    

            except Exception as e:
                self.num_exception += 1
                self.exceptions.append(e)

                state = 0
                comment = str(e)
                log_affinity = 0


            self.pdb_names.append(pdb_name)
            self.ligand_names.append(ligand_name.strip("(").strip(")"))
            self.log_affinities.append(log_affinity)
            self.states.append(state)
            self.comments.append(comment)

            self.num_records += 1

        max_log_affinity = np.log(10.**0)
        min_log_affinity = np.log(10.**-18)
        self.normalized_affinities = (self.log_affinities - min_log_affinity) / (max_log_affinity - min_log_affinity)

    def _parse_bindingdb(self, binding_db_index):
        with open(binding_db_index) as fin:
            reader = csv.reader(fin, delimiter='\t')
            head = reader.next()
            # select the important columns
            #     Ki(nM) 
            #     IC50(nM) 
            #     Kd(nM)
            #     pH
            #     Temp (C)
            #     Ligand HET ID
            #     PDB ID(s) for Ligand-Target Complex
            collections = map(lambda row:[row[8],row[9],row[10],row[14],
                                        row[15],row[26],row[27]],reader)
            
            # remove record if the ligand or receptor ID missing
            valid = filter(lambda row: 
                                not(row[-1]=='' or row[-2]==''), collections)
            
            # remove ligand-receptor record if it appears more than once
            pairs = map(lambda row:(row[-2],row[-1]),valid)
            counter = Counter(pairs)
            unique_pair = [k for k,v in counter.items() if v==1]
            unique_entry = filter(lambda row: 
                                    (row[-2],row[-1]) in unique_pair, valid)
            
            # Every record only have one PDB ID
            single_pairs = []
            for entry in unique_entry:
                for pdb in entry[-1].split(','):
                    single_pairs.append(entry[:-1]+[pdb])
        
            # remove records which have more than one kind of measure value
            better = []
            for entry in single_pairs:
                # only 25 entry have more than one kind of measure
                c = 0
                pos = 0
                for i in range(3):
                    if not entry[i] == '':
                        c +=1
                        pos = i
                if c==1:
                    better.append([entry[pos]]+entry[3:])
            
            # remove the record if its affinity value not precise
            temp = filter(lambda x:x[0][0] not in ['<', '>'], better)
            records = map(lambda x:[float(x[0])]+x[1:], temp)

            for affinity, ph, temp, lig, rec in records:
                self.pdb_names.append(rec)
                self.ligand_names.append(lig)
                self.log_affinities.append(np.log(float(affinity)) - np.log(10.0 ** 9))
                self.states.append(1)
                self.comments.append('success')

                self.num_records += 1

            max_log_affinity = np.log(10.**0)
            min_log_affinity = np.log(10.**-18)
            self.normalized_affinities = (self.log_affinities - min_log_affinity) / (max_log_affinity - min_log_affinity)

def binding_affinity(index_path, init='binding_affinity_init'):
    """
    Parse binding affinity record from index_path

    Example:
    <pre lang="python">
    binding_affinity('nr.csv','bindingmoad')
    </pre>

    Output:
    <pre lang="python">
    [['4CPA','GLY',-19.1138279245,0.538831666908,1,'success'],
     ['4FAB','FDS',-18.5485141155,0.552471259564,1,'success']]
    </pre>

    :param index_path: record file 
    :param init: str init function name
    :return:
    Nested list [ [pdb_name, ligand_names, log_affinities, normalized_affinities, states, comments] ]
    
    """
    init = eval(init)

    init.parse_func(index_path)


    result = [[ init.pdb_names[i].upper(),
                init.ligand_names[i],
                float(init.log_affinities[i]),
                float(init.normalized_affinities[i]),
                init.states[i],
                init.comments[i]]
                    for i in range(len(init.pdb_names))]

    return result


