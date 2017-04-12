import os123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport sqlite3123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport config123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport time123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom config import lock123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom utils import lockit123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport csv123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom collections import namedtuple, OrderedDict123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtable = namedtuple('Table',['name','columns','primary_key'])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtables store the information about the table to be created in the database ( except scoring_terms )123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtable:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    name: name of the tabel in database, name of the csv file when export the table123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    columns: the name and value type for each columns in the table123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    primary_key: the name of the primary key for this table123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFscoring_terms table:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    This table store the different scoring terms' value caculated by smina, 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    the scoring terms are defined in `config.scoring_terms`.123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFWhen initialize the database, it first parse config.scoring_terms and add it in tables  123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFand then create all table defined in tables123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF"""123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFtables = {123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'ligand_atom_num':table(*['ligand_atom_num',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OrderedDict([('name','text'),('heavy_atom_num','integer')]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ['name']]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'receptor_info':table(*['receptor_info',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OrderedDict([('name','text'),('experiment','text'),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                     ('resolution','read'),('heavy_atom_num','integer'),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                     ('residue_num','ingeter'),('chain_num','integer')]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ['name']]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'rotable_bond':table(*['rotable_bond',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OrderedDict([('ligand','text'),('rotable_bond','ingeter')]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ['ligand']]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'rotable_bond_state':table(*['rotable_bond_state',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OrderedDict([('ligand','text'),('state','integer'),('comment','text')]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ['ligand']]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'reorder_state':table(*['reorder_state',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OrderedDict([('ligand','text'),('identifier','text'),('state','integer'),('comment','text')]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ['ligand','identifier']]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'split_state':table(*['split_state',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OrderedDict([('pdb','text'),('state','integer'),('comment','text')]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ['pdb']]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'similarity':table(*['similarity',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OrderedDict([('ligand_a','text'),('ligand_b','text'),('finger_print','text'),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ('similarity','real')]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ['ligand_a','ligand_b','finger_print']]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'similarity_state':table(*['similarity_state',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OrderedDict([('ligand_a','text'),('ligand_b','text'),('finger_print','text'),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                     ('state','integer'),('comment','text')]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ['ligand_a','ligand_b','finger_print']]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'overlap':table(*['overlap',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OrderedDict([('docked_ligand','text'),('crystal_ligand','text'),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ('position','integer'),('cutoff_A','real'),('identifier','text'),('overlap_ratio','real')]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ['docked_ligand', 'crystal_ligand', 'position','cutoff_A','identifier']]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'overlap_state':table(*['overlap_state',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OrderedDict([('docked_ligand','text'),('crystal_ligand','text'),('identifier','text'),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ('state','integer'),('comment','text')]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ['docked_ligand','crystal_ligand','identifier']]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'rmsd':table(*['rmsd',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OrderedDict([('docked_ligand','text'),('crystal_ligand','text'),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ('position','ingeter'),('identifier','text'),('rmsd','real')]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ['docked_ligand','crystal_ligand','position','identifier']]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'rmsd_state':table(*['rmsd_state',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OrderedDict([('docked_ligand','text'),('crystal_ligand','text'),('identifier','text'),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ('state','integer'),('comment','text')]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ['docked_ligand', 'crystal_ligand','identifier']]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'native_contact':table(*['native_contact',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OrderedDict([('docked_ligand','text'),('position','integer'),('identifier','text'),('distance_threshold','real'),('native_contact_ratio','real')]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ['docked_ligand','position','identifier','distance_threshold']]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'native_contact_state':table(*['native_contact_state',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OrderedDict([('docked_ligand','text'),('identifier','text'),('state','integer'),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ('comment','text')]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ['docked_ligand','identifier']]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'dock_state':table(*['dock_state',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OrderedDict([('docked_ligand','text'),('identifier','text'),('state','integer'),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ('comment','text')]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ['docked_ligand','identifier']]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'add_hydrogens_state': table(*['add_hydrogens_state',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OrderedDict([('name','text'),('identifier','text'),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ('state','integer'),('comment','success')]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ['name','identifier']]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    'minimize_state': table(*['minimize_state',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        OrderedDict([('name','text'),('identifier','text'),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ('state','integer'),('comment','success')]),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        ['name','identifier']])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFclass database:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    A simple wrapper for sqlite3123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Generate sql query and execute it123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    Now only support create table and data insert123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def __init__(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.db_path = config.db_path123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.export_dir = config.table_dir123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.tables = tables123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # create scoring table base on content in config.scoring_terms123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.add_scoring_term_tabel()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not os.path.exists(os.path.dirname(self.db_path)):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            os.makedirs(os.path.dirname(self.db_path))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not os.path.exists(self.db_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.backup_and_reset_db()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.connect_db()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def connect_db(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conn = sqlite3.connect(self.db_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.connect = True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "connect to %s" % self.db_path123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def backup_db(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        create a copy of current sqlite database123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        :return: 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        backup_db_path = self.db_path.replace('.', '_'+time.strftime("%Y-%m-%d-%H:%M:%S", time.gmtime()) +'.')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if os.path.exists(self.db_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            cmd = 'cp %s %s' % (self.db_path , backup_db_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            os.system(cmd)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print "backup database %s" % backup_db_path123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def backup_and_reset_db(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        backup current database and create a new one123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        :return: 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if os.path.exists(self.db_path):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            backup_db_path = self.db_path.replace('.', '_' + time.strftime("%Y-%m-%d-%H:%M:%S", time.gmtime()) + '.')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            os.rename(self.db_path, backup_db_path)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.connect_db()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.create_table()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    @lockit123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def insert_or_replace(self, tabel, values, head=None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db_value = lambda x:'"%s"' % x if type(x).__name__ == 'str' else str(x)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db_values = [ map(db_value, value) for value in values ]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #print db_values123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sql_values = [ '(' + ','.join(value) + ')' for value in db_values ]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #print sql_values123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'REPLACE INTO ' + tabel + ' '123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not head is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            stmt += '('+ ','.join(head) + ')'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt += ' VALUES '123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt += ','.join(sql_values)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt += ';'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #print stmt123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not self.connect:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.connect_db()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.conn.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        except Exception as e:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print e123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conn.commit()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    @lockit123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def insert_or_ignore(self, tabel, values, head=None):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db_value = lambda x: '"%s"' % x if type(x).__name__ == 'str' else str(x)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db_values = [map(db_value, value) for value in values]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #print db_values123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sql_values = ['(' + ','.join(value) + ')' for value in db_values]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #print sql_values123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'INSERT OR IGNORE INTO ' + tabel + ' '123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not head is None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            stmt += '(' + ','.join(head) + ')'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt += ' VALUES '123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt += ','.join(sql_values)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt += ';'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #print stmt123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if not self.connect:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.connect_db()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.conn.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        except Exception as e:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print e123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.conn.commit()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def get_all_success(self, table_name):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        get all enrty in _state table with state=1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        columns = self.tables[table_name].columns.keys()[:-2]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        columns = ','.join(columns)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'select ' + columns + ' from ' + table_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt += ' where state = 1 ;'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print stmt123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor = self.conn.cursor()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        # fetch all result is a list of tuple123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        values = cursor.fetchall()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        values = map(lambda x:list(x), values)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return values123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def if_success(self, table_name, values):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        find if there's success record in _state table123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db_value = lambda x: '"%s"' % x if type(x).__name__ == 'str' else str(x)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        db_values = map(db_value, values)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        columns = self.tables[table_name].primary_key123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #print columns123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cond = map(lambda (col,val) : '%s=%s' % (col,val), zip(columns, db_values))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cond.append('state=1')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt = 'select count(*) from ' + table_name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        stmt += ' where ' + ' and '.join(cond) + ';'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print stmt123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor = self.conn.cursor()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #fetch one will return tuple like (3,)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        values = cursor.fetchone()[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        #print values123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return values123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def create_table(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for tab in tables.values():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            stmt = 'create table '+ tab.name + ' ('123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            for key in tab.columns.keys():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                stmt += key + ' ' + tab.columns[key]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                if key in tab.primary_key:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    stmt += ' not null ,'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    stmt += ' ,'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            stmt += 'primary key(' + ','.join(tab.primary_key) + '));'123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            print tab.name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            self.conn.execute(stmt)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "Create all %d tables" % len(tables)        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def add_scoring_term_tabel(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        columns of this tabel will determined by 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        the content of config.scoring_tems 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        columns = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        columns.append(('ligand','text'))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        columns.append(('position','integer'))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for row in open(config.scoring_terms):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            row = row.strip().split('  ')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            col = row[1].replace(',',' ')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            col = '"%s"' % col123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            columns.append((col,'real'))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        self.tables['scoring_terms'] = table(*['scoring_terms',123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            OrderedDict(columns),123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ['ligand','position']])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    def export(self):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        export data from database to csv file123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        """123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cursor = self.conn.cursor()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for tab in self.tables.values():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            table_path = os.path.join(self.export_dir, tab.name+'.csv')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            os.system('mkdir -p %s' % self.export_dir)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            cursor.execute('SELECT * FROM %s' % tab.name)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            with open(table_path,'w') as fout:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                csv_out = csv.writer(fout)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                csv_out.writerow([d[0] for d in cursor.description])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                for result in cursor:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    csv_out.writerow(result)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                print 'export table %s' % tab.name123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF