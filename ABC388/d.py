import numpy as np

N = int(input())
A = np.array(list(map(int, input().split())), dtype=int)

for n in range(1, N):
    count = np.count_nonzero(A[:n] > 0)

    A[n] += count

    A[:n] -= (A[:n] > 0)

print(" ".join(map(str, A)))
