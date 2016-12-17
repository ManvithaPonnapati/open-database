#!/usr/bin/env python123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF# $Header: /opt/cvs/python/packages/share1.5/AutoDockTools/Utilities24/prepare_gpf4.py,v 1.16.2.2 2011/06/14 17:25:12 rhuey Exp $123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport string123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport os.path123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFimport glob123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom MolKit import Read123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom AutoDockTools.GridParameters import GridParameters, grid_parameter_list4123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom AutoDockTools.GridParameters import GridParameter4FileMaker123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFfrom AutoDockTools.atomTypeTools import AutoDock4_AtomTyper123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFdef usage():123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "Usage: prepare_gpf4.py -l pdbqt_file -r pdbqt_file "123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "     -l ligand_filename"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "     -r receptor_filename"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "Optional parameters:"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "    [-i reference_gpf_filename]"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "    [-o output_gpf_filename]"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "    [-x flexres_filename]"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "    [-p parameter=newvalue. For example: -p ligand_types='HD,Br,A,C,OA' or p npts='60,60,66' or gridcenter='2.5,6.5,-7.5']"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "    [-d directory of ligands to use to set types]"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "    [-y boolean to center grids on center of ligand]"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "    [-n boolean to NOT size_box_to_include_ligand]"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "    [-I increment npts in all 3 dimensions by this integer]"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "    [-v]"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "Prepare a grid parameter file (GPF) for AutoDock4."123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "   The GPF will by default be <receptor>.gpf. This"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    print "may be overridden using the -o flag."123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    123343DJNBFHJBJNKFJNBHDRFBNJKDJUNFif __name__ == '__main__':123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    import getopt123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    import sys123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    try:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        opt_list, args = getopt.getopt(sys.argv[1:], 'vl:r:i:x:o:p:d:ynI:')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    except getopt.GetoptError, msg:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print 'prepare_gpf4.py: %s' % msg123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        usage()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sys.exit(2)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    receptor_filename = ligand_filename = None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    list_filename = gpf_filename = gpf_filename = None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    output_gpf_filename = None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    flexres_filename = None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    directory = None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    parameters = []123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    verbose = None123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    center_on_ligand = False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    size_box_to_include_ligand = True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    npts_increment = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    ligand_types_defined = False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for o, a in opt_list:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if o in ('-v', '--v'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            verbose = 1123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if o in ('-l', '--l'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            ligand_filename = a123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if verbose: print 'ligand_filename=', ligand_filename123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if o in ('-r', '--r'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            receptor_filename = a123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if verbose: print 'receptor_filename=', receptor_filename123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if o in ('-i', '--i'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            gpf_filename = a123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if verbose: print 'reference_gpf_filename=', gpf_filename123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if o in ('-x', '--x'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            flexres_filename = a123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if verbose: print 'flexres_filename=', flexres_filename123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if o in ('-o', '--o'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            output_gpf_filename = a123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if verbose: print 'output_gpf_filename=', output_gpf_filename123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if o in ('-p', '--p'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            parameters.append(a)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if a.split('=')[0]=="ligand_types": ligand_types_defined = True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if verbose: print 'parameters=', parameters123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if o in ('-d', '--d'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            directory = a123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if verbose: print 'directory=', directory123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if o in ('-y', '--y'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            center_on_ligand = True123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if verbose: print 'set center_on_ligand to ', center_on_ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if o in ('-n', '--n'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            size_box_to_include_ligand = False123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if verbose: print 'set size_box_to_include_ligand to ', size_box_to_include_ligand123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if o in ('-I', '--I'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            npts_increment = int(a)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if verbose: print 'set npts_increment to ', npts_increment123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if o in ('-h', '--'):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            usage()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            sys.exit()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if (not receptor_filename) or (ligand_filename is None and directory is None and ligand_types_defined is False):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "prepare_gpf4.py: ligand and receptor filenames"123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        print "                    must be specified."123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        usage()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        sys.exit()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    gpfm = GridParameter4FileMaker(size_box_to_include_ligand=size_box_to_include_ligand,verbose=verbose)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if gpf_filename is not None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        gpfm.read_reference(gpf_filename)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if ligand_filename is not None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        gpfm.set_ligand(ligand_filename)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    gpfm.set_receptor(receptor_filename)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if directory is not None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        gpfm.set_types_from_directory(directory)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if flexres_filename is not None:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        flexmol = Read(flexres_filename)[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        flexres_types = flexmol.allAtoms.autodock_element123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        lig_types = gpfm.gpo['ligand_types']['value'].split()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        all_types = lig_types123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for t in flexres_types:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            if t not in all_types: 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                all_types.append(t)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        all_types_string = all_types[0]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if len(all_types)>1:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            for t in all_types[1:]:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF                all_types_string = all_types_string + " " + t123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        gpfm.gpo['ligand_types']['value'] = all_types_string 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for param_str in parameters:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if param_str.find("parameter_file")>-1:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            parameters.append("custom_parameter_file=1")123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            break123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    for p in parameters:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        key,newvalue = string.split(p, '=')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if key=='gridcenter' and newvalue.find(',')>-1:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            newvalue = newvalue.split(',')123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            newvalue = string.join(newvalue)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        kw = {key:newvalue}123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        apply(gpfm.set_grid_parameters, (), kw)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    #gpfm.set_grid_parameters(spacing=1.0)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if center_on_ligand is True:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        gpfm.gpo['gridcenterAuto']['value'] = 0123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        cenx,ceny,cenz = gpfm.ligand.getCenter()123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        gpfm.gpo['gridcenter']['value'] = "%.3f %.3f %.3f" %(cenx,ceny,cenz)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    if npts_increment:123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        orig_npts = gpfm.gpo['npts']['value']  #[40,40,40]123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if verbose: print "before increment npts=", orig_npts123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        for ind in range(3):123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF            gpfm.gpo['npts']['value'][ind] += npts_increment123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF        if verbose: print "after increment npts =", gpfm.gpo['npts']['value']123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF    gpfm.write_gpf(output_gpf_filename)123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF#prepare_gpf4.py -l 1ebg_lig.pdbqt -r 1ebg_rec.pdbqt -p spacing=0.4 -p ligand_types="HD,Br,A,C,OA" -p npts="60,60,60" -i ref.gpf -o testing.gpf 123343DJNBFHJBJNKFJNBHDRFBNJKDJUNF