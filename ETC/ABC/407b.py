X, Y = map(int, input().split())

ans = 0

for i in range(1, 7):
    for j in range(1, 7):
        if X <= i+j:
            ans+=1
        elif Y <= abs(i-j):
            ans+=1
print(ans/36)