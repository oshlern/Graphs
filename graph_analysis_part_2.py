from graphs import *
import numpy as np

not_connected = True
while not_connected:
    g = generate_random_graph(7, 7)
    not_connected = not g.is_connected()

g.calc_eigs()
print("Adjacency matrix: {}".format(g.A))
A_vals, A_vs = np.linalg.eig(g.A)
print("vals: {}, vs: {}".format(np.diag(A_vs), A_vs))
print("Laplacian: {}".format(g.L))
print("vals: {}, vs: {}".format(np.diag(g.eigs), g.eigvs))


g.calc_periods()
print("periods: {}".format(g.periods))

g.display_frucht()

# m = Markoc


# for i in range(7,20):
#     not_connected = True
#     while not_connected:
#         g = generate_random_graph(7, 20)
#         not_connected = not g.is_connected()
#     print(g.calc_periods())
