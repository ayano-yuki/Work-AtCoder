# from collections import deque
#
# Q = int(input())
# queries = [list(map(int, input().split())) for _ in range(Q)]
#
# snake_queue = deque()
# prefix_sum = [0]
#
# for query in queries:
#     if query[0] == 1:
#         snake_queue.append(query[1])
#         prefix_sum.append(prefix_sum[-1] + query[1])
#     elif query[0] == 2:
#         removed_value = snake_queue.popleft()
#         prefix_sum.pop(0)
#         prefix_sum = [x - removed_value for x in prefix_sum]
#     else:
#         print(prefix_sum[query[1] - 1])


from collections import deque

Q = int(input())
queries = [list(map(int, input().split())) for _ in range(Q)]

snake_queue = deque()
prefix_sum = deque([0])
removed_value = 0

for query in queries:
    if query[0] == 1:
        snake_queue.append(query[1])
        prefix_sum.append(prefix_sum[-1] + query[1])
    elif query[0] == 2:
        removed_value += snake_queue.popleft()
        prefix_sum.popleft()
    else:
        print(prefix_sum[query[1] - 1]-removed_value)