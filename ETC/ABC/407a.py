A, B = map(int, input().split())

if A/B - A//B < 0.5:
    print(A // B)
else :
    print(A // B + 1)