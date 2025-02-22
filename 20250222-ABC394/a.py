import re

text = input()
result = re.sub(r"[^2]", "", text)

print(result) 