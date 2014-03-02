#Search input x for examples of 4-tuples of ints or 2-lists of ints
#Then perform function f on them and return x.
#x can be a dict,tuple,or list
def convert(x,f):
    if isinstance(x,list):
        if len(x) == 2:
            if isinstance(x[0],int) and isinstance(x[1],int):
                x = f(x)
            else:
               pass
        if len(x) != 0:
            for i in xrange(0,len(x)):
                x[i] = coord_pair_convert(x[i],f)

    if isinstance(x,tuple):
        if len(x) == 4:
            if isinstance(x[0],int) and isinstance(x[1],int) and isinstance(x[2],int) and isinstance(x[3],int):
                x = f(x)
            else:
               pass

    if isinstance(x,dict):
        if len(x) != 0:
            for i in xrange(0,len(x)):
                x[i] = coord_pair_convert(x[i],f)

    return x
