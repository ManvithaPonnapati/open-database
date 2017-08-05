


def sum_abc(a,b,c):
    print "sum ABC", a+b+c


print '{}_ddddd_{}'.format(1,2)

a ='print {}'.format((1,2,3))
print a
exec(a)

b = 'sum_abc{}'.format((1,2,3))
print b
exec(b)

t = [1,2,3]
c= 'sum_abc{}'.format(tuple(t))

#print tuple(t)