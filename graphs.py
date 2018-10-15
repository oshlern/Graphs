import math, random, copy, time#, cProfile
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import LineCollection
import numpy as np

def almost_zero(x):
    if x**2 < 0.0001:
        return True
    else:
        return False

class Node:
    def __init__(self, name="node"):
        self.id = name
        self.x = self.y = None # Pointer and mutability won't matter because they need to be redefined, not modified
        self.edges = []
    
    def __str__(self):
        return str(self.id)

class Edge:
    def __init__(self, *vs, strength=None):
        assert len(vs) != 0, "Empty edge"
        assert all([isinstance(v, Node) for v in vs]), "Edge given a non node_type (given {})".format(vs)
        self.vs = list(vs)
        self.capacitated = False
        if strength != None:
            self.set_strength(strength)

    def set_strength(self, strength):
        self.capacitated = True
        self.strength = strength

    def __str__(self):
        string = "("
        for v in self.vs:
            string += str(v) + ", "
        return string[:-2] + ")"

class DirectedEdge(Edge):
    def __init__(self,  v1, v2, strength=None):
        self.v1 = v1
        self.v2 = v2
        super(DirectedEdge, self).init_strength(strength)

class Graph:
    def __init__(self, edges, vs=None):
        self.edges = edges
        self.vs = vs
        self.n = len(vs)
        self.connect_pointers()
    
    def edges_to_str(self, es):
        edge_str = ""
        for e in self.edges:
            edge_str += str(e) + ", "
        return edge_str[:-2]

    def connect_pointers(self):
        # reset pointers
        for v in self.vs:
            v.edges = []
        # set pointers
        for e in self.edges:
            has_vs = False
            for v in e.vs:
                if v in self.vs:
                    v.edges.append(e)
                    has_vs = True
                else:
                    self.vs.remove(v)
                    e.vs.remove(v)
            if not has_vs:
                self.edges.remove(e)

    def generate_adjacency(self):
        self.n = len(self.vs)
        self.A = np.zeros((self.n, self.n))
        indices = {v: i for i,v in enumerate(self.vs)}
        for e in self.edges:
            assert len(e.vs) == 2
            i, j = indices[e.vs[0]], indices[e.vs[1]]
            if e.capacitated:
                s = e.strength
            else:
                s = 1
            self.A[i, j] += s
            if not isinstance(e, DirectedEdge):
                self.A[j,i] += s
        return self.A

    def get_A(self):
        self.A = self.generate_adjacency()
        return self.A
    
    def generate_degrees(self):
        self.degrees = [len(v.edges) for v in self.vs]
        self.D = np.diag(self.degrees)
        return self.degrees

    def generate_laplacian(self):
        self.generate_adjacency()
        self.generate_degrees()
        self.L = self.D - self.A
        return self.L

    def calc_eigs(self):
        self.generate_laplacian()
        self.eigs, self.eigvs = np.linalg.eig(self.L)
        self.num_components = sum([almost_zero(eig) for eig in self.eigs])
        return self.eigs, self.eigvs

    def remove_vertex(self, v): # do we want to mutate the vertices? thinking about subset graphs. I think we'll clone, so it's okay to mutate
        assert isinstance(v, Node), "{} is not a node".format(v)
        assert v in self.vs, "cannot remove vertex because {} not in graph".format(v)
        self.vs.remove(v) # remove vertex
        for e in v.edges: # loop over adjacent edges
            # remove edge from adjacent vertices
            for adjacent_v in e.vs: # going to include v but that's filtered out
                if adjacent_v in self.vs:
                    if e in adjacent_v.edges:
                        adjacent_v.edges.remove(e)
            # remove edge, even if hypergraph
            if e in self.edges: # if there's an edge that wasn't there already, that's fine
                self.edges.remove(e)
            del e
        del v
        self.n -= 1

    def remove_edge(self, e):
        assert isinstance(e, Edge), "{} is not an edge".format(e)
        assert e in self.edges, "cannot remove edge because {} not in graph".format(v)
        for v in e.vs: # remove edge from adjacent vertices
            v.edges.remove(e)
        self.edges.remove(e)
        del e

    def is_connected(self):
        queue = [self.vs[0]]
        reachable_vs = [self.vs[0]]
        unreachable_vs = self.vs[1:]
        while len(queue) > 0: #subset? len(reachable_vs)?
            v = queue.pop(0)
            # print("UNREACHABLE: ", [str(v) for v in unreachable_vs])
            # print("REACHABLE: ", [str(v) for v in reachable_vs])
            # print("ALL: ", [str(v) for v in self.vs])
            # print([str(e) for e in v.edges])
            for edge in v.edges:
                for adj_v in edge.vs:
                    assert adj_v in self.vs
                    # print(adj_v, ", unreachable: ", [str(v) for v in unreachable_vs])
                    if adj_v in unreachable_vs:
                        # print("edge: ", edge, v, adj_v)
                        reachable_vs.append(adj_v)
                        queue.append(adj_v)
                        unreachable_vs.remove(adj_v)
                        # print(adj_v, unreachable_vs, reachable_vs, self.vs)
            if len(unreachable_vs) == 0:
                return True
        return False

    def is_connected_efficient(self):
        self.calc_eigs()
        return self.num_components == 1

    def calc_period(self):
        self.period = 1 # add actual code

    def display(self, radius=0.03):
        fig, ax = plt.subplots()

        edges = LineCollection([[(v.x, v.y) for v in e.vs] for e in self.edges]) # bad for hypergraphs
        ax.add_collection(edges)

        for v in self.vs:
            ax.add_artist(Circle((v.x, v.y), radius, color="black"))
            plt.text(v.x, v.y + radius*2, str(v))

        ax.set_xlim(min([v.x for v in self.vs]) - 0.5, max([v.x for v in self.vs]) + 0.5)
        ax.set_ylim(min([v.y for v in self.vs]) - 0.5, max([v.y for v in self.vs]) + 0.5)
        plt.show()

    def display_frucht(self, radius=0.8):
        for i, v in enumerate(self.vs):
            v.x = radius*math.cos(i/self.n * math.tau)
            v.y = radius*math.sin(i/self.n * math.tau)
        self.display()
    
    def display_random(self, width=3):
        for v in self.vs:
            v.x = width*random.random()
            v.y = width*random.random()
        self.display()

    def display_grid(self, width=3):
        self.n = len(self.vs)
        sqrt = round(math.sqrt(self.n))
        row, col = 0,  0
        for v in self.vs:
            v.x = row * width/sqrt
            v.y = col * width/sqrt

            row += 1
            if row == sqrt:
                row = 0
                col += 1
        self.display()

    def __str__(self):
        node_str = "NODES:  "
        for v in self.vs: # ugh why does sum not work for lists of strs
            node_str += str(v) + ", "
        edge_str = "EDGES:  "
        for e in self.edges:
            edge_str += str(e) + ", "
        return node_str[:-2] + "\n" + edge_str[:-2]

