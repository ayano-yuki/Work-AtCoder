number = int(input())

factorial = 1
n = 1

while factorial < number:
    n += 1
    factorial *= n
print(n)