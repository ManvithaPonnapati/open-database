import multiprocessing
import itertools
import nano_tools
import nano_lib
import time


class AffinityDB:
    """
    Run anything function with multithread pool
    """
    def __init__(self):
        pass


    def run_multiprocess(self,args_list, func,pool_size=10):

        # reassemble arguments as list of things that we will feed at a single execution
        #print map(list,zip(*args_list))
        commands = [[func] + list(x) for x in zip(*args_list)]

        #self._func = eval(func)
        pool = multiprocessing.Pool(pool_size)
        proc_res = pool.map_async(wrap, commands)
        proc_res.get()
        pool.close()
        pool.join()


def wrap(args):
    """
    For any function that


    :param args:
    :return:
    """
    print "wrap"
    try:
        #nano_lib.zz.printnumber(*args)
        #print "args:", args
        print "--------------------------------------"
        cmd = args[0] + '{}'.format(tuple(args[1:]))
        exec(cmd)
        print "======================================"
    except Exception as e:
        print "insert failure to the cmd table"
        print str(e)
    else:
        print "insert as success to the cmd table"
        print "insert results to the results table"
