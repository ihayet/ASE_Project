from abc import abstractmethod

class VAL():
    total = 0

    def __init__(self, n, s):
        self.col_pos = n
        self.col_name = s
        self.has = []

    @abstractmethod
    def add(self, x):
        pass

    @abstractmethod
    def mid(self):
        pass

    @abstractmethod
    def div(self):
        pass

    @abstractmethod
    def rnd(self, x, n):
        pass

    def get_pos(self):
        return self.col_pos

    def get_name(self):
        return self.col_name