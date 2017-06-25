"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFcreate database123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport os 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport sys 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport sqlite3123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport base64 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport json123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport config 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport time 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom config import lock 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom utils import lockit, param_equal 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport csv 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport numpy as np123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport pandas as pd123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom collections import namedtuple, OrderedDict, Counter123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom database_table import basic_tables, tables123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass AffinityDatabase:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    A simple warpper for sqlite3123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def __init__(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.db_path = config.db_path123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.tables = tables123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not os.path.exists(os.path.dirname(self.db_path)):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print self.db_path123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            os.makedirs(os.path.dirname(self.db_path))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not os.path.exists(self.db_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.backup_and_reset_db()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.connect_db()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def connect_db(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conn = sqlite3.connect(self.db_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.connect = True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "connect to %s" % self.db_path123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def backup_db(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        backup_db_path = self.db_path.replace('.', '_'+time.strftime("%Y-%m-%d-%H:%M:%S", time.gmtime()) +'.')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if os.path.exists(self.db_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            cmd = 'cp %s %s' % (self.db_path , backup_db_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            os.system(cmd)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "backup database %s" % backup_db_path123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def backup_and_reset_db(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        backup current database and create a new one123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        :return: 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if os.path.exists(self.db_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            backup_db_path = self.db_path.replace('.', '_' + time.strftime("%Y-%m-%d-%H:%M:%S", time.gmtime()) + '.')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            os.rename(self.db_path, backup_db_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.connect_db()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.init_table()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def new_table_idx(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'select table_idx from db_info;'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor = self.conn.cursor()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        values = cursor.fetchall()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        values = map(lambda x:x[0], values)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if len(values) == 0:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            idx = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        elif not len(values) == max(values):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            rest =  list(set(range(1, max(values))) - set(values))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            idx = rest[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            idx = max(values) + 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def create_table(self, table_type, table_param):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_idx = self.new_table_idx()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_name = '{}_{}'.format(table_type, table_idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        tab = self.tables[table_type]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        encoded_param = base64.b64encode(json.dumps(table_param))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        create_time = time.strftime("%Y-%m-%d", time.gmtime())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        datum = [table_name, table_type, table_idx, create_time, encoded_param]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        data = [datum]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.insert('db_info',data)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'create table ' + table_name + ' ('        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for key in tab.columns.keys():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            stmt += key + ' ' + tab.columns[key]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if key in tab.primary_key:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                stmt += ' not null ,'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                stmt += ' ,'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt += 'primary key(' + ','.join(tab.primary_key) + '));'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conn.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if 'depend' in table_param.keys():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            depend_tables = table_param['depend']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            for tab_idx in depend_tables:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                self.insert('dependence',[[tab_idx, table_idx]])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conn.commit()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return table_idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def get_table_name_by_idx(self, idx):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        idx = int(idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor = self.conn.cursor()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'select name from db_info where table_idx=%d;' % idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        value = cursor.fetchone()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if value is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("No table with idx: {}".format(idx))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return value[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def get_table(self, idx, with_param=True):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        idx = int(idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor = self.conn.cursor()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'select name, parameter from db_info where table_idx=%d;' % idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        value = cursor.fetchone()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if value is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("No table with idx: {}".format(idx))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            table_name, coded_param = value 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if with_param:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                param = json.loads(base64.b64decode(coded_param))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                return table_name, param123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                return table_name 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def get_folder(self, idx):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        idx = int(idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_name, table_param = self.get_table(idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not 'output_folder' in table_param.keys():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("table {} doesn't have corresponding folder".format(table_name))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return table_param['output_folder']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def delete_table(self, idx):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        idx = int(idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # if exists get the ble_name and table_taparam123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_name, table_param = self.get_table(idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # delete all table depend on it123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor = self.conn.cursor()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'select dest from dependence where source=%d;' % idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        values = cursor.fetchall()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if values:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            for val in values:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                # will return a tuple like (1,)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                self.delete_table(val[0])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # delete from dependence123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'delete from dependence where source=%d;' % idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # delete from dependence123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'delete from dependence where dest=%d;' % idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # delete from db_info123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'delete from db_info where table_idx=%d;' % idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # drop table123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'drop table %s' % table_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conn.commit()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # if have data with this table remove relative data123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if 'output_folder' in table_param.keys():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            folder_name = '{}_{}'.format(idx, table_param['output_folder'])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            del_folder_name = 'del_' + folder_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            folder_dir = os.path.join(config.data_dir, folder_name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            del_folder_dir = os.path.join(config.data_dir, del_folder_name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if os.path.exists(folder_dir):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                os.system('mv {} {} '.format(folder_dir, del_folder_dir))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                os.system('rm -r {}'.format(del_folder_dir))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    @lockit123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def insert(self, table_idx, values, head=None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.insert_or_replace(table_idx, values, head)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def insert_or_replace(self, table_idx, values, head=None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if table_idx in basic_tables.keys():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            table_name = table_idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            table_idx = int(table_idx)       123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            table_name = self.get_table(table_idx, with_param=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db_value = lambda x:'"%s"' % x if type(x).__name__ in ['str','unicode'] else str(x)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db_values = [ map(db_value, value) for value in values ]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sql_values = [ '(' + ','.join(value) + ')' for value in db_values ]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'replace into ' + table_name + ' '123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if head is not None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            stmt += '(' + ','.join(head) + ')'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt += ' values '123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt += ','.join(sql_values)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt += ';'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #print stmt123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conn.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conn.commit()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def primary_key_for(self, idx):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        idx = int(idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'select type from db_info where table_idx=%d;' % idx123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor = self.conn.cursor()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        value = cursor.fetchone()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if value is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            raise Exception("No table with idx: {}".format(idx))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            table_type = value[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return tables[table_type].primary_key123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def get_primary_columns_on_key(self, idx, kw):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        idx = int(idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_name = self.get_table(idx, with_param=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        primary_key = self.primary_key_for(idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'select ' + ','.join(primary_key) + ' from ' + table_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt += ' where '123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt += ' and '.join(['{}={}'.format(key, kw[key]) for key in kw.keys()])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt += ';'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor = self.conn.cursor()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        values = cursor.fetchall()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return values123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def get_all_success(self, idx):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        idx = int(idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_name = self.get_table(idx, with_param=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        primary_key = self.primary_key_for(idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'select ' + ','.join(primary_key) + ' from ' + table_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt += ' where state=1;'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor = self.conn.cursor()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        values = cursor.fetchall()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return self.get_primary_columns_on_key(idx, {'state':1})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def get_all_failed(self, idx):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        idx = int(idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_name = self.get_table(idx, with_param=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        primary_key =  self.primary_key_for(idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'select ' + ','.join(primary_key) + ' from ' + table_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt += ' where state=0;'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor = self.conn.cursor()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        values = cursor.fetchall()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        '''123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return self.get_primary_columns_on_key(idx, {'state':0})123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def get_all_dix(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'select table_idx from db_info;'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor = self.conn.cursor()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        values = cursor.fetchall()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        values = map(lambda x:x[0], values)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return values123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def get_idx_by_type(self, table_type):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'select table_idx from db_info '123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt += ' where type="%s";' % table_type123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor = self.conn.cursor()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        values = cursor.fetchall()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        values = map(lambda x:x[0], values)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return values123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def get_success_data(self, idx, dataframe=False):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        idx = int(idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_name, table_param = self.get_table(idx, with_param=True)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'select * from ' + table_name 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt += ' where state=1'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor = self.conn.cursor()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        values = cursor.fetchall()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        columns = list(map(lambda x:x[0], cursor.description))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if dataframe:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                import pandas as pd 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            except:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                raise Exception("Cannot import pandas")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            df = pd.DataFrame(values, columns=columns)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return (table_name, table_param, df)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            return (table_name, table_param, columns,  values)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def get_failed_reason(self, idx):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        idx = int(idx)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        table_name = self.get_table(idx, with_param=False)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'select comment from ' + table_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt += ' where state=0;'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor = self.conn.cursor()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        values = cursor.fetchall()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        reason_c = Counter(values)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        reason_n = np.asarray(reason_c.items())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        df = pd.DataFrame(reason_n, columns=['reason','count'])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return (table_name, df)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def init_table(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print 'init'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for tab in basic_tables.values():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            stmt = 'create table '+ tab.type + ' ('123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            for key in tab.columns.keys():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                stmt += key + ' ' + tab.columns[key]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                if key in tab.primary_key:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    stmt += ' not null ,'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    stmt += ' ,'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            stmt += 'primary key(' + ','.join(tab.primary_key) + '));'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "create ",tab.type123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print stmt123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.conn.execute(stmt) 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF