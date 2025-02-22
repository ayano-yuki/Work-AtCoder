text = input()
stack = []
matching_bracket = {')': '(', ']': '[', '>': '<'}

for char in text:
    if char in '([<':
        stack.append(char)
    elif char in ')]>':
        if stack and stack[-1] == matching_bracket[char]:
            stack.pop()
        else:
            print("No")
            break
else:
    if not stack:
        print("Yes")
    else:
        print("No")
