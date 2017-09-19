<table>

<tr><td><b>activity</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
activity(
	pair_name,
	target_id,
	init=activity_init,
)
</pre>
</td>
</tr>
<tr><td>Description</td>
<td>Getting bioactivity result from local chembl database     query by the `target_chembl_id`<br><br>Example:<br><pre lang="python"><br>activity('154L_A_188_NAG','CHEMBL2366438')<br></pre><br><br>Output:<br><pre lang="python"><br>[['154L_A_188_NAG','CHEMBL3070308','CHEMBL2366438','CHEMBL223593',9,'IC50','=',28.0,'nM','CC(Oc1ccc(Oc2ncc(cc2Cl)C(F)(F)F)cc1)C(=O)O']]<br></pre><br><br></td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>pair_name</code></b>:str combined receptor id and ligand info {receptor_id}_{chain}_{resnum}_{resname}</li>
<li><b><code>target_id</code></b>:str chembl_target_id</li>
<li><b><code>init</code></b>:str init function name</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul><li>nested list:</li>
<li>[pair_name, aid, tid, mid, confidence_score, type, relation, value, unit, smile]</li></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><b>binding_affinity</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
binding_affinity(
	index_path,
	init=binding_affinity_init,
)
</pre>
</td>
</tr>
<tr><td>Description</td>
<td>Parse binding affinity record from index_path<br><br>Example:<br><pre lang="python"><br>binding_affinity('nr.csv','bindingmoad')<br></pre><br><br>Output:<br><pre lang="python"><br>[['4CPA','GLY',-19.1138279245,0.538831666908,1,'success'],<br> ['4FAB','FDS',-18.5485141155,0.552471259564,1,'success']]<br></pre><br></td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>index_path</code></b>:record file</li>
<li><b><code>init</code></b>:str init function name</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul><li>Nested list [ [pdb_name, ligand_names, log_affinities, normalized_affinities, states, comments] ]</li></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><b>blast</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
blast(
	rec_outpath,
	lig_outpath,
	init=blast_init,
)
</pre>
</td>
</tr>
<tr><td>Description</td>
<td>Applying protein sequence blast on the receptor<br><br>Example:<br><pre lang="python"><br>blast('split/10MH_C_427_5NC/10MH_C_427_5NC_receptor.pdb','split/10MH_C_427_5NC/10MH_C_427_5NC_ligand.pdb')<br></pre><br><br>Output:<br><pre lang="python"><br>[['10MH_C_427_5NC', 'CHEMBL2242732', 0.44, 'FFAGFPCQFSISGMENVKNFKRERIQTLSAYGKMKFGNSVV']]<br></pre><br></td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>rec_outpath</code></b>:str:: relative path of receptor</li>
<li><b><code>lig_outpath</code></b>:str:: relative path of ligand</li>
<li><b><code>init</code></b>:str:: init func name</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul><li>nested list: [ [pair_name, chembl_target_id, identity, sequence]]</li></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><b>dock</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
dock(
	rec_outpath,
	reorder_outpath,
	init=dock_init,
)
</pre>
</td>
</tr>
<tr><td>Description</td>
<td>Docking the ligand by smina<br><br>Example:<br><pre lang="python"><br>dock('3_split_receptor/10MH/10MH_B_407_5CM_receptor.pdb','4_reorder/10MH/10MH_B_407_5CM_ligand.pdb')<br></pre><br><br>Output:<br><pre lang="python"><br>[['3_split_receptor/10MH/10MH_B_407_5CM_receptor.pdb', '4_reorder/10MH/10MH_B_407_5CM_ligand.pdb', '5_vinardo/10MH/10MH_C_427_5NC_ligand.pdb']]<br></pre><br></td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>rec_outpath</code></b>:str relative path for receptor</li>
<li><b><code>reorder_outpath</code></b>:str relative path for reorder ligand</li>
<li><b><code>init</code></b>:str init func naem</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul><li>Nested list [[receptor_path, ligand_path, dock_result_path]]</li></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><b>download_pdb</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
download_pdb(
	pdb_id,
	init=download_pdb_init,
)
</pre>
</td>
</tr>
<tr><td>Description</td>
<td>Download PDB crystal structure from the Protein Data Bank.<br><br>Example:<br><pre lang="python"><br>download_pdb('104M')<br></pre><br><br>Output:<br><pre lang="python"><br>[['104M','download/104M.pdb']]<br></pre><br></td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>pdb_id</code></b>:string (4-letter PDB ID IE: 1QGT)</li>
<li><b><code>dir_path</code></b>:string (folder in which to save the pdb file)</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul><li>nested list [[pdb_identifier, download_file_path]]</li></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><b>generate_conformers</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
generate_conformers(
	uid,
	lig_file,
	init=generate_conformers_init,
)
</pre>
</td>
</tr>
<tr><td>Description</td>
<td>Forgets the initial coordinates of the molecule. Looses all hydrogens. Adds all hydrogens.<br>Generates random conformers. Optimizes conformers with MMFF94 Force Field.<br>Saves multiframe PDB file of the ligand with new coordinates.</td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>lig_file</code></b>:string (path to the ligand file in the PDB format to read)</li>
<li><b><code>init</code></b>:string (init function)</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul><li>nested list:</li>
<li>of dimension [1x[string]]. String is the relative path to the output file.</li></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><b>num_atoms</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
num_atoms(
	pdb_file,
	init=num_atoms_init,
)
</pre>
</td>
</tr>
<tr><td>Description</td>
<td>Counter the number of atom<br><br>Example:<br><pre lang="python"><br>num_atoms('4_reorder/10MH/10MH_B_407_5CM_ligand.pdb')<br></pre><br><br>Output:<br><pre lang="python"><br>[[10]]<br></pre><br></td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>pdb_file</code></b>:relative path of the pdb file</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul><li>nested list [[atom_num]]</li></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><b>pdb2mol</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
pdb2mol(
	uid,
	lig_file,
	init=pdb2mol_init,
)
</pre>
</td>
</tr>
<tr><td>Description</td>
<td>Convert .pdb file to .mol file</td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>lig_file</code></b>:string (relative path to the ligand file)</li>
<li><b><code>init</code></b>:string (init function)</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><b>reorder</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
reorder(
	rec_outpath,
	lig_outpath,
	init=reorder_init,
)
</pre>
</td>
</tr>
<tr><td>Description</td>
<td>Parse the ligand by smina, and then output it. So the order of the atom keeps the same as the docking result<br><br>Example:<br><pre lang="python"><br>reorder('3_split_receptor/10MH/10MH_B_407_5CM_receptor.pdb','2_split_ligand/10MH/10MH_B_407_5CM_ligand.pdb')<br></pre><br><br>Output:<br><pre lang="python"><br>[['3_split_receptor/10MH/10MH_B_407_5CM_receptor.pdb', '4_reorder/10MH/10MH_B_407_5CM_ligand.pdb']]<br></pre><br></td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>rec_outpath</code></b>:str relative path for receptor</li>
<li><b><code>lig_outpath</code></b>:str relative path for ligand</li>
<li><b><code>init</code></b>:str initialize module</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul><li>:returns:</li>
<li>nested list: [[receptor_output_path, reorder_ligand_output_path]]</li></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><b>save_record_tfr</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
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
</td>
</tr>
<tr><td>Description</td>
<td>Save input data into Tensorflow Record</td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>filename</code></b>:string (file path to the output file)</li>
<li><b><code>pos_per_binder</code></b>:integer (number of positions per binder)</li>
<li><b><code>cryst_elem</code></b>:np.array shape=[n_elem] type=float32 (elements of the ligand)</li>
<li><b><code>cryst_coord</code></b>:np.array shape=[n_elem, 3] type=float32 (coordinates of the elements of the ligand)</li>
<li><b><code>binders_elem</code></b>:list of np.array of shape=[n_elem] type=float32 (elements of binders)</li>
<li><b><code>binders_coordsets</code></b>:list of np.array [pos_per_binder, n_elem, 3 ] (coordinate sets per each of the bidners)</li>
<li><b><code>cryst_label</code></b>:float32 (something about the crystal pose, like binding affinity)</li>
<li><b><code>binders_labels</code></b>:list of np.array shape=[pos_per_binder] type=float32</li>
<li><b><code>rec_elem</code></b>:np.array of shape [n_elem] of float32</li>
<li><b><code>rec_coord</code></b>:np.array of shape [n_elem, 3]</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul><li>None</li></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><b>get_decoys</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
get_decoys(
	pdb_file,
	mol_file,
	num_atoms,
	init=get_decoys_init,
)
</pre>
</td>
</tr>
<tr><td>Description</td>
<td>For each binding ligand, get a list of decoy ligands. We filter by number of atoms and maximum common<br>substructure (MCS). Returns filepaths to all binding ligand - decoy pair.<br></td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>pdb_file</code></b>:pdb format ligand</li>
<li><b><code>mol_file</code></b>:mol format ligand</li>
<li><b><code>num_atoms</code></b>:ligand's atom number</li>
<li><b><code>init</code></b>:</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul><li>nested list [[pdb_file, decoy_files]]</li></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><b>search_decoys</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
search_decoys(
	molfile_path,
)
</pre>
</td>
</tr>


