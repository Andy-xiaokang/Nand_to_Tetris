import re
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


pattern = r'(\w+)?=?([\w\+\-\&\|\!]+);?(\w+)?'
string = "0;JMP"
def parse(s):
    matches = re.finditer(pattern, s)
    for match in matches:
        dest = match.group(1)
        comp = match.group(2)
        jump = match.group(3)
    return dest, comp, jump
dest, comp, jump = parse(string)
print(dest)
print(comp)
print(jump)
print("111" + dest_table[dest] + comp_table[comp] + jump_table[jump])

number = 42  # Replace with your desired number
binary = bin(number)[2:]  # Convert to binary and remove '0b' prefix
binary_16bit = format(int(binary, 2), '016b')  # Format as a 16-bit binary string

print(binary_16bit)

