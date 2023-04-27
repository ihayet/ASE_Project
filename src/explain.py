from utils import value, rnd, get_ofile
from lists import kap, map
from bins import bins
from strings import o, oo

def xpln(data, best, rest):
    def v(has):
        return value(has, len(best.rows), len(rest.rows), "best")

    def score(ranges):
        rule = RULE(ranges, maxSizes)
        oo(showRule(rule))

        if rule:
            bestr = selects(rule, best.rows)
            restr = selects(rule, rest.rows)

            if len(bestr) + len(restr) > 0:
                return v({"best": len(bestr), "rest": len(restr)}), rule

    tmp, maxSizes = [], {}
    for ranges in bins(data.cols.xcols, {"best": best.rows, "rest": rest.rows}):
        maxSizes[ranges[0]['txt']] = len(ranges)
        print('')
        get_ofile().write('\n')
        for range in ranges:
            print(range['txt'], range['lo'], range['hi'])
            get_ofile().write(str(range['txt']) + ' ' + str(range['lo']) + ' ' + str(range['hi']) + '\n')
            tmp.append({"range": range, "max": len(ranges), "val": v(range['y'].has)})
    
    rule, most = firstN(sorted(tmp, key=lambda x: x["val"], reverse=True), score)
    return rule, most

def firstN(sortedRanges, scoreFun):
    def useful(range):
        if range['val'] > 0.05 and range['val'] > first / 10:
            return range
    print('')
    get_ofile().write('\n')
    for r in sortedRanges:
        print(r['range']['txt'], r['range']['lo'], r['range']['hi'], rnd(r['val']), o(r['range']['y'].has))
        get_ofile().write(str(r['range']['txt']) + ' ' + str(r['range']['lo']) + ' ' + str(r['range']['hi']) + ' ' + str(rnd(r['val'])) + o(r['range']['y'].has) + '\n')
    first = sortedRanges[0]['val']
    sortedRanges = list(filter(useful, sortedRanges))
    most, out = -1, None

    def fun(r):
        return r['range'], None
    
    print()
    get_ofile().write('\n')
    for n in range(1, len(sortedRanges) + 1):
        tempList = list(map(sortedRanges[:n], fun))
        tmp, rule = scoreFun(tempList)
        if tmp and tmp > most:
            out, most = rule, tmp
    return out, most

def showRule(rule):
    def pretty(range):
        if range['lo'] == range['hi']:
            return range['lo'], None
        else:
            return [range['lo'], range['hi']], None
    
    def merges(attr, ranges):
        return map(merge(sorted(ranges, key=lambda x: x["lo"])), pretty), attr
    
    def merge(t0):
        t, j = [], 0
        while j < len(t0):
            left, right = t0[j], t0[j + 1] if j + 1 < len(t0) else None
            if right and left["hi"] == right["lo"]:
                left["hi"] = right["hi"]
                j += 1
            t.append({"lo": left["lo"], "hi": left["hi"]})
            j += 1
        return t if len(t0) == len(t) else merge(t)
    
    return kap(rule, merges)

def selects(rule, rows):
    def disjunction(ranges, row):
        for range in ranges:
            lo, hi, at = range["lo"], range["hi"], range["at"]
            x = row.cells[at]
            
            if x == "?":
                return True
            if lo == hi and lo == x:
                return True
            if lo <= x and x < hi:
                return True
        return False

    def conjunction(row):
        for _, ranges in rule.items():
            if not disjunction(ranges, row):
                return False
        return True
    
    def fun(r):
        if conjunction(r):
            return r, None
        else:
            return None, None

    tmpRows = [row for row in map(rows, fun) if row is not None]

    return map(tmpRows, fun)

def prune(rule, maxSize):
    n = 0
    for txt in list(rule):
        n += 1
        if len(rule[txt]) == maxSize[txt]:
            n += 1
            rule.pop(txt, None)
    if n > 0:
        return rule

def RULE(ranges, maxSize):
    t = {}
    for range in ranges:
        if range['txt'] not in t:
            t[range['txt']] = []
        t[range['txt']].append({"lo": range['lo'], "hi": range['hi'], "at": range['at']})
    
    return t

