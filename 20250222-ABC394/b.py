N = int( input() )
box = []
for i in range(N):
    box.append( input() )


box = sorted(box, key=len)
print("".join(box))