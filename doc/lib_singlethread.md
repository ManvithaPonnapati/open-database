[TOC]

# lib_singlethread
## binding\_affinity\_op
### binding\_affinity
```
binding_affinity(
	index_path,
	source,
)
```


**Args**
- **`index_path`** : path of the input file
- **`source`** : type of file ['pdbbind', 'bindingmoad', 'bindingdb']

**Returns**

parse result [ pdb_names, ligand_names, log_affinities, normalized_affinities, states, comments]


