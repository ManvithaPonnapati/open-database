

def sum_diff(num1,num2,num3=1):
    my_sum = num1 + num2
    my_diff = num1 - num2
    return [[my_sum,my_diff]]


def multi_out(num):
   if num % 3 == 0:
       return [[0]]
   elif num % 3 == 1:
       return [[1],[1]]
   elif num % 3 == 2:
       return [[2],[2],[2]]
