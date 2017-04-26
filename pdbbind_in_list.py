import math123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef get_pdbdata(protein_name = [],binding_energy = []):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #path_to_textfile = ~/common/data/general-set-except-refined/index/INDEX_core_data.2016123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    with open("INDEX_core_data.2016") as f:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        protein_list = f.readlines()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for protein in protein_list:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                unit = protein[protein.index("M")-1:protein.index("M")+1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                if unit == "mM": # 1mM = 1e+9nm123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    binding_energy.append(float(protein[protein.index("=")+1:protein.index("M")-1]) * 1000000000) 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                elif unit == "uM": # 1uM = 1000000pm123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    binding_energy.append(float(protein[protein.index("=")+1:protein.index("M")-1]) * 1000000)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                elif unit == "nM": # 1nM = 1000pm123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    binding_energy.append(float(protein[protein.index("=")+1:protein.index("M")-1]) * 1000)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                elif unit == "pM": # 1pM = 0.001nm123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    binding_energy.append(float(protein[protein.index("=")+1:protein.index("M")-1]))123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                else:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                    raise ValueError123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                protein_name.append(protein[:4])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            except:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                break123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        return protein_name,binding_energy123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef get_protein_name():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return get_pdbdata()[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef get_binding_energy(protein_energy = get_pdbdata()[1]):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    log_energy = [1]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    max_energy = math.log(protein_energy[0])123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for data in protein_energy[1:]:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        log_energy.append(math.log(data)/max_energy)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    return log_energy123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFprint(get_pdbdata())123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF