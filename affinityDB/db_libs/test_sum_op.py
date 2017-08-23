import sys
class Test_sum_init:
    this_module = sys.modules[__name__]
    def __init__(self):
        self.this_module.test_sum_init = self

def test_sum(num1,num2,init="test_sum_init"):
    my_sum = num1 + num2
    my_diff = num1 - num2
    return [[my_sum,my_diff]]
