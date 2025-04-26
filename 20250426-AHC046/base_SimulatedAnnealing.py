import time
import random
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

            # 移動(M)
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < N and not visited[nx][ny]:
                visited[nx][ny] = True
                prev[nx][ny] = (x, y)
                move[nx][ny] = ('M', d)
                q.append((nx, ny))

            # 滑走(S)
            nx, ny = x, y
            while True:
                tx, ty = nx + dx, ny + dy
                if 0 <= tx < N and 0 <= ty < N:
                    nx, ny = tx, ty
                else:
                    break
            if (nx, ny) != (x, y) and not visited[nx][ny]:
                visited[nx][ny] = True
                prev[nx][ny] = (x, y)
                move[nx][ny] = ('S', d)
                q.append((nx, ny))

    path = []
    x, y = goal
    if not visited[x][y]:
        return []  # ゴールに到達できない

    while (x, y) != start:
        m, d = move[x][y]
        path.append((m, d))
        px, py = prev[x][y]
        x, y = px, py
    path.reverse()
    return path

def build_actions():
    actions = []
    cur = targets[0]
    for i in range(1, M):
        nxt = targets[i]
        actions.extend(bfs(cur, nxt))
        cur = nxt
    return actions

def evaluate(actions):
    return M + 2*N*M - len(actions)

def simulated_annealing(time_limit=1.9):
    start_time = time.time()
    best_actions = build_actions()
    best_score = evaluate(best_actions)

    while time.time() - start_time < time_limit:
        idx = random.randint(0, M-2)
        cur = targets[idx]
        nxt = targets[idx+1]
        
        new_path = bfs(cur, nxt)
        if not new_path:
            continue

        new_actions = []
        for i in range(1, M):
            if i == idx + 1:
                new_actions.extend(new_path)
            else:
                from_pos = targets[i-1]
                to_pos = targets[i]
                new_actions.extend(bfs(from_pos, to_pos))
        
        new_score = evaluate(new_actions)

        if new_score > best_score:
            best_score = new_score
            best_actions = new_actions

    return best_actions

actions = simulated_annealing()

for a, d in actions:
    print(a, d)
