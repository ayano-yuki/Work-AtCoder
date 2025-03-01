N = int(input())

grid = [['.'] * N for _ in range(N)]
for i in range(1, N + 1):
    j = N + 1 - i

    if i > j:
        continue
    
    color = '#' if i % 2 == 1 else '.'
    for r in range(i - 1, j):
        for c in range(i - 1, j):
            grid[r][c] = color

for row in grid:
    print("".join(row))