def generate_graph(edges):
    nodes, es = {}, []
    for edge in edges:
        for node in edge[:2]:
            if node not in nodes:
                nodes[node] = Node(node)
        v1, v2 = nodes[edge[0]], nodes[edge[1]]
        e = Edge(v1, v2)#, *edge[2:])
        for edge_list in [v1.edges, v2.edges, es]:
            edge_list.append(e)
    return Graph(es, list(nodes.values()))

def generate_random_graph(n, k): # n = # vs, k = # edges
    vs = [Node(i+1) for i in range(n)]
    es = []
    possible_edges = []
    for i in range(n):
        possible_edges += [(i, j) for j in range(i+1, n)]
    for _ in range(k):
        i, j = random.choice(possible_edges)
        es.append(Edge(vs[i], vs[j]))
        possible_edges.remove((i,j))
    del possible_edges
    return Graph(es, vs)


def test():
    edge_list = [(1,3), (2,3), (3,4), (4,6), (5,2), (6,1), (5,4)]
    # graph = generate_graph(edge_list)
    
    # graph.remove_vertex(graph.vs[1])
    # print(graph)
    # graph.remove_edge(graph.edges[1])
    
    graph = generate_random_graph(10, 15)
    print("Graph: ", graph)
    print("Connected? ", graph.is_connected())
    print("Laplacian: ", graph.generate_laplacian())
    # s = time.time()
    print("eigs: ", graph.calc_eigs()[0])
    # print(time.time() - s)
    print("Num components: ", graph.num_components)
    graph.display_frucht()
    # graph.display_random()
    # graph.display_grid()

    # graph2 = generate_random_graph(6, 4)
    # print(graph2)

if __name__ == "__main__":
    test()