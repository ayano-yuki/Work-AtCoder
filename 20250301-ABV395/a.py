N = int(input())
A = list(map(int,input().split()))

ans = all(A[i] < A[i+1] for i in range(N-1))
if ans:
    print("Yes")
else:
    print("No")