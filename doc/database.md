[TOC]

# database
## AffinityDB
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
Writes all arguments to `arg_xxx_func` table, record outputs to `out_xxx_table`. Record state of the function's
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


