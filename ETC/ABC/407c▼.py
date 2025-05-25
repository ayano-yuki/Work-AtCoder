def min_operations_math(S):
    N = len(S)
    total = 0
    for i in reversed(range(N)):
        current = int(S[i])
        next_digit = int(S[i+1]) if i + 1 < N else 0
        b = (10 + current - next_digit) % 10
        total += b
    return total + N

S = input().strip()
print(min_operations_math(S))
