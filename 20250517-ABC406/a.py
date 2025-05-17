A, B, C, D = map(int, input().split())

deadline = A * 60 + B
submitted = C * 60 + D

if submitted < deadline:
    print("Yes")
else:
    print("No")
