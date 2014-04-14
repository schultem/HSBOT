#return the mode of a dict
def countdict(items):
    d = {}
    max_i=0
    for i in items:
        if i in d:
            d[i] = d[i]+1
            if d[i]>max_i:
                max_i=i
        else:
            d[i] = 1
            if d[i]>max_i:
                max_i=i
    return i