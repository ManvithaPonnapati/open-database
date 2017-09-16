import sys,os,sqlite3,time,imp,logging
import multiprocessing


class AffinityDB:
    python_to_sql = {int: 'integer', float: 'float', str: 'text'}
    sql_to_python = {'integer': int, 'float': float, 'text': str}
    multithread_libs_path = "/".join(os.path.realpath(__file__).split("/")[:-2]) + "/lib_multithread"

    def __init__(self,db_root,db_name):
        """
        Initialize database

        :param db_root: root dir for all the data 
        :param db_name: name of the sqlite db file
        :return:
        None
        """
        db_path = os.path.join(db_root,db_name+".db")
        self.conn = sqlite3.connect(db_path)

        # create cron table if it has not been created
        table_names = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        if "cron" not in [table_name[0] for table_name in table_names]:
            sql_cmd = "create table \"cron\"(cron_idx integer, time string, init_param string)"
            self.conn.execute(sql_cmd)
            logging.info("cron table was not in the database and was created")

    def open_table_with_queue(self,table_name,col_names,col_types,commit_sec=1):
        """ Creates an output table, and a queue to feed this table. Creates a background thread to take results
        from the queue and insert into the table.

        Example:
        <pre lang="python">
        out_q,stop_event = afdb.open_table_with_queue(table_name="some_table",col_names=["num"],col_types=[int])
        zsh
        for i in range(1000):
            out_q.put([i])
        stop_event.set()
        </pre>

        :param table_name: string (name of the table prefix out_xxx_ will be appended)
        :param col_names: list of strings (names of the columns)
        :param col_types: list of python types (column types)
        :return:
        multiprocessing queue: event to close the table and terminate thread.


        """
        time_stamp = time.strftime("%h_%y_%Y_%M_%S").lower()
        assert type(table_name)==str, "arg table_name should be a string"
        assert type(col_names)==list and type(col_names[0])==str, "arg col_names should be a list of strings"
        assert type(col_types)==list and type(col_types[0])==type, "arg col_names should be a list of types"
        assert len(col_names)==len(col_types), "mismatch between the number of column names and types"

        # write the initial state of the init function to cron
        sql_cmd = "select cron_idx from cron"
        cron_idx = len(self.conn.execute(sql_cmd).fetchall())
        sql_cmd = "insert into cron values({},\"{}\",\"{}\")".format(cron_idx+1,time_stamp,None)
        self.conn.execute(sql_cmd)
        self.conn.commit()
        out_table = "out_" + str(cron_idx).zfill(3) + "_" + table_name
        num_args = len(col_types)

        # create empty sqlite3 table for outputs
        col_types = [self.python_to_sql[col_type] for col_type in col_types]
        sql_cmd = 'create table \"' + out_table + '\" (out_idx integer not null, '
        sql_cmd += ", ".join([str(col_names[i])+" "+str(col_types[i]) for i in range(num_args)])
        sql_cmd += ", primary key(out_idx));"
        self.conn.execute(str(sql_cmd))

        # assemble the insert into the database command
        out_sql_cmd = "insert into \"" + out_table + "\" values (?,"
        out_sql_cmd += ", ".join(["?" for col_type in col_types]) + ");"
        self._out_q = multiprocessing.Queue()

        def autocommit(quit):
            out_idx = 0
            out_q_sets = []
            commit_clock = time.time()
            commit_exceptions = []
            while not quit.is_set():
                # put the results from the argument queue to the sqlite database
                while self._out_q.qsize() > 0:
                    out_q_set = self._out_q.get()
                    out_q_set = [out_idx] + out_q_set
                    out_q_sets.append(out_q_set)
                    out_idx += 1
                if time.time() - commit_clock > commit_sec:
                    try:
                        self.conn.executemany(out_sql_cmd, out_q_sets)
                    except Exception as e:
                        commit_exceptions.append(e)
                    out_q_sets = []
                    self.conn.commit()
                    commit_clock = time.time()

            # performing final actions to close table with the queue
            while self._out_q.qsize() > 0:
                out_q_set = self._out_q.get()
                out_q_set = [out_idx] + out_q_set
                out_q_sets.append(out_q_set)
                out_idx += 1
            try:
                self.conn.executemany(out_sql_cmd, out_q_sets)
            except Exception as e:
                commit_exceptions.append(e)
            # update the cron table
            self.conn.commit()
            mssg = "Number of autocommit exceptions:" + str(len(commit_exceptions)) + str(commit_exceptions)[:3000]
            logging.warning("autocommit exceptions:"+ str(len(commit_exceptions)))
            sql_cmd = "update cron set init_param=\"{}\" where cron_idx={};".format(mssg,cron_idx+1)
            self.conn.execute(sql_cmd)
            self.conn.execute(sql_cmd)
            self.conn.commit()
        close_event = multiprocessing.Event()
        multiprocessing.Process(target=autocommit,args=(close_event,)).start()
        return self._out_q,close_event

    def run_multithread(self,func,arg_sets,num_threads=10,commit_sec=1):
        """ Run any function in lib_multithread in multiple threads.
        Writes all arguments to `arg_xxx_func` table, record outputs to `out_xxx_table`. Record state of the function's
        initializer to cron table.
        If the task is interrupted in the process of execution, it is possible to resume with `AffinityDB.continue(*)`

        Example:
        <pre lang="python">
        run_multithread('download',[['10MD','3EML']])
        </pre>

        :param func: string (a name of the function to execute)
        :param arg_sets: lits of tuples (every tuple is an argument set for a single run of a function)
        :param num_threads: integer (number of independent processes)
        :param commit_sec: integer (time delay in flushing outputs to the arg_ and out_ tables)
        :return: 
        None
        """
        time_stamp = time.strftime("%h_%y_%Y_%M_%S").lower()

        # Check 1: input types
        assert type(func)==str, "name of the function should be passed as string"
        assert len(func.split("/")) == 1, "Functions should be defined in database libs and should not need prefix"
        assert (len(func.split("."))) == 1, "Functions should be defined in database libs and should not need prefix"
        assert type(arg_sets)==list, "arg_sets should be a list"

        # Check 2: Check if the function is defined correctly in multithread_ops
        lib_name = func + "_op"
        fp, path, descr = imp.find_module(lib_name, [self.multithread_libs_path])
        lib_mod = imp.load_module(lib_name, fp, path, descr)
        iref = eval("lib_mod." + func.capitalize() + "_init")
        func_ref = eval("lib_mod." + func)
        assert (set(iref.arg_types).issubset([int, float, str])), "Expected arg_types in: int,float,str."
        assert (set(iref.out_types).issubset([int, float, str])), "Expected out_types in: int,float,str."
        assert all([type(out_name) == str for out_name in iref.out_names]), "out_names should be a list of strings"
        assert len(iref.out_types) == len(iref.out_names), "Bad number of output types."
        assert len(func_ref.__defaults__) == 1, "function should have a single default arg \"init\" "
        func_args = func_ref.__code__.co_varnames[:func_ref.__code__.co_argcount]
        assert func_args[-1] == "init", "init function should have \"init\" as its last argument"
        assert type(func_ref.__defaults__[-1]) == str, "init function default should be a string"
        assert func_ref.__code__.co_argcount -1 == len(iref.arg_types), "Wrong number of arguments in init function:" \
              + str(len(iref.arg_types)) + " expected:" + str(func_ref.__code__.co_argcount -1)

        # Check3: check if the function was initialized
        init_state = str(eval("lib_mod." + func_ref.__defaults__[-1]).__dict__)

        # Check4: check the arguments requirement for the function
        assert all([type(arg_set) == tuple for arg_set in arg_sets]), "one or more args in arg_sets are not tuples"
        num_args = len(iref.arg_types)
        for arg_set in arg_sets:
            assert(len(arg_set)==num_args), "arg set has incorrect length:" + str(arg_set)
            for i in range(num_args):
                assert (type(arg_set[i]) in [str, unicode] if iref.arg_types[i] == str
                        else isinstance(arg_set[i], iref.arg_types[i])), \
                    "argument " + str(i) + " has incorrect type" + str(type(arg_set[i]))
        logging.info("parameter check for run_multithread function successfully passed")

        # write the initial state of the init function to cron
        sql_cmd = "select cron_idx from cron"
        cron_idx = len(self.conn.execute(sql_cmd).fetchall())
        sql_cmd = "insert into cron values({},\"{}\",\"{}\")".format(cron_idx+1,time_stamp,init_state)
        self.conn.execute(sql_cmd)
        self.conn.commit()

        # initialize important parameters before running
        arg_table = "arg_" + str(cron_idx).zfill(3) + "_" + func
        out_table = "out_" + str(cron_idx).zfill(3) + "_" + func
        var_names = list(func_ref.__code__.co_varnames)[:num_args]
        num_outs = len(iref.out_types)
        num_runs = len(arg_sets)

        # create empty sqlite3 table for commands
        arg_types = [self.python_to_sql[arg_type] for arg_type in iref.arg_types]
        sql_cmd = 'create table \"' + arg_table + '\" (run_idx integer not null, '
        sql_cmd += ", ".join([str(var_names[i])+" "+str(arg_types[i]) for i in range(num_args)])
        sql_cmd += ", run_state integer, run_message text, primary key(run_idx));"
        self.conn.execute(str(sql_cmd))

        # fill sqlite3 table with single commands that python threads will execute
        sql_cmd = "insert into \"" + arg_table + "\" values (?,"
        sql_cmd += ", ".join(["?" for _ in arg_types]) + ",?,?);"
        arg_sets = [(i,) + arg_sets[i] + (None,None,) for i in range(num_runs)]
        self.conn.executemany(sql_cmd,arg_sets)

        # create empty sqlite3 table for the outputs
        out_types = [self.python_to_sql[out_type] for out_type in iref.out_types]
        sql_cmd = 'create table \"' + out_table + '\" (out_idx integer not null, run_idx integer not null, '
        sql_cmd += ", ".join([str(iref.out_names[i])+" "+str(out_types[i]) for i in range(num_outs)])
        sql_cmd += ", primary key(out_idx));"
        self.conn.execute(str(sql_cmd))
        # run a regular continue command with the threads
        self.coninue(arg_table,num_threads=num_threads,commit_sec=commit_sec)


    def coninue(self,arg_table,num_threads,commit_sec):
        """ Continue the interrupted run_multithread function.

        Example:
        <pre lang="python">
        continue('arg_000_download_pdb',100,60)
        </pre>

        :param arg_table: string (name of the sqlite table with arguments of the function to run)
        :param num_threads: integer (number of processes)
        :param commit_sec: integer (write outputs to the database every number of tasks)
        :return: 
        None
        """
        # get constant hardwired parameters
        func = arg_table[8:] # function name starts after 8th letter
        out_table = "out_" + arg_table[4:]
        # import the corresponding to the function module
        lib_name = func + "_op"
        fp, path, descr = imp.find_module(lib_name, [self.multithread_libs_path])
        lib_mod = imp.load_module(lib_name, fp, path, descr)
        func_ref = eval("lib_mod." + func)

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
        thrs = [pool.apply_async(_thread_proxie,args=(func_ref,task_q,arg_q,out_q,out_types,i)) for i in range(num_threads)]

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


