from graphs import *
import numpy as np
import copy

np.set_printoptions(precision=3)
n, k = 7, 20

not_connected = True
while not_connected:
    g = generate_random_graph(n, k)
    not_connected = not g.is_connected_efficient()

print("Constructed graph with {} vertices and {} edges\n".format(n,k))

def steps_1_to_3(g):
    g.calc_eigs()
    print("Adjacency matrix:\n{}".format(g.A))
    A_vals, A_vs = np.linalg.eig(g.A)
    print("A eigenvals:\n{}\nA eigenvectors:\n{}\n".format(np.diag(A_vs), A_vs))
    print("Laplacian:\n{}".format(g.L))
    print("L eigenvals:\n{}\nL eigenvectors:\n{}\n".format(g.eigs, g.eigvs))

    g.calc_periods()
    print("periods: {}\n".format(g.periods))

    # g.display_frucht()

    m = Markov(g)

    A = m.generate_adjacency()
    # print("markov adjacency\n{}".format(A))
    A100 = np.linalg.matrix_power(A, 100)
    print("markov adjacency^100\n{}\n".format(A100))
    probs = np.diagonal(A100)
    print("probabilities of returning: {}\n".format(probs))


def test():
    steps_1_to_3(g)

    for i in range(np.random.randint(1,6)):
        not_connected = True
        counter = 0
        while not_connected:
            copy = duplicate_graph(g)
            random_edge = np.random.choice(copy.edges)
            copy.remove_directed_edge(random_edge.vs[0],random_edge.vs[1])
            not_connected = not copy.is_connected()
            counter += 1
            if counter == 1000:
                print("Cannot remove more edges and keep graph connected, stopping at {}".format(i))
                break
        else:
            g = copy
            continue
        break

    steps_1_to_3(g)

def testing():
    g = generate_random_graph(3,3)
    print(g)
    print(g.generate_adjacency())
    random_edge = np.random.choice(copy.edges)
    g.remove_directed_edge(random_edge.vs[0],random_edge.vs[1])
    print(g)
    print(g.generate_adjacency())

testing()

