N = int(input())  
A = list(map(int, input().split()))  

i, j = 0, 0  
count = 0  

while i < N and j < N:
    if A[i] * 2 <= A[j]:
        count += 1  
        i += 1 
        j += 1 
    else:
        j += 1 

print(count)
