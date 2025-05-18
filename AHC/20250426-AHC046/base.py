from collections import deque

DIRS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
DIR_LIST = ['U', 'D', 'L', 'R']

N, M = map(int, input().split())
targets = [tuple(map(int, input().split())) for _ in range(M)]

def bfs(start, goal):
    visited = [[False]*N for _ in range(N)]
    prev = [[None]*N for _ in range(N)]
    move = [[None]*N for _ in range(N)]

    q = deque()
    q.append(start)
    visited[start[0]][start[1]] = True

    while q:
        x, y = q.popleft()
        if (x, y) == goal:
            break
        for d in DIR_LIST:
            dx, dy = DIRS[d]
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < N and not visited[nx][ny]:
                visited[nx][ny] = True
                prev[nx][ny] = (x, y)
                move[nx][ny] = d
                q.append((nx, ny))

    path = []
    x, y = goal
    while (x, y) != start:
        d = move[x][y]
        path.append(('M', d))
        dx, dy = DIRS[d]
        x -= dx
        y -= dy
    path.reverse()
    return path

actions = []
cur = targets[0]
for i in range(1, M):
    nxt = targets[i]
    actions.extend(bfs(cur, nxt))
    cur = nxt

for a, d in actions:
    print(a, d)
