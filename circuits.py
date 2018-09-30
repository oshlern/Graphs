from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import math

wire_color = "black"
unit = 1
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

    def split_across(self, n):
        return [Box(self.x+self.w*((0.5+i)/n-1/2), self.y, self.w/n, self.h) for i in range(n)]

    def split_vertically(self, n):
        return [Box(self.x, self.y+self.h*(i/n), self.w, self.h/n) for i in range(n)]

class ResistorGroup(ABC):
    def __init__(self, rs):
        self.rs = rs

    @abstractmethod
    def display(self, box):
        "display self within alloted box on graph"
        return

class SeriesGroup(ResistorGroup):
    def __init__(self, rs):
        self.rs = list(rs)
        self.r = sum([r.r for r in self.rs])

    def display(self, box, plot):
        boxes = box.split_vertically(len(self.rs))
        for r,b in zip(self.rs,boxes):
            r.display(b, plot)

    def __str__(self): # []
        string = "[" + str(self.rs[0])
        for r in self.rs[1:]:
            string += "," + str(r)
        return string + "]"

class ParallelGroup(ResistorGroup):
    def __init__(self, rs):
        self.rs = list(rs)
        self.r = 1/sum([1/r.r for r in self.rs])

    def display(self, box, plot):
        boxes = box.split_across(len(self.rs))
        for r,b in zip(self.rs,boxes):
            r.display(b, plot)
        plot.plot([boxes[0].x, boxes[-1].x], [box.y, box.y], color=wire_color)
        plot.plot([boxes[0].x, boxes[-1].x], [box.y+box.h, box.y+box.h], color=wire_color)

    def __str__(self): # ()
        string = "(" + str(self.rs[0])
        for r in self.rs[1:]:
            string += "," + str(r)
        return string + ")"

class Resistor(ResistorGroup):
    def __init__(self, resistance, color="orange"):
        self.r = resistance
        self.color = color

    def display(self, box, plot):
        n = 5
        w = math.log(1+math.log(1+self.r))
        print(self.r, w, box.w, min(w,box.w/2))
        xs = [box.x] + [box.x + (-1)**i * min(w/100, box.w/2) for i in range(n)] + [box.x]
        ys = [box.y + box.h*((i/(n+1)+ 1)/3) for i in range(n+2)]
        plot.plot(xs, ys, linewidth=w, color=self.color)
        plot.plot([box.x, box.x], [box.y, box.y + box.h/3], color=wire_color)
        plot.plot([box.x, box.x], [box.y+box.h*2/3, box.y + box.h], color=wire_color)

    def __str__(self):
        return str(self.r)

class Battery:
    def __init__(self, V, rs, color="green"):
        self.V = V
        self.rs = rs
        self.color = color

    def display(self, plot):
        self.rs.display(Box(0.5, 0, 1, 1), plot)
        plot.plot([-0.5, -0.5, 0.5, 0.5], [0, -0.2, -0.2, 0], wire_color)
        plot.plot([-0.5, -0.5, 0.5, 0.5], [1, 1.2, 1.2, 1], wire_color)
        plot.plot([-0.75, -0.25, -0.25, -0.75, -0.75], [0, 0, 1, 1, 0], self.color)

def gen(rs):
    if type(rs) == int or type(rs) == float:
        out = Resistor(rs)
    else:
        assert len(rs) >= 2

        if type(rs) == tuple:
            out = ParallelGroup([gen(r) for r in rs])
        
        elif type(rs) == list:
            out = SeriesGroup([gen(r) for r in rs])
        else:
            print("AHH")
    # print(out, rs)
    return out

display_box = Box(0.5, 1, 1, 1)

def test():
    rs = [(1,3),(12,4,[1,(10,[2,8])])]
    rs = [1,2,(2,1,[100,3])]
    group = gen(rs)
    # print(group)
    # group.display(display_box, plt)
    bat =  Battery(12, group)
    bat.display(plt)
    plt.show()

if __name__ == "__main__":
    test()