from re import S
from SYM import SYM
from NUM import NUM
from strings import o, oo, show, fmt
from lists import map
from utils import many, getThe, setThe, cliffsDelta, diffs, rand, rint, rnd, setSeed, get_ofile, copy, last, has, value
from repgrid import repcols, reprows, repplace, repgrid
from explain import xpln, showRule, selects
from mycsv import csv
from DATA import DATA
from bins import bins
from mystatistics import RX, bootstrap, gaussian, tiles, scottKnot
import numpy as np

def settings_test():
    err = 0
    val = oo(getThe())
    err += 1 if val != '{:Far 0.95 :Sample 512 :dump false :file etc/data/auto93.csv :go all :help false :min 0.5 :p 2 :seed 937162211}' else 0
    return 0

def rand_test():
    err = 0
    
    r1, r2 = [], []
    setSeed(1)
    for i in range(10000): r1.append(rint(100, 0))
    setSeed(1)
    for i in range(10000): r2.append(rint(100, 0))

    for (i, v) in enumerate(r1): assert(v == r2[i])

    return err

def sym_test():
    err, sym = 0, SYM()
    for c in ["a","a","a","a","b","b","c"]:
        sym.add(c)
    
    print(sym.mid(), rnd(sym.div()))

    if sym.mid() != "a":
        err += 1
    if sym.div() > (1.379 + 0.001) or sym.div() < (1.379 - 0.001):
        err += 1
    return err

def num_test():
    n = NUM()
    for i in range(0, 10):
        n.add(i)
    print('', n.total, n.mid(), n.div())
    
    return 0

def csv_test():
    err, n = 0, 0
    t = csv(getThe()['file'])

    for i in range(len(t)):
        for j in range(len(t[i])):
            n += 1
    if n != 8*399:
        err += 1
    return err

def data_test():
    err = 0
    
    data = DATA(getThe()['file'])
    col = data.cols.ycols[0]
    print(col.lo, col.hi, col.mid(), col.div())
    oo(data.stats())

    return err

def stats_test():
    err = 0
    res = ''
    data = DATA(getThe()['file'], None, None)
    for k, cols in zip(['y', 'x'], [data.cols.ycols, data.cols.xcols]):
        res += k + ' mid ' + o(data.stats('mid', cols, 2)) + '\n'
        res += ' ' + ' div ' + o(data.stats('div', cols, 2))
        if k != 'x': res += '\n'
    print(res)
    get_ofile().write(res + '\n')
    err += 1 if res != 'y mid {:Acc+ 15.57 :Lbs- 2970.42 :Mpg+ 23.84}\n  div {:Acc+ 2.76 :Lbs- 846.84 :Mpg+ 8.34}\nx mid {:Clndrs 5.45 :Model 76.01 :Volume 193.43 :origin 1}\n  div {:Clndrs 1.7 :Model 3.7 :Volume 104.27 :origin 1.3273558482394003}' else 0
    return err

def clone_test():
    err = 0
    
    data1 = DATA(getThe()['file'])
    data2 = data1.clone(data1.rows)
    oo(data1.stats())
    oo(data2.stats())

    return err

def around_test():
    err = 0
    o_file = get_ofile()
    data = DATA(getThe()['file'], None, None)
    
    around_dict = data.around(data.rows[0], None)
    
    pval = str(0) + ' ' + str(0) + ' ' + o(data.rows[0].cells)
    print(pval)
    o_file.write(pval + '\n')

    for n, (r, t) in enumerate(around_dict.items()):
        if n>0 and (n+1)%50==0:
            pval = str(n+1) + ' ' + str(rnd(t['dist'], 2)) + ' ' +  str(o(t['row'].cells))
            print(pval)
            o_file.write(pval + '\n')

    return err

def half_test():
    err = 0
    o_file = get_ofile()

    data = DATA(getThe()['file'], None, None)
    left, right, A, B, mid, c = data.half(None, None, None)
    
    print(len(left), len(right))
    l, r = data.clone(left), data.clone(right)
    print('l', o(l.stats()))
    print('r', o(r.stats()))

    return err

def cluster_test():  
    err = 0

    data = DATA(getThe()['file'])
    show(data.cluster(), 'mid', data.cols.ycols, 1, None)

    return err

