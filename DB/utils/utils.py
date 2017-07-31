import os
import sys
import config
import sqlite3
from config import lock
from functools import wraps
import time
import subprocess
import json 

mkdir = lambda path: os.system('mkdir -p {}'.format(path))

def count_lines(file_path):
    
    cmd = 'wc -l %s ' % file_path
    cl = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    cl.wait()
    cont = cl.communicate()[0].strip().split(' ')[0]
    try:
        value = int(cont)
    except Exception as e:
        print(e)
        value = None
    
    return value

def lockit(func):
    """
    lock before running functiong
    """
    @wraps(func)
    def function_in_lock(*args, **kwargs):
        lock.acquire()
        result = func(*args, **kwargs)
        lock.release()
        return result
    return function_in_lock

def timeit(record):
    def _timeit(func):
        """
        counter the time to run a function
        """
        @wraps(func)
        def function_in_timer(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            data = [func.__name__, str(duration)]
            if record:
                head = ['func','time']
                log('func_timer.csv',','.join(data), head = ','.join(head))
            else:
                print('\t'.join(['timer']+data))
        return  function_in_timer
    return _timeit

def create(tabel, kw, primarykey, lock):
    """
    create tabel
    """

def get(tabel, cond, value, lock):
    """
    get value from tabel
    """
    lock.acquire()
    cmd = "SELECT "
    cmd += ','.join(value)
    cmd += "from " + tabel
    cmd += "where "
    cmd += ' AND '.join()
    cursor = conn.execute()


def insert(tabel, content, head, lock):
    """
    inseert centent into tabel
    """
    lock.acquire()
    
    values = ["(" + ','.join([]) ]

    cmd = "INSERT INTO " + tabel
    cmd += "(" + ",".join(head) + ")"
        
    lock.release()


def param_equal(param1, param2):
    if type(param1).__name__ == 'dict' and type(param2).__name__ == 'dict':

        if not sorted(param1.keys()) == sorted(param2.keys()):
            return False 
        else:
            for key in param1.keys():
                if not param_equal(param1[key], param2[key]):
                    return False
            return True
    elif type(param1).__name__ in ['list','tuple'] and type(param2).__name__ in ['list','tuple']:
        if not sorted(list(param1)) == sorted(list(param2)):
            return False
        else:
            return True
    elif type(param1).__name__ in ['unicode','str','int','float'] and type(param2).__name__ in ['unicode','str','int','float']:
        if not str(param1) == str(param2):
            return False 
        else:
            return True 
    else:
        raise TypeError("Unknown data type %s in parameter" % type(param1).__name__)
    
         

@lockit
def log(log_file, log_content, head=None, lock=None):
    """
    write down log information
    :param log_file: name of log file
    :param log_content: string or list of string, log content
    :param head: head for csv or tsv output file
    :return:
    """

    if isinstance(log_content, str):
        log_content = [log_content]

    mkdir(config.log_dir)

    log_file_path = os.path.join(config.log_dir, log_file)
    if not os.path.exists(log_file_path) and not head is None:
        with open(log_file_path, 'w') as fout:
            fout.write(head+'\n')
    with open(log_file_path, 'a') as fout:
        for cont in log_content:
            if type(cont).__name__ == 'list':
                print(cont)
            fout.write(cont+'\n')


