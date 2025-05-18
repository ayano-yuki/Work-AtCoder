N, _ = map(int, input().split())
min_sum = float('inf') 

pairs = []
for _ in range(N):
    U, D = map(int, input().split())
    sum_ud = U + D
    pairs.append(sum_ud)
    if sum_ud < min_sum:
        min_sum = sum_ud

total_diff = sum(abs(sum_ud - min_sum) for sum_ud in pairs)

print(total_diff)
