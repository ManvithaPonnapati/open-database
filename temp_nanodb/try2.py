import sqlite3
import time
import os



db_path = "/home/maksym/Projects/new_data/nano.db"
os.system('rm ' + db_path)
conn = sqlite3.connect(db_path,check_same_thread=False)
cmd = 'create table sqr_sqrt (idx integer not null,sqr integer, sqrt float, msg text, primary key(idx));'
conn.execute(cmd)

for i in range(1000):
    cmd = str("insert into sqr_sqrt values ({},{},{},{});").format(i,'NULL','NULL','NULL')
    print cmd
    #time.sleep(10)
    conn.execute(cmd)

conn.commit()

i =0
while i < 100:
    i+=3

    cmd = "replace into sqr_sqrt  values ({},{},{},{});".format(i, i**2, i**0.5, '\'success\'')
    print cmd
    # time.sleep(10)
    conn.execute(cmd)

conn.commit()

# task
# insert nothing
# get and substitute nothing




conn.close()


