N, L = map(int, input().split())
K = int(input())
A = list(map(int, input().split()))

def is_possible(min_len):
    count = 0
    last = 0
    for a in A:
        if a - last >= min_len:
            count += 1
            last = a
    if L - last >= min_len:
        count += 1
    return count >= K + 1

low = 0
high = L + 1

# 二分探索
while high - low > 1:
    mid = (low + high) // 2
    if is_possible(mid):
        low = mid
    else:
        high = mid

print(low)
