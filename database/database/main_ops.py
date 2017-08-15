import sys,os,sqlite3,time
import multiprocessing
sys.path.append('../')
from dataset_libs import EXMPL1
from dataset_libs import VDS1
from dataset_libs import NEW


class AffinityDB:
    python_to_sql = {int: 'integer', float: 'float', str: 'string'}
    sql_to_python = {'integer': int, 'float': float, 'string': str}

    def __init__(self,db_path):
        self.conn = sqlite3.connect(db_path)

    def run_multithread(self,func,arg_types,arg_lists,out_types,out_names,num_threads=10,commit_sec=1):
        """ Given set of tasks (any function in python) , breaks the tasks between a given number of processes
        to execute. Writes inputs into arg_ sqlite table and outputs into _out sqlite table.

        Important:
        Function should take a single set of arguments IE: find_roots(a_x2,b_x,c)
        and output 1/many sets of outputs as a nested list: IE: [[-0.5]] for find_root(0,6,3),
        [[-5][5]] for find_root(25,0,0)

        If the task is interrupted in the process of execution, it is possible to resume with AffinityDB.continue(*)

        :param func: string (a name of the function to execute)
        :param arg_types: list of [int,float,str] (python argument types)
        :param arg_lists: nested list: ([arg1,arg1,arg1],[arg2,arg2,arg2],[arg3,arg3,arg3]])
        :param out_types: list of [int,float,str]
        :param out_names: list of strings (what are the names of the outputs of the function)
        :param num_threads: integer number (number of independent processes)
        :return: None
        """
        time_stamp = time.strftime("%h_%y_%Y_%M_%S").lower()
        arg_table = time_stamp + "_arg_" + func
        out_table = time_stamp + "_out_" + func
        assert type(arg_lists)==list, "list of inputs is expected"
        assert all([type(arg_list)==list for arg_list in arg_lists]),"list of lists of inputs is expected"
        assert(set(arg_types).issubset([int,float,str])), "Expected keywords: int,float,str."
        assert len(arg_types)==len(arg_lists), "Bad number of argument types." + str(len(arg_types))
        assert len(out_types)==len(out_names), "Bad number of output types."
        assert all([len(arg_list) == len(arg_lists[0]) for arg_list in arg_lists]), \
            "List of arguments should be all of the same length."
        for i in range(len(arg_types)):
            assert all([isinstance(arg,arg_types[i]) for arg in arg_lists[i]]),"Incorrect type in arg_list" + str(i)
        if eval(func).__defaults__ is not None:
            req_args = eval(func).__code__.co_argcount - len(eval(func).__defaults__)
        else:
            req_args = eval(func).__code__.co_argcount
        assert req_args >= len(arg_types), "missing arguments" + str(req_args) + "found:" + str(len(arg_types))


        num_args = len(arg_types)
        var_names = list(eval(func).__code__.co_varnames)[:num_args]
        num_outs = len(out_types)
        num_runs = len(arg_lists[0])

        # create empty sqlite3 table for commands
        arg_types = [self.python_to_sql[arg_type] for arg_type in arg_types]
        sql_cmd = 'create table \"' + arg_table + '\" (run_idx integer not null, '
        sql_cmd += ", ".join([str(var_names[i])+" "+str(arg_types[i]) for i in range(num_args)])
        sql_cmd += ", run_state integer, run_message text, primary key(run_idx));"
        self.conn.execute(str(sql_cmd))

        # fill sqlite3 table with single commands that python threads will execute
        sql_cmd = "insert into \"" + arg_table + "\" values (?,"
        sql_cmd += ", ".join(["?" for arg_type in arg_types]) + ",?,?);"
        arg_lists = [range(num_runs)] + arg_lists  # one column is used for run_index
        arg_sets = [list(x) + [None] + [None] for x in zip(*arg_lists)]
        self.conn.executemany(sql_cmd,arg_sets)

        # create empty sqlite3 table for the outputs
        out_types = [self.python_to_sql[out_type] for out_type in out_types]
        sql_cmd = 'create table \"' + out_table + '\" (out_idx integer not null, run_idx integer not null, '
        sql_cmd += ", ".join([str(out_names[i])+" "+str(out_types[i]) for i in range(num_outs)])
        sql_cmd += ", primary key(out_idx));"
        self.conn.execute(str(sql_cmd))
        # run a regular continue command with the threads
        self.coninue(arg_table,num_threads=num_threads,commit_sec=commit_sec)


    def coninue(self,arg_table,num_threads,commit_sec):
        """ Continue the interrupted run_multithread function.
        :param arg_table: string (name of the sqlite table with arguments of the function to run)
        :param num_threads: integer (number of processes)
        :param commit_freq: integer (write outputs to the database every number of tasks - has a dramatic effect on
        speed)
        :return: None
        """
        # get constant hardwired parameters
        time_stamp = arg_table[:17] # first 17 symbols are the time stamp
        func = arg_table[22:] # function name starts after 17 + 5 letters
        out_table = time_stamp + "_out_" + func

        # retrieve all sets of parameters to run function with
        cursor = self.conn.cursor()
        sql_cmd = 'pragma table_info(\"{}\")'.format(arg_table)
        cursor.execute(sql_cmd)
        arg_infos = cursor.fetchall()
        arg_names = [str(arg_info[1]) for arg_info in arg_infos][:-2]
        sql_cmd = 'select ' + " ,".join(arg_names) + ' from \"' + arg_table + '\" where run_state is NULL;'
        cursor.execute(sql_cmd)
        arg_sets = cursor.fetchall()
        num_tasks = len(arg_sets)

        # retrieve the information about the output data types of the function
        sql_cmd = 'pragma table_info(\"{}\")'.format(out_table)
        cursor.execute(sql_cmd)
        out_infos = cursor.fetchall()
        out_types = ([str(out_info[2]) for out_info in out_infos[2:]])
        out_types = [AffinityDB.sql_to_python[out_type] for out_type in out_types]

        # run tasks with the multiprocessing pool (on the background)
        pool = multiprocessing.Pool(num_threads)
        m = multiprocessing.Manager()
        task_q = m.Queue()
        arg_q = m.Queue()
        out_q = m.Queue()
        [task_q.put(arg_set) for arg_set in arg_sets]
        thrs = [pool.apply_async(_thread_proxie,args=(func,task_q,arg_q,out_q,out_types,i)) for i in range(num_threads)]

        # collect the results from the processes in the main thread
        arg_sql_cmd = 'update \"' + arg_table + '\" set run_state=?, run_message=? where run_idx=?'
        out_sql_cmd = "insert into \"" + out_table + "\" values (?,?,"
        out_sql_cmd += ", ".join(["?" for out_type in out_types]) + ");"

        out_idx = 0
        arg_q_sets = []
        out_q_sets = []
        commit_clock = time.time()
        for i in range(num_tasks):
            # put the results from the argument queue to the sqlite database
            arg_q_set = arg_q.get()
            arg_q_sets.append(arg_q_set)
            # put the results from the outputs queue to the database
            while out_q.qsize() > 0:
                out_q_set = out_q.get()
                out_q_set = [out_idx] + out_q_set
                out_q_sets.append(out_q_set)
                out_idx+=1
            if time.time() - commit_clock > commit_sec:
                self.conn.executemany(arg_sql_cmd,arg_q_sets)
                self.conn.executemany(out_sql_cmd,out_q_sets)
                out_q_sets = []
                arg_q_sets = []
                self.conn.commit()
                commit_clock = time.time()

        # wait for all tasks to complete, report error messages caught by pool threads
        [thr.get() for thr in thrs]
        self.conn.executemany(arg_sql_cmd, arg_q_sets)
        self.conn.executemany(out_sql_cmd, out_q_sets)
        self.conn.commit()


