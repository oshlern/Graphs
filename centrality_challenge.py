from graphs import *



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

def get_alpha_centrality(g, a):
    cs = np.dot(np.linalg.inv(np.identity(g.n) - a*g.generate_adjacency().T), np.ones(g.n))
    return list(cs/sum(cs))

# n = 10
# for i in range(1,n):
#     B = generate_random_bipartite(i, n-i, np.random.randint(1,i*(n-i)))
#     C_in, C_out, C = get_degree_centralities(B)
#     Max = max(C)
#     avg = sum(C)/len(C)
#     print("average: {}, max: {}".format(avg, Max))
#     B.display_degree_centrality = True
#     B.display_frucht()

n = 7
for i in range(1,11):
    B = generate_random_graph(n,i)
    # C_in, C_out, C = get_degree_centralities(B)
    for a in range(1,10):
        alpha = a/10
        C = get_alpha_centrality(B, alpha)
        Max = max(C)
        avg = sum(C)/len(C)
        print("a: {}, average: {}, max: {}, cs: {}".format(alpha, avg, Max, C))
    B.display_degree_centrality = True
    B.display_frucht()
