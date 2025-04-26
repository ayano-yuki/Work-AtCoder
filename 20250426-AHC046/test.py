import time
import random
from heapq import heappop, heappush
from collections import deque

DIRS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
DIR_LIST = ['U', 'D', 'L', 'R']

N, M = map(int, input().split())
targets = [tuple(map(int, input().split())) for _ in range(M)]
start_time = time.time()

# 初期状態：全てのマスは空き（False = 空き, True = ブロック）
blocks = [[False]*N for _ in range(N)]

# A*探索：滑走と移動を考慮
def a_star(start, goal, blocks):
    sx, sy = start
    gx, gy = goal
    visited = [[False]*N for _ in range(N)]
    prev = [[None]*N for _ in range(N)]
    move = [[None]*N for _ in range(N)]
    dist = [[float('inf')]*N for _ in range(N)]
    dist[sx][sy] = 0

    heap = [(0 + abs(sx - gx) + abs(sy - gy), 0, sx, sy)]
    while heap:
        _, cost, x, y = heappop(heap)
        if visited[x][y]:
            continue
        visited[x][y] = True
        if (x, y) == (gx, gy):
            break
        for d in DIR_LIST:
            dx, dy = DIRS[d]
            # 移動（M）
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < N and not blocks[nx][ny]:
                if cost + 1 < dist[nx][ny]:
                    dist[nx][ny] = cost + 1
                    prev[nx][ny] = (x, y)
                    move[nx][ny] = ('M', d)
                    heappush(heap, (dist[nx][ny] + abs(nx - gx) + abs(ny - gy), dist[nx][ny], nx, ny))
            # 滑走（S）
            nx, ny = x, y
            while True:
                tx, ty = nx + dx, ny + dy
                if 0 <= tx < N and 0 <= ty < N and not blocks[tx][ty]:
                    nx, ny = tx, ty
                else:
                    break
            if (nx, ny) != (x, y) and cost + 1 < dist[nx][ny]:
                dist[nx][ny] = cost + 1
                prev[nx][ny] = (x, y)
                move[nx][ny] = ('S', d)
                heappush(heap, (dist[nx][ny] + abs(nx - gx) + abs(ny - gy), dist[nx][ny], nx, ny))

    path = []
    x, y = gx, gy
    if not visited[x][y]:
        return []
    while (x, y) != start:
        act, d = move[x][y]
        path.append((act, d))
        x, y = prev[x][y]
    path.reverse()
    return path

# 焼きなまし法でブロック設置を最適化（訪問順序は固定）
def simulated_annealing(actions, score_func, duration=1.9):
    best_actions = list(actions)
    best_score = score_func(best_actions)
    current_actions = list(best_actions)
    T0 = 1.0
    T1 = 0.1
    t_start = time.time()
    while time.time() - t_start < duration:
        t = (time.time() - t_start) / duration
        T = T0 * (1 - t) + T1 * t
        new_blocks = [[random.choice([False, False, False, True]) for _ in range(N)] for _ in range(N)]
        # 評価
        actions = []
        pos = targets[0]
        valid = True
        for i in range(1, M):
            nxt = targets[i]
            path = a_star(pos, nxt, new_blocks)
            if not path:
                valid = False
                break
            actions.extend(path)
            pos = nxt
        if not valid:
            continue
        new_score = score_func(actions)
        delta = new_score - best_score
        if delta > 0 or random.random() < pow(2.718, delta / T):
            best_score = new_score
            best_actions = actions
    return best_actions

# スコア評価関数
def score_func(actions):
    return M * 1000 - len(actions)

# 最初のルート
actions = []
pos = targets[0]
for i in range(1, M):
    path = a_star(pos, targets[i], blocks)
    if not path:
        break
    actions.extend(path)
    pos = targets[i]

# 焼きなましで微調整
actions = simulated_annealing(actions, score_func, duration=1.9 - (time.time() - start_time))

# 出力
for a, d in actions:
    print(a, d)
