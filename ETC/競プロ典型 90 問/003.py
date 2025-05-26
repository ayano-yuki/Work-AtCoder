from collections import deque

N = int(input())
graph = [[] for _ in range(N + 1)]

for _ in range(N - 1):
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)

dist = [-1] * (N + 1)
dist[1] = 0
q = deque([1])

while q:
    v = q.popleft()
    for nv in graph[v]:
        if dist[nv] == -1:
            dist[nv] = dist[v] + 1
            q.append(nv)

s = dist.index(max(dist))

dist = [-1] * (N + 1)
dist[s] = 0
q = deque([s])

while q:
    v = q.popleft()
    for nv in graph[v]:
        if dist[nv] == -1:
            dist[nv] = dist[v] + 1
            q.append(nv)

print(max(dist) + 1)
