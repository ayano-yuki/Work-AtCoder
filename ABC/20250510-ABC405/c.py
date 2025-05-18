N = int(input())
A = list(map(int, input().split()))

total_sum = sum(A)
ans = 0

for i in range(N):
    total_sum -= A[i]
    ans += A[i] * total_sum

print(ans)
