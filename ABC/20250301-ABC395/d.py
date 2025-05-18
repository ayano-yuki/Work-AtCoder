N, Q = map(int, input().split())

querys = []
for _ in range(Q):
    querys.append( list(map(int, input().split())) )

TORI = {i: i for i in range(1, N + 1)}
reverse_map = {i: i for i in range(1, N + 1)}

for query in querys:    
    if query[0] == 1:
        _, a, b = query
        TORI[a] = b
        reverse_map[b] = a

    elif query[0] == 2:
        _, a, b = query
        key_a = reverse_map[a] 
        key_b = reverse_map[b] 
        
        TORI[key_a] = b
        TORI[key_b] = a
        
        reverse_map[a] = key_b
        reverse_map[b] = key_a

    elif query[0] == 3:
        _, a = query
        print(TORI[a])
