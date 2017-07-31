


tables = {
    'local_csd_load':table(*['local_csd_load',
                    OrderedDict(
                        [
                            ('Molecule_ID', 'text'), 
                            ('Coordinates', 'blob'),
                            ('Elements', 'blob'),
                            #('Molecule_Information', 'text'), 
                            #('Crystal_Information', 'text'),
                            ##('Entry_Information', 'text'),
                            ('SMILES', 'blob'),
                            ('hbond_donors', 'integer'),
                            ('hbond_acceptors', 'integer'),
                            ('has_disorder', 'integer'),
                            ('has_3d_structure', 'integer'),
                            ('is_organometallic', 'integer'),
                            ('is_polymeric', 'integer'),
                            ('is_organic', 'integer'),
                            ('r_factor', 'blob'),
                            ('molecular_weight', 'blob'),
                            ('temperature', 'blob'),
                            ('rotatable_bonds', 'blob'),
                            ('state','integer'),
                            ('comment','blob')
                        ]
                    )
}
