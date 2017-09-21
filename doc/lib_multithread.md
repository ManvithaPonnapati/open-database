
-[Functions](#functions)
  * [activity](#activity)
-[Functions](#functions)
  * [binding_affinity](#binding_affinity)
-[Functions](#functions)
  * [blast](#blast)
-[Functions](#functions)
  * [dock](#dock)
-[Functions](#functions)
  * [download_pdb](#download_pdb)
-[Functions](#functions)
  * [generate_conformers](#generate_conformers)
-[Functions](#functions)
  * [num_atoms](#num_atoms)
-[Functions](#functions)
  * [pdb2mol](#pdb2mol)
-[Functions](#functions)
  * [reorder](#reorder)
-[Functions](#functions)
  * [save_record_tfr](#save_record_tfr)
-[Functions](#functions)
  * [get_decoys](#get_decoys)
  * [search_decoys](#search_decoys)
-[Functions](#functions)
  * [split_pdb](#split_pdb)
-[Functions](#functions)
  * [test_multout](#test_multout)
-[Functions](#functions)
  * [test_sum](#test_sum)
-[Functions](#functions)
  * [save_record_tfr](#save_record_tfr)
  * [write_ars2_tfr](#write_ars2_tfr)
- [Activity_init](#activity_init)
  * [__init__](#__init__)
- [Binidng_affinity_init](#binidng_affinity_init)
  * [__init__](#__init__)
- [Blast_init](#blast_init)
  * [__init__](#__init__)
- [Dock_init](#dock_init)
  * [__init__](#__init__)
- [Download_pdb_init](#download_pdb_init)
  * [__init__](#__init__)
- [Generate_conformers_init](#generate_conformers_init)
  * [__init__](#__init__)
- [Num_atoms_init](#num_atoms_init)
  * [__init__](#__init__)
- [Pdb2mol_init](#pdb2mol_init)
  * [__init__](#__init__)
- [Reorder_init](#reorder_init)
  * [__init__](#__init__)
- [Search_decoys_init](#search_decoys_init)
  * [__init__](#__init__)
- [Split_pdb_init](#split_pdb_init)
  * [__init__](#__init__)
- [Test_multout_init](#test_multout_init)
  * [__init__](#__init__)
- [Test_sum_init](#test_sum_init)
  * [__init__](#__init__)
- [WriteARS2TFRInit](#writears2tfrinit)
  * [__init__](#__init__)
<table>

<tr bgcolor="#FFFFFF"><td><h4><b>activity</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/activity_op.py">lib_multithread/activity_op.py</a><br><pre lang="python">
activity(
	pair_name,
	target_id,
	init=activity_init,
)
</pre>
Getting bioactivity result from local chembl database     query by the `target_chembl_id`

Example:
<pre lang="python">
activity('154L_A_188_NAG','CHEMBL2366438')
</pre>

Output:
<pre lang="python">
[['154L_A_188_NAG','CHEMBL3070308','CHEMBL2366438','CHEMBL223593',9,'IC50','=',28.0,'nM','CC(Oc1ccc(Oc2ncc(cc2Cl)C(F)(F)F)cc1)C(=O)O']]
</pre>



Args:
<ul><li><b><code>pair_name</code></b>:str combined receptor id and ligand info {receptor_id}_{chain}_{resnum}_{resname}</li>
<li><b><code>target_id</code></b>:str chembl_target_id</li>
<li><b><code>init</code></b>:str init function name</li></ul>


Returns:
<ul><li>nested list:</li>
<li>[pair_name, aid, tid, mid, confidence_score, type, relation, value, unit, smile]</li></ul>
</td>
</tr>


<tr bgcolor="#FFFFFF"><td><h4><b>binding_affinity</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/binidng_affinity_op.py">lib_multithread/binidng_affinity_op.py</a><br><pre lang="python">
binding_affinity(
	index_path,
	init=binding_affinity_init,
)
</pre>
Parse binding affinity record from index_path

Example:
<pre lang="python">
binding_affinity('nr.csv','bindingmoad')
</pre>

Output:
<pre lang="python">
[['4CPA','GLY',-19.1138279245,0.538831666908,1,'success'],
 ['4FAB','FDS',-18.5485141155,0.552471259564,1,'success']]
</pre>


Args:
<ul><li><b><code>index_path</code></b>:record file</li>
<li><b><code>init</code></b>:str init function name</li></ul>


Returns:
<ul><li>Nested list [ [pdb_name, ligand_names, log_affinities, normalized_affinities, states, comments] ]</li></ul>
</td>
</tr>


<tr bgcolor="#FFFFFF"><td><h4><b>blast</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/blast_op.py">lib_multithread/blast_op.py</a><br><pre lang="python">
blast(
	rec_outpath,
	lig_outpath,
	init=blast_init,
)
</pre>
Applying protein sequence blast on the receptor

Example:
<pre lang="python">
blast('split/10MH_C_427_5NC/10MH_C_427_5NC_receptor.pdb','split/10MH_C_427_5NC/10MH_C_427_5NC_ligand.pdb')
</pre>

Output:
<pre lang="python">
[['10MH_C_427_5NC', 'CHEMBL2242732', 0.44, 'FFAGFPCQFSISGMENVKNFKRERIQTLSAYGKMKFGNSVV']]
</pre>


Args:
<ul><li><b><code>rec_outpath</code></b>:str:: relative path of receptor</li>
<li><b><code>lig_outpath</code></b>:str:: relative path of ligand</li>
<li><b><code>init</code></b>:str:: init func name</li></ul>


Returns:
<ul><li>nested list: [ [pair_name, chembl_target_id, identity, sequence]]</li></ul>
</td>
</tr>


<tr bgcolor="#FFFFFF"><td><h4><b>dock</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/dock_op.py">lib_multithread/dock_op.py</a><br><pre lang="python">
dock(
	rec_outpath,
	reorder_outpath,
	init=dock_init,
)
</pre>
Docking the ligand by smina

Example:
<pre lang="python">
dock('3_split_receptor/10MH/10MH_B_407_5CM_receptor.pdb','4_reorder/10MH/10MH_B_407_5CM_ligand.pdb')
</pre>

Output:
<pre lang="python">
[['3_split_receptor/10MH/10MH_B_407_5CM_receptor.pdb', '4_reorder/10MH/10MH_B_407_5CM_ligand.pdb', '5_vinardo/10MH/10MH_C_427_5NC_ligand.pdb']]
</pre>


Args:
<ul><li><b><code>rec_outpath</code></b>:str relative path for receptor</li>
<li><b><code>reorder_outpath</code></b>:str relative path for reorder ligand</li>
<li><b><code>init</code></b>:str init func naem</li></ul>


Returns:
<ul><li>Nested list [[receptor_path, ligand_path, dock_result_path]]</li></ul>
</td>
</tr>


<tr bgcolor="#FFFFFF"><td><h4><b>download_pdb</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/download_pdb_op.py">lib_multithread/download_pdb_op.py</a><br><pre lang="python">
download_pdb(
	pdb_id,
	init=download_pdb_init,
)
</pre>
Download PDB crystal structure from the Protein Data Bank.

Example:
<pre lang="python">
download_pdb('104M')
</pre>

Output:
<pre lang="python">
[['104M','download/104M.pdb']]
</pre>


Args:
<ul><li><b><code>pdb_id</code></b>:string (4-letter PDB ID IE: 1QGT)</li>
<li><b><code>dir_path</code></b>:string (folder in which to save the pdb file)</li></ul>


Returns:
<ul><li>nested list [[pdb_identifier, download_file_path]]</li></ul>
</td>
</tr>


<tr bgcolor="#FFFFFF"><td><h4><b>generate_conformers</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/generate_conformers_op.py">lib_multithread/generate_conformers_op.py</a><br><pre lang="python">
generate_conformers(
	uid,
	lig_file,
	init=generate_conformers_init,
)
</pre>
Forgets the initial coordinates of the molecule. Looses all hydrogens. Adds all hydrogens.
Generates random conformers. Optimizes conformers with MMFF94 Force Field.
Saves multiframe PDB file of the ligand with new coordinates.

Args:
<ul><li><b><code>lig_file</code></b>:string (path to the ligand file in the PDB format to read)</li>
<li><b><code>init</code></b>:string (init function)</li></ul>


Returns:
<ul><li>nested list:</li>
<li>of dimension [1x[string]]. String is the relative path to the output file.</li></ul>
</td>
</tr>


<tr bgcolor="#FFFFFF"><td><h4><b>num_atoms</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/num_atoms_op.py">lib_multithread/num_atoms_op.py</a><br><pre lang="python">
num_atoms(
	pdb_file,
	init=num_atoms_init,
)
</pre>
Counter the number of atom

Example:
<pre lang="python">
num_atoms('4_reorder/10MH/10MH_B_407_5CM_ligand.pdb')
</pre>

Output:
<pre lang="python">
[[10]]
</pre>


Args:
<ul><li><b><code>pdb_file</code></b>:relative path of the pdb file</li></ul>


Returns:
<ul><li>nested list [[atom_num]]</li></ul>
</td>
</tr>


<tr bgcolor="#FFFFFF"><td><h4><b>pdb2mol</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/pdb2mol_op.py">lib_multithread/pdb2mol_op.py</a><br><pre lang="python">
pdb2mol(
	uid,
	lig_file,
	init=pdb2mol_init,
)
</pre>
Convert .pdb file to .mol file

Args:
<ul><li><b><code>lig_file</code></b>:string (relative path to the ligand file)</li>
<li><b><code>init</code></b>:string (init function)</li></ul>


Returns:
<ul></ul>
</td>
</tr>


<tr bgcolor="#FFFFFF"><td><h4><b>reorder</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/reorder_op.py">lib_multithread/reorder_op.py</a><br><pre lang="python">
reorder(
	rec_outpath,
	lig_outpath,
	init=reorder_init,
)
</pre>
Parse the ligand by smina, and then output it. So the order of the atom keeps the same as the docking result

Example:
<pre lang="python">
reorder('3_split_receptor/10MH/10MH_B_407_5CM_receptor.pdb','2_split_ligand/10MH/10MH_B_407_5CM_ligand.pdb')
</pre>

Output:
<pre lang="python">
[['3_split_receptor/10MH/10MH_B_407_5CM_receptor.pdb', '4_reorder/10MH/10MH_B_407_5CM_ligand.pdb']]
</pre>


Args:
<ul><li><b><code>rec_outpath</code></b>:str relative path for receptor</li>
<li><b><code>lig_outpath</code></b>:str relative path for ligand</li>
<li><b><code>init</code></b>:str initialize module</li></ul>


Returns:
<ul><li>:returns:</li>
<li>nested list: [[receptor_output_path, reorder_ligand_output_path]]</li></ul>
</td>
</tr>


<tr bgcolor="#FFFFFF"><td><h4><b>save_record_tfr</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/save_record_tfr_op.py">lib_multithread/save_record_tfr_op.py</a><br><pre lang="python">
save_record_tfr(
	filename,
	cryst_elem,
	cryst_coord,
	binders_elem,
	binders_coordsets,
	cryst_label,
	binders_labels,
	rec_elem,
	rec_coord,
)
</pre>
Save input data into Tensorflow Record

Args:
<ul><li><b><code>filename</code></b>:string (file path to the output file)</li>
<li><b><code>pos_per_binder</code></b>:integer (number of positions per binder)</li>
<li><b><code>cryst_elem</code></b>:np.array shape=[n_elem] type=float32 (elements of the ligand)</li>
<li><b><code>cryst_coord</code></b>:np.array shape=[n_elem, 3] type=float32 (coordinates of the elements of the ligand)</li>
<li><b><code>binders_elem</code></b>:list of np.array of shape=[n_elem] type=float32 (elements of binders)</li>
<li><b><code>binders_coordsets</code></b>:list of np.array [pos_per_binder, n_elem, 3 ] (coordinate sets per each of the bidners)</li>
<li><b><code>cryst_label</code></b>:float32 (something about the crystal pose, like binding affinity)</li>
<li><b><code>binders_labels</code></b>:list of np.array shape=[pos_per_binder] type=float32</li>
<li><b><code>rec_elem</code></b>:np.array of shape [n_elem] of float32</li>
<li><b><code>rec_coord</code></b>:np.array of shape [n_elem, 3]</li></ul>


Returns:
<ul><li>None</li></ul>
</td>
</tr>


<tr bgcolor="#FFFFFF"><td><h4><b>get_decoys</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/search_decoys_op.py">lib_multithread/search_decoys_op.py</a><br><pre lang="python">
get_decoys(
	pdb_file,
	mol_file,
	num_atoms,
	init=get_decoys_init,
)
</pre>
For each binding ligand, get a list of decoy ligands. We filter by number of atoms and maximum common
substructure (MCS). Returns filepaths to all binding ligand - decoy pair.


Args:
<ul><li><b><code>pdb_file</code></b>:pdb format ligand</li>
<li><b><code>mol_file</code></b>:mol format ligand</li>
<li><b><code>num_atoms</code></b>:ligand's atom number</li>
<li><b><code>init</code></b>:</li></ul>


Returns:
<ul><li>nested list [[pdb_file, decoy_files]]</li></ul>
</td>
</tr>


<tr bgcolor="#FFFFFF"><td><h4><b>search_decoys</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/search_decoys_op.py">lib_multithread/search_decoys_op.py</a><br><pre lang="python">
search_decoys(
	molfile_path,
)
</pre>
</td>
</tr>


<tr bgcolor="#FFFFFF"><td><h4><b>split_pdb</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/split_pdb_op.py">lib_multithread/split_pdb_op.py</a><br><pre lang="python">
split_pdb(
	uid,
	pdb_file,
	init=split_pdb_init,
)
</pre>
Iterates through every ligand molecule in the crystal structure (frequently there are a few). For each ligand
selects and crops its binding site (any atom of Protein/DNA/Cofactor within the cutoff distance). Saves pairs of
files: ligand + this ligand's binding site.

Example:
<pre lang="python">
split_pdb('105M','download/105M.pdb')
</pre>

Output:
<pre lang="python">
[['05M_A_155_HEM','split/105M_A_155_HEM/105M_A_155_HEM_receptor.pdb','split/105M_A_155_HEM/105M_A_155_HEM_ligand.pdb',30,100]]
</pre>


Args:
<ul><li><b><code>pdb_file</code></b>:string (relative path the the file to split)</li>
<li><b><code>cutoff_dist</code></b>:float (distance of any atoms in the binding site from any atom of the ligand to be saved)</li>
<li><b><code>min_rec_atoms</code></b>:minimun number of atoms be saved as binding site</li>
<li><b><code>min_lig_atoms</code></b>:minumum number of atoms for ligand to be saved</li>
<li><b><code>init</code></b>:string (init function in this module)</li></ul>


Returns:
<ul><li>nested list of pairs of file names of dimensions [num_pairs x [string,string,int,int]] or     [num_pairs x [lig_file,bindsite_file,lig_num_atoms,bindsite_num_atoms]]</li></ul>
</td>
</tr>


<tr bgcolor="#FFFFFF"><td><h4><b>test_multout</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/test_multout_op.py">lib_multithread/test_multout_op.py</a><br><pre lang="python">
test_multout(
	num,
	init=test_multout_init,
)
</pre>
</td>
</tr>


<tr bgcolor="#FFFFFF"><td><h4><b>test_sum</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/test_sum_op.py">lib_multithread/test_sum_op.py</a><br><pre lang="python">
test_sum(
	num1,
	num2,
	init=test_sum_init,
)
</pre>
</td>
</tr>


<tr bgcolor="#FFFFFF"><td><h4><b>save_record_tfr</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/save_record_tfr_op.py">lib_multithread/save_record_tfr_op.py</a><br><pre lang="python">
save_record_tfr(
	filename,
	cryst_elem,
	cryst_coord,
	binders_elem,
	binders_coordsets,
	cryst_label,
	binders_labels,
	rec_elem,
	rec_coord,
)
</pre>
Save input data into Tensorflow Record

Args:
<ul><li><b><code>filename</code></b>:string (file path to the output file)</li>
<li><b><code>pos_per_binder</code></b>:integer (number of positions per binder)</li>
<li><b><code>cryst_elem</code></b>:np.array shape=[n_elem] type=float32 (elements of the ligand)</li>
<li><b><code>cryst_coord</code></b>:np.array shape=[n_elem, 3] type=float32 (coordinates of the elements of the ligand)</li>
<li><b><code>binders_elem</code></b>:list of np.array of shape=[n_elem] type=float32 (elements of binders)</li>
<li><b><code>binders_coordsets</code></b>:list of np.array [pos_per_binder, n_elem, 3 ] (coordinate sets per each of the bidners)</li>
<li><b><code>cryst_label</code></b>:float32 (something about the crystal pose, like binding affinity)</li>
<li><b><code>binders_labels</code></b>:list of np.array shape=[pos_per_binder] type=float32</li>
<li><b><code>rec_elem</code></b>:np.array of shape [n_elem] of float32</li>
<li><b><code>rec_coord</code></b>:np.array of shape [n_elem, 3]</li></ul>


Returns:
<ul><li>None</li></ul>
</td>
</tr>


<tr bgcolor="#FFFFFF"><td><h4><b>write_ars2_tfr</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/write_ars2_tfr_op.py">lib_multithread/write_ars2_tfr_op.py</a><br><pre lang="python">
write_ars2_tfr(
	rec_file,
	cryst_lig_file,
	bind_lig_file,
	decoy_files,
	out_tfr_file,
	init=write_ars2_tfr_init,
)
</pre>
For each protein/ligand crystal pair, write one tfrecord with the following:
> rec_elem, rec_coord, cryst_elem, cryst_coord
> lig_nelems, lig_elem, lig_nframes, lig_coordsets, lig_labels


Args:
<ul><li><b><code>rec_file</code></b>:filepath to receptor PDB</li>
<li><b><code>cryst_lig_file</code></b>:filepath to crystal ligand PDB</li>
<li><b><code>bind_lig_file</code></b>:filepath to conformers of crystal ligand PDB</li>
<li><b><code>decoy_files</code></b>:comma separated filepath to decoy ligands PDB</li>
<li><b><code>out_tfr_file</code></b>:filepath to write tf record to</li></ul>


Returns:
<ul></ul>
</td>
</tr>



<tr bgcolor="#F6F8FA"><td><h3>Activity_init</h3><i>Class</i></td>
</tr>
<tr bgcolor="#FFFFFF"><td><h4><b>__init__</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/activity_op.py">lib_multithread/activity_op.py</a><br><pre lang="python">
__init__(
	self,
	data_dir,
	db_path,
)
</pre>
Initialize activity func

Args:
<ul><li><b><code>data_dir</code></b>:str dir for the folder to save data</li>
<li><b><code>db_path</code></b>:str path for the chembl database</li></ul>


Returns:
<ul><li>None</li></ul>
</td>
</tr>


<tr bgcolor="#F6F8FA"><td><h3>Binidng_affinity_init</h3><i>Class</i></td>
</tr>
<tr bgcolor="#FFFFFF"><td><h4><b>__init__</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/binidng_affinity_op.py">lib_multithread/binidng_affinity_op.py</a><br><pre lang="python">
__init__(
	self,
	db_root,
	parse_type,
)
</pre>
Initialize binding affinity parse func

Args:
<ul><li><b><code>db_root</code></b>:string (path to the root folder of the database)</li>
<li><b><code>parse_type</code></b>:source of binding affinity record ['pdbbind','bindingmoad','bindingdb']</li></ul>


Returns:
<ul><li>None</li></ul>
</td>
</tr>


<tr bgcolor="#F6F8FA"><td><h3>Blast_init</h3><i>Class</i></td>
</tr>
<tr bgcolor="#FFFFFF"><td><h4><b>__init__</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/blast_op.py">lib_multithread/blast_op.py</a><br><pre lang="python">
__init__(
	self,
	data_dir,
	blast_db,
)
</pre>
Initialize blast func

Args:
<ul><li><b><code>data_dir</code></b>:str dir for the data</li>
<li><b><code>blast_db</code></b>:str path of the blast database</li></ul>


Returns:
<ul><li>None</li></ul>
</td>
</tr>


<tr bgcolor="#F6F8FA"><td><h3>Dock_init</h3><i>Class</i></td>
</tr>
<tr bgcolor="#FFFFFF"><td><h4><b>__init__</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/dock_op.py">lib_multithread/dock_op.py</a><br><pre lang="python">
__init__(
	self,
	data_dir,
	dock_folder,
	smina_path,
	dock_param,
)
</pre>


Args:
<ul><li><b><code>data_dir</code></b>:str dir for the folder to save data</li>
<li><b><code>dock_folder</code></b>:str name of the folder to save reorder output</li>
<li><b><code>smina_path</code></b>:str path for teh executable smina program</li>
<li><b><code>dock_param</code></b>:dict docking parameter {'args':[...], 'kwargs':{...}}</li></ul>


Returns:
<ul></ul>
</td>
</tr>


<tr bgcolor="#F6F8FA"><td><h3>Download_pdb_init</h3><i>Class</i></td>
</tr>
<tr bgcolor="#FFFFFF"><td><h4><b>__init__</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/download_pdb_op.py">lib_multithread/download_pdb_op.py</a><br><pre lang="python">
__init__(
	self,
	db_root,
	download_dir,
)
</pre>
Initialize download func

Args:
<ul><li><b><code>db_root</code></b>:string (root folder directory for the files in the database)</li>
<li><b><code>download_dir</code></b>:string (name of the directory where to put downloaded PDBs)</li></ul>


Returns:
<ul><li>None</li></ul>
</td>
</tr>


<tr bgcolor="#F6F8FA"><td><h3>Generate_conformers_init</h3><i>Class</i></td>
</tr>
<tr bgcolor="#FFFFFF"><td><h4><b>__init__</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/generate_conformers_op.py">lib_multithread/generate_conformers_op.py</a><br><pre lang="python">
__init__(
	self,
	db_root,
	conformers_dir,
	num_conformers,
	out_H,
)
</pre>


Args:
<ul><li><b><code>db_root</code></b>:string (database root)</li>
<li><b><code>conformers_dir</code></b>:string (name of the directory where to put generated conformers)</li>
<li><b><code>num_conformers</code></b>:int (number of the conformers to output)</li>
<li><b><code>out_H</code></b>:bool T/F (Add hydrogen atoms to the output. All input hydorogen atoms are always lost.)</li></ul>


Returns:
<ul></ul>
</td>
</tr>


<tr bgcolor="#F6F8FA"><td><h3>Num_atoms_init</h3><i>Class</i></td>
</tr>
<tr bgcolor="#FFFFFF"><td><h4><b>__init__</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/num_atoms_op.py">lib_multithread/num_atoms_op.py</a><br><pre lang="python">
__init__(
	self,
	db_root,
)
</pre>
Initialize num_atoms func

Args:
<ul><li><b><code>db_root</code></b>:string (path to the root of the database)</li></ul>


Returns:
<ul><li>None</li></ul>
</td>
</tr>


<tr bgcolor="#F6F8FA"><td><h3>Pdb2mol_init</h3><i>Class</i></td>
</tr>
<tr bgcolor="#FFFFFF"><td><h4><b>__init__</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/pdb2mol_op.py">lib_multithread/pdb2mol_op.py</a><br><pre lang="python">
__init__(
	self,
	db_root,
	molfile_dir,
)
</pre>


Args:
<ul><li><b><code>db_root</code></b>:string (database root)</li>
<li><b><code>molfile_dir</code></b>:string (relative path where to create the output directory with .mol files)</li></ul>


Returns:
<ul></ul>
</td>
</tr>


<tr bgcolor="#F6F8FA"><td><h3>Reorder_init</h3><i>Class</i></td>
</tr>
<tr bgcolor="#FFFFFF"><td><h4><b>__init__</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/reorder_op.py">lib_multithread/reorder_op.py</a><br><pre lang="python">
__init__(
	self,
	data_dir,
	reorder_folder,
	smina_path,
	dock_param,
)
</pre>
Initialize reorder func


Args:
<ul><li><b><code>data_dir</code></b>:str dir for the folder to save data</li>
<li><b><code>reorder_folder</code></b>:str name of the folder to save reorder output</li>
<li><b><code>smina_path</code></b>:str path for teh executable smina program</li>
<li><b><code>dock_param</code></b>:dict docking parameter {'args':[...], 'kwargs':{...}}</li></ul>


Returns:
<ul><li>None</li></ul>
</td>
</tr>


<tr bgcolor="#F6F8FA"><td><h3>Search_decoys_init</h3><i>Class</i></td>
</tr>
<tr bgcolor="#FFFFFF"><td><h4><b>__init__</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/search_decoys_op.py">lib_multithread/search_decoys_op.py</a><br><pre lang="python">
__init__(
	self,
	db_root,
	decoy_ids,
	decoy_natoms,
	decoy_molfiles,
	max_decoys=10,
	atom_diff=5,
	max_substruct=5,
)
</pre>


Args:
<ul><li><b><code>db_root</code></b>:</li>
<li><b><code>decoy_ids</code></b>:</li>
<li><b><code>decoy_natoms</code></b>:</li>
<li><b><code>decoy_molfiles</code></b>:</li>
<li><b><code>max_decoys</code></b>:</li>
<li><b><code>atom_diff</code></b>:</li>
<li><b><code>max_substruct</code></b>:</li></ul>


Returns:
<ul><li>None</li></ul>
</td>
</tr>


<tr bgcolor="#F6F8FA"><td><h3>Split_pdb_init</h3><i>Class</i></td>
</tr>
<tr bgcolor="#FFFFFF"><td><h4><b>__init__</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/split_pdb_op.py">lib_multithread/split_pdb_op.py</a><br><pre lang="python">
__init__(
	self,
	db_root,
	split_dir,
	discard_h=True,
	cutoff_dist=10,
	min_rec_atoms=10,
	min_lig_atoms=5,
)
</pre>


Args:
<ul><li><b><code>db_root</code></b>:string (path to the root folder of the database)</li>
<li><b><code>split_dir</code></b>:string (where to put split pdbs)</li>
<li><b><code>discard_h</code></b>:Bool T/F (discard all hydrogens for both ligand and receptor defaults to True)</li></ul>


Returns:
<ul></ul>
</td>
</tr>


<tr bgcolor="#F6F8FA"><td><h3>Test_multout_init</h3><i>Class</i></td>
</tr>
<tr bgcolor="#FFFFFF"><td><h4><b>__init__</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/test_multout_op.py">lib_multithread/test_multout_op.py</a><br><pre lang="python">
__init__(
	self,
)
</pre>
</td>
</tr>


<tr bgcolor="#F6F8FA"><td><h3>Test_sum_init</h3><i>Class</i></td>
</tr>
<tr bgcolor="#FFFFFF"><td><h4><b>__init__</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/test_sum_op.py">lib_multithread/test_sum_op.py</a><br><pre lang="python">
__init__(
	self,
)
</pre>
</td>
</tr>


<tr bgcolor="#F6F8FA"><td><h3>WriteARS2TFRInit</h3><i>Class</i></td>
</tr>
<tr bgcolor="#FFFFFF"><td><h4><b>__init__</b></h4><br><br>Defined in <a href="https://github.com/mitaffinity/open-database/tree/master/affinityDB/lib_multithread/write_ars2_tfr_op.py">lib_multithread/write_ars2_tfr_op.py</a><br><pre lang="python">
__init__(
	self,
	num_bind_confs,
	num_decoy_confs,
	num_decoys,
)
</pre>
</td>
</tr>


