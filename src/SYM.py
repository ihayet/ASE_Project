from VAL import VAL
import math

class SYM(VAL):
    def __init__(self, *args):
        if len(args) > 0: 
            super().__init__(args[0], args[1])
        elif len(args) == 0:
            super().__init__(None, None)
        self.total, self.most, self.mode = 0, 0, None
        self.sym_counter = {}
        self.has = self.sym_counter

    def add(self, x):        
        if x != "?":
            self.total += 1

            if x in self.sym_counter:
                self.sym_counter[x] += 1
            else:
                self.sym_counter[x] = 1

            if self.sym_counter[x] > self.most:
                self.most = self.sym_counter[x]
                self.mode = x

    def mid(self, col=None):
        return self.mode

    def div(self):
        def ent(p):
            return p*math.log(p, 2)

        e = 0
        for sym in self.sym_counter:
            e += ent(self.sym_counter[sym]/self.total)

        return -e

    def rnd(self, x, n):
        return x

    def dist(self, s1, s2):
        distance = 1 if s1=='?' and s2=='?' else 0 if s1==s2 else 1
        return distance