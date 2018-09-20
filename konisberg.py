import math

A, B, C, D = [1], [1], [1], [1]
print("A\tB\tC\tD")
print("{}\t{}\t{}\t{}".format(A[-1], B[-1], C[-1], D[-1]))
def display(a,  b, c, d, precision=False):
    if not precision:
        print("{}\t{}\t{}\t{}".format(a, b, c, d))
    else:
        print("{0:.14f}\t{0:.14f}\t{0:.14f}\t{0:.14f}".format(a, b, c, d))

def normalize(a, b, c, d):
    norm = math.sqrt(a**2 + b**2 + c**2 + d**2)
    # print(a,b,c,d,a/norm, b/norm, c/norm, d/norm)
    return a/norm, b/norm, c/norm, d/norm

for i in range(7):
    A += [2*C[-1] + D[-1]]
    B += [2*C[-1] + D[-1]]
    C += [2*A[-1] + 2*B[-1] + D[-1]]
    D += [A[-1] + B[-1] + C[-1]]
    display(A[-1], B[-1], C[-1], D[-1])
    # a, b, c, d = normalize(A[-1], B[-1], C[-1], D[-1])
    # display(a, b, c, d)

print("total number of walks:") # 478654742
print(A[-1] + B[-1] + C[-1] + D[-1])
    


