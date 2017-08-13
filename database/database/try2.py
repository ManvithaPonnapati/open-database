import sqlite3,os,time
import numpy as np

some_list = ["a","fdfdf","g"]
print np.asarray(some_list)





# interval = 1
# commit_clock = time.time()
#
# while True:
#     if time.time() - commit_clock > interval:
#         print " every 1 second"
#         commit_clock = time.time()

# db_path = "/home/maksym/Projects/new_data/nano.db"
# num_iters = 10000
# conn = sqlite3.connect(db_path)
#
#
#
#
# cursor = conn.cursor()
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# downs_table,ups_table = cursor.fetchall()
# downs_table = downs_table[0]
# ups_table = ups_table[0]
#
# #sql_cmd = "alter table \"{}\" add column num7".format(ups_table)
# #cursor.execute(sql_cmd)
#
# sql_tmp = "update \"{}\"".format(ups_table) + " set num7={} where out_idx={}"
#
#
# start =time.time()
# for i in range(num_iters):
#     sql_cmd = sql_tmp.format(i+99,i)
#     conn.execute(sql_cmd)
# conn.commit()
# print "time:", time.time() - start
#
#
# sql_tmp = "update \"{}\"".format(ups_table) + " set num7=? where out_idx=?"
# arg_list = [(i+99,i) for i in range(10000)]
#
# start = time.time()
# conn.executemany(sql_tmp,arg_list)
# conn.commit()
# print "time:", time.time() - start