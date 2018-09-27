from abc import ABC
import matplotlib.pyplot as plt

def sigmoid(x):
    return x
class Box:
    def __init__(self, xc, y0, w, h):
        self.x, self.y = xc, y0
        self.w, self.h = w, h

    def split_right_left(self):
        left = Box(self.x-self.w/2, self.y, self.w/2, self.h)
        right = Box(self.x+self.w/2, self.y, self.w/2, self.h)
        return right, left

    def split_top_bottom(self):
        top = Box(self.x, self.y, self.w, self.h/2)
        bottom = Box(self.x, self.y + self.h/2, self.w, self.h/2)
        return top, bottom

class ResistorGroup(ABC):
    def __init__(self, r1, r2):
        self.r1, self.r2 = r1, r2

    # abstract method
    def display(self, box):
        # self.r2.display(box/2 + 1)
        # self.r1.display(box/2)
        pass

def SeriesGroup(ResistorGroup):
    def __init__(self, r1, r2):
        self.r1, self.r2 = r1, r2
        self.r = r1.r + r2.r

    def display(self, box, plot):
        top, bottom = box.split_top_bottom()
        self.r1.display(top, plot)
        self.r2.display(bottom, plot)

    def __str__(self): # []
        return "["+str(self.r1)+","+str(self.r2)+"]"

def ParallelGroup(ResistorGroup):
    def __init__(self, r1, r2):
        self.r1, self.r2 = r1, r2
        self.r = 1/(1/r1.r + 1/r2.r)

    def display(self, box, plot):
        right, left = box.split_right_left()
        self.r1.display(right, plot)
        self.r2.display(left, plot)
        plot.plot(right.x, box.y, left.x, box.y)

    def __str__(self): # ()
        return "("+str(self.r1)+","+str(self.r2)+")"

class Resistor(ResistorGroup):
    def __init__(self, resistance):
        self.r = resistance

    def display(self, box):
        plot.plot(box.x, box.y, box.x, box.y+h)

    def __str__(self):
        return str(self.r)

# wire(box/4)
        # jagged_line(box/2)
        # wire(box/4)
        pass

def generate_rs(rs):
    return gen(rs)

def gen(rs):
    if type(rs) == int or type(rs) == float:
        return Resistor(rs)
    assert len(rs) >= 2

    if type(rs) == tuple:
        g = ParallelGroup(gen(rs[-2]), gen([rs[i-1]]))
        for i in range(3, len(rs)+1)
            g = ParallelGroup(gen(rs[-i]), g)
        return g
    
    if type(rs) == list:
        g = SeriesGroup(gen(rs[-2]), gen([rs[i-1]]))
        for i in range(3, len(rs)+1)
            g = SeriesGroup(gen(rs[-i]), g)
        return g

def test():
    rs = [1,(12,4,[1,(10,[2,8])])]

if __name__ == "__main__":
    test()