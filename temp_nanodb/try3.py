import os,sqlite3,time
import numpy as np
import multiprocessing
import threading
from functools import partial

# register input
# create a table with commands

# run_mutltithread(function,inputs,input_types)
# only text,float,and integers are supported

db_path = "/home/maksym/Projects/new_data/nano.db"
os.system('rm ' + db_path)

class AffinityDB:
    python_to_sql = {int: 'integer', float: 'float', str: 'string'}
    sql_to_python = {'integer': int, 'float': float, 'string': str}

    def __init__(self,db_path):

        self.conn = sqlite3.connect(db_path)

    def run_multithread(self,func,arg_types,arg_lists,out_types,out_names,num_threads=1):

        assert(set(arg_types).issubset([int,float,str])), \
            "Unknown input_type. Expected keywords: int,float,str."
        assert(len(arg_types)==len(arg_lists)),\
            "Number of arguments in arg_types and arg_lists should be equal, " \
            "but are: " + str(len(arg_types)) + " and " + str(len(arg_lists))
        assert all([len(arg_list) == len(arg_lists[0]) for arg_list in arg_lists]), \
            "One or more lists in arg_lists are of a different length"
        # TODO: assert evrey input in the list is of a given type
        # todo: assert out names and out types

        num_args = len(arg_types)
        var_names = list(eval(func).__code__.co_varnames)[:num_args]
        num_outs = len(out_types)
        num_runs = len(arg_lists[0])

        # initiate sqlite3 table for commands
        arg_types = [self.python_to_sql[arg_type] for arg_type in arg_types]
        sql_cmd = 'create table arg_' + func + ' (run_idx integer not null, '
        sql_cmd += ", ".join([str(var_names[i])+" "+str(arg_types[i]) for i in range(num_args)])
        sql_cmd += ", run_state integer, run_message text, primary key(run_idx));"
        self.conn.execute(str(sql_cmd))

        # fill sqlite3 table with single commands that python threads will execute
        sql_cmd = "insert into arg_" + func + " values ("
        sql_cmd += ", ".join(["{}" for i in range(num_args+3)]) + ");"
        arg_lists = [range(num_runs)] + arg_lists # one column is used for run_index
        arg_sets = [list(x) + ['NULL'] + ['NULL'] for x in zip(*arg_lists)]
        sql_cmds = [sql_cmd.format(*arg_set) for arg_set in arg_sets]
        [self.conn.execute(sql_cmd) for sql_cmd in sql_cmds]
        self.conn.commit()

        # create sqlite3 table for the outputs
        out_types = [self.python_to_sql[out_type] for out_type in out_types]
        sql_cmd = 'create table out_' + func + ' (run_idx integer not null, out_idx integer not null, '
        sql_cmd += ", ".join([str(out_names[i])+" "+str(out_types[i]) for i in range(num_outs)])
        sql_cmd += ", primary key(out_idx));"
        self.conn.execute(str(sql_cmd))
        # run a regular continue command with the threads
        # FIXME: func should be time_idx
        self.coninue(func,num_threads=num_threads)


    def coninue(self,func,num_threads=1):
        """
        Continue running any function based on cmd_ in the table
        :param func:
        :param time:
        :return:
        """
        # retrieve sets of arguments from sqlite columns
        cursor = self.conn.cursor()
        sql_cmd = 'pragma table_info(arg_{})'.format(func)
        cursor.execute(sql_cmd)
        arg_infos = cursor.fetchall()
        arg_types = ([str(arg_info[2]) for arg_info in arg_infos][:-2])
        arg_types = [self.sql_to_python[arg_type] for arg_type in arg_types]

        # find the information about the data types in the results
        sql_cmd = 'pragma table_info(arg_{})'.format(func)
        cursor.execute(sql_cmd)
        out_infos = cursor.fetchall()
        out_types = ([str(out_info[2]) for out_info in out_infos][:-2])
        out_types = [AffinityDB.sql_to_python[out_type] for out_type in out_types]

        # retrieve all sets of parameters to run function with
        arg_names = [str(arg_info[1]) for arg_info in arg_infos][:-2]
        sql_cmd = 'select ' + " ,".join(arg_names) + ' from arg_' + func + ' where run_state is NULL;'
        cursor.execute(sql_cmd)
        arg_sets = cursor.fetchall()

        # run tasks with the multiprocessing pool (on the background)
        pool = multiprocessing.Pool(num_threads)
        m = multiprocessing.Manager()
        arg_q = m.Queue()
        out_q = m.Queue()
        tasks = []
        for arg_set in arg_sets:
            task = pool.apply_async(_thread_proxie,args=(func,arg_set,arg_q,out_q,out_types,))
            tasks.append(task)

        # create processes to read from the argument and from the output queues
        arg_sql_cmd = 'update arg_' + func + ' set run_state={} where run_idx={}'


        def _log_arg_to_sql(conn=self.conn):
            while True:
                arg_mssg = arg_q.get()
                sql_cmd = arg_sql_cmd.format(arg_mssg[0],arg_mssg[2])
                print sql_cmd
                conn.execute(sql_cmd)
