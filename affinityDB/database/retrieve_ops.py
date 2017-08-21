import sqlite3,os,re,time
from itertools import compress
import numpy as np

class DatabaseGardener:

    def __init__(self,db_path):
        self.conn = sqlite3.connect(db_path)

    def up_merge(self,ups_table,downs_table,col_names):
        """ Moves and add columns either from the argument or from the output table one level up (only to the output
        table). Option when a single argument set yields multiple results in the output table is also supported.

        :param ups_table: string (name of the upstream output table)
        :param downs_table: string (name of the downstream argument or output table)
        :param col_names: list of strings (names of the columns in the downstream table to merge)
        :return: None
        """
        # FIXME: add support for the unrelated tables (should become key-merge)
        cursor = self.conn.cursor()
        num_cols = len(col_names)

        # find the data types of the columns to transfer
        sql_cmd = "pragma table_info(\"{}\")".format(downs_table)
        cursor.execute("{}".format(sql_cmd))
        # cursor.execute(sql_cmd)
        # cursor.execute("pragma table_info('aug_17_2017_54_16_arg_dataset_libs.NEW.get_ligand_decoys')")
        arg_infos = cursor.fetchall()
        arg_dict = {}
        [arg_dict.update({arg_info[1]:arg_info[2]}) for arg_info in arg_infos]
        print sql_cmd
        print arg_infos
        print arg_dict
        col_types = [arg_dict[col_name] for col_name in col_names]

        # initialize the columns in the upstream table
        sql_tmp = "alter table \"{}\" add column ".format(ups_table)
        for i in range(num_cols):
            sql_cmd = sql_tmp + ", ".join([" ".join([col_names[i],col_types[i]])]) + ";"
            cursor.execute(sql_cmd)
        self.conn.commit()

        # fetch values to transfer
        sql_cmd = "select " + ", ".join(col_names) + " from \"{}\"".format(downs_table)
        cursor.execute(sql_cmd)
        transfer_vals = cursor.fetchall()

        # get the run_idx (order of the values) in the upstream table
        sql_cmd = "select run_idx from \"{}\"".format(ups_table)
        cursor.execute(sql_cmd)
        up_order = cursor.fetchall()
        up_order = [list(idx) for idx in zip(*up_order)][0]

        # gather the transfer values from the downstream table with order
        transfer_vals = map(lambda i: transfer_vals[i] + (i,), up_order)

        # insert columns into the upstream table
        sql_tmp = "update \"{}\" set ".format(ups_table)
        sql_tmp += ", ".join([col_names[i]+ "=?" for i in range(num_cols)])
        sql_tmp += " where run_idx=?;"

        self.conn.executemany(sql_tmp,transfer_vals)
        self.conn.commit()

    def retrieve(self, table, cols, col_rules):
        """ Retrieves column values from a single table based on a given filtering rule.
        example:
        my_db.retrieve(some_table_table,["num1","num2"],{"remainder_div_3":"{}==1 or {}==2", "sum":"{}<200"})
        will retrieve:
        columns called "num1" and "num2" from some table. That have value 1 or 2 in the ramainder_div_3 column. Column
        named "sum" of which would be less than 200. All columns are combined with an "AND" statement.
        :param table: string (name of the table to retrieve from)
        :param columns: list of strings (names of the columns to retrieve)
        :param column_rules: dictionary of rules that will be eveluated
        :return: nested list in which is entry in a list a a column with filtered requested values
        """
        # todo: add string comp support
        cursor = self.conn.cursor()
        num_cols = len(col_rules)

        # from the table select all the columns to filter for
        sql_cmd = "select " + ", ".join([key for key in col_rules]) + " from \"" + table + "\""
        cursor.execute(sql_cmd)
        filter_sets = cursor.fetchall()

        # repeat every argument number of times it appears in the selection
        mult = [len(re.findall("{}", col_rules[key])) for key in col_rules]

        def _repeat_vals(vals, repeats):
            rep_vals = []
            [[rep_vals.append(vals[i]) for _ in range(repeats[i])] for i in range(num_cols)]
            return rep_vals

        filter_sets = [_repeat_vals(set, mult) for set in filter_sets]

        # evaluate every row to get a boolean mask of examples
        rule_tmp = "(" + ") and (".join([col_rules[key] for key in col_rules]) + ")"
        sel_mask = [eval(rule_tmp.format(*val_set)) for val_set in filter_sets]

        # from the table get all the columns to retrieve
        sql_cmd = "select " + " ,".join(cols) + " from \"" + table + "\""
        cursor.execute(sql_cmd)
        sel_sets = cursor.fetchall()

        # apply a boolean mask to take only entries that fit the selection rule
        sel_sets = list(compress(sel_sets, sel_mask))
        sel_vals = [list(x) for x in zip(*sel_sets)]
        return sel_vals
