

def sumqrt(num1,num2,num3=1):
#    print num1,num2
    #time.sleep(1)
    return [[num1+ num2],[num1-num2]]


afdb = AffinityDB(db_path)

arg_ones = np.arange(10000) +7
arg_twos = np.arange(10000) + 15
afdb.run_multithread("sumqrt",arg_types=[int,int],arg_lists=[arg_ones,arg_twos],out_types=[int],out_names=['sumqrt'],num_threads=10,commit_freq=500)
