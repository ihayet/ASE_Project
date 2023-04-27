import re
from NUM import NUM
from SYM import SYM

class COLS:
    def __init__(self, t):
        self.names = t
        self.all, self.xcols, self.ycols, self.skipcols = [], [], [], []
        self.klass = ''
        for n, s in enumerate(t):
            col = NUM(n,s.strip()) if (len(re.findall(r'^[A-Z]+', s.strip())) > 0) else SYM(n, s.strip())
            self.all.append(col)

            self.skipcols.append(col) if (len(re.findall(r'X$', s.strip())) > 0) else self.assign_klass(col) if (len(re.findall(r'!$', s.strip())) > 0) else 1
            self.ycols.append(col) if len(re.findall(r'[!+-]$', s.strip())) > 0 else self.xcols.append(col) if len(re.findall(r'X$', s.strip())) == 0 else -1

    def add(self, row):
        [col.add(row.get_cells()[col.get_pos()]) for col in self.xcols]
        [col.add(row.get_cells()[col.get_pos()]) for col in self.ycols]

    def assign_klass(self, col):
        self.klass = col