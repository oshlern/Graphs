import math, random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import LineCollection


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
        self.vs = vs
        self.init_strength(strength)

    def init_strength(self, strength=None):
        if strength != None:
            self.capacitated = True
            self.strength = strength
        else:
            self.capacitated = False

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

    def remove_edge(self, e):
        assert isinstance(e, Edge), "{} is not an edge".format(e)
        assert e in self.edges, "cannot remove edge because {} not in graph".format(v)
        for v in e.vs: # remove edge from adjacent vertices
            v.edges.remove(e)
        self.edges.remove(e)
        del e

    def display(self, radius=0.03):
        segs = tuple([[(v.x, v.y) for v in e.vs] for e in self.edges])
        edges = LineCollection(segs) # bad for hypergraphs
        fig, ax = plt.subplots()
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
        possible_edges += [(i, j) for j in range(n)]
    for _ in range(k):
        i, j = random.choice(possible_edges)
        es.append(Edge(vs[i], vs[j]))
        possible_edges.remove((i,j))
    del possible_edges
    return Graph(es, vs)

if __name__ == "__main__":
    edge_list = [(1,3), (2,3), (3,4), (4,6), (5,2), (6,1), (5,4)]
    graph = generate_graph(edge_list)
    print(graph)
    # graph.remove_vertex(graph.vs[1])
    # print(graph)
    # graph.remove_edge(graph.edges[1])
    # print(graph)
    graph = generate_random_graph(13, 25)
    graph.display_frucht()

    # graph2 = generate_random_graph(6, 4)
    # print(graph2)