<table>

<tr><td><h3>AffinityDB</h3><i>Class</i></td>
</tr>
<tr><td><h4><b>__init__</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/database/main_ops.py">database/main_ops.py</a><br><pre lang="python">
__init__(
	self,
	db_root,
	db_name,
)
</pre>
Initialize database


Args:
<ul><li><b><code>db_root</code></b>:root dir for all the data</li>
<li><b><code>db_name</code></b>:name of the sqlite db file</li></ul>


Returns:
<ul><li>None</li></ul>
</td>
</tr>


<tr><td><h4><b>coninue</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/database/main_ops.py">database/main_ops.py</a><br><pre lang="python">
coninue(
	self,
	arg_table,
	num_threads,
	commit_sec,
)
</pre>
Continue the interrupted run_multithread function.

Example:
<pre lang="python">
continue('arg_000_download_pdb',100,60)
</pre>


Args:
<ul><li><b><code>arg_table</code></b>:string (name of the sqlite table with arguments of the function to run)</li>
<li><b><code>num_threads</code></b>:integer (number of processes)</li>
<li><b><code>commit_sec</code></b>:integer (write outputs to the database every number of tasks)</li></ul>


Returns:
<ul><li>None</li></ul>
</td>
</tr>


<tr><td><h4><b>open_table_with_queue</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/database/main_ops.py">database/main_ops.py</a><br><pre lang="python">
open_table_with_queue(
	self,
	table_name,
	col_names,
	col_types,
	commit_sec=1,
)
</pre>
Creates an output table, and a queue to feed this table. Creates a background thread to take results
from the queue and insert into the table.

Example:
<pre lang="python">
out_q,stop_event = afdb.open_table_with_queue(table_name="some_table",col_names=["num"],col_types=[int])
zsh
for i in range(1000):
    out_q.put([i])
stop_event.set()
</pre>


Args:
<ul><li><b><code>table_name</code></b>:string (name of the table prefix out_xxx_ will be appended)</li>
<li><b><code>col_names</code></b>:list of strings (names of the columns)</li>
<li><b><code>col_types</code></b>:list of python types (column types)</li></ul>


Returns:
<ul><li>multiprocessing queue: event to close the table and terminate thread.</li></ul>
</td>
</tr>


<tr><td><h4><b>run_multithread</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/database/main_ops.py">database/main_ops.py</a><br><pre lang="python">
run_multithread(
	self,
	func,
	arg_sets,
	num_threads=10,
	commit_sec=1,
)
</pre>
Run any function in lib_multithread in multiple threads.
Writes all arguments to `arg_xxx_func` table, record outputs to `out_xxx_table`. Record state of the function's
initializer to cron table.
If the task is interrupted in the process of execution, it is possible to resume with `AffinityDB.continue(*)`

Example:
<pre lang="python">
run_multithread('download',[['10MD','3EML']])
</pre>


Args:
<ul><li><b><code>func</code></b>:string (a name of the function to execute)</li>
<li><b><code>arg_sets</code></b>:lits of tuples (every tuple is an argument set for a single run of a function)</li>
<li><b><code>num_threads</code></b>:integer (number of independent processes)</li>
<li><b><code>commit_sec</code></b>:integer (time delay in flushing outputs to the arg_ and out_ tables)</li></ul>


Returns:
<ul><li>None</li></ul>
</td>
</tr>


<tr><td><h3>DatabaseMaster</h3><i>Class</i></td>
</tr>
<tr><td><h4><b>__init__</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/database/master_ops.py">database/master_ops.py</a><br><pre lang="python">
__init__(
	self,
	db_path,
)
</pre>
Initialize database master


Args:
<ul><li><b><code>db_path</code></b>:path of the sqlite database file</li></ul>


Returns:
<ul><li>None</li></ul>
</td>
</tr>


<tr><td><h4><b>list_search</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/database/master_ops.py">database/master_ops.py</a><br><pre lang="python">
list_search(
	self,
	search_with,
	search_in,
)
</pre>
Search with each element of the `search_with` in the list `search_in`.
Then get three lists:
- hits_idx:
A list of length len(search_with) of lists. Internal list is indexes [j1,j2,j3,j4] such that values         search_with[i] == search_in[j1], search_with[i] == search_in[j2], ...
- hits_val:
Same as hits_idx but lists with values instead of indexes
- pairs_idx:
Two lists of the same length. search_with[pairs_idx[0][i]] == search_in[pairs_idx[1][i]]

Example:
<pre lang="python">
list_search(['3AT1','2TPI'],['2TPI','3EML','3AT1','2TPI'])
</pre>

Output:
<pre lang="python">
[[2],[0,3]],
[['3AT1'],['2PTI','2PTI']],
[[0,2],[1,0],[1,3]]
</pre>


Args:
<ul><li><b><code>search_with</code></b>:list of [str/float/int]</li>
<li><b><code>search_in</code></b>:list of [str/float/int]</li></ul>


Returns:
<ul><li>three lists: hits_idx, hits_val, pairs_idx</li></ul>
</td>
</tr>


<tr><td><h4><b>merge</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/database/master_ops.py">database/master_ops.py</a><br><pre lang="python">
merge(
	self,
	into_table,
	from_table,
	merge_cols,
	order,
)
</pre>
Merges any table into the output table

Suggestion:
When providing order, please, use `run_idx` for the argument table, and `out_idx` for the output table.
Also, it the `arg_table` it is a good idea to select `run_idx ==1`

Example:
<pre lang="python">
merge('out_000_dock','arg_000_reorder','reorder_outpath',[[1,4,2,3],[1,2,3,4]])
</pre>


Args:
<ul><li><b><code>into_table</code></b>:string (table to merge into)</li>
<li><b><code>from_table</code></b>:string (table to merge from)</li>
<li><b><code>merge_cols</code></b>:list of strings (names of the columns in merge_from to merge)</li>
<li><b><code>order</code></b>:Two lists of the same length. into_table_idx <-- from_table_idx         First list: idx of the `into_table`,  second list: idx of the `from table` to merge.</li></ul>


Returns:
<ul><li>None</li></ul>
</td>
</tr>


<tr><td><h4><b>retrieve</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/database/master_ops.py">database/master_ops.py</a><br><pre lang="python">
retrieve(
	self,
	table,
	cols,
	col_rules,
)
</pre>
Retrieves column values from a single table based on a given filtering rule.

Example:
<pre lang="python">
my_db.retrieve(some_table_table,["num1","num2"],{"remainder_div_3":"{}==1 or {}==2", "sum":"{}<200"})
</pre>
will retrieve:
<pre lang="python">
columns called "num1" and "num2" from some table. That have value 1 or 2 in the ramainder_div_3 column. Column
named "sum" of which would be less than 200. All columns are combined with an "AND" statement.
</pre>


Args:
<ul><li><b><code>table</code></b>:string (name of the table to retrieve from)</li>
<li><b><code>columns</code></b>:list of strings (names of the columns to retrieve)</li>
<li><b><code>column_rules</code></b>:dictionary of rules that will be evaluated</li></ul>


Returns:
<ul><li>Nested list in which is entry in a list a a column with filtered requested values</li></ul>
</td>
</tr>


