from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import math

wire_color = "black"

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
    current, dvoltage = None, None

    def __init__(self, rs):
        self.rs = rs

    @property
    def i(self):
        return self.current

    @property
    def dv(self):
        return self.dvoltage

    def calc_i(self):
        assert self.dv != None and self.r != None
        self.set_i(self.dv / self.r)

    def calc_dv(self):
        assert self.i != None and self.r != None
        self.set_dv(self.i * self.r)

    def set_i(self, i):
        self.current = i

    def set_dv(self, dv):
        self.dvoltage = dv

    def calc_i_or_dv(self):
        assert self.dvoltage != None or self.current != None
        if self.dvoltage == None:
            self.calc_dv()
        elif self.current == None:
            self.calc_i()

    @property
    @abstractmethod
    def r(self):
        pass

    @abstractmethod
    def display(self, box):
        "display self within alloted box on graph"
        return

class SeriesGroup(ResistorGroup):
    def __init__(self, rs):
        self.rs = list(rs)

    @property
    def r(self):
        return sum([r.r for r in self.rs])

    def set_i(self, i):
        super(SeriesGroup, self).set_i(i)
        for r in self.rs:
            r.set_i(i)

    def calc(self):
        self.calc_i_or_dv()
        for r in self.rs:
            r.calc()

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

    @property
    def r(self):
        return 1/sum([1/r.r for r in self.rs])

    def set_dv(self, dv):
        super(ParallelGroup, self).set_dv(dv)
        for r in self.rs:
            r.set_dv(dv)

    def calc(self):
        self.calc_i_or_dv()
        for r in self.rs:
            r.calc()

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
    def __init__(self, resistance, color="red"):
        self.resistance = resistance
        self.color = color

    @property
    def r(self):
        return self.resistance

    def calc(self):
        return self.calc_i_or_dv()

    def display(self, box, plot):
        n, font_size = 5, 5
        w = math.log(1+math.log(1+self.r))
        width = min(w/100, box.w/2)
        xs = [box.x] + [box.x + (-1)**i * width for i in range(n)] + [box.x]
        ys = [box.y + box.h*((i/(n+1)+ 1)/3) for i in range(n+2)]
        plot.plot(xs, ys, linewidth=w, color=self.color)
        plot.plot([box.x, box.x], [box.y, box.y + box.h/3], color=wire_color)
        plot.plot([box.x, box.x], [box.y+box.h*2/3, box.y + box.h], color=wire_color)

        if self.current != None:
            string = "{0:.6f}".format(self.i) + "A"
            plt.text(box.x + width, box.y + box.h/2 + box.h/6, string, color="blue", horizontalalignment="left", verticalalignment="bottom", fontsize=font_size)
        if self.dvoltage != None:
            string = "{0:.6f}".format(self.dv) + "V"
            plt.text(box.x + width, box.y + box.h/2 - box.h/6, string, color="green", horizontalalignment="left", verticalalignment="top", fontsize=font_size)
        string =  str(self.r) + "Ω"
        plt.text(box.x + width, box.y + box.h/2, string, color=self.color, horizontalalignment="left", verticalalignment="center", fontsize=font_size)

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
        plt.text(-0.5, 0.5, str(self.V) + "V", horizontalalignment="center", color=self.color, weight="bold", fontsize=20)

    def calc_ivs(self):
        self.rs.set_dv(self.V)
        self.rs.calc()

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
    return out

display_box = Box(0.5, 1, 1, 1)

def test():
    # rs = [10, 45, (20,10)]
    # rs = [(1,3),(12,4,[1,(10,[2,8])])]
    rs = [(1,[3,(1,[2,4]),2]),(12,[([3,1],100),10],[1,(10,[2,8])])]
    # rs = ([10000, 3400],[2000,4500],[3,5,(10000,3000)])
    group = gen(rs)
    print(group.r)
    bat =  Battery(10, group)
    bat.calc_ivs()
    bat.display(plt)
    plt.show()

if __name__ == "__main__":
    test()