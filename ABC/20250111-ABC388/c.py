from bisect import bisect_left

N = int(input())
A = list(map(int, input().split()))

count = 0
A.sort()

for i in range(len(A)):
    target = 2 * A[i]
    idx = bisect_left(A, target, i + 1) 
    count += len(A) - idx

print(count)
