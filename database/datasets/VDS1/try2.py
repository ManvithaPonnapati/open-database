import sys

# this is a pointer to the module object instance itself.



class Init_download:
    this_module = sys.modules[__name__]
    def __init__(self,val):
        self.val = val
        self.this_module.init_download = self
        print "initialized init download"

def download(init="init_download"):
    init = eval(init)
    print init.val


#def download(variable):

#print sys.modules[__name__]

#Init_download(10)
#ownload(10)
#print this_module.a
# simpler idea  - call init; and give init
# harder idea - call injit, and it will
# third idea - call the init from the function itself - not safe with multithread