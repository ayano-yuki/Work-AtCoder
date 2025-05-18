text = input()

result = []
i = 0

while i < len(text):
    if text[i] == 'W':  
        count = 0
        while i < len(text) and text[i] == 'W':
            count += 1
            i += 1
        if i < len(text) and text[i] == 'A':
            result.append("A" + "C" * count)
            i += 1
        else:
            result.append("W" * count)
    else:
        result.append(text[i])
        i += 1

print("".join(result))
