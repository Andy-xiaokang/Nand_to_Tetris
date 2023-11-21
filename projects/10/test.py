import re
code = "while (~(key = 0)) {"
delimeters = re.findall(r"[\[\]\(\)\{\}\,\.\;\-\~ ]", "while (~(key = 0)) {")
print(delimeters)
tokens = []
for delimeter in delimeters:
    print(code.split(sep=delimeter, maxsplit=1))
    first, code = code.split(delimeter, maxsplit=1)[0], code.split(delimeter, maxsplit=1)[1]
    if first:
        tokens.append(first)
    if delimeter == ' ':
        continue
    else:
        tokens.append(delimeter)
print(tokens)


a = "hello"

print(f"{a}, world")