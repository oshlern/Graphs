from graphs import *
import numpy as np
import copy

np.set_printoptions(precision=3)
n, k = 7, 17


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


def main():
    global g

    not_connected = True
    while not_connected:
        g = generate_random_graph(n, k)
        not_connected = not g.is_connected_efficient()

    print("Constructed graph with {} vertices and {} edges\n".format(n,k))

    # print(edges_to_str(g.vs[0].edges))
    # print([[str(v) for v in e.vs] for e in g.vs[0].edges])

    steps_1_to_3(g)
    num_deletions = np.random.randint(3,6)
    for i in range(num_deletions):
        not_connected = True
        counter = 0
        while not_connected:
            clone = duplicate_graph(g)
            random_edge = np.random.choice(clone.edges)
            # print("pre A\n", clone.generate_adjacency())
            # print("pre", g)
            clone.remove_directed_edge(random_edge.vs[0],random_edge.vs[1])
            # print("post", g)
            # print("post A\n", clone.generate_adjacency())
            not_connected = not clone.is_connected()
            counter += 1
            # print("Edge: {}, connected: {}, counter: {}".format(random_edge, not not_connected, counter))
            if counter == 10:
                print("Cannot remove more directed edges and keep graph connected, stopping at {}".format(i))
                break
        else:
            print("Removed edge {}".format(random_edge))
            g = clone
            continue
        break
    else:
        print("Removed {} directed edges from graph\n".format(num_deletions))

    steps_1_to_3(g)

def testing():
    g = generate_random_graph(5,3)
    print(g)
    print(g.generate_adjacency())
    random_edge = np.random.choice(g.edges)
    g.remove_directed_edge(random_edge.vs[0],random_edge.vs[1])
    print(g)
    print(g.generate_adjacency())

main()

