import os, sys, multiprocessing, time, sqlite3, math, threading, logging
from collections import namedtuple, OrderedDict

#------------------------------------CONFIG---------------------------------------#

class FLAGS:
    # number of process running at the same time

    database_root = '/home/maksym/Projects/new_data'
    db_path = os.path.join(database_root, 'affinity.db')
    data_dir = os.path.join(database_root,'data')

    table_idx = 0

#------------------------------------BUCKET---------------------------------------#

class Bucket(object):

    def __init__(self, database):
        self.stop = False
        self.bucket = []
        self.db = database
        tr = threading.Thread(target=self._autocommit)
        tr.daemon = False
        tr.start()


    def insert(self, stmt):
        self.bucket.append(stmt)

    def commit(self):
        for stmt in self.bucket:
            logging.debug("executing sql command from bucket:",stmt)
            self.db.conn.execute(stmt)
        self.db.conn.commit()
        self.bucket = []
        logging.info('commited')

    # start dropping data to the database with a background thread
    def _autocommit(self):
        while not self.stop:
            time.sleep(0.5)
            self.commit()
            logging.info('autocommited')

    # todo: create a queue and dequeue everythong from the bucket


#------------------------------------TABLE----------------------------------------#

table = namedtuple('Table', ['type', 'columns', 'primary_key'])


class AffinityDatabase:

    """Configures db_path and connects db with SQLite
    """
    def __init__(self):
        self.db_path = FLAGS.db_path

        if not os.path.exists(self.db_path): #initialize database
            if not os.path.exists(os.path.dirname(self.db_path)):
                os.makedirs(os.path.dirname(self.db_path))
            self.conn = sqlite3.connect(self.db_path,check_same_thread=False)
        else: #initialize table
            self.conn = sqlite3.connect(self.db_path,check_same_thread=False)

    # Create a new table with parameters:
    # table_param: dictionary holding basic information of table
    # table_def: tables with definition for the table's columns/primary keys

    def create_table_with_def(self, table_param, table_def):
        print 'Creating a new table...'

#        FLAGS.table_name = '{}_{}'.format(table_def.type, FLAGS.table_idx)
#        print "flags table name", FLAGS.table_name
#        time.sleep(1)
        FLAGS.table_name = "test_fib"

        # create table -table_name- (key1 value1 , ... primary key(,-primarykey-));
        stmt = 'create table ' + FLAGS.table_name + ' ('
        for key in table_def.columns.keys():
            stmt += key + ' ' + table_def.columns[key]
            if key in table_def.primary_key:
                stmt += ' not null ,'
            else:
                stmt += ' ,'
        stmt += 'primary key(' + ','.join(table_def.primary_key) + '));'

        stmt = 'create table test_fib (idx integer not null ,fib_num integer ,sqrt float ,primary key(idx));'
        stmt = str(stmt)
        print "create table stmt!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111", stmt


        self.conn.execute(stmt)
        self.conn.commit()

    # Inserts into table with index table_idx content in values
    def insert(self, values, head=None, bucket=None):
        print 'Inserting values into table...'

        db_value = lambda x: '"%s"' % x if type(x).__name__ in ['str','unicode'] else str(x)
        db_values = [map(db_value, value) for value in values]
        sql_values = [ '(' + ','.join(value) + ')' for value in db_values]

        stmt = 'replace into ' + FLAGS.table_name + ' '
        if head is not None:
            stmt += '(' + ','.join(head) + ')'
        stmt += ' values '
        stmt += ','.join(sql_values)
        stmt += ';'

        print 'insert stmt!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! '+stmt
        bucket.insert(stmt)


def fib_db(col_names, data_types, primary_key):
    """"
    col_names: list (str) of the names of the columns
    data_types: list (str) of the data types the corresponding columns will contain
    primary_key: (str) contains the name of the primary key
    """

    num_rows = 100

    # creates a list containing the fibonacci numbers
    if 'fib_num' in col_names:
        fib = [0, 1, 1]
        while len(fib) <= num_rows:
            fib.append(fib[-1] + fib[-2])

    # defines all functions available to be accessed
    func_defs = {'idx': (lambda x: x),
                'square': (lambda x: x**2),
                'cube': (lambda x: x**3),
                'sqrt': (lambda x: math.sqrt(x)),
                'fib_num': (lambda x: fib[x])}

    if len(col_names) == 0 or primary_key is None:
        raise ValueError("Must declare at least one column name and primary key")
    if len(col_names) != len(data_types):
        raise ValueError("Number of columns and data types do not match")
    for col_name in col_names:
        if col_name not in func_defs.keys():
            raise ValueError("Column " + col_name + " not in permissible columns")

    db = AffinityDatabase()

    table_param = {'func': 'test_fib', 'output_folder': FLAGS.data_dir}
    columns = [(col_names[i], data_types[i]) for i in range(len(col_names))]
    table_def = table(*['test_fib', OrderedDict(columns), [primary_key]])

    db.create_table_with_def(table_param, table_def)
    bucket = Bucket(db)

    for i in range(1, num_rows+1):
        to_insert = [[func_defs[col_names[j]](i) for j in range(len(col_names))]]
        db.insert(to_insert, bucket=bucket)

    bucket.stop = True


#os.system('rm -r vds_pdb')
col_names = ['idx', 'fib_num', 'sqrt']
dtypes = ['integer', 'integer', 'float']
primary_key = 'idx'

fib_db(col_names, dtypes, primary_key)