def optimize_test():
    err = 0

    data = DATA(getThe()['file'])
    best, rest, evals = data.sway()

    print('\nall\t', o(data.stats()))
    get_ofile().write('\nall    \t' + o(data.stats()) + '\n')

    print('   \t', o(data.stats(_what='div')))
    get_ofile().write('       \t' + o(data.stats(_what='div')) + '\n')

    print('\nbest\t', o(best.stats()))
    get_ofile().write('\nbest\t' + o(best.stats()) + '\n')

    print('    \t', o(best.stats(_what='div')))
    get_ofile().write('    \t' + o(best.stats(_what='div')) + '\n')

    print('\nrest\t', o(rest.stats()))
    get_ofile().write('\nrest\t' + o(rest.stats()) + '\n')

    print('    \t', o(rest.stats(_what='div')))
    get_ofile().write('    \t' + o(rest.stats(_what='div')) + '\n')

    print('\nall ~= best?', o(diffs(best.cols.ycols, data.cols.ycols)) + '\n')
    get_ofile().write('\nall ~= best?' + o(diffs(best.cols.ycols, data.cols.ycols)) + '\n\n')

    print('best ~= rest?', o(diffs(best.cols.ycols, rest.cols.ycols)) + '\n')
    get_ofile().write('best ~= rest?' + o(diffs(best.cols.ycols, rest.cols.ycols)) + '\n\n')

    print('best ~= best?', o(diffs(data.cols.ycols, data.cols.ycols)) + '\n')

    return err

def copy_test():
    t1 = { 'a': 1, 'b': { 'c': 2, 'd': [3] } }
    t2 = copy(t1)
    t2['b']['d'][0] = 10000
            
    print('b4\t', end='')
    get_ofile().write('b4\t')
    oo(t1)
    print('\nafter\t')
    get_ofile().write('after\t')
    oo(t2)

    return 0

def repcols_test():
    t = repcols(getThe()['file'])
    
    try:
        for col in t.cols.xcols:
            print('{' + 'a NUM' + ' :at {}'.format(col.get_pos()) + ' :hi {}'.format(col.hi) + ' :lo {}'.format(col.lo) + ' :m2 {}'.format(rnd(col.m2, 3)) + ' :mu {}'.format(rnd(col.mu), 3) + ' :n {}'.format(col.total) + ' :txt {}'.format(col.get_name()) + '}')
            get_ofile().write('{' + 'a NUM' + ' :at {}'.format(col.get_pos()) + ' :hi {}'.format(col.hi) + ' :lo {}'.format(col.lo) + ' :m2 {}'.format(rnd(col.m2, 3)) + ' :mu {}'.format(rnd(col.mu), 3) + ' :n {}'.format(col.total) + ' :txt {}'.format(col.get_name()) + '}\n')
    except Exception:
        pass

    try:
        for row in t.rows:
            print('{' + 'a ROW :cells ' + str(row.cells) + '}')
            get_ofile().write('{' + 'a ROW :cells ' + str(row.cells) + '}\n')
    except Exception:
        pass

    return 0

def reprows_test():
    t = reprows(getThe()['file'])
    
    try:
        for col in t.cols.xcols:
            print('{' + 'a NUM' + ' :at {}'.format(col.get_pos()) + ' :hi {}'.format(col.hi) + ' :lo {}'.format(col.lo) + ' :m2 {}'.format(rnd(col.m2, 3)) + ' :mu {}'.format(rnd(col.mu), 3) + ' :n {}'.format(col.total) + ' :txt {}'.format(col.get_name()) + '}')
            get_ofile().write('{' + 'a NUM' + ' :at {}'.format(col.get_pos()) + ' :hi {}'.format(col.hi) + ' :lo {}'.format(col.lo) + ' :m2 {}'.format(rnd(col.m2, 3)) + ' :mu {}'.format(rnd(col.mu), 3) + ' :n {}'.format(col.total) + ' :txt {}'.format(col.get_name()) + '}\n')
    except Exception:
        pass

    try:
        for row in t.rows:
            print('{' + 'a ROW :cells ' + str(row.cells) + '}')
            get_ofile().write('{' + 'a ROW :cells ' + str(row.cells) + '}\n')
    except Exception:
        pass

    return 0

def synonyms_test():
    t = repcols(getThe()['file'])
    clustered = t.cluster(cols=t.cols.xcols)
    show(clustered)

    return 0

