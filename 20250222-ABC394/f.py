from collections import defaultdict

def find_alcan_subgraph(n, edges):
    degree = [0] * (n + 1)
    
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
    
    valid_vertices = []
    for  i in range(1, n + 1):
        if degree[i] == 1 or degree[i] == 4:
            valid_vertices.append(i)
            
    has_four_degree_vertex = any(degree[v] == 4 for v in valid_vertices)
    if has_four_degree_vertex:
        return len(valid_vertices)
    else:
        return 0

N = int(input())
edges = [tuple(map(int, input().split())) for _ in range(N - 1)] 
result = find_alcan_subgraph(N, edges)
if result > 0:
    print(result)
else:
    print(-1)