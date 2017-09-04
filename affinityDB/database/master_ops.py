import sqlite3,os,re,time
from itertools import compress
import numpy as np

class DatabaseMaster:

    def __init__(self,db_path):
        self.conn = sqlite3.connect(db_path)

    def merge(self,into_table,from_table,merge_cols,order):
        """
        Merges any table into the output table
        :param into_table: string (table to merge into)
        :param from_table: string (table to merge from)
        :param merge_cols: list of strings (names of the columns in merge_from to merge)
        :param order: Two lists of the same length. into_table_idx <-- from_table_idx
        First list: idx of the "into_table",  second list: idx of the "from table" to merge.

        Suggestion:
        When providing order, please, use run_idx for the argument table, and out_idx for the output table.
        Also, it the arg_table it is a good idea to select run_idx ==1

        :return: None
        """

        assert len(order)==2, "order should contain 2 lists [[idx_to_update(into_table)],[idx_of_updates(from_table)]]"
        cursor = self.conn.cursor()
        num_cols = len(merge_cols)

        # find the data types of the columns to transfer
        sql_cmd = "pragma table_info(\"{}\")".format(from_table)
        cursor.execute("{}".format(sql_cmd))

        arg_infos = cursor.fetchall()
        arg_dict = {}
        [arg_dict.update({arg_info[1]:arg_info[2]}) for arg_info in arg_infos]
        col_types = [arg_dict[col_name] for col_name in merge_cols]

        # initialize the columns in the table where cols will be added
        sql_tmp = "alter table \"{}\" add column ".format(into_table)
        for i in range(num_cols):
            sql_cmd = sql_tmp + ", ".join([" ".join([merge_cols[i],col_types[i]])]) + ";"
            cursor.execute(sql_cmd)
        self.conn.commit()

        # fetch values to transfer
        sql_cmd = "select " + ", ".join(merge_cols) + " from \"{}\"".format(from_table)
        cursor.execute(sql_cmd)
        transfer_vals = cursor.fetchall()

        # gather the transfer values from the downstream table with order
        transfer_vals = map(lambda i: transfer_vals[order[1][i]] + (order[0][i],), order[0])

        # insert columns into the upstream table
        sql_tmp = "update \"{}\" set ".format(into_table)
        sql_tmp += ", ".join([merge_cols[i]+ "=?" for i in range(num_cols)])
        sql_tmp += " where out_idx=?;"
        self.conn.executemany(sql_tmp,transfer_vals)
        self.conn.commit()

    def list_search(self, search_with, search_in):
        """ Search with each element of the "search_with" in the list "search_in".

        :param search_with: list of [str/float/int]
        :param search_in: list of [str/float/int]
        :return:
        hits_idx:
        A list of length len(search_with) of lists. Internal list is indexes [j1,j2,j3,j4] such that values
        search_with[i] == search_in[j1], search_with[i] == search_in[j2], ...
        hits_val:
        Same as hits_idx but lists with values instead of indexes
        pairs_idx:
        Two lists of the same length. search_with[pairs_idx[0][i]] == search_in[pairs_idx[1][i]]
        """
        sw = np.asarray(search_with)
        si = np.asarray(search_in)

        # sort search_in, count every element
        order_si = np.argsort(si)
        sorted_si = si[order_si]
        unique_si, counts_si = np.unique(sorted_si, return_counts=True)

        # search sorted
        hits_unq_idx = np.searchsorted(unique_si, sw)
        hits_mask = np.in1d(sw, unique_si)

        # loop through every query and add all of its examples to the answer list
        hits_idx = []
        hits_val = []
        pair_idx = [[], []]

        for i in range(len(sw)):
            if not hits_mask[i]:
                hits_idx.append([])
                hits_val.append([])
            else:
                # one matches many form of output
                hit_idx = [order_si[j + hits_unq_idx[i]] for j in range(counts_si[hits_unq_idx[i]])]
                hits_idx.append(hit_idx)
                q_hit_val = list(si[hit_idx])
                hits_val.append(q_hit_val)
                # one matches one form of output
                [[pair_idx[0].append(i), pair_idx[1].append(idx)] for idx in hit_idx]
        return hits_idx, hits_val, pair_idx


    def retrieve(self, table, cols, col_rules):
        """ Retrieves column values from a single table based on a given filtering rule.
        example:
        my_db.retrieve(some_table_table,["num1","num2"],{"remainder_div_3":"{}==1 or {}==2", "sum":"{}<200"})
        will retrieve:
        columns called "num1" and "num2" from some table. That have value 1 or 2 in the ramainder_div_3 column. Column
        named "sum" of which would be less than 200. All columns are combined with an "AND" statement.
        :param table: string (name of the table to retrieve from)
        :param columns: list of strings (names of the columns to retrieve)
        :param column_rules: dictionary of rules that will be evaluated
        :return: nested list in which is entry in a list a a column with filtered requested values
        """
        # todo: add string comp support
        cursor = self.conn.cursor()

        # from the table get all the columns to retrieve
        sql_cmd = "select " + " ,".join(cols) + " from \"" + table + "\""
        cursor.execute(sql_cmd)
        sel_sets = cursor.fetchall()

        if len(col_rules)==0:
            sel_vals = sel_sets
        else:
            # from the table select all the columns to filter for
            sql_cmd = "select " + ", ".join([key for key in col_rules]) + " from \"" + table + "\""
            cursor.execute(sql_cmd)
            filter_sets = cursor.fetchall()

            # repeat every argument number of times it appears in the selection
            mult = [len(re.findall("{}", col_rules[key])) for key in col_rules]

            def _repeat_vals(vals, repeats):
                rep_vals = []
                [[rep_vals.append(vals[i]) for _ in range(repeats[i])] for i in range(len(col_rules))]
                return rep_vals
            filter_sets = [_repeat_vals(set, mult) for set in filter_sets]

            # evaluate every row to get a boolean mask of examples
            rule_tmp = "(" + ") and (".join([col_rules[key] for key in col_rules]) + ")"
            sel_mask = [eval(rule_tmp.format(*val_set)) for val_set in filter_sets]

            # apply a boolean mask to take only entries that fit the selection rule
            sel_sets = list(compress(sel_sets, sel_mask))
            sel_vals = [list(x) for x in zip(*sel_sets)]
        return sel_vals
