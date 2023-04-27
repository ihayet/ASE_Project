import math
from utils import getThe, rand, many, rnd, cliffsDelta, rint
from NUM import NUM

def RX(t, s):
    sorted(t)
    return {"name": s or "", "rank": 0, "n": len(t), "show": "", "has": t, "show": ''}

def gaussian(mu, sd):
    mu = mu or 0
    sd = sd or 1
    return mu + sd * math.sqrt(-2 * math.log(rand())) * math.cos(2 * math.pi * rand())

def delta(i, other):
    e, y, z, = 1e-32, i, other
    return abs(y.mid() - z.mid()) / ((e + (y.div()**2)/y.total + (z.div()**2)/z.total)**0.5)

def bootstrap(y0, z0):
    x, y, z, yhat, zhat = NUM(), NUM(), NUM(), [], []

    # x will hold all of y0, z0
    # y contains just y0
    # z contains just z0
    for y1 in y0:
        x.add(y1)
        y.add(y1)

    for z1 in z0:
        x.add(z1)
        z.add(z1)

    xmu, ymu, zmu = x.mid(), y.mid(), z.mid()
    
    # yhat and zhat are y,z fiddled to have the same mean (recommended by Efrom)
    for y1 in y0: yhat.append(y1 - ymu + xmu)
    for z1 in z0: zhat.append(z1 - zmu + xmu)

    # tobs is some delta seen in the whole space
    tobs = delta(y, z)

    n = 0
    for i in range(getThe()['bootstrap']):
        # here we look at some delta from just part of the space
        # if the part delta is bigger than the whole, then increment n
        yhatnum = NUM()
        zhatnum = NUM()

        for i in many(yhat, len(yhat)): yhatnum.add(i)
        for i in many(zhat, len(zhat)): zhatnum.add(i)

        if delta(yhatnum, zhatnum) > tobs:
            n += 1

    # if we have seen enough n, then we are the same
    return n / getThe()['bootstrap'] >= getThe()['conf']

def tiles(rxs):
    lo, hi = math.inf, -math.inf
    for rx in rxs:
        lo, hi = min(lo, rx['has'][0]), max(hi, rx['has'][-1])

    for rx in rxs:
        t, u = rx['has'], []
        def of(x, most): return max(1, min(most, x))
        def at(x): return t[of(math.floor((len(t)-1)*x), len(t)-1)]
        def pos(x): return math.floor(of(getThe()['width']*(x-lo)/(hi-lo+1E-32), getThe()['width']))
        
        for i in range(getThe()['width']): u.append(" ")

        a, b, c, d, e = at(.1), at(.3), at(.5), at(.7), at(.9)
        A, B, C, D, E = pos(a), pos(b), pos(c), pos(d), pos(e)

        for i in range(A, B+1): u.append('')
        for i in range(D, E+1): u.append('')
        u.append('')

        for i in range(A, B+1): u[i] = "-"
        for i in range(D, E+1): u[i] = "-"
        u[getThe()['width']//2] = "|"
        u[C] = "*"
        
        rx['show'] = "".join(u) + " {" + str(rnd(a, 2))

        for x in [b, c, d, e]:
            rx['show'] += ", " + str(rnd(x, 2))
        rx['show'] += "}"

    return rxs

def merge(rx1, rx2):
    rx3 = RX([], rx1['name'])
    
    for x in rx2['has']: 
        rx3['has'].append(x)

    sorted(rx3['has'])
    rx3['n'] = len(rx3['has'])
    
    return rx3

def scottKnot(rxs):
    cohen = 0.35
    
    def merges(i, j):
        out = RX([], rxs[i]['name'])
        for k in range(i, j):
            out = merge(out, rxs[j])

        outnum = NUM()
        for val in out['has']:
            outnum.add(val)
        out['mid'] = outnum.mid()
        out['div'] = outnum.div()

        return out
    def same(lo, cut, hi):
        l = merges(lo, cut)
        r = merges(cut+1, hi)
        return cliffsDelta(l['has'], r['has']) and bootstrap(l['has'], r['has'])
    def recurse(lo, hi, rank):
        b4 = merges(lo, hi)
        best = 0
        cut = 0
        for j in range(lo, hi):
            if j > lo and j < hi:
                l = merges(lo, j)
                r = merges(j, hi)
                now = (l['n'] * (l['mid'] - b4['mid'])**2 + r['n'] * (r['mid'] - b4['mid'])**2) / (l['n'] + r['n'])
                if now > best:
                    if abs(l['mid'] - r['mid']) >= cohen:
                        cut, best = j, now
        
        if cut and not same(lo, cut, hi):
            rank = recurse(lo, cut, rank)
            rank = recurse(cut+1, hi, rank)
        else:
            for i in range(lo, hi):
                rxs[i]['rank'] = rank
        
        return rank
    
    def sort_rxs(rxs):
        for rx in rxs:
            inum = NUM()
            for val in rx['has']:
                inum.add(val)
            rx['mid'] = inum.mid()
            rx['div'] = inum.div()
        
        for i in range(len(rxs)):
            for j in range(i, len(rxs)):
                if rxs[i]['mid'] > rxs[j]['mid']:
                    tmp = rxs[i]
                    rxs[i] = rxs[j]
                    rxs[j] = tmp
    
    sort_rxs(rxs)
    cohen = merges(0, len(rxs)-1)['div'] * 0.35
    recurse(0, len(rxs)-1, 1)

    return rxs

    