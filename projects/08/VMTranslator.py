import sys
import re
import os


class VMTranslator:
    def __init__(self, directory):
        self.directory = directory
        self.vmfiles = []
        self.asmcode = []
        for file in os.listdir(directory):
            if file.endswith(".vm"):
                self.vmfiles.append(os.path.join(directory, file))
        self.asmcode += self.c_init("Sys.init", "0")
    
    def parser(self):
        for file in self.vmfiles:
            single_vmtranslator = SVMTranslator(file)
            single_vmtranslator.parser()
            self.asmcode += single_vmtranslator.asmcode
    def writter(self):
        with open(self.get_output_filename(), "w") as file:
            for single_asmcode in self.asmcode:
                file.write(single_asmcode + '\n')
                
    def c_init(self, func_name, nargs):
        asm_code = ["@256", "D=A", "@SP", "M=D"] #SP=256
        push_DtoSP = ["@SP", "A=M", "M=D", "@SP", "M=M+1"]
        asm_code += ["@bootstrap", "D=A"] + push_DtoSP # push return address
        for pointer in ["LCL", "ARG", "THIS", "THAT"]:
            asm_code += [f"@{pointer}", "D=M"] + push_DtoSP # push LCL, ARG, THIS, THAT restore caller's state
        asm_code += [f"@{int(nargs) + 5}", "D=A", "@SP", "D=M-D", "@ARG", "M=D"] # ARG = SP - 5 - nargs
        asm_code += ["@SP", "D=M", "@LCL", "M=D"] # LCL = SP
        asm_code += [f"@{func_name}", "0;JMP"]  # goto function
        asm_code += ["(bootstrap)"]  # the next line's number of asm code in assemble
        return asm_code 
        
    def get_output_filename(self):
        return os.path.join(self.directory, os.path.basename(self.directory) + ".asm")

class SVMTranslator:
    comparison_count = 0
    ret_index = 0
    def __init__(self, filepath):  # assume filepath is ./ProgramFlow/BasicLoop/BasicLoop.vm
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
        # self.comparison_count = 0 this is wrong!!! 
        self.curr_funcname = ""
        # self.ret_index = 0 this is worong !!!
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
            self.asmcode += ["\n//" + single_vmcode]
            if keywords[0] in self.arithmetic_dict:
                self.asmcode += self.c_arithmetic(keywords[0])
            elif keywords[0] == "push":
                self.asmcode += self.c_push(keywords[1], keywords[2])
            elif keywords[0] == "pop":
                self.asmcode += self.c_pop(keywords[1], keywords[2])
            elif keywords[0] in ["label", "if-goto", "goto"]:
                self.asmcode += self.c_branch(keywords[0], keywords[1])
            elif keywords[0] == "function":
                self.asmcode += self.c_function(keywords[1], keywords[2])
            elif keywords[0] == "call":
                self.asmcode += self.c_call(keywords[1], keywords[2])
            elif keywords[0] == "return":
                self.asmcode += self.c_return()
                
    def c_function(self, func_name, nvars):
        self.curr_funcname = func_name
        asm_code = [f"({func_name})"]   # the vm code has assumed the function's name is class.function
        for i in range(int(nvars)):
            asm_code += ["@SP", "A=M", "M=0", "@SP", "M=M+1"]
        return asm_code
        
    def c_call(self, func_name, nargs):
        return_label = f"{func_name}$ret{self.ret_index}" # return_label is a alias for an address in assembler
        push_DtoSP = ["@SP", "A=M", "M=D", "@SP", "M=M+1"]
        asm_code = [f"@{return_label}", "D=A"] + push_DtoSP # push return address
        for pointer in ["LCL", "ARG", "THIS", "THAT"]:
            asm_code += [f"@{pointer}", "D=M"] + push_DtoSP # push LCL, ARG, THIS, THAT restore caller's state
        asm_code += [f"@{int(nargs) + 5}", "D=A", "@SP", "D=M-D", "@ARG", "M=D"] # ARG = SP - 5 - nargs
        asm_code += ["@SP", "D=M", "@LCL", "M=D"] # LCL = SP
        asm_code += [f"@{func_name}", "0;JMP"]  # goto function
        asm_code += [f"({return_label})"]  # the next line's number of asm code in assemble
        SVMTranslator.ret_index += 1
        return asm_code
        
    def c_return(self):
        asm_code = ["@LCL", "D=M", "@R13", "M=D"] # frame = LCL
        asm_code += ["@5", "D=A", "@R13", "A=M-D", "D=M", "@R14", "M=D"] # retAddr = *(frame - 5)
        asm_code += ["@SP", "AM=M-1", "D=M", "@ARG", "A=M", "M=D"] # *ARG = pop()
        asm_code += ["@ARG", "D=M+1", "@SP", "M=D"] # SP = ARG + 1
        asm_code += ["@R13", "A=M-1", "D=M", "@THAT", "M=D"]  # THAT = *(frame - 1)
        asm_code += ["@2", "D=A", "@R13", "A=M-D", "D=M", "@THIS", "M=D"]  # THIS = *(frame - 2)
        asm_code += ["@3", "D=A", "@R13", "A=M-D", "D=M", "@ARG", "M=D"]   # ARG = *(frame - 3)
        asm_code += ["@4", "D=A", "@R13", "A=M-D", "D=M", "@LCL", "M=D"]   # LCL = *(frame -4)
        asm_code += ["@R14", "A=M", "0;JMP"]  # goto retaddr
        return asm_code
            
    def c_branch(self, command, labelname):
        if command == "label":
            return [f"({self.curr_funcname}${labelname})"]
        elif command == "if-goto":
            return ["@SP", "AM=M-1", "D=M", f"@{self.curr_funcname}${labelname}", "D;JNE"]
        elif command == "goto":
            return [f"@{self.curr_funcname}${labelname}", "0;JMP"]
        
    def c_arithmetic(self, command):
        if command in ["neg", "not"]:
            return ["@SP", "A=M-1", "M=" + self.arithmetic_dict[command] + "M"]
        elif command in ["add", "sub", "and", "or"]:
            return ["@SP", "AM=M-1", "D=M", "A=A-1", "M=M" + self.arithmetic_dict[command] + "D"]
        elif command in ["eq", "gt", "lt"]:
            label = f"{command}_" + str(self.comparison_count)
            asm_code = ["@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", "M=-1",   # set op1 default true
                    "@" + label, "D;" + self.arithmetic_dict[command], # if op1 operator op2 true then not change op1
                    "@SP", "A=M-1", "M=0", "(" + label +")"]
            SVMTranslator.comparison_count += 1
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
            asm1 = [f"@{index}", "D=A", f"@{self.segment_dict[segment]}", "A=M+D", "D=M"]
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
    
    def get_funcname(self):
        return self.filename.replace(".vm", f".{self.curr_funcname}")
    
    def writter(self):
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
    input_file_dir = sys.argv[1]
    if os.path.isfile(input_file_dir):
        vmtranslator = SVMTranslator(input_file_dir)
        vmtranslator.parser()
        vmtranslator.writter()
    elif os.path.isdir(input_file_dir):
        vmtranslator = VMTranslator(input_file_dir)
        vmtranslator.parser()
        vmtranslator.writter()
        print(vmtranslator.get_output_filename())
        print(vmtranslator.vmfiles)

if __name__ == "__main__":
    main()
    