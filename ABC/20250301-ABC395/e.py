import heapq
import sys

INF = sys.maxsize

N, M, X = map(int, input().split())

edges = []
for _ in range(M):
    u, v = map(int, input().split())
    edges.append((u, v))

graph = [[] for _ in range(N+1)]
reverse_graph = [[] for _ in range(N+1)]

for u, v in edges:
    graph[u].append(v)
    reverse_graph[v].append(u)

dist = [[INF, INF] for _ in range(N+1)]

dist[1][0] = 0
pq = [(0, 1, 0)]

while pq:
    cost, node, reversed_flag = heapq.heappop(pq)

    if reversed_flag == 0:
        for next_node in graph[node]:
            if dist[next_node][reversed_flag] > cost + 1:
                dist[next_node][reversed_flag] = cost + 1
                heapq.heappush(pq, (cost + 1, next_node, reversed_flag))

        if dist[node][1] > cost + X:
            dist[node][1] = cost + X
            heapq.heappush(pq, (cost + X, node, 1))

    else:
        for next_node in reverse_graph[node]:
            if dist[next_node][reversed_flag] > cost + 1:
                dist[next_node][reversed_flag] = cost + 1
                heapq.heappush(pq, (cost + 1, next_node, reversed_flag))

        if dist[node][0] > cost + X:
            dist[node][0] = cost + X
            heapq.heappush(pq, (cost + X, node, 0))

print(min(dist[N][0], dist[N][1]))


# Dijkstraアルゴリズム