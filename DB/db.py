import os
import sys 
import sqlite3
import base64 
import json
import db_config
import time 
from db_config import lock 
from utils.utils import lockit

from db_table import basic_tables, tables


class AffinityDatabase:
    """
    A simple warpper for sqlite3
    """

    def __init__(self):
        self.db_path = db_config.db_path
        self.tables = tables


        if not os.path.exists(self.db_path):
            # init db
            if not os.path.exists(os.path.dirname(self.db_path)):
                os.makedirs(os.path.dirname(self.db_path))
            self.conn = sqlite3.connect(self.db_path)
            self.init_table()
        else:
            # connect db
            self.conn = sqlite3.connect(self.db_path)

    def regist_table(self, name,table):
        print "regist table !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 1"
        # add new type of table in tables
        self.tables.update({name:table})


    def new_table_idx(self):
        '''
        before create a new table 
        get the idx of the table to be inserted

        return :
            ids:: int

        '''
        print "new table idx !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!6 "

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
        #print "table param:", table_param
        #time.sleep(100)
        print "create table with def !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1!!!8"
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
        print "get table !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 11"
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
        print "get folder !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 13"
        idx = int(idx)
        table_name, table_param = self.get_table(idx)
        
        if not 'output_folder' in table_param.keys():
            raise Exception("table {} doesn't have corresponding folder".format(table_name))
        else:
            return table_param['output_folder']


    @lockit
    def insert(self, table_idx, values, head=None, bucket=None):
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
        print "inser or replace !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!15"
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


        if bucket is None:
            self.conn.execute(stmt)
            self.conn.commit()
        else:
            print('insert stmt '+stmt)
            bucket.insert(stmt)

    def primary_key_for(self, idx):
        '''
        get the table's primary keys which table_idx is idx

        args:
            idx:: int

        return:
            primary_keys:: list of str

        '''
        print "primary key for !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!16"
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
        print "get primary columns on key !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 18"
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


    def init_table(self):
        '''
        when creating new sqlite db,
        create basic table in the database

        '''
        print "init table !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 22"
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