def _thread_proxie(func,task_q,arg_q,out_q,out_types,thr_i):
    """
    Runs a function func with the set of arguments arg_set. Checks is the output of the function is a nested list.
    Checks if every example in the nested list is has type out_types. Sends status updates of tasks to the arg_q,
    sends output updates of the task to the out_q.

    :param func: string (a name of the function to run)
    :param arg_set: list (set of arguments)
    :param arg_q: multiprocessing.Queue() (which to send task status updates to)
    :param out_q: multiprocessing.Queue() (which to send outputs to)
    :param out_types: list of [int,flaot,string] (expected kinds of outputs from the function)
    :return:
    """
    while task_q.qsize() > thr_i*2:
        arg_set = task_q.get()
        try:
            arg_types = [type(arg) for arg in arg_set]
            num_out = len(out_types)
            task = func + "(" + ", ".join(
                ["\"{}\"" if arg_type == unicode else "{}" for arg_type in arg_types[1:]]) + ")"
            task = task.format(*arg_set[1:])
            outss = eval(task)

            assert type(outss) == list, "list of outputs is expected"
            assert all([type(outs) == list for outs in outss]), "list of lists of outputs expected"
            for outs in outss:
                assert len(outs) == len(out_types), "incorrect number of outputs:" + str(len(outs))
                got_out_types = [type(outs[i]) for i in range(num_out)]
                assert all([got_out_types[i] == out_types[i]]), "incorrect outputs type:" + str(got_out_types)

            # update the argument table with the success message
            arg_q.put([1, 'success', arg_set[0]])
            # update the results table with the results
            for outs in outss:
                out_q.put([arg_set[0]] + outs)
        except Exception as e:
            # update the argument table with the error message
            arg_q.put([0, str(e), arg_set[0]])