def prototypes_test():
    t = reprows(getThe()['file'])
    clustered = t.cluster(cols=t.cols.xcols)
    show(clustered)

    return 0

def position_test():
    t = reprows(getThe()['file'])
    clustered = t.cluster()
    
    repplace(clustered)

    return 0

def every_test():
    repgrid(getThe()['file'])

    return 0

def reservoir_test():
    options = getThe()
    options['Max'] = 32
    setThe(options)

    num1 = NUM()
    for i in range(1, 10001):
        num1.add(i)
    oo(has(num1))

    return 0

def cliffs_test():
    assert True == cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [8, 7, 6, 2, 5, 8, 7, 3]), '1'
    assert False == cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [9, 9, 7, 8, 10, 9, 6]), '2'

    t1, t2 = [], []
    for i in range(1, 1001): t1.append(rand())
    for i in range(1, 1001): t2.append(rand()**0.5)
    
    assert True == cliffsDelta(t1, t1), '3'
    assert False == cliffsDelta(t1, t2), '4'

    diff, j = False, 1.0
    def fun(x):
        return x*j, None
    while not diff:
        t3 = map(t1, fun)
        diff = cliffsDelta(t1, t3)
        print(">", rnd(j), diff)
        j = j*1.025

    return 0

def dist_test():
    data = DATA(getThe()['file'])
    num = NUM()
    for _, row in enumerate(data.rows):
        num.add(data.dist(row, data.rows[0]))
    oo({'lo': num.lo, 'hi': num.hi, 'mid': rnd(num.mid()), 'div': rnd(num.div())})

    return 0

def bins_test():
    data = DATA(getThe()['file'])
    best, rest = data.sway()

    print('all\t', o({'best': len(best.rows), 'rest': len(rest.rows)}))
    for k, t in enumerate(bins(data.cols.xcols, {'best': best.rows, 'rest': rest.rows})):
        for single_range in t:
            print('{}\t{}\t{}\t{}\t{}'.format(single_range['txt'], single_range['lo'], single_range['hi'], rnd(value(single_range['y'].has, len(best.rows), len(rest.rows), 'best')), single_range['y'].has))
        print()

    return 0

def xpln_test():
    data = DATA(getThe()['file'])
    best, rest, evals = data.sway()
    rule, most = xpln(data, best, rest)
    if rule:
        print("\n-----------\nexplain=", o(showRule(rule)))
        get_ofile().write('\n-----------\nexplain=' + o(showRule(rule)) + '\n')
        
        print("all               ", o(data.stats()), o(data.stats(_what='div')))
        get_ofile().write('all               ' + o(data.stats()) + ' ' + o(data.stats(_what='div')) + '\n')
        
        best1 = DATA(None, cols = [data.cols.names], rows = [row.get_cells() for row in best.rows])
        print(fmt("sway with %5s evals", evals), o(best1.stats()), o(best1.stats(_what='div')))
        get_ofile().write(fmt("sway with %5s evals", evals) + ' ' + o(best1.stats()) + ' ' + o(best1.stats(_what='div')) + '\n')
        
        data1 = DATA(None, cols = [data.cols.names], rows = [row.get_cells() for row in selects(rule, data.rows)])
        print(fmt("xpln on   %5s evals", evals), o(data1.stats()), o(data1.stats(_what='div')))
        get_ofile().write(fmt("xpln on   %5s evals", evals) + ' ' + o(data1.stats()) + ' ' + o(data1.stats(_what='div')) + '\n')
        
        top = data.betters(len(best.rows))
        top = DATA(None, cols = [data.cols.names], rows = [row.get_cells() for row in top])
        print(fmt("sort with %5s evals", len(data.rows)), o(top.stats()), o(top.stats(_what='div')))
        get_ofile().write(fmt("sort with %5s evals", len(data.rows)) + ' ' + o(top.stats()) + ' ' + o(top.stats(_what='div')) + '\n')

    return 0

def ok_test():
    setSeed(1)
    return 0

def sample_test():
    for i in range(10):
        print(''.join(many(['a', 'b', 'c', 'd', 'e'], 5)))
        get_ofile().write(''.join(many(['a', 'b', 'c', 'd', 'e'], 5)) + '\n')
    return 0

