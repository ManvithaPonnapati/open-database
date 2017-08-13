import os,sqlite3,time

db_path = "/home/maksym/Projects/new_data/nano.db"
num_iters = 10000
os.remove(db_path)

#conn.execute('PRAGMA synchronous=OFF')
#sql_cmd = "create table random_name (num1 integer not null, num2 integer, primary_key(num1))"
#sql_tmp = "insert into random_name values ({},{})"


conn = sqlite3.connect(db_path)
# make a list of tuples
conn.execute("create table random_name (num1 integer, num2 integer, primary key(num1));")
start = time.time()
t_list = [(i,i+99) for i in range(num_iters)]
sql_tmp ="insert into random_name values " + ", ".join(["{}" for _ in range(num_iters)])
sql_cmd = sql_tmp.format(*t_list)
conn.execute(sql_cmd)
conn.commit()
print "time:", time.time() - start

os.remove(db_path)
conn = sqlite3.connect(db_path)
conn.execute("create table random_name (num1 integer, num2 integer, primary key(num1));")
start = time.time()
for i in range(num_iters):
    sql_cmd = "insert into random_name values ({},{})".format(i,i+99)
    conn.execute(sql_cmd)
conn.commit()
print "time:", time.time() - start


#c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
os.remove(db_path)
conn = sqlite3.connect(db_path)
conn.execute("create table random_name (num1 integer, num2 integer, primary key(num1));")
start = time.time()

t_list = [(i,i+99) for i in range(num_iters)]
conn.executemany("insert into random_name values (?,?)",t_list)
conn.commit()
print "time:", time.time() - start

# ------------------------------------- updaters -------------------------------------------------------

os.remove(db_path)
conn = sqlite3.connect(db_path)
conn.execute("create table random_name (num1 integer, num2 integer, primary key(num1));")
t_list = [(i,i+99) for i in range(num_iters)]
conn.executemany("insert into random_name values (?,?)",t_list)
conn.commit()
start = time.time()

t_list = [i for i in range(num_iters)]
sql_cmd = "alter table random_name add column num3"
conn.execute(sql_cmd)
for i in range(num_iters):
    sql_cmd = "update random_name set num3={} where num1={}".format(i+999,i)
    conn.execute(sql_cmd)
conn.commit()
print "time:", time.time() - start




# os.remove(db_path)
# conn = sqlite3.connect(db_path)
# conn.execute("create table random_name (num1 integer, num2 integer, primary key(num1));")
# t_list = [(i,i+99) for i in range(num_iters)]
# conn.executemany("insert into random_name values (?,?)",t_list)
# conn.commit()
# start = time.time()
#
# t_list = [i for i in range(num_iters)]
# sql_cmd = "alter table random_name add column num3"
# conn.execute(sql_cmd)
#
#     sql_cmd = "update random_name set num3={}".format(i)
#     conn.execute(sql_cmd)
# conn.commit()
# print "time:", time.time() - start