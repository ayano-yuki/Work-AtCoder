N = int(input())
A = list(map(int, input().split()))

last_seen = {}
min_length = float('inf')

for i in range(N):
    value = A[i]
    
    if value in last_seen:
        min_length = min(min_length, i - last_seen[value] + 1)
    
    last_seen[value] = i

if min_length == float('inf'):
    print(-1)
else:
    print(min_length)

# スライディングウィンドウ（Sliding Window）、ハッシュマップ（Hash Map）