def gauss_test():
    t = []
    for i in range(0, 10**4):
        t.append(gaussian(10, 2))
    
    n = NUM()
    for val in t:
        n.add(val)
    
    print('', n.total, n.mid(), n.div())
    get_ofile().write('' + ' ' + str(n.total) + ' ' + str(n.mid()) + ' ' + str(n.div()) + '\n')
    return 0

def bootmu_test():
    a, b = [], []

    for i in range(100): a.append(gaussian(10, 1))
    print('', 'mu', 'sd', 'cliffs', 'boot', 'both')
    get_ofile().write('' + ' mu' + ' sd' + ' cliffs' + ' boot' + ' both\n')
    print('' + ' --' + ' --' + ' ------' + ' ----' + ' ----')
    get_ofile().write('' + ' --' + ' --' + ' ------' + ' ----' + ' ----\n')

    for mu in np.linspace(10, 11, 10):
        b = []
        for i in range(100): b.append(gaussian(mu, 1))
        cl = cliffsDelta(a, b)
        bs = bootstrap(a, b)
        print('', rnd(mu, 1), 1, cl, bs, cl and bs)
        get_ofile().write('' + ' ' + str(rnd(mu, 1)) + ' ' + str(1) + ' ' + str(cl) + ' ' + str(bs) + ' ' + str(cl and bs) + '\n')
    
    return 0

def basic_test():
    print("\t\ttruee", bootstrap([8, 7, 6, 2, 5, 8, 7, 3], [8, 7, 6, 2, 5, 8, 7, 3]), cliffsDelta( [8, 7, 6, 2, 5, 8, 7, 3], [8, 7, 6, 2, 5, 8, 7, 3]))
    get_ofile().write("\t\ttruee " + str(bootstrap([8, 7, 6, 2, 5, 8, 7, 3], [8, 7, 6, 2, 5, 8, 7, 3])) + ' ' + str(cliffsDelta( [8, 7, 6, 2, 5, 8, 7, 3], [8, 7, 6, 2, 5, 8, 7, 3])) + '\n')
    print("\t\tfalse", bootstrap([8, 7, 6, 2, 5, 8, 7, 3],  [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]), cliffsDelta( [8, 7, 6, 2, 5, 8, 7, 3],  [0.1, 0.2, 0.3, 0.4, 0.5, 0.7])) 
    get_ofile().write("\t\tfalse " + str(bootstrap([8, 7, 6, 2, 5, 8, 7, 3],  [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])) + ' ' + str(cliffsDelta( [8, 7, 6, 2, 5, 8, 7, 3],  [0.1, 0.2, 0.3, 0.4, 0.5, 0.7])) + '\n')
    print("\t\tfalse", bootstrap([0.34, 0.49, 0.51, 0.6, .34, .49, .51, .6], [0.6,  0.7,  0.8,  0.9,   .6,   .7,   .8,  .9]), cliffsDelta([0.34, 0.49, 0.51, 0.6, 0.34, 0.49, 0.51, 0.6],  [0.6, 0.7, 0.8, 0.9, 0.6, 0.7, 0.8, 0.9]))
    get_ofile().write("\t\tfalse " + str(bootstrap([0.34, 0.49, 0.51, 0.6, .34, .49, .51, .6], [0.6,  0.7,  0.8,  0.9,   .6,   .7,   .8,  .9])) + ' ' + str(cliffsDelta([0.34, 0.49, 0.51, 0.6, 0.34, 0.49, 0.51, 0.6],  [0.6, 0.7, 0.8, 0.9, 0.6, 0.7, 0.8, 0.9])) + '\n')

    return 0

def pre_test():
    print('\neg3')
    get_ofile().write('\nneg3\n')
    d = 1
    for i in range(10):
        t1, t2 = [], []
        for j in range(32):
            t1.append(gaussian(10, 1))
            t2.append(gaussian(d*10, 1))
        print('\t', rnd(d, 2) , d<1.1, bootstrap(t1, t2), bootstrap(t1, t1))
        get_ofile().write('\t' + ' ' + str(rnd(d, 2)) + ' ' + str(d<1.1) + ' ' + str(bootstrap(t1, t2)) + ' ' + str(bootstrap(t1, t1)) + '\n')
        d = d + 0.05
    return 0