<tr><td><b>split_pdb</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
split_pdb(
	uid,
	pdb_file,
	init=split_pdb_init,
)
</pre>
</td>
</tr>
<tr><td>Description</td>
<td>Iterates through every ligand molecule in the crystal structure (frequently there are a few). For each ligand<br>selects and crops its binding site (any atom of Protein/DNA/Cofactor within the cutoff distance). Saves pairs of<br>files: ligand + this ligand's binding site.<br><br>Example:<br><pre lang="python"><br>split_pdb('105M','download/105M.pdb')<br></pre><br><br>Output:<br><pre lang="python"><br>[['05M_A_155_HEM','split/105M_A_155_HEM/105M_A_155_HEM_receptor.pdb','split/105M_A_155_HEM/105M_A_155_HEM_ligand.pdb',30,100]]<br></pre><br></td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>pdb_file</code></b>:string (relative path the the file to split)</li>
<li><b><code>cutoff_dist</code></b>:float (distance of any atoms in the binding site from any atom of the ligand to be saved)</li>
<li><b><code>min_rec_atoms</code></b>:minimun number of atoms be saved as binding site</li>
<li><b><code>min_lig_atoms</code></b>:minumum number of atoms for ligand to be saved</li>
<li><b><code>init</code></b>:string (init function in this module)</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul><li>nested list of pairs of file names of dimensions [num_pairs x [string,string,int,int]] or     [num_pairs x [lig_file,bindsite_file,lig_num_atoms,bindsite_num_atoms]]</li></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><b>test_multout</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
test_multout(
	num,
	init=test_multout_init,
)
</pre>
</td>
</tr>


