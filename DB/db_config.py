import os
import sys
from collections import namedtuple
import multiprocessing

"""
variable shared between file
"""

manager = multiprocessing.Manager()
lock = manager.Lock()

"""
Parameter
"""
db_name='affinity.db'

# number of process running at the same time
process_num = 4


script_path = sys.path[0]
database_root = '/home/maksym/Projects/t_data'


db_path =os.path.join(database_root, db_name)

data_dir = os.path.join(database_root,'data')

export_dir = os.path.join(database_root, 'export')

"""
File Path 
"""

