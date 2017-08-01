from collections import namedtuple, OrderedDict

table = namedtuple('Table',['type','columns','primary_key'])

"""
tables store the information about the table to be created in the database ( except scoring_terms )
table:
    name: name of the table in database, name of the csv file when export the table
    columns: the name and value type for each columns in the table
    primary_key: the name of the primary key for this table
    

    
When initialize the database, it first parse config.scoring_terms and add it in tables  
and then create all table defined in tables
"""

basic_tables = {
    'dependence':table(*['dependence',
                    OrderedDict(
                        [
                            ('source','integer'),
                            ('dest','integer')
                        ]
                    ),
                    ['source','dest']]),
    'db_info':table(*['db_info',
                    OrderedDict(
                        [
                            ('name','text'),
                            ('type','text'),
                            ('table_idx','integer'),
                            ('create_time','text'),
                            ('parameter','text')
                        ]
                    ),
                    ['table_idx']]),
}

tables = {
    'download':table(*['download',
                     OrderedDict(
                         [
                             ('receptor','text'),
                             ('experiment','text'),
                             ('resolution','real'),
                             ('state','integer'),
                             ('comment','text')
                         ]
                     ),
                     ['receptor']]),
    'split_ligand':table(*['splited_ligand',
                     OrderedDict(
                        [
                            ('receptor','text'),
                            ('chain','text'),
                            ('resnum','text'),
                            ('resname','text'),
                            ('resid','text'),
                            ('heavy_atom','integer'),
                            ('max_size_on_axis', 'real'),
                            ('state','integer'),
                            ('comment','text')
                        ]
                     ),
                     ['receptor','chain','resnum','resname']
                ]),
    'split_receptor':table(*['splited_receptor',
                        OrderedDict(
                            [
                                ('receptor','text'),
                                ('chain','text'),
                                ('resnum','text'),
                                ('resname','text'),
                                ('heavy_atom','integer'),
                                ('experiment','text'),
                                ('resolution','real'),
                                ('state','integer'),
                                ('comment','text')
                            ]
                        ),
                        ['receptor','chain','resnum','resname']
                ])
}

