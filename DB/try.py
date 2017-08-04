import threading
import time

def printfunc():
    for i in range(210000000):
        print i
        time.sleep(0.1)



tr = threading.Thread(target=printfunc)
tr.daemon= True
tr.start()

print "all done !!!!!!!!!!!"