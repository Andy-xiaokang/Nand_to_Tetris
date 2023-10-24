import sys
import re

pattern_to_remove = r'//.*'
symbol_table = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "R0": 0, "R1": 1, "R2":2, "R3": 3, "R4": 4, "R5": 5, "R6": 6, "R7": 7,
    "R8": 8, "R9":9, "R10":10, "R11": 11, "R12": 12, "R13": 13, "R14": 14, "R15": 15,
    "SCREEN": 16384, "KBD": 24576
}
dest_table = {
    None: "000", 'M': "001", 'D': "010", "MD": "011", 'A': "100", "AM": "101", "AD": "110", "AMD": "111"
}
jump_table = {
    None: "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}
comp_table = {
    '0': "0101010", '1': "0111111", "-1": "0111010",
    'D': "0001100", 'A': "0110000",
    "!D": "0001101", "!A": "0110001",
    "-D": "0001111", "-A": "0110011",
    "D+1": "0011111", "A+1": "0110111",
    "D-1": "0001110", "A-1": "0110010",
    "D+A": "0000010", "D-A": "0010011", "A-D": "0000111",
    "D&A": "0000000", "D|A": "0010101",

    "M": "1110000", "!M": "1110001", "-M": "1110011",
    "M+1": "1110111", "M-1": "1110010",
    "D+M": "1000010", "D-M": "1010011", "M-D": "1000111",
    "D&M": "1000000", "D|M": "1010101"
}


if len(sys.argv) != 2:
    print("usage python assembler.py filename.asm")
filepath = sys.argv[1]
filename = re.findall(r'[A-Z][a-z]*', filepath)[0]

try:
    with open(filepath, "r") as file:
        lines = file.readlines()
except FileNotFoundError:
    print("no such file")

# lines without space and comments
lines1 = []
for line in lines:
    line_without_space = line.replace(" ", "")
    line_without_spaceandcomments = re.sub(pattern_to_remove, "", line_without_space) 
    if line_without_spaceandcomments and line_without_spaceandcomments != '\n':
        lines1.append(line_without_spaceandcomments)

def find_label(label):
    return label.lstrip('(').rstrip(")\n")
# first add LABEL symlol to the table
i = 0
for line in lines1:
    if not line.startswith("("):
        i = i + 1         # current i has been the next command index
    elif line.startswith("("):
        label = find_label(line)
        if label not in symbol_table:
            symbol_table[label] = i
# second add variable symbol to the table
j = 16
for line in lines1:
    if line.startswith("@"):
        variable = line.lstrip("@").rstrip('\n')
        if (variable not in symbol_table) and (not variable.isdigit()):
            symbol_table[variable] = j
            j = j + 1

lines2 = []
for line in lines1:
    if not line.startswith("("):
        lines2.append(line)

for line in lines2:
    print(line, end = "")

print(symbol_table)

pattern = r'(\w+)?=?([\w\+\-\&\|\!]+);?(\w+)?'
def parsec(s):
    matches = re.finditer(pattern, s)
    for match in matches:
        dest = match.group(1)
        comp = match.group(2)
        jump = match.group(3)
    return "111" + comp_table[comp] + dest_table[dest] + jump_table[jump]
def parsea(s):
    string = s.lstrip("@").rstrip('\n')
    if string.isdigit():
        number = int(string)
    else:
        number = symbol_table[s.lstrip("@").rstrip('\n')]
    binary = bin(number)[2:]  # Convert to binary and remove '0b' prefix
    binary_16bit = format(int(binary, 2), '016b')  # Format as a 16-bit binary string
    return binary_16bit
    

with open(filename + ".hack", "w") as file:
    for line in lines2:
        if line.startswith('@'):
            file.write(parsea(line) + "\n")
        else:
            file.write(parsec(line) + "\n")