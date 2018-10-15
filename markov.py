from graphs import *

class Markov(Graph):
    def  __init__(self, edges, vs=None):
        super(Markov, self).__init__(self, edges, vs=vs)
        for v in self.vs:
            if all([edge.capacitated for edge in v.edges]):
                total = sum([edge.strength for edge in v.edges])
                for edge in v.edges:
                    edge.strength /= total
            else:
                for edge in v.edges:
                    edge.set_strength(1/len(v.edges))

    def calc_period(self):
        self.period = 1 # add actual code