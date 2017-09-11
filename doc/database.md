[TOC]

# database
## Class
## AffinityDB
### \_\_init\_\_
```
__init__(
	self,
	db_root,
	db_name,
)
```


### coninue
```
coninue(
	self,
	arg_table,
	num_threads,
	commit_sec,
)
```
Continue the interrupted run_multithread function.

**Args**
- **`arg_table`** : string (name of the sqlite table with arguments of the function to run)
- **`num_threads`** : integer (number of processes)
- **`commit_sec`** : integer (write outputs to the database every number of tasks)

**Returns**
None


### open\_table\_with\_queue
```
open_table_with_queue(
	self,
	table_name,
	col_names,
	col_types,
	commit_sec=1,
)
```
Creates an output table, and a queue to feed this table. Creates a background thread to take results
from the queue and insert into the table.

Exaple usage:
```python
out_q,stop_event = afdb.open_table_with_queue(table_name="some_table",col_names=["num"],col_types=[int])
for i in range(1000):
    out_q.put([i])
stop_event.set()
```


**Args**
- **`table_name`** : string (name of the table prefix out_xxx_ will be appended)
- **`col_names`** : list of strings (names of the columns)
- **`col_types`** : list of python types (column types)

**Returns**
multiprocessing queue: event to close the table and terminate thread.


### run\_multithread
```
run_multithread(
	self,
	func,
	arg_sets,
	num_threads=10,
	commit_sec=1,
)
```
Run any function in lib_multithread in multiple threads.
Writes all arguments to arg_xxx_func table, record outputs to out_xxx_table. Record state of the function's
initializer to cron table.

If the task is interrupted in the process of execution, it is possible to resume with `AffinityDB.continue(*)`


**Args**
- **`func`** : string (a name of the function to execute)
- **`arg_sets`** : lits of tuples (every tuple is an argument set for a single run of a function)
- **`num_threads`** : integer (number of independent processes)
- **`commit_sec`** : integer (time delay in flushing outputs to the arg_ and out_ tables)

**Returns**
None


## DatabaseMaster
### \_\_init\_\_
```
__init__(
	self,
	db_path,
)
```


### list\_search
```
list_search(
	self,
	search_with,
	search_in,
)
```
Search with each element of the "search_with" in the list "search_in".


**Args**
- **`search_with`** : list of [str/float/int]
- **`search_in`** : list of [str/float/int]

**Returns**

hits_idx:
A list of length len(search_with) of lists. Internal list is indexes [j1,j2,j3,j4] such that values         search_with[i] == search_in[j1], search_with[i] == search_in[j2], ...
hits_val:
Same as hits_idx but lists with values instead of indexes
pairs_idx:
Two lists of the same length. search_with[pairs_idx[0][i]] == search_in[pairs_idx[1][i]]


### merge
```
merge(
	self,
	into_table,
	from_table,
	merge_cols,
	order,
)
```
Merges any table into the output table

Suggestion:
When providing order, please, use `run_idx` for the argument table, and `out_idx` for the output table.
Also, it the `arg_table` it is a good idea to select `run_idx ==1`


**Args**
- **`into_table`** : string (table to merge into)
- **`from_table`** : string (table to merge from)
- **`merge_cols`** : list of strings (names of the columns in merge_from to merge)
- **`order`** : Two lists of the same length. into_table_idx <-- from_table_idx         First list: idx of the "into_table",  second list: idx of the "from table" to merge.

**Returns**

None


### retrieve
```
retrieve(
	self,
	table,
	cols,
	col_rules,
)
```
Retrieves column values from a single table based on a given filtering rule.
example:
```python
my_db.retrieve(some_table_table,["num1","num2"],{"remainder_div_3":"{}==1 or {}==2", "sum":"{}<200"})
```
will retrieve:
columns called "num1" and "num2" from some table. That have value 1 or 2 in the ramainder_div_3 column. Column
named "sum" of which would be less than 200. All columns are combined with an "AND" statement.


**Args**
- **`table`** : string (name of the table to retrieve from)
- **`columns`** : list of strings (names of the columns to retrieve)
- **`column_rules`** : dictionary of rules that will be evaluated

**Returns**
nested list in which is entry in a list a a column with filtered requested values


