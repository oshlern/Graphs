import math, random

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
        assert not all([isinstance(v, Node) for v in vs]), "Edge given a non node_type (given {})".format(vs)
        self.vs = vs
        init_strength(strength)

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

    def remove_vertex(v): # do we want to mutate the vertices? thinking about subset graphs. I think we'll clone, so it's okay to mutate
        assert isinstance(v, Node), "{} is not a node".format(v)
        assert v in self.vs, "cannot remove vertex because {} not in graph".format(v)
        self.vs.remove(v)
        for e in v.edges:
            for adjacent_v in e.vs: # going to include v but that's filtered out
                if adjacent_v in self.vs:
                    if e in adjacent_v.edges:
                        adjacent_v.edges.remove(e)

            # remove adjacent edges
            if edge in self.edges: # if there's an edge that wasn't there already, that's fine
                self.edges.remove(edge)
            del edge
        
        del v
        


    def display(self):
        # implement mathplotlib
        pass

    def display_frucht(self, radius=3):
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
        # print(v1, v2, edge)
        e = Edge(v1, v2)#, *edge[2:])
        for edge_list in [v1.edges, v2.edges, es]:
            edge_list.append(e)
    return Graph(es, list(nodes.values()))

def generate_random_graph(n, k): # n = # vs, k = # edges
    vs = [Node(i+1) for i in range(n)]
    es = []
    possible_edges = []
    for i in range(k):
        possible_edges += [(i, j) for j in range(k)]
    for _ in range(k):
        i, j = random.choice(possible_edges)
        es.append(Edge(vs[i], vs[j]))
        possible_edges.remove((i,j))
    del possible_edges
    # print(vs, es)
    return Graph(es, vs)

edge_list = [(1,3), (2,3), (3,4), (4,6), (5,2), (6,1), (5,4)]
graph = generate_graph(edge_list)

print(graph)

graph2 = generate_random_graph(6, 4)

print(graph2)