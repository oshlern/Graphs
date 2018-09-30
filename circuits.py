from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import math

# def sigmoid(x):
#     return x
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

    @abstractmethod
    def display(self, box):
        "display self within alloted box on graph"
        return

def SeriesGroup(ResistorGroup):
    def __init__(self, *rs):
        self.rs = rs
        self.r = sum(self.rs)

    def display(self, box, plot):
        top, bottom = box.split_top_bottom()
        self.r1.display(top, plot)
        self.r2.display(bottom, plot)

    def __str__(self): # []
        string = "[" + str(self.rs[0])
        for r in self.rs[1:]:
            string += "," + str(r)
        return string + "]"

def ParallelGroup(ResistorGroup):
    def __init__(self, *rs):
        self.rs = rs
        self.r = 1/sum([1/r.r for r in self.rs])

    def display(self, box, plot):
        boxes = box.split_across(n)
        for r,b in zip(rs,boxes):
            r.display(b, plot)
        plot.plot([boxes[0].x, boxes[-1].x] [box.y, , box.y])

    def __str__(self): # ()
        string = "(" + str(self.rs[0])
        for r in self.rs[1:]:
            string += "," + str(r)
        return string + ")"

class Resistor(ResistorGroup):
    def __init__(self, resistance):
        self.r = resistance

    def display(self, box):
        w = math.log(self.r)
        n = 5
        xs = [box.x] + [box.x + (-1)**i * w for i in range(n)] + [box.x]
        ys = [box.y + i/(n+1)*h for i in range(n+2)]
        plot.plot(xs, ys, line_width=w/3)

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