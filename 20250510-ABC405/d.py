import sys
from collections import deque

input = sys.stdin.readline

H, W = map(int, input().split())
grid = [list(input().strip()) for _ in range(H)]

dirs = [(-1, 0, '^'), (1, 0, 'v'), (0, -1, '<'), (0, 1, '>')]

dist = [[-1] * W for _ in range(H)]
prev = [[None] * W for _ in range(H)]

q = deque()
for i in range(H):
    for j in range(W):
        if grid[i][j] == 'E':
            dist[i][j] = 0
            q.append((i, j))

while q:
    y, x = q.popleft()
    for dy, dx, _ in dirs:
        ny, nx = y + dy, x + dx
        if 0 <= ny < H and 0 <= nx < W:
            if grid[ny][nx] == '.' and dist[ny][nx] == -1:
                dist[ny][nx] = dist[y][x] + 1
                prev[ny][nx] = (-dy, -dx)
                q.append((ny, nx))

res = [[''] * W for _ in range(H)]
for i in range(H):
    for j in range(W):
        if grid[i][j] == '#':
            res[i][j] = '#'
        elif grid[i][j] == 'E':
            res[i][j] = 'E'
        else:
            dy, dx = prev[i][j]
            for ddy, ddx, arrow in dirs:
                if dy == ddy and dx == ddx:
                    res[i][j] = arrow
                    break

sys.stdout.write('\n'.join(''.join(row) for row in res) + '\n')
