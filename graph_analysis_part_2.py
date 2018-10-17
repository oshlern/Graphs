from graphs import *
import numpy as np

not_connected = True
while not_connected:
    g = generate_random_graph(7, 20)
    not_connected = not g.is_connected_efficient()

def steps_1_to_3(g):
    g.calc_eigs()
    print("Adjacency matrix: {}".format(g.A))
    A_vals, A_vs = np.linalg.eig(g.A)
    print("vals: {}, vs: {}".format(np.diag(A_vs), A_vs))
    print("Laplacian: {}".format(g.L))
    print("vals: {}, vs: {}".format(np.diag(g.eigs), g.eigvs))


    g.calc_periods()
    print("periods: {}".format(g.periods))

    # g.display_frucht()

    g.markovify()

    A = g.generate_adjacency()
    A100 = np.linalg.matrix_power(A, 100)
    probs = np.diagonal(A100)
    print("probabilities of returning: {}".format(probs))

steps_1_to_3(g)

for i in range(np.random.randint(1,6)):
    not_connected = True
    counter = 0
    while not_connected:
        copy = Graph(g.edges, g.vs)
        random_edge = np.random.choice(copy.edges)
        copy.remove_directed_edge(random_edge.vs[0],random_edge.vs[1])
        not_connected = not copy.is_connected_efficient()
        counter += 1
        if counter == 1000:
            print("AHHHHH")
            break
    g = copy
steps_1_to_3(g)



