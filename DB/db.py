"""
create database
"""

import os 
import sys 
import sqlite3
import base64 
import json
import db_config 
import time 
from db_config import lock 
from utils.utils import lockit, param_equal 
import csv 
import numpy as np
import pandas as pd
from collections import namedtuple, OrderedDict, Counter
from db_table import basic_tables, tables

class AffinityDatabase:
    """
    A simple warpper for sqlite3
    """

    def __init__(self):
        self.db_path = db_config.db_path
        self.tables = tables

        if not os.path.exists(os.path.dirname(self.db_path)):
            print (self.db_path)
            os.makedirs(os.path.dirname(self.db_path))
        
        if not os.path.exists(self.db_path):
            self.backup_and_reset_db()
        else:
            self.connect_db()

    def regist_table(self, name,table):
        # add new type of table in tables
        self.tables.update({name:table})

    def update_table(self, tables):
        # merge self.tables with  tables
        self.tables.update(tables)

    def connect_db(self):

        self.conn = sqlite3.connect(self.db_path)
        self.connect = True
        print ("connect to %s" % self.db_path)

    def backup_db(self):

        backup_db_path = self.db_path.replace('.', '_'+time.strftime("%Y-%m-%d-%H:%M:%S", time.gmtime()) +'.')

        if os.path.exists(self.db_path):
            cmd = 'cp %s %s' % (self.db_path , backup_db_path)
            os.system(cmd)
            print ("backup database %s" % backup_db_path)

    def backup_and_reset_db(self):
        """
        backup current database and create a new one
        :return: 
        """
        if os.path.exists(self.db_path):
            backup_db_path = self.db_path.replace('.', '_' + time.strftime("%Y-%m-%d-%H:%M:%S", time.gmtime()) + '.')
            os.rename(self.db_path, backup_db_path)


        self.connect_db()
        self.init_table()

    def new_table_idx(self):
        '''
        before create a new table 
        get the idx of the table to be inserted

        return :
            ids:: int

        '''
        stmt = 'select table_idx from db_info;'
        cursor = self.conn.cursor()
        cursor.execute(stmt)
        values = cursor.fetchall()
        values = map(lambda x:x[0], values)
        if len(values) == 0:
            idx = 1
        elif not len(values) == max(values):
            rest =  list(set(range(1, max(values))) - set(values))
            idx = rest[0]
        else:
            idx = max(values) + 1
    
        return idx



    def get_table_type_by_idx(self, idx):
        '''
        get the type of table by given table_idx

        return :
            table_type :: str

        '''
        idx = int(idx)
        cursor = self.conn.cursor()
        stmt = 'select type from db_info where table_idx=%d;' % idx
        cursor.execute(stmt)
        value = cursor.fetchone()
        if value is None:
            raise Exception("No table with idx: {}".format(idx))
        else:
            return value[0]

    def create_table_with_def(self, table_param, table_def):
        '''
        create a tabel with given table_param and table_def

        args:
            table_param:: dict
                basic information for the table tobe created
            
            table_def:: tables
                definition for the table's columns, primary keys

        return:
            idx:: int
        '''

        table_idx = self.new_table_idx()
        table_name = '{}_{}'.format(table_def.type, table_idx)
        
        encoded_param = base64.b64encode(json.dumps(table_param))
        create_time = time.strftime("%Y-%m-%d", time.gmtime())
        datum = [table_name, table_def.type, table_idx, create_time, encoded_param]
        data = [datum]
        self.insert('db_info',data)
        
        stmt = 'create table ' + table_name + ' ('        
        for key in table_def.columns.keys():
            stmt += key + ' ' + table_def.columns[key]
            if key in table_def.primary_key:
                stmt += ' not null ,'
            else:
                stmt += ' ,'
        stmt += 'primary key(' + ','.join(table_def.primary_key) + '));'
        print(stmt)            
        self.conn.execute(stmt)  

        if 'depend' in table_param.keys():
            depend_tables = table_param['depend']
            for tab_idx in depend_tables:
                self.insert('dependence',[[tab_idx, table_idx]])

        self.conn.commit()

        return table_idx    
        

    def create_table(self, table_type, table_param):
        '''
        create a table with given table_type and table_param

        args:
            table_param:: dict
                basic information for the table tobe created

            table_type:: str
                type of table, can get the table_def from self.tables[table_type]

        return:
            idx:: int
        '''
        table_idx = self.new_table_idx()
        table_name = '{}_{}'.format(table_type, table_idx)
        tab = self.tables[table_type]

        encoded_param = base64.b64encode(json.dumps(table_param))
        create_time = time.strftime("%Y-%m-%d", time.gmtime())
        datum = [table_name, table_type, table_idx, create_time, encoded_param]
        data = [datum]
        self.insert('db_info',data)

        if table_param['func'] == 'insert_column':
            self.insert_column_in_table(table_idx, table_name, table_type, table_param)
        else:
            stmt = 'create table ' + table_name + ' ('        
            for key in tab.columns.keys():
                stmt += key + ' ' + tab.columns[key]
                if key in tab.primary_key:
                    stmt += ' not null ,'
                else:
                    stmt += ' ,'
            stmt += 'primary key(' + ','.join(tab.primary_key) + '));'
            print(stmt)            
            self.conn.execute(stmt)

        if 'depend' in table_param.keys():
            depend_tables = table_param['depend']
            for tab_idx in depend_tables:
                self.insert('dependence',[[tab_idx, table_idx]])

        self.conn.commit()

        return table_idx

    def get_table_name_by_idx(self, idx):
        '''
        get the name of table which table_idx is idx

        args:
            idx:: int

        return:
            table_name ::str

        '''
        idx = int(idx)
        cursor = self.conn.cursor()
        stmt = 'select name from db_info where table_idx=%d;' % idx
        cursor.execute(stmt)
        value = cursor.fetchone()
        if value is None:
            raise Exception("No table with idx: {}".format(idx))
        else:
            return value[0]

    def get_table(self, idx, with_param=True):
        '''
        get the name and table_param of table which table_idx is idx

        args:
            idx:: int
                table_idx of the table

            with_param:: bool
                if return table_param

        return:
            table_name:: str

            table_param:: dict

        '''
        idx = int(idx)
        cursor = self.conn.cursor()
        stmt = 'select name, parameter from db_info where table_idx=%d;' % idx
        cursor.execute(stmt)
        value = cursor.fetchone()

        if value is None:
            raise Exception("No table with idx: {}".format(idx))
        else:
            table_name, coded_param = value 
            
            if with_param:
                param = json.loads(base64.b64decode(coded_param))
                return table_name, param
            else:
                return table_name 


    def get_folder(self, idx):
        '''
        get the output folder of the table whit table_idx 

        args:
            idx:: int

        reutrn:
            output_folder:: str
                name of the folder store the output file of target table
        '''
        idx = int(idx)
        table_name, table_param = self.get_table(idx)
        
        if not 'output_folder' in table_param.keys():
            raise Exception("table {} doesn't have corresponding folder".format(table_name))
        else:
            return table_param['output_folder']

    def delete_table(self, idx):
        '''
        delete table with table_idx and all the table depended it
        along with the data of those table

        args:
            idx:: int


        '''
        idx = int(idx)
        # if exists get the ble_name and table_taparam
        table_name, table_param = self.get_table(idx)

        # delete all table depend on it
        cursor = self.conn.cursor()
        stmt = 'select dest from dependence where source=%d;' % idx
        cursor.execute(stmt)
        values = cursor.fetchall()
        if values:
            for val in values:
                # will return a tuple like (1,)
                self.delete_table(val[0])

        # delete from dependence
        stmt = 'delete from dependence where source=%d;' % idx
        cursor.execute(stmt)

        # delete from dependence
        stmt = 'delete from dependence where dest=%d;' % idx

        # delete from db_info
        stmt = 'delete from db_info where table_idx=%d;' % idx
        cursor.execute(stmt)

        # drop table
        stmt = 'drop table %s' % table_name
        cursor.execute(stmt)

        self.conn.commit()
        # if have data with this table remove relative data
        if 'output_folder' in table_param.keys():
            folder_name = '{}_{}'.format(idx, table_param['output_folder'])
            del_folder_name = 'del_' + folder_name
            folder_dir = os.path.join(db_config.data_dir, folder_name)
            del_folder_dir = os.path.join(db_config.data_dir, del_folder_name)
            if os.path.exists(folder_dir):
                
                os.system('mv {} {} '.format(folder_dir, del_folder_dir))
                os.system('rm -r {}'.format(del_folder_dir))


    @lockit
    def insert(self, table_idx, values, head=None, bucket=None):
        '''
        insert values to into dataabse

        args:
            table_idx:: int

            values:: list of value list
                content to be inserted
            head:: list of str
                table head 

            bucket:: object
                object to hold the insert statement
        '''
        self.insert_or_replace(table_idx, values, head, bucket)

    def insert_or_replace(self, table_idx, values, head=None, bucket=None):
        '''
        insert database by "replace into"
        which will replace the existing entry

        args:
            table_idx:: int

            values:: list of value list
                content to be inserted
            head:: list of str
                table head 

            bucket:: object
                object to hold the insert statement
        '''        
        if table_idx in basic_tables.keys():
            table_name = table_idx
        else:
            table_idx = int(table_idx)       
            table_name = self.get_table(table_idx, with_param=False)

        db_value = lambda x:'"%s"' % x if type(x).__name__ in ['str','unicode'] else str(x)
        db_values = [ map(db_value, value) for value in values ]
        sql_values = [ '(' + ','.join(value) + ')' for value in db_values ]

        stmt = 'replace into ' + table_name + ' '
        if head is not None:
            stmt += '(' + ','.join(head) + ')'
        stmt += ' values '
        stmt += ','.join(sql_values)
        stmt += ';'

        #print(stmt)
        #print stmt

        if bucket is None:
            self.conn.execute(stmt)
            self.conn.commit()
        else:
            print('insert stmt '+stmt)
            bucket.insert(stmt)


    def insert_column_in_table(self, table_idx, table_name, table_type, table_param):
        cursor = self.conn.cursor()
        old_table_name = self.get_table_name_by_idx(table_param['download_idx'])
        stmt = 'create table ' + table_name + ' as select * from '+ old_table_name
        cursor.execute(stmt)
        try:
            stmt = 'alter table ' + table_name + ' add column ' + table_param['column_name'] + ' '+table_param['column_dtype']
            cursor.execute(stmt)
        except:
            print('Column Already Exists')
            pass
        if table_param['column_data'] is not None:
            time_array = []
            col_data = np.load(table_param['column_data']+'.npy')
            for i in range(colData.shape[0]):
                id_val = col_data[i][0]
                data_val = col_data[i][1]
                start_time = time.time()
                stmt = 'update ' + table_name + ' set ' + table_param['column_name']
                stmt += ' = ' + str(data_val) 
                stmt += ' where receptor like '+ "'%s'" % (str(id_val))#primary key
                cursor.execute(stmt)
                time_array.append(time.time()-start_time)
                print("Elapsed ", time.time()-start_time)
            print('Mean ', np.mean(np.array(time_array)))
        self.conn.commit()


    def primary_key_for(self, idx):
        '''
        get the table's primary keys which table_idx is idx

        args:
            idx:: int

        return:
            primary_keys:: list of str

        '''
        idx = int(idx)
        stmt = 'select type from db_info where table_idx=%d;' % idx
        cursor = self.conn.cursor()
        cursor.execute(stmt)
        value = cursor.fetchone()
        if value is None:
            raise Exception("No table with idx: {}".format(idx))
        else:
            table_type = value[0]
            return tables[table_type].primary_key


    def get_num_primary_columns_on_key(self, idx, kw):
        '''
        get the number of entry from table which table_idx is idx
        with restriction kw

        args:
            idx:: int

            kw:: dict
                restrict column name and value
                e.g. {'state':1} to select all success result


        reutrn:
            num_of_entry:: int


        '''
        idx = int(idx)
        table_name = self.get_table(idx, with_param=False)
        #primary_key = self.primary_key_for(idx)
        stmt = 'select count(*) from ' + table_name
        stmt += ' where '
        stmt += ' and '.join(['{}={}'.format(key, kw[key]) for key in kw.keys()])
        stmt += ';'
        cursor = self.conn.cursor()
        cursor.execute(stmt)
        values = cursor.fetchone()
        return values[0]        

    def get_primary_columns_on_key(self, idx, kw):
        '''
        get the primary columns' content from table which table_idx is idx
        with restriction kw

        args:
            idx:: int

            kw:: dict
                restrict column name and value
                e.g. {'state':1} to select all success result

        return:
            content:: list
                e.g. [('3eml',),('1a2b',),...] for download, which has only one primary key
                     or [('3eml','A','123','SO4),...] for splited_ligand, which has four primary keys

        '''
        idx = int(idx)
        table_name = self.get_table(idx, with_param=False)
        primary_key = self.primary_key_for(idx)
        stmt = 'select ' + ','.join(primary_key) + ' from ' + table_name
        stmt += ' where '
        stmt += ' and '.join(['{}={}'.format(key, kw[key]) for key in kw.keys()])
        stmt += ';'
        cursor = self.conn.cursor()
        cursor.execute(stmt)
        values = cursor.fetchall()
        return values

    def get_num_all_success(self, idx):
        '''
        get the number of entry from table which table_idx is idx and state is 1

        '''
        return self.get_num_primary_columns_on_key(idx, {'state':1})

    def get_num_all_failed(self, idx):
        '''
        get the number of entry from table which table_idx is idx and state is 1

        '''
        return self.get_num_primary_columns_on_key(idx, {'state':0})

    def get_all_success(self, idx):
        '''
        idx = int(idx)
        table_name = self.get_table(idx, with_param=False)
        primary_key = self.primary_key_for(idx)
        stmt = 'select ' + ','.join(primary_key) + ' from ' + table_name
        stmt += ' where state=1;'
        cursor = self.conn.cursor()
        cursor.execute(stmt)
        values = cursor.fetchall()
        '''
        return self.get_primary_columns_on_key(idx, {'state':1})

    def get_all_failed(self, idx):
        '''
        idx = int(idx)
        table_name = self.get_table(idx, with_param=False)
        primary_key =  self.primary_key_for(idx)
        stmt = 'select ' + ','.join(primary_key) + ' from ' + table_name
        stmt += ' where state=0;'
        cursor = self.conn.cursor()
        cursor.execute(stmt)
        values = cursor.fetchall()
        '''
        return self.get_primary_columns_on_key(idx, {'state':0})


    def get_all_dix(self):
        '''
        get all tables' table_idx from database
        '''
        stmt = 'select table_idx from db_info;'
        cursor = self.conn.cursor()
        cursor.execute(stmt)
        values = cursor.fetchall()
        values = map(lambda x:x[0], values)
        return values

    def get_idx_by_type(self, table_type):
        '''
        get table_idx for all table which type is table_type
        '''
        stmt = 'select table_idx from db_info '
        stmt += ' where type="%s";' % table_type
        cursor = self.conn.cursor()
        cursor.execute(stmt)
        values = cursor.fetchall()
        values = map(lambda x:x[0], values)
        return values


    def get_success_data(self, idx, dataframe=False):
        idx = int(idx)
        table_name, table_param = self.get_table(idx, with_param=True)
        stmt = 'select * from ' + table_name 
        stmt += ' where state=1' #what does this statement do?
        print (stmt)
        cursor = self.conn.cursor()
        cursor.execute(stmt)
        values = cursor.fetchall()
        columns = list(map(lambda x:x[0], cursor.description))
        if dataframe:
            try:
                import pandas as pd 
            except:
                raise Exception("Cannot import pandas")
            df = pd.DataFrame(values, columns=columns)
            return (table_name, table_param, df)
        else:
            return (table_name, table_param, columns,  values)

    def get_failed_reason(self, idx):
        '''
        get the comment from table which table_idx idx is idx and state is 0
        '''
        idx = int(idx)
        table_name = self.get_table(idx, with_param=False)
        stmt = 'select comment from ' + table_name
        stmt += ' where state=0;'
        cursor = self.conn.cursor()
        cursor.execute(stmt)
        values = cursor.fetchall()
        reason_c = Counter(values)
        reason_n = np.asarray(reason_c.items())
        df = pd.DataFrame(reason_n, columns=['reason','count'])
        return (table_name, df)
        


    def init_table(self):
        '''
        when creating new sqlite db,
        create basic table in the database

        '''
        print ('init')
        for tab in basic_tables.values():
            stmt = 'create table '+ tab.type + ' ('
            for key in tab.columns.keys():
                stmt += key + ' ' + tab.columns[key]
                if key in tab.primary_key:
                    stmt += ' not null ,'
                else:
                    stmt += ' ,'
            stmt += 'primary key(' + ','.join(tab.primary_key) + '));'
            print ("create ",tab.type)
            print (stmt)
            self.conn.execute(stmt) 
