import sys,time

class Test_multout_init:
    this_module = sys.modules[__name__]
    def __init__(self):
        self.this_module.test_multout_init = self


def test_multout(num,init="test_multout_init"):
   if num % 3 == 0:
       time.sleep(0.0001)
       return [[0]]
   elif num % 3 == 1:
       return [[1],[1]]
   elif num % 3 == 2:
       return [[2],[2],[2]]
