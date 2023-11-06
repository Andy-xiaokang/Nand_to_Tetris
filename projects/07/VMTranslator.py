import sys
import re

class VMTranslator:
    def __init__(self, filepath):
        self._filepath = filepath
        self.filename = re.findall(r"[\w]+.vm", self.filepath)[0]
        self.vmcode = []
        self.asmcode = []
        self.arithmetic_dict = {
            "neg": "-", "not": "!",
            "add": "+", "sub": "-", "and": "&", "or": "|",
            "eq": "JEQ", "gt": "JGT", "lt": "JLT"
        }
        self.segment_dict = {
            "local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT",
            "temp": "5", "pointer": "3"
        }
        self.comparison_count = 0
        with open(filepath, 'r') as file:
            for line in file:
                if line.startswith("//"):
                    continue
                elif not line.strip():
                    continue
                else:
                    self.vmcode.append(re.sub(r"\s+//.*","", line.strip()))
                    
    def parser(self):
        for single_vmcode in self.vmcode:
            keywords = single_vmcode.split()
            if len(keywords) == 1:
                self.asmcode += self.c_arithmetic(keywords[0])
            elif keywords[0] == "push":
                self.asmcode += self.c_push(keywords[1], keywords[2])
            elif keywords[0] == "pop":
                self.asmcode += self.c_pop(keywords[1], keywords[2])
        
    def c_arithmetic(self, command):
        if command in ["neg", "not"]:
            return ["@SP", "A=M-1", "M=" + self.arithmetic_dict[command] + "M"]
        elif command in ["add", "sub", "and", "or"]:
            return ["@SP", "AM=M-1", "D=M", "A=A-1", "M=M" + self.arithmetic_dict[command] + "D"]
        elif command in ["eq", "gt", "lt"]:
            label = "COMPARISON_" + str(self.comparison_count)
            asm_code = ["@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", "M=-1",   # set op1 default true
                    "@" + label, "D;" + self.arithmetic_dict[command], # if op1 operator op2 true then not change op1
                    "@SP", "A=M-1", "M=0", "(" + label +")"]
            self.comparison_count += 1
            return asm_code
    
    def c_push(self, segment, index):
        """push segment index => assemblly code 

        Args:
            segment (str): keywords of segment
            index (str): the interger of push argument

        Returns:
            str: assemblly code
            
        asm1: get the specific stack M to D
        asm2: push the D to SP and SP++
        """
        asm2 = ["@SP", "A=M", "M=D", "@SP", "M=M+1"]
        if segment == "constant":
            asm1 = ["@"+index, "D=A"]
        elif segment == "static":
            asm1 = ["@" + self.filename + "." + index, "D=M"]
        elif segment in ["temp", "pointer"]:
            asm1 = ["@" + self.segment_dict[segment], "D=A", "@" + index, "D=A+D", "@R15", "M=D", "@R15", "A=M", "D=M"]
        elif segment in ["local", "argument", "this", "that"]:
            asm1 = ["@" + self.segment_dict[segment], "D=M", "@" + index, "D=A+D", "@R15", "M=D", "@R15", "A=M", "D=M"]
        asm2 = ["@SP", "A=M", "M=D", "@SP", "M=M+1"]
        return asm1 + asm2
    
    def c_pop(self, segment, index):  # constant segment has no pop
        """pop segment index => assemblly code

        Args:
            segment (str): segment keyword
            index (index): index keyword

        Returns:
            str: assemblly code
        """
        if segment == "static":
            asm1 = ["@SP", "AM=M-1", "D=M"]
            asm2 = ["@" + self.filename + "." + index, "M=D"]
        elif segment in ["temp", "pointer"]:
            asm1 = ["@" + self.segment_dict[segment], "D=A", "@" + index, "D=A+D", "@R15", "M=D"]
            asm2 = ["@SP", "AM=M-1", "D=M", "@R15", "A=M", "M=D"]
        elif segment in ["local", "argument", "this", "that"]:
            asm1 = ["@" + self.segment_dict[segment], "D=M", "@" + index, "D=A+D", "@R15", "M=D"] 
            asm2 = ["@SP", "AM=M-1", "D=M", "@R15", "A=M", "M=D"]
        return asm1 + asm2
    
    def output_filepath(self):
        return re.sub(self.filename, self.filename.replace(".vm", ".asm"), self.filepath)
    
    def witter(self):
        with open(self.output_filepath(), "w") as file:
            for single_asmcode in self.asmcode:
                file.write(single_asmcode + '\n')
    
    @property
    def filepath(self):
        return self._filepath
        
    @filepath.setter
    def filepath(self, filepath):
        assert filepath.endswith(".vm")
        self._filepath = filepath

def main():
    if len(sys.argv) != 2:
        raise ValueError("usage: python VMTranslator.py filename.vm")
    intput_filepath = sys.argv[1]
    vmtranslator = VMTranslator(intput_filepath)
    vmtranslator.parser()
    vmtranslator.witter()
    
if __name__ == "__main__":
    main()
    