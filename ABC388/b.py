N, D = map(int, input().split())
snakes = [tuple(map(int, input().split())) for _ in range(N)]

results = []

for k in range(1, D + 1):
    max_weight = 0
    for T, L in snakes:
        weight = T * (L + k)
        max_weight = max(max_weight, weight)
    results.append(max_weight)

for result in results:
    print(result)
