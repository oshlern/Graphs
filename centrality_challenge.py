from graphs import *

def generate_random_bipartite(n1, n2, k):
    vs1 = [Node("a" + str(i+1)) for i in range(n1)]
    vs2 = [Node("b" + str(i+1)) for i in range(n2)]
    es = []
    possible_edges = []
    for i in range(n1):
        possible_edges += [(i, j) for j in range(n2)]
    for _ in range(k):
        i, j = random.choice(possible_edges)
        es.append(Edge(vs1[i], vs2[j]))
        possible_edges.remove((i,j))
    del possible_edges
    return Graph(es, vs1+vs2)

# B = generate_random_bipartite(4, 5, 10)
# B.display_degree_centrality = True
# B.display_frucht()

def get_degree_centralities(g):
    C_in, C_out, C = [], [], []
    for v in g.vs:
        c_in = len(v.get_incoming())
        c_out = len(v.get_outgoing())
        c = len(v.edges)
        C_in.append(c_in/(len(g.vs)-1))
        C_out.append(c_out/(len(g.vs)-1))
        C.append(c/(len(g.vs)-1))
    return C_in, C_out, C

n = 10
for i in range(1,n):
    B = generate_random_bipartite(i, n-i, np.random.randint(1,i*(n-i)))
    C_in, C_out, C = get_degree_centralities(B)
    Max = max(C)
    avg = sum(C)/len(C)
    print("average: {}, max: {}".format(avg, Max))
    B.display_degree_centrality = True
    B.display_frucht()
    