#                conn.commit()

                print "arg q get:",arg_mssg

        def _log_out_to_sql():
            while True:
                print "out q get:", out_q.get()
        def _autocommit(conn=self.conn):
            conn.commit()
            time.sleep(0.1)

        log_arg_thread = multiprocessing.Process(target=_log_arg_to_sql)
        log_arg_thread.daemon = True
        log_out_thread = multiprocessing.Process(target=_log_arg_to_sql)
        log_out_thread.daemon = True
        commit_thread = multiprocessing.Process(target=_log_arg_to_sql)
        commit_thread.daemon = True

        log_arg_thread.start()
        log_out_thread.start()
        commit_thread.start()

        # while True:
        #     print "arg_q.get():", arg_q.get()


        # wait for all tasks to complete, report error messages that were not caught in pool
        [task.get() for task in tasks]

        #for i in range(100):
        #    print arg_q.get()
#        workers = pool.apply_async(_thread_proxie, ([1,2,3],[4,5,6]))

#        proc_res = pool.apply_async(_thread_proxie,[(1,1),(2,2)])
#        proc_res.get()
#       pool.close()
#        pool.join()

#        out_vals = [eval(task) for task in tasks]
        # update the arguments table
#        print sql_cmd
#        sql_cmd = 'update arg_' + func + ' set run_state={},run_message=\'success\' where run_idx={}'.format(1, 0)
#        self.conn.execute(sql_cmd)
#        self.conn.commit()



def _thread_proxie(func,arg_set,arg_q,out_q,out_types):
    try:
        task = func + "(" + ", ".join(["{}" for _ in arg_set[1:]]) +")"
        task = task.format(*arg_set[1:])
        outs = eval(task)
        # update the argument table with the success message
        arg_q.put((1,'success',arg_set[0]))
        # update the results table with the results

    except Exception as e:
            # update the argument table with the error message
            arg_q.put(0,str(e),arg_set[0])

class Bucket_proxie:

    # bucket should receive the run number (arg_set number)
    # should have two queues (arg_queue + out_queue)
    # should handle commits to both queues at the same time safely (it can only receive clean data from the proxie)

    def __init__(self, conn, func, arg_types, out_types, commit_freq=0.5):

        self._should_stop = False
        self.conn = conn
        self.func = func
        self.commit_freq = commit_freq


        #self.arg_q = multiprocessing.Queue()
        #self.out_q = multiprocessing.Queue()
        # todo: create a queue and dequeue everything from the bucket

#        self.tr = threading.Thread(target=self._flush)
#        self.tr.start()


    def request_stop(self):
        self._should_stop = True

    # start dropping data to the database with a background thread
    # def _flush(self):
    #     while not self._should_stop:
    #         time.sleep(self.commit_freq)
    #         # logging.info('autocommit')
    #
    #         # self.conn.execute(stmt)
    #         # self.conn.commit()
    #         print "flushing arguments:", [arg_set for arg_set in self.arg_q]
    #         self.arg_q = []
    #         print "flushing outputs:", [out_set for out_set in self.out_q]
    #         self.out_q = []

        #print arg_sets
        # initialize bucket
        #self.bucket_proxie = Bucket_proxie(self.conn,func,arg_types,out_types)
        # convert sets of argumnets into tasks to run
        # task = func + "(" + ", ".join(["{}" for _ in arg_sets[0][1:]]) +")"
        # tasks = [(arg_set[0],task.format(*arg_set[1:]),1,1) for arg_set in arg_sets]




def sumqrt(num1,num2,num3=1):
    print num1,num2
#    time.sleep(1)
    return num1+ num2


afdb = AffinityDB(db_path)

arg_ones = np.arange(10000) +7
arg_twos = np.arange(10000) + 15

afdb.run_multithread("sumqrt",arg_types=[int,int],arg_lists=[arg_ones,arg_twos],out_types=[int],out_names=['sumqrt'],num_threads=20)


