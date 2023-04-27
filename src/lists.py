from collections import OrderedDict
from ROW import ROW

def map(t, fun):
    temp = {}
    tempList = []
    if isinstance(t, dict):
        for k, v in t.items():
            v, k = fun(v)
                        
            if k is not None: temp[k] = v
            else: tempList.append(v)
    elif isinstance(t, list):
        for k, v in enumerate(t):
            v, k = fun(v)
            
            if k is not None: tempList[k] = v
            else: tempList.append(v)
    return temp if len(temp) > 0 else tempList

def kap(t, fun):
    if isinstance(t, dict):
        temp = {}
        for k, v in t.items():
            v, k = fun(k, v)
            temp[k if k is not None else len(temp.keys())] = v
    elif isinstance(t, list):
        temp = [None] * len(t)
        for k, v in enumerate(t):
            v, k = fun(k, v)
            temp[k if k is not None else len(temp)] = v
    return temp

def sort(t, k):
    if isinstance(t, dict):
        t = sorted(t.items(), key=lambda x: x[1][k])
    else:
        t = sorted(t, key=lambda x: x[k])
    return t

def keys(t):
    ks = t.keys()
    ks.sort()
    return ks