def five_test():
    for rx in tiles(scottKnot([RX([0.34,0.49,0.51,0.6,.34,.49,.51,.6],"rx1"),
         RX([0.6,0.7,0.8,0.9,.6,.7,.8,.9],"rx2"),
         RX([0.15,0.25,0.4,0.35,0.15,0.25,0.4,0.35],"rx3"),
         RX([0.6,0.7,0.8,0.9,0.6,0.7,0.8,0.9],"rx4"),
         RX([0.1,0.2,0.3,0.4,0.1,0.2,0.3,0.4],"rx5")])):
    
        print(str(rx['name']), str(rx['rank']), str(rx['show']))
        get_ofile().write(str(rx['name']) + ' ' + str(rx['rank']) + ' ' + str(rx['show']) + '\n')
    
    return 0

def six_test():
    for rx in tiles(scottKnot([
         RX([101,100,99,101,99.5,101,100,99,101,99.5],"rx1"),
         RX([101,100,99,101,100,101,100,99,101,100],"rx2"),
         RX([101,100,99.5,101,99,101,100,99.5,101,99],"rx3"),
         RX([101,100,99,101,100,101,100,99,101,100],"rx4")])):
        
        print(str(rx['name']),str(rx['rank']),str(rx['show']))
        get_ofile().write(str(rx['name'] + ' ' + str(rx['rank']) + ' ' + str(rx['show'])) + '\n')
    return 0

def tiles_test():
    rxs,a,b,c,d,e,f,g,h,j,k=[],[],[],[],[],[],[],[],[],[],[]
    
    for i in range(0, 1000):  a.append(gaussian(10,1))
    for i in range(0, 1000):  b.append(gaussian(10.1,1))
    for i in range(0, 1000):  c.append(gaussian(20,1))
    for i in range(0, 1000):  d.append(gaussian(30,1))
    for i in range(0, 1000):  e.append(gaussian(30.1,1))
    for i in range(0, 1000):  f.append(gaussian(10,1))
    for i in range(0, 1000):  g.append(gaussian(10,1))
    for i in range(0, 1000):  h.append(gaussian(40,1))
    for i in range(0, 1000):  j.append(gaussian(40,3))
    for i in range(0, 1000):  k.append(gaussian(10,1))
    
    for k, v in enumerate([a,b,c,d,e,f,g,h,j,k]): rxs.append(RX(v, 'rx{}'.format(k)))

    def sort_rxs(rxs):
        for rx in rxs:
            inum = NUM()
            for val in rx['has']:
                inum.add(val)
            rx['mid'] = inum.mid()
        
        for i in range(len(rxs)):
            for j in range(i, len(rxs)):
                if rxs[i]['mid'] > rxs[j]['mid']:
                    tmp = rxs[i]
                    rxs[i] = rxs[j]
                    rxs[j] = tmp

    sort_rxs(rxs)
    
    for rx in tiles(rxs): 
        print('', rx['name'], rx['show'])
        get_ofile().write(' ' + str(rx['name']) + ' ' + str(rx['show']) + '\n')

    return 0

def sk_test():
    rxs,a,b,c,d,e,f,g,h,j,k=[],[],[],[],[],[],[],[],[],[],[]
    
    for i in range(0, 1000):  a.append(gaussian(10,1))
    for i in range(0, 1000):  b.append(gaussian(10.1,1))
    for i in range(0, 1000):  c.append(gaussian(20,1))
    for i in range(0, 1000):  d.append(gaussian(30,1))
    for i in range(0, 1000):  e.append(gaussian(30.1,1))
    for i in range(0, 1000):  f.append(gaussian(10,1))
    for i in range(0, 1000):  g.append(gaussian(10,1))
    for i in range(0, 1000):  h.append(gaussian(40,1))
    for i in range(0, 1000):  j.append(gaussian(40,3))
    for i in range(0, 1000):  k.append(gaussian(10,1))
    
    for k, v in enumerate([a,b,c,d,e,f,g,h,j,k]): rxs.append(RX(v, 'rx{}'.format(k)))
    
    for rx in tiles(scottKnot(rxs)): 
        print('', rx['rank'], rx['name'], rx['show'])
        get_ofile().write('' + ' ' + str(rx['rank']) + ' ' + str(rx['name']) + ' ' + str(rx['show']) + '\n')

    return 0