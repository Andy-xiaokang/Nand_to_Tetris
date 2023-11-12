import os
print(os.path.basename("/Users/andy/Desktop/nand2tetris/projects/08/test.py"))
print(os.getcwd())
print(os.path.isfile("/Users/andy/Desktop/nand2tetris/projects/08"))
print(os.path.isfile("/Users/andy/Desktop/nand2tetris/projects/08/test.py"))
print(os.path.isfile("./test.py"))

arithmetic_dict = {
    "neg": "-", "not": "!",
    "add": "+", "sub": "-", "and": "&", "or": "|",
    "eq": "JEQ", "gt": "JGT", "lt": "JLT"
}

print("neg" in arithmetic_dict)
a = 1
b = 2

print(f"{a + 3}23")
