### First approach to calculate the number of partitions of N=25 into K in {2...N} parts with numbers between a and b (here always 1 and N-1)

import itertools
from more_itertools import pairwise

def k_partition(n, k, a, b):
    if k == 1 and a <= n <= b:
        yield [n]
    elif n > 0 and k > 0:
        for x in range(a, b+1):
            for p in k_partition(n-x, k-1, x, b):
                yield [x] + p


N = 5
n_parts = 0
result = []
for k in range(2,N+1):
    L = list(k_partition(N, k, 1, N-1))
    print("Number of partitions of length", k, "is:", len(L))
    print(L)
    result += L
    n_parts += len(L)

print("Final number of partitions ", n_parts )

print("Final list", result)



######### add colors NOT FINISHED YET
colors = ["blue", "green", "red","yellow","grey"]
colored_circles = []
for circle in result:
    if len(circle) > 3:
        perm_colors = list(itertools.combinations_with_replacement(colors, len(circle)))
        for perm_col in perm_colors:
            include = True
            for x in list(zip(perm_col[-1:] + perm_col[:-1], perm_col, perm_col[1:] + perm_col[:1])):
                if x[0]==x[1] or x[1] == x[2]:
                    include = False
                    #print(x, len(circle), perm_col)
            if(include):
                print(len(circle), perm_col)
                circle_col = circle + list(perm_col)
                colored_circles.append(circle_col)
    else:
        perm_colors = list(itertools.permutations(colors, len(circle)))
        for perm_col in perm_colors:
            circle_col = circle + list(perm_col)
            colored_circles.append(circle_col)



print(colored_circles)
