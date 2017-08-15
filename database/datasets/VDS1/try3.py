import try2


#module_names = ["os,sys"]
#modules = map(__import__, module_names)
#print modules


os = __import__("os")

print os.path
# try2.a = 1
# try2.b =10
# try2.sum_function()

#print try2
#foo = "try2"
#exec(foo + " = '__import__(foo)'")
#print bar
#print bar
#something else
#ome_name = "lol"
#exec(some_name + "= '")

# = __import__(some_name)

try2.Init_download(10)
try2.download()

# this works like charm, but I need a way to check that the function was initialized

print try2.download.__code__.co_varnames
init = try2.download.__defaults__[0]
try:
    getattr(try2,"lol")
except AttributeError as e:
    print "it looks like the function needs an initializer, but it was not initialized\n",e

