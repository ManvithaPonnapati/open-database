    def druglike_molecules(self, idx):
        """
        Restrictions are in order of [hbond_donors, hbonds_acceptors, has_disorder, has_3d_structure, is_organometallic, is_polymeric, is_organic, r_factor, molecular_weight]
        """
        restrictions = {"hbond_donors":[None, 5], "hbond_acceptors":[None, 10], "has_disorder":[0, 0], "has_3d_structure":[1, 1], "is_organometallic":[0, 0], "is_polymeric":[0, 0], "is_organic":[1, 1], "r_factor":[0, 15], "molecular_weight":[150.0, 600.0]} #"temperature":[150, 310]}
        _, _, df = db.get_success_data(idx, dataframe=True)
        primary_key = db.primary_key_for(idx)
        for rest in restrictions: 
            df = table(df).apply_rest(rest, restrictions[rest])
        if self.ligand is None:
            self.ligand  = df 
        else:
            self.ligand = self.ligand & df

        folder_name = db.get_folder(idx)
        self.ligand_folder = '{}_{}'.format(idx, folder_name)
        self.data_type = 'csd'        
        return self

    def nondruglike_molecules(self, idx):
        """
        Restrictions are in order of [hbond_donors, hbonds_acceptors, has_disorder, has_3d_structure, is_organometallic, is_polymeric, is_organic, r_factor, molecular_weight]
        """
        restrictions = {"hbond_donors":[None, 5], "hbond_acceptors":[None, 10], "has_disorder":[0, 0], "has_3d_structure":[1, 1], "is_organometallic":[0, 0], "is_polymeric":[0, 0], "is_organic":[1, 1], "r_factor":[0, 15], "molecular_weight":[150.0, 600.0]} #"temperature":[150, 310]}
        _, _, df_all = db.get_success_data(idx, dataframe=True)
        primary_key = db.primary_key_for(idx)
        df_drugs = df_all.copy()
        for rest in restrictions: 
            df_drugs = table(df_drugs).apply_rest(rest, restrictions[rest])
        df_merge = df_all.merge(df_drugs, indicator=True, how='outer')
        df_nondrug = df_merge[df_merge['_merge'] == 'left_only']
        if self.ligand is None:
            self.ligand  = df_nondrug 
        else:
            self.ligand = self.ligand & df_nondrug

        folder_name = db.get_folder(idx)
        self.ligand_folder = '{}_{}'.format(idx, folder_name)
        self.data_type = 'csd'        
return self
