filepath = "./Stack/Add/add.vm"
print("./Stack/Add/add.vm".endswith(".vm"))
import re
filename = re.findall(r"[\w]+.vm", filepath)[0]
print(filename)
output_filepath = re.sub(filename, filename.replace(".vm", ".asm"), filepath)
print(output_filepath)

print(bool("     ".strip()))

with open("./StackArithmetic/SimpleAdd/SimpleAdd.vm", "r") as file:
    for line in file:
        print(line, end = "")
s = "label IF_FALSE         // if n>=2, returns fib(n-2)+fib(n-1)\n"
print(re.sub(r"\s+//.*","", s.strip()))
print("M=M" + "&" + "D")
