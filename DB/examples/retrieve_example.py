
def example1():
    '''
    simple example for retrive data

    '''

    # create retrive_data class
    ra = retrive_data()

    # get the info for receptor from table: 2
    ra.receptor(2)

    # get the info for ligand from table: 3
    ra.crystal(3)

    # get the info for affinity from table: 4
    ra.log_affinity(4, None)

    # export the data to the folder named 'test_tfr_one' as TFRecord
    ra.export_data_to('test_tfr_one','tfr')
    
    #table = ra.export_table()

def example2():
    '''
    example to show how to combine result coming from diffrernt way
    '''

    # create retrive_data object
    r  = retrive_data()

    # set the table to get ligand
    # receptor from table:2
    # reordered ligand from table:3
    # docked ligand from table:4
    # affinity information from table:5
    # select the record which have norm affinity value
    rb = r.recpeotr(2).crystal(3).docked(4).norm_affinity(5,None)

    # overlap info from table 6
    # select the position with overlap ratio value <= 0.5
    rc = rb.same().overlap(6,[None,0.5])

    # overlap info from table 6 rmsd info from table 7
    # select teh position with overlap ratio value > 0.5 and rmas value <= 2
    rd = rb.same().overlap(6,(0.5,None)).rmsd(7,[None,2])


    re = rc | rd 
    table = re.export_table()
    
def example3():
    r = retrive_data()
    r.receptor(43, None).crystal(36).log_affinity(44, None)
    r.export_data_to('debug_hydro_removal', 'av4')

def example4():
    r = retrive_data()
    r.receptor(43, None).ligand_size(54, [None, 20]).log_affinity(44, None)
    a = retrive_data()
    a.receptor(43, None).ligand_size(54, [None, 20]).log_affinity(46, None)
    b = retrive_data()
    b.receptor(43, None).ligand_size(54, [None, 20]).log_affinity(47, None)
    c = r | a | b
    #r.crystal(54)
    #r.ligand_size(54, [None, 20])
    c.export_data_to('big_vijay_data', 'av4')

if __name__ == '__main__':
    example4()

