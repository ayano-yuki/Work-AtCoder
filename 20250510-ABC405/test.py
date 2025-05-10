MOD = 998244353
from collections import Counter
from math import factorial

MAX_N = 250000
fact = [1] * (MAX_N + 1)
inv_fact = [1] * (MAX_N + 1)

def modinv(x):
    return pow(x, MOD - 2, MOD)

for i in range(2, MAX_N + 1):
    fact[i] = fact[i - 1] * i % MOD
inv_fact[MAX_N] = modinv(fact[MAX_N])
for i in range(MAX_N - 1, 0, -1):
    inv_fact[i] = inv_fact[i + 1] * (i + 1) % MOD

N, Q = map(int, input().split())
A = list(map(int, input().split()))

for _ in range(Q):
    L, R, X = map(int, input().split())
    B = A[L-1:R]
    B = [b for b in B if b < X]
    
    if not B:
        print(1)
        continue
    
    counter = Counter(B)
    total_elements = sum(counter.values())
    result = fact[total_elements]
    
    for freq in counter.values():
        result = result * inv_fact[freq] % MOD
    
    print(result)
