import math

class Node:
    def __init__(self, x, y, parent = None, role = None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = -1
        self.h = -1
        self.f = -1
        self.start = False
        self.end = False
        self.wall = False
        self.open = False
        self.closed = False

        if role == 's':
            self.start = True
        elif role == 'e':
            self.end = True
        elif role == '':
            self.wall = True

    def __eq__(self, o: object) -> bool:
        return o.x == self.x and o.y == self.y

    def set_parent(self, parent):
        self.parent = parent

    def compute_gcost(self, start):
        self.g = math.sqrt((start.x - self.x) ** 2 + (start.y - self.y) ** 2) if not self.start else 0

    def compute_hcost(self, end):
        self.h = math.sqrt((end.x - self.x) ** 2 + (end.y - self.y) ** 2) if not self.end else 0

    def compute_fcost(self):
        self.f = self.g + self.h
