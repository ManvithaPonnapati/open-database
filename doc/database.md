# Database



[TOC]



***
## database
### database.DatabaseMaster
#### list\_search
Search with each element of the "search_with" in the list "search_in".


**args**
:param search_with: list of [str/float/int]
:param search_in: list of [str/float/int]

**returns**
:return:
hits_idx:
A list of length len(search_with) of lists. Internal list is indexes [j1,j2,j3,j4] such that values
search_with[i] == search_in[j1], search_with[i] == search_in[j2], ...
hits_val:
Same as hits_idx but lists with values instead of indexes
pairs_idx:
Two lists of the same length. search_with[pairs_idx[0][i]] == search_in[pairs_idx[1][i]]

#### merge
Merges any table into the output table

**args**
:param into_table: string (table to merge into)
:param from_table: string (table to merge from)
:param merge_cols: list of strings (names of the columns in merge_from to merge)
:param order: Two lists of the same length. into_table_idx <-- from_table_idx

**returns**
First list: idx of the "into_table",  second list: idx of the "from table" to merge.

Suggestion:
When providing order, please, use run_idx for the argument table, and out_idx for the output table.
Also, it the arg_table it is a good idea to select run_idx ==1

:return: None

#### retrieve
Retrieves column values from a single table based on a given filtering rule.
example:
my_db.retrieve(some_table_table,["num1","num2"],{"remainder_div_3":"{}==1 or {}==2", "sum":"{}<200"})
will retrieve:
columns called "num1" and "num2" from some table. That have value 1 or 2 in the ramainder_div_3 column. Column
named "sum" of which would be less than 200. All columns are combined with an "AND" statement.

**args**
:param table: string (name of the table to retrieve from)
:param columns: list of strings (names of the columns to retrieve)
:param column_rules: dictionary of rules that will be evaluated

**returns**
:return: nested list in which is entry in a list a a column with filtered requested values

#### \_\_init\_\_

### database.AffinityDB
#### coninue
Continue the interrupted run_multithread function.

**args**
:param arg_table: string (name of the sqlite table with arguments of the function to run)
:param num_threads: integer (number of processes)
:param commit_sec: integer (write outputs to the database every number of tasks)

**returns**
:return: None

#### run\_multithread
Run any function in lib_multithread in multiple threads.
Writes all arguments to arg_xxx_func table, record outputs to out_xxx_table. Record state of the function's
initializer to cron table.

If the task is interrupted in the process of execution, it is possible to resume with AffinityDB.continue(*)


**args**
:param func: string (a name of the function to execute)
:param arg_sets: lits of tuples (every tuple is an argument set for a single run of a function)
:param num_threads: integer (number of independent processes)
:param commit_sec: integer (time delay in flushing outputs to the arg_ and out_ tables)

**returns**
:return: None

#### open\_table\_with\_queue
Creates an output table, and a queue to feed this table. Creates a background thread to take results
from the queue and insert into the table.


**args**
:param table_name: string (name of the table prefix out_xxx_ will be appended)
:param col_names: list of strings (names of the columns)
:param col_types: list of python types (column types)

**returns**
:return: multiprocessing queue, event to close the table and terminate thread.

Exaple usage:
out_q,stop_event = afdb.open_table_with_queue(table_name="some_table",col_names=["num"],col_types=[int])
for i in range(1000):
    out_q.put([i])
stop_event.set()

#### \_\_init\_\_

