import os
import sys 
import sqlite3 
import base64
import json 
import db_config
import time 
from db_config import lock 
#from utils.utils import lockit 
import pymysql
from db_table import basic_tables, tables

class AffinityDatabase(object):

    def __init__(self, db_type='sqlite'):
        if db_type == 'mysql':
            self.init_mysql()

        else:
            self.init_sqlite()

    def init_mysql(self):
        self.tables = tables 
        self.conn = pymysql.connect(host='localhost',user='root',passwd='password', database='affinity')
        self.cursor = self.conn.cursor()
        self.cursor.execute('create database if not exists affinity;')

        for tab in basic_tables.values():
            stmt = 'create table if not exists '+ tab.type + ' ('
            for key in tab.columns.keys():
                stmt += key + ' ' + tab.columns[key]
                if key in tab.primary_key:
                    stmt += ' not null ,'
                else:
                    stmt += ' ,'
            stmt += 'primary key(' + ','.join(tab.primary_key) + '));'
            print ("create ",tab.type)
            print (stmt)
            self.cursor.execute(stmt)    

    def init_sqlite(self):
        self.db_path = db_config.db_path
        self.tables = tables 

        if not os.path.exists(os.path.dirname(self.db_path)):
            os.makedirs(os.path.dirname(self.db_path))

        if not os.path.exists(self.db_path):
            self.conn = sqlite3.connect(self.db_path)
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

        else:
            self.conn = sqlite3.connect(self.db_path)

    def regist_table(self, table_type, table_def):
        '''
        regist new table type
        '''
        self.tables.update({table_type: table_def})

    def idx_for_new_table(self):
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
        else:
            idx = max(values) + 1
    
        return idx

    def create_table(self, table_param,table_type=None, table_def=None):
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
        
        if table_type is None:
            table_type = table_def.type

        if table_def is None:
            table_def = self.tables[table_type]

        table_idx = self.idx_for_new_table()
        table_name = '{}_{}'.format(table_type, table_idx)
        
        encoded_param = base64.b64encode(json.dumps(table_param))
        create_time = time.strftime("%Y-%m-%d", time.gmtime())
        datum = [table_name, table_type, table_idx, create_time, encoded_param]
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
        cursor = self.conn.cursor()            
        cursor.execute(stmt)  

        if 'depend' in table_param.keys():
            depend_tables = table_param['depend']
            for tab_idx in depend_tables:
                self.insert('dependence',[[tab_idx, table_idx]])

        self.conn.commit()
        return table_idx


    def get_table_info(self, idx):
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

            param = json.loads(base64.b64decode(coded_param))
            return table_name, param

    #@lockit        
    def insert(self, table_idx, values, head=None, bucket=None, method='replace'):
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
            table_name, _ = self.get_table_info(table_idx)
        
        if method == 'replace':
            insert_method = 'replace into '
        elif method == 'ignore':
            insert_method = 'insert or ignore '
        

        for value in values:
            db_value = lambda x:'"%s"' % x if type(x).__name__ in ['str','unicode'] else str(x)
            db_values = [ map(db_value, v) for v in [value] ]
            sql_values = [ '(' + ','.join(value) + ')' for value in db_values ]

            stmt = insert_method + table_name + ' '
            if head is not None:
                stmt +='(' + ','.join(head) + ')'
            stmt += ' values '
            stmt += ','.join(sql_values)
            stmt += ';'

            if bucket is None:
                cursor = self.conn.cursor()
                cursor.execute(stmt)
                self.conn.commit()
            else:
                print('insert stmt '+stmt)
                bucket.insert(stmt)


    def delete_table(self, idx):
        idx = int(idx)
        # if exists get the ble_name and table_taparam
        table_name, table_param = self.get_table_info(idx)

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

    def select_from_table(self, table_idx, table_columns, table_rest=None):
        '''
        select the content from table

        args:
            table_idx:: int
                index of the table
            
            table_columns:: list of str
                name of columns to be selected

            table_rest:: list of [column_name, op, value]
                restriction for table
                e.g. ['resolution','<','3']

        '''
        table_name, _ = self.get_table_info(table_idx)

        stmt = 'select ' + ','.join(table_columns) + ' from ' + table_name
        if table_rest is not None:
            stmt += ' where '
            stmt += ' and '.join(['{}{}{}'.format(rest[0], rest[1], rest[2]) for rest in table_rest])
        stmt += ';'


        cursor = self.conn.cursor()
        cursor.execute(stmt)
        values = cursor.fetchall()
        return values

    def count_from_table(self, table_idx, table_rest=None):
        '''
        count the entry in table

        args:


        '''
        table_name, _ = self.get_table_info(table_idx)

        stmt = 'select count(*) from ' + table_name
        if table_rest is not None:
            stmt += ' where '
            stmt += ' and '.join(['{}{}{}'.format(rest[0], rest[1], rest[2]) for rest in table_rest])
        stmt += ';'


        cursor = self.conn.cursor()
        cursor.execute(stmt)
        values = cursor.fetone()
        return values[0]       





if __name__ == '__main__':
    AffinityDatabaseMy()
