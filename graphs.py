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
    strength = 1

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
        self.vs = [v1, v2]
        self.capacitated = False
        if strength != None:
            super(DirectedEdge, self).set_strength(strength)

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
        self.vs = []
        for e in self.edges:
            for v in e.vs:
                if not v in self.vs:
                    self.vs.append(v)
        # reset pointers
        for v in self.vs:
            v.edges = []
        # set pointers
        for e in self.edges:
            if len(e.vs) == 0:
                self.edges.remove(e)
                continue
            for v in e.vs:
                v.edges.append(e)

    def generate_adjacency(self):
        assert self.n == len(self.vs)
        self.A = np.zeros((self.n, self.n))
        indices = {v: i for i,v in enumerate(self.vs)}
        for e in self.edges:
            assert len(e.vs) == 2
            i, j = indices[e.vs[0]], indices[e.vs[1]]
            self.A[i, j] += e.strength
            if not isinstance(e, DirectedEdge):
                self.A[j,i] += e.strength
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

    def split_edge(self, e):
        assert e in self.es
        assert not isinstance(e, DirectedEdge)
        assert len(e.vs) == 2
        v1, v2 = e.vs
        e1 = DirectedEdge(v1, v2, e.strength)
        e2 = DirectedEdge(v2, v1, e.strength)
        for edge_list in [self.edges, v1.edges, v2.edges]:
            edge_list.remove(e)
            edge_list.append(e1)
            edge_list.append(e2)
        return e1, e2
        # will break for removing vertices. Add incoming and outgoing edge lists for nodes
        # alternatively, check if v == e.v1 when using the edge

    def remove_directed_edge(self, v1, v2):
        assert v1 in self.vs and v2 in self.vs
        for e in v1.edges:
            assert e in self.edges and v1 in e.vs
            if v2 in e.vs:
                if isinstance(e, DirectedEdge): 
                    self.remove_edge(e)
                else:
                    new_e = DirectedEdge(v2, v1, e.strength)
                    for edge_list in [v1.edges, v2.edges, self.edges]:
                        edge_list[edge_list.index(e)] = new_e
                    del e
                break

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

    def calc_periods(self):
        self.A = self.generate_adjacency()
        current_A = self.A
        cycles = [[] for i in range(len(self.edges)*2)]
        for k in range(1,self.n+1):
            for i in range(self.n):
                if current_A[i,i] > 0:
                    cycles[i].append(k)
            current_A = np.dot(current_A, self.A)
        self.periods = [np.gcd.reduce(cycles[i]) for i in range(self.n)]
        return self.periods

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
        node_str = "NODES: " + sum([str(v) + ", " for v in self.vs], "")
        edge_str = "EDGES: " + sum([str(e) + ", " for v in self.edges], "")
        return node_str[:-2] + "\n" + edge_str[:-2]

def duplicate_vs_es(old_vs, old_es):
    vs, es =  {}, []
    for v in old_vs:
        vs[v.id] = Node(v.id)
    for e in old_es:
        es.append(Edge(*[vs[v.id] for v in e.vs]))
    return vs, es

def duplicate_graph(g, return_args=False):
    vs, edges =  duplicate_vs_es(g.vs, g.edges)
    return Graph(edges, vs)

class Markov(Graph):
    def  __init__(self, edges, vs=None):
        if isinstance(edges, Graph):
            self.vs, self.edges = duplicate_vs_es(edges.vs, edges.edges)
        else:
            self.vs, self.edges = duplicate_vs_es(vs, edges)
        self.n = len(self.vs)
        for e in copy.copy(self.edges):
            if not isinstance(e, DirectedEdge):     
                assert len(e.vs) == 2
                v1, v2 = e.vs
                if e.capacitated:
                    e1 = DirectedEdge(v1, v2, e.strength)
                    e2 = DirectedEdge(v2, v1, e.strength)
                else:
                    e1 = DirectedEdge(v1, v2)
                    e2 = DirectedEdge(v2, v1)
                self.edges.remove(e)
                self.edges.append(e1)
                self.edges.append(e2)
        
        self.connect_pointers()
        for v in self.vs:
            total = 0
            for e in v.edges:
                assert isinstance(e, DirectedEdge)
                if e.v1 == v:
                    total += e.strength
            for e in v.edges:
                if e.v1 == v:
                    e.set_strength(e.strength/total)



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