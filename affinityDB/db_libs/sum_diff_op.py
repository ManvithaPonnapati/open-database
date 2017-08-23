import sys
class Sum_diff_init:
    this_module = sys.modules[__name__]
    def __init__(self):
        self.this_module.sum_diff_init = self

def sum_diff(num1,num2,init="sum_diff_init"):
    my_sum = num1 + num2
    my_diff = num1 - num2
    return [[my_sum,my_diff]]
