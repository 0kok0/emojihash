# First approach to calculate the number of partitions of N=25 into K in {2...N} parts
# with numbers between a and b (here always 1 and N-1)

import itertools
import string

# calculate the number of partions of length k for a number n
# each segment is required to be between a and b
# (a and b are not necessary but can be helpful later).
def k_partition(n, k, a, b):
    if k == 1 and a <= n <= b:
        yield [n]
    elif n > 0 and k > 0:
        for x in range(a, b+1):
            for p in k_partition(n-x, k-1, x, b):
                yield [x] + p

# N length of cricle in px
N = 5
# bounds for length of segments
lower_bound_k = 2
upper_bound_k = N-1

# get partitions for circle without colors
result = []
for k in range(lower_bound_k,upper_bound_k+1):
    L = list(k_partition(N, k, 1, N-1))
    result += L

print("Final number of partitions", len(result) )
print("Final list without colores", result)



# combine colors and list of partitions
# create a list of 32 elements representing the 32 colors.
#colors = list(string.ascii_uppercase) + ['aa','bb','cc','dd','ee','ff','gg']
colors = ["A","B","C","D","E","F"]
colored_circles = []
for circle in result:
        perm_colors = list(itertools.permutations(colors, len(circle)))
        for perm_col in perm_colors:
            circle_col = circle + list(perm_col)
            colored_circles.append(circle_col)


print("Final list of colored combinations", colored_circles)
print(len(colored_circles),"colored circles for circle length N =", N,"and segment length k from", lower_bound_k,"to",upper_bound_k,"and",len(colors),"colors")
