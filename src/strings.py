from collections import OrderedDict
from utils import get_ofile, last, rnd
from lists import sort, map, kap
import re

def fmt(sControl, *args):
    ret = ''
    i, x, counter = 0, 0, 0
    rangeArr = range(len(sControl))
    
    while x < len(sControl) - 1:
        i = rangeArr[x]
        i2 = rangeArr[x+1]

        if sControl[i] == '%':
            if sControl[i2] == 'o':
                ret += str(oct(args[counter]))
                x += 1
            elif sControl[i2] == 'x':
                ret += str(hex(args[counter]))
                x += 1
            elif sControl[i2] == 'X':
                ret += str(hex(args[counter]).upper())
                x += 1
            else:
                ret += str(args[counter])
                x += 1
            counter += 1
        else:
            ret += str(sControl[i])
        x += 1
    
    if x < len(sControl):
        ret += sControl[rangeArr[x]]
    return ret

def oo(options):
    val = o(options)
    o_file = get_ofile()
    o_file.write(str(val) + '\n')
    print(val)
    return options

def o(options):
    if isinstance(options, dict):
        ks = list(options.keys())
        ks.sort()
        val = '{'
        for i, k in enumerate(ks):
            val += ':'
            val += str(k)
            val += ' ' + str(options[k]).lower()
            if i < len(ks)-1:
                val += ' '
        val += '}'        
    elif isinstance(options, list):
        val = '{'
        for i, k in enumerate(options):
            val += str(k)
            if i < len(options)-1:
                val += ' '
        val += '}'
    else:
        val = str(options)

    return val

def coerce(s):
    def fun(s1):
        if s1 == "true":
            return True
        elif s1 == "false":
            return False
        return s1
    
    val = None

    try:
        val = float(s) if ('.' in s) else int(s)
    except TypeError as te:
        val = fun(s)
    except ValueError as ve:
        val = fun(s.strip())

    return val

def show(node, what=None, cols=None, nPlaces=None, lvl=None):
  o_file = get_ofile()
  if node:
    lvl = lvl or 0
    
    pval = fmt("%s[%s]", str('|.. '*lvl), str(len(node['data'].rows)))
    print(pval, end='')
    o_file.write(pval)
    
    pval = o(node['data'].stats()) if ('left' not in node) else ''
    print(pval)
    o_file.write(pval + '\n')

    if 'left' in node:
        show(node['left'], what, cols, nPlaces, lvl+1)
    if 'right' in node:
        show(node['right'], what, cols, nPlaces, lvl+1)