def _thread_proxie(func_ref,task_q,arg_q,out_q,out_types,thr_i):
    """
    Runs a function func with the set of arguments `arg_set`. Checks is the output of the function is a nested list.
    Checks if every example in the nested list is has type `out_types`. Sends status updates of tasks to the `arg_q`,
    sends output updates of the task to the `out_q`.

    :param func: string (a name of the function to run)
    :param arg_set: list (set of arguments)
    :param arg_q: multiprocessing.Queue() (which to send task status updates to)
    :param out_q: multiprocessing.Queue() (which to send outputs to)
    :param out_types: list of [int,float,string] (expected kinds of outputs from the function)
    :return: None
    """
    func = func_ref
    while task_q.qsize() > thr_i*2:
        arg_set = task_q.get()
        try:
            arg_types = [type(arg) for arg in arg_set]
            num_out = len(out_types)
            task = "func(" + ", ".join(
                ["\"{}\"" if arg_type in [type(u'str'), type('str')] else "{}" for arg_type in arg_types[1:]]) + ")"
            task = task.format(*arg_set[1:])
            outss = eval(task)
            assert type(outss) == list, "list of outputs is expected"
            assert all([type(outs) == list for outs in outss]), "list of lists of outputs expected"
            assert len(outss) > 0, "function returned 0 output sets"
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
