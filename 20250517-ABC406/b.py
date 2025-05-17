N, K = map(int, input().split())
A = list(map(int, input().split()))

value = 1
for a in A:
    value *= a
    if len(str(value)) > K:
        value = 1

print(value)