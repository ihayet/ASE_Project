from COLS import COLS
from ROW import ROW
from mycsv import csv
from lists import map, kap, sort
from utils import getThe, rnd, cosine, many, any, last
import math

class DATA:
    def __init__(self, src, cols=None, rows=None):
        self.rows, self.cols = [], None
        map(csv(src), lambda x: self.add(x)) if src is not None else map(cols+rows, lambda x: self.add(x))            

    def add(self, t):
        if not self.cols is None:
            t = t if isinstance(t, ROW) else ROW(t)
            self.rows.append(t)
            self.cols.add(t)
        else:
            self.cols = COLS(t)
        return t, None

    def clone(self, rows):
        data = DATA(None, [self.cols.names], [row.get_cells() for row in (rows if rows is not None else self.rows)])
        return data

    def stats(self, _what=None, _cols=None, _nPlaces=None):
        def fun(k, col):
            if _nPlaces: val = rnd(col.mid() if _what=='mid' or _what==None else col.div(), _nPlaces)
            else: val = rnd(col.mid() if _what=='mid' or _what==None else col.div())
            return val, col.get_name()
        
        cols = _cols or self.cols.ycols

        colsdict = {}
        for (i, v) in enumerate(cols): colsdict[i] = v
        tmp = kap(colsdict, fun)
        tmp["N"] = len(self.rows)

        return tmp
    
    def better(self, row1, row2):
        s1, s2, ys = 0, 0, self.cols.ycols
        x, y = 0, 0
        for _, col in enumerate(ys):
            x = col.norm(row1.cells[col.get_pos()])
            y = col.norm(row2.cells[col.get_pos()])
            s1 = s1 - math.exp(col.w * (x-y)/len(ys))
            s2 = s2 - math.exp(col.w * (y-x)/len(ys))
        return s1/len(ys) < s2/len(ys)

    def betters(self, n):
        rowcopy = [row for row in self.rows]

        for r in range(len(rowcopy)):
            for _r in range(len(rowcopy)):
                if self.better(rowcopy[r], rowcopy[_r]):
                    tmp = rowcopy[_r]
                    rowcopy[_r] = rowcopy[r]
                    rowcopy[r] = tmp
        
        return rowcopy[:n]

    def dist(self, row1, row2, cols=None):
        n, d = 0, 0
        for _, col in enumerate(cols or self.cols.xcols):
            n += 1
            d += col.dist(row1.cells[col.get_pos()], row2.cells[col.get_pos()])**getThe()['p']
        val = (d/n)**(1/getThe()['p'])
        return val

    def around(self, row1, rows):
        def fun(row2):
            ret = dict()
            ret['row'] = row2
            ret['dist'] = self.dist(row1, row2, self.cols.xcols)
            return ret, None
        
        mapped_val = map(rows or self.rows, fun)
        sorted_val = sort(mapped_val, 'dist')

        return sorted_val

    def furthest(self, row1, rows):
        t = self.around(row1, rows)
        return t[len(t)-1]

    def half(self, rows=None, cols=None, above=None):
        A, B, c = 0, 0, 0
        left, right = [], []

        def gap(r1, r2): return self.dist(r1, r2, cols)
        def project(row):
            x, y = cosine(self.dist(row, A, cols), self.dist(row, B, cols), c)
            ret = {}
            row.x, row.y = x, y
            ret['row'] = row
            ret['dist'] = x
            return ret, None
        
        rows = rows or self.rows
        some = many(rows, getThe()['Halves'])        
        A = above if getThe()['Reuse'] and above else any(self.rows)
        B = self.furthest(A, some)['row']
        c = self.dist(A, B, None)
        
        temp = sort(map(rows, project), 'dist')
        for n, t in enumerate(temp):
            if n < math.floor(len(rows)/2):
                left.append(t['row'])
                mid = t['row']
            else:
                right.append(t['row'])

        evals = 1 if getThe()['Reuse'] and above else 2

        return left, right, A, B, mid, c, evals

    def cluster(self, rows=None, cols=None, above=None):
        rows = rows or self.rows
        cols = cols or self.cols.xcols    

        # newrows = []
        # for row in rows:
        #     r = ROW([val for val in row.cells])
        #     r.x, r.y = row.x, row.y
        #     newrows.append(r)

        node = {
            'data': self.clone(rows)
        }       
        
        if len(rows) >= 2 * len(self.rows) ** getThe()['min']:
            left, right, node['A'], node['B'], node['mid'], node['c'] = self.half(rows, cols, above)
            
            node['left'] = self.cluster(left, cols, node['A'])
            node['right'] = self.cluster(right, cols, node['B'])
        
        return node

    def sway(self):
        def worker(rows, worse, evals0, above=None):
            if len(rows) <= len(self.rows) ** getThe()['min']:
                return rows, many(worse, getThe()['rest'] * len(rows)), evals0
            else:
                left, right, A, B, _mid, _c, evals = self.half(rows, None, above)
                if self.better(B, A): 
                    left, right, A, B = right, left, B, A
                for row in right: worse.append(row)
                return worker(left, worse, evals0+evals, A)
        
        best, rest, evals = worker(self.rows, [], 0)
        return self.clone(best), self.clone(rest), evals

    def sway2(self):
        