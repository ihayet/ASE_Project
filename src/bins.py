from SYM import SYM
from lists import map, sort
from utils import getThe, copy
from strings import o
import math

def RANGE(_at, _txt, _lo, _hi=None):
    return {'at':_at, 'txt':_txt, 'lo':_lo, 'hi':_hi or _lo, 'y':SYM()}

def extend(range, n, s):
    range['lo'] = min(n, range['lo'])
    range['hi'] = max(n, range['hi'])
    range['y'].add(s)

def bins(cols, rowss):
    def itself(x): return x, None

    out = []
    for col in cols:
        ranges = {}
        for y, rows in rowss.items():
            for row in rows:
                x = row.cells[col.get_pos()]
                if x != '?':
                    k = int(bin(col, x))
                    ranges[k] = ranges[k] if k in ranges else RANGE(col.get_pos(), col.get_name(), x)
                    extend(ranges[k], x, y)

        ranges = sort(map(ranges, itself), 'lo')

        out.append(ranges if isinstance(col, SYM) else mergeAny(col, ranges))
    
    return out

def bin(col, x):
    if x=='?' or isinstance(col, SYM): 
        return x
    tmp = (col.hi - col.lo)/(getThe()['bins'] - 1)
    return 1 if col.hi == col.lo else math.floor(x/tmp + 0.5)*tmp

def mergeAny(col, ranges0):
    def noGaps(t):
        for j in range(1, len(t)):
            t[j]['lo'] = t[j-1]['hi']

        if(len(t) > 1):
            t[0]['lo'] = -math.inf
            t[len(t)-1]['hi'] = math.inf

        return t

    ranges1, j = [], 0
    while j < len(ranges0):
        left, right = ranges0[j], ranges0[j+1] if j+1<len(ranges0) else None
        if right:
            y = merge2(left['y'], right['y'])
            if y:
                j += 1
                left['hi'], left['y'] = right['hi'], y
        if left: ranges1.append(left)
        j += 1

    if len(ranges0)==len(ranges1):
        return noGaps(ranges0) 
    else:
        return mergeAny(col, ranges1)

def merge2(col1, col2):
    new = merge(col1, col2)

    val1 = new.div()*new.total
    val2 = col1.div()*col1.total + col2.div()*col2.total

    if val1 <= val2:
        return new

def merge(col1, col2):
    new = copy(col1)

    if isinstance(col1, SYM):
        for n in col2.has: 
            new.add(n)
    else:
        for n in col2.has:
            new.add(n)
        new.lo = min(col1.lo, col2.lo)
        new.hi = max(col1.hi, col2.hi)
    return new