<tr><td><b>test_sum</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
test_sum(
	num1,
	num2,
	init=test_sum_init,
)
</pre>
</td>
</tr>


<tr><td><b>save_record_tfr</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
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
</td>
</tr>
<tr><td>Description</td>
<td>Save input data into Tensorflow Record</td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>filename</code></b>:string (file path to the output file)</li>
<li><b><code>pos_per_binder</code></b>:integer (number of positions per binder)</li>
<li><b><code>cryst_elem</code></b>:np.array shape=[n_elem] type=float32 (elements of the ligand)</li>
<li><b><code>cryst_coord</code></b>:np.array shape=[n_elem, 3] type=float32 (coordinates of the elements of the ligand)</li>
<li><b><code>binders_elem</code></b>:list of np.array of shape=[n_elem] type=float32 (elements of binders)</li>
<li><b><code>binders_coordsets</code></b>:list of np.array [pos_per_binder, n_elem, 3 ] (coordinate sets per each of the bidners)</li>
<li><b><code>cryst_label</code></b>:float32 (something about the crystal pose, like binding affinity)</li>
<li><b><code>binders_labels</code></b>:list of np.array shape=[pos_per_binder] type=float32</li>
<li><b><code>rec_elem</code></b>:np.array of shape [n_elem] of float32</li>
<li><b><code>rec_coord</code></b>:np.array of shape [n_elem, 3]</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul><li>None</li></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><b>write_ars2_tfr</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
write_ars2_tfr(
	rec_file,
	cryst_lig_file,
	bind_lig_file,
	decoy_files,
	out_tfr_file,
	init=write_ars2_tfr_init,
)
</pre>
</td>
</tr>
<tr><td>Description</td>
<td>For each protein/ligand crystal pair, write one tfrecord with the following:<br>> rec_elem, rec_coord, cryst_elem, cryst_coord<br>> lig_nelems, lig_elem, lig_nframes, lig_coordsets, lig_labels<br></td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>rec_file</code></b>:filepath to receptor PDB</li>
<li><b><code>cryst_lig_file</code></b>:filepath to crystal ligand PDB</li>
<li><b><code>bind_lig_file</code></b>:filepath to conformers of crystal ligand PDB</li>
<li><b><code>decoy_files</code></b>:comma separated filepath to decoy ligands PDB</li>
<li><b><code>out_tfr_file</code></b>:filepath to write tf record to</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>



