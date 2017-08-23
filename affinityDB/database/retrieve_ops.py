import sqlite3,os,re,time
from itertools import compress
import numpy as np

class DatabaseMaster:

    def __init__(self,db_path):
        self.conn = sqlite3.connect(db_path)

    def merge(self,into_table,from_table,merge_cols,order):
        """ Moves and add columns either from the argument or from the output table one level up (only to the output
        table). Option when a single argument set yields multiple results in the output table is also supported.

        :param ups_table: string (name of the upstream output table)
        :param downs_table: string (name of the downstream argument or output table)
        :param col_names: list of strings (names of the columns in the downstream table to merge)
        :return: None
        """
        assert len(order)==2, "order should contain 2 lists [[into_order],[from_order]]"
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
        transfer_vals = map(lambda i: transfer_vals[i] + (order[0][i],), order[1])

        # insert columns into the upstream table
        sql_tmp = "update \"{}\" set ".format(into_table)
        sql_tmp += ", ".join([merge_cols[i]+ "=?" for i in range(num_cols)])
        sql_tmp += " where out_idx=?;"
        self.conn.executemany(sql_tmp,transfer_vals)
        self.conn.commit()

    def merge_order(self, query, target):
        """
        Finds what to take from the query to merge
        :param query: list of str/float/int (look up for a pair for each in the list)
        :param target: list of str/float/int (list where to look up from)
        :return:
        1) list of list of indices of the target len(list) == len(query) len(list[0]) == number of mathes for 0th term
        2) list of list of values
        3) 2D list of pairs [[query_idx],[target_idx]] len([query_idx]) == len(target_idx) == num_pairs
        """
        query = np.asarray(query)
        target = np.asarray(target)

        # sort target; select unique indices
        order_t = np.argsort(target)
        sorted_t = target[order_t]
        unique_t, counts_t = np.unique(sorted_t, return_counts=True)

        # search sorted
        merge_idx = np.searchsorted(unique_t, query)
        merge_mask = np.in1d(query, unique_t)

        # make a for loop to clunge the things together
        q_hits_idx = []
        q_hits_val = []
        pair_idx = [[], []]
        for i in range(len(query)):
            if not merge_mask[i]:
                q_hits_idx.append([])
                q_hits_val.append([])
            else:
                # one matches many form of output
                q_hit_idx = [order_t[j + merge_idx[i]] for j in range(counts_t[i])]
                q_hits_idx.append(q_hit_idx)
                q_hit_val = list(target[q_hit_idx])
                q_hits_val.append(q_hit_val)
                # one mathes one form of output
                [[pair_idx[0].append(i), pair_idx[1].append(idx)] for idx in q_hit_idx]
        return q_hits_idx, q_hits_val, pair_idx


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
