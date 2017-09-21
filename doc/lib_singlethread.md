
-[Functions](#functions)
  * [binding_affinity](#binding_affinity)
<table>

<tr bgcolor="#FFFFFF"><td><h4><b>binding_affinity</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_singlethread/binding_affinity_op.py">lib_singlethread/binding_affinity_op.py</a><br><pre lang="python">
binding_affinity(
	index_path,
	source,
)
</pre>


Args:
<ul><li><b><code>index_path</code></b>:path of the input file</li>
<li><b><code>source</code></b>:type of file ['pdbbind', 'bindingmoad', 'bindingdb']</li></ul>


Returns:
<ul><li>parse result [ pdb_names, ligand_names, log_affinities, normalized_affinities, states, comments]</li></ul>
</td>
</tr>


