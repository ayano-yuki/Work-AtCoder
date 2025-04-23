from collections import deque

Q = int(input())
queries = [input().strip() for _ in range(Q)]

queue = deque()

results = []

for query in queries:
    if query.startswith('1'):
        _, x = query.split()
        queue.append(int(x))
    else:
        results.append(queue.popleft())

for result in results:
    print(result)
