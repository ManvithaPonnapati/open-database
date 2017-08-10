

def sum_diff(num1,num2,num3=1):
    my_sum = num1 + num2
    my_diff = num1 - num2
    return [[my_sum,my_diff]]

def string_test(num):
   some_string = "ABCDEEFGHK"
   one_ten = num %10
   return [[some_string[:one_ten]]]


def strings_test(string):
   some_string = "ABCDEEFGHK"
   #one_ten = num %10
   return [[some_string + string]]
