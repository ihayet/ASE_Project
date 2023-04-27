class ROW:
    def __init__(self, t):
        self.cells = []
        self.x, self.y = 0, 0
        for val in t:
            self.cells.append(val)

    def get_cells(self):
        return self.cells