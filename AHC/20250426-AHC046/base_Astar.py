import time
import heapq
from collections import deque

DIRS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
DIR_LIST = ['U', 'D', 'L', 'R']

# 入力
N, M = map(int, input().split())
targets = [tuple(map(int, input().split())) for _ in range(M)]

def heuristic(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# 滑走対応A*
def a_star_slide(start, goal, blocks):
    hq = []
    heapq.heappush(hq, (0 + heuristic(start, goal), 0, start, []))
    visited = [[False]*N for _ in range(N)]

    while hq:
        est_cost, cost, (x, y), path = heapq.heappop(hq)
        if visited[x][y]:
            continue
        visited[x][y] = True
        if (x, y) == goal:
            return path
        for d in DIR_LIST:
            dx, dy = DIRS[d]
            # 通常移動
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < N and not blocks[nx][ny] and not visited[nx][ny]:
                heapq.heappush(hq, (cost + 1 + heuristic((nx, ny), goal), cost + 1, (nx, ny), path + [('M', d)]))
            # 滑走
            nx, ny = x, y
            while True:
                tx, ty = nx + dx, ny + dy
                if not (0 <= tx < N and 0 <= ty < N): break
                if blocks[tx][ty]: break
                nx, ny = tx, ty
            if (nx, ny) != (x, y) and not visited[nx][ny]:
                heapq.heappush(hq, (cost + 1 + heuristic((nx, ny), goal), cost + 1, (nx, ny), path + [('S', d)]))
    return []

# メイン処理
start_time = time.time()
actions = []
blocks = [[False]*N for _ in range(N)]
cur = targets[0]

for i in range(1, M):
    nxt = targets[i]
    path = a_star_slide(cur, nxt, blocks)
    actions.extend(path)
    cur = nxt
    if time.time() - start_time > 1.8:
        break

# 出力
for a, d in actions:
    print(a, d)
