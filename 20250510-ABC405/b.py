N, M = map(int, input().split())
A = list(map(int, input().split()))

required = set(range(1, M + 1))

for remove_count in range(N + 1):
    current = A[:N - remove_count]
    if set(current) < required:
        print(remove_count)
        break