<tr><td><h2>Activity_init</h2></td>
<td></td>
</tr>
<tr><td><b>__init__</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
__init__(
	self,
	data_dir,
	db_path,
)
</pre>
</td>
</tr>
<tr><td>Description</td>
<td>Initialize activity func</td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>data_dir</code></b>:str dir for the folder to save data</li>
<li><b><code>db_path</code></b>:str path for the chembl database</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul><li>None</li></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><h2>Binidng_affinity_init</h2></td>
<td></td>
</tr>
<tr><td><b>__init__</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
__init__(
	self,
	db_root,
	parse_type,
)
</pre>
</td>
</tr>
<tr><td>Description</td>
<td>Initialize binding affinity parse func</td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>db_root</code></b>:string (path to the root folder of the database)</li>
<li><b><code>parse_type</code></b>:source of binding affinity record ['pdbbind','bindingmoad','bindingdb']</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul><li>None</li></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><h2>Blast_init</h2></td>
<td></td>
</tr>
<tr><td><b>__init__</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
__init__(
	self,
	data_dir,
	blast_db,
)
</pre>
</td>
</tr>
<tr><td>Description</td>
<td>Initialize blast func</td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>data_dir</code></b>:str dir for the data</li>
<li><b><code>blast_db</code></b>:str path of the blast database</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul><li>None</li></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><h2>Dock_init</h2></td>
<td></td>
</tr>
<tr><td><b>__init__</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
__init__(
	self,
	data_dir,
	dock_folder,
	smina_path,
	dock_param,
)
</pre>
</td>
</tr>
<tr><td>Description</td>
<td></td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>data_dir</code></b>:str dir for the folder to save data</li>
<li><b><code>dock_folder</code></b>:str name of the folder to save reorder output</li>
<li><b><code>smina_path</code></b>:str path for teh executable smina program</li>
<li><b><code>dock_param</code></b>:dict docking parameter {'args':[...], 'kwargs':{...}}</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><h2>Download_pdb_init</h2></td>
<td></td>
</tr>
<tr><td><b>__init__</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
__init__(
	self,
	db_root,
	download_dir,
)
</pre>
</td>
</tr>
<tr><td>Description</td>
<td>Initialize download func</td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>db_root</code></b>:string (root folder directory for the files in the database)</li>
<li><b><code>download_dir</code></b>:string (name of the directory where to put downloaded PDBs)</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul><li>None</li></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><h2>Generate_conformers_init</h2></td>
<td></td>
</tr>
<tr><td><b>__init__</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
__init__(
	self,
	db_root,
	conformers_dir,
	num_conformers,
	out_H,
)
</pre>
</td>
</tr>
<tr><td>Description</td>
<td></td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>db_root</code></b>:string (database root)</li>
<li><b><code>conformers_dir</code></b>:string (name of the directory where to put generated conformers)</li>
<li><b><code>num_conformers</code></b>:int (number of the conformers to output)</li>
<li><b><code>out_H</code></b>:bool T/F (Add hydrogen atoms to the output. All input hydorogen atoms are always lost.)</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><h2>Num_atoms_init</h2></td>
<td></td>
</tr>
<tr><td><b>__init__</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
__init__(
	self,
	db_root,
)
</pre>
</td>
</tr>
<tr><td>Description</td>
<td>Initialize num_atoms func</td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>db_root</code></b>:string (path to the root of the database)</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul><li>None</li></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><h2>Pdb2mol_init</h2></td>
<td></td>
</tr>
<tr><td><b>__init__</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
__init__(
	self,
	db_root,
	molfile_dir,
)
</pre>
</td>
</tr>
<tr><td>Description</td>
<td></td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>db_root</code></b>:string (database root)</li>
<li><b><code>molfile_dir</code></b>:string (relative path where to create the output directory with .mol files)</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><h2>Reorder_init</h2></td>
<td></td>
</tr>
<tr><td><b>__init__</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
__init__(
	self,
	data_dir,
	reorder_folder,
	smina_path,
	dock_param,
)
</pre>
</td>
</tr>
<tr><td>Description</td>
<td>Initialize reorder func<br></td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>data_dir</code></b>:str dir for the folder to save data</li>
<li><b><code>reorder_folder</code></b>:str name of the folder to save reorder output</li>
<li><b><code>smina_path</code></b>:str path for teh executable smina program</li>
<li><b><code>dock_param</code></b>:dict docking parameter {'args':[...], 'kwargs':{...}}</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul><li>None</li></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><h2>Search_decoys_init</h2></td>
<td></td>
</tr>
<tr><td><b>__init__</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
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
</td>
</tr>
<tr><td>Description</td>
<td></td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>db_root</code></b>:</li>
<li><b><code>decoy_ids</code></b>:</li>
<li><b><code>decoy_natoms</code></b>:</li>
<li><b><code>decoy_molfiles</code></b>:</li>
<li><b><code>max_decoys</code></b>:</li>
<li><b><code>atom_diff</code></b>:</li>
<li><b><code>max_substruct</code></b>:</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul><li>None</li></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><h2>Split_pdb_init</h2></td>
<td></td>
</tr>
<tr><td><b>__init__</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
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
</td>
</tr>
<tr><td>Description</td>
<td></td>
</tr>

<tr><td>Args</td>
<td><ul><li><b><code>db_root</code></b>:string (path to the root folder of the database)</li>
<li><b><code>split_dir</code></b>:string (where to put split pdbs)</li>
<li><b><code>discard_h</code></b>:Bool T/F (discard all hydrogens for both ligand and receptor defaults to True)</li></ul></td>
</tr>

<tr><td>Returns</td>
<td><ul></ul></td>
</tr>
<tr><td></td>
<td></td>
</tr>


<tr><td><h2>Test_multout_init</h2></td>
<td></td>
</tr>
<tr><td><b>__init__</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
__init__(
	self,
)
</pre>
</td>
</tr>


<tr><td><h2>Test_sum_init</h2></td>
<td></td>
</tr>
<tr><td><b>__init__</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
__init__(
	self,
)
</pre>
</td>
</tr>


<tr><td><h2>WriteARS2TFRInit</h2></td>
<td></td>
</tr>
<tr><td><b>__init__</b></td>
<td></td>
</tr>
<tr><td>Function</td>
<td><pre lang="python">
__init__(
	self,
	num_bind_confs,
	num_decoy_confs,
	num_decoys,
)
</pre>
</td>
</tr>


