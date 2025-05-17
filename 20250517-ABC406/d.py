import sys
input = sys.stdin.readline

H, W, N = map(int, input().split())
row_count = [0] * H
col_count = [0] * W
row_to_cols = [[] for _ in range(H)]
col_to_rows = [[] for _ in range(W)]

for _ in range(N):
    x, y = map(int, input().split())
    x -= 1
    y -= 1
    row_count[x] += 1
    col_count[y] += 1
    row_to_cols[x].append(y)
    col_to_rows[y].append(x)

Q = int(input())
row_deleted = [False] * H
col_deleted = [False] * W

for _ in range(Q):
    t, v = map(int, input().split())
    v -= 1
    if t == 1:
        if row_deleted[v]:
            print(0)
            continue
        ans = row_count[v]
        print(ans)
        row_deleted[v] = True
        for c in row_to_cols[v]:
            if not col_deleted[c]:
                col_count[c] -= 1
        row_count[v] = 0
    else:  # t == 2
        if col_deleted[v]:
            print(0)
            continue
        ans = col_count[v]
        print(ans)
        col_deleted[v] = True
        for r in col_to_rows[v]:
            if not row_deleted[r]:
                row_count[r] -= 1
        col_count[v] = 0
