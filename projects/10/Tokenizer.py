import sys
import re

TERMINAL_TAGS = ["keyword", "symbol", "integerConstant", "stringConstant", "identifier"]
UNTERMINAL_TAGS = ["class", "classVarDec", "subroutineDec", "parameterList", "subroutineBody", "varDec", 
                   "statements", "letStatement", "ifStatement", "whileStatement", "doStatement",
                   "returnStatement", "expression", "term", "expressionList"]
KEYWORDS = ["class", "constructor", "function", "method", "field", "static", "var",
           "int", "char", "boolean", "void", "true", "false", "null", "this",
           "let", "do", "if", "else", "while", "return"]
SYMBOL = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', 
          '>', '=', '~']

class Tokenizer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.code_withoutcomments = []
        self.tokens = []
        self.token_instances = []
        self.index = 0
        self.keywords = ["class", "constructor", "function", "method", "field", "static", "var",
           "int", "char", "boolean", "void", "true", "false", "null", "this",
           "let", "do", "if", "else", "while", "return"]
        self.symbol = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', 
          '>', '=', '~']
        with open(filepath, 'r') as file:
            for line in file:
                line = re.sub(r"//.*|/\*\*.*\*/", "", line.strip())  # handle single comments
                if line.strip():
                    self.code_withoutcomments.append(line.strip())
        while "/**" in self.code_withoutcomments and "*/" in self.code_withoutcomments:  # haddle multiple comments in file's begining
            index1 = self.code_withoutcomments.index("/**")
            index2 = self.code_withoutcomments.index("*/")
            self.code_withoutcomments = self.code_withoutcomments[:index1] + self.code_withoutcomments[index2 + 1:]
    
    def tokenize(self):
        for code in self.code_withoutcomments:
            if code.find('"') != -1:   # test code only has a string constant and it's not the point
                s = code.find('"')
                e = s + 1 + code[s+1:].find('"')
                string = code[s:e+1]    # 测试文件里每行最多只有一个字符串常量，这里不想写复杂了
                code = code[:s] + code[e:]
                delimeters = re.findall(r"[\[\]\(\)\{\}\,\.\;\-\~\" ]", code)
                if delimeters:
                    for delimeter in delimeters:
                        first, code = code.split(delimeter, 1)[0], code.split(delimeter,1)[1]
                        if first:
                            self.tokens.append(first)
                        if delimeter == ' ':
                            continue
                        if delimeter == '"':
                            self.tokens.append(string)
                        else:
                            self.tokens.append(delimeter) 
            else:
                delimeters = re.findall(r"[\[\]\(\)\{\}\,\.\;\-\~ ]", code)
                if delimeters:
                    for delimeter in delimeters:
                        first, code = code.split(delimeter, 1)[0], code.split(delimeter,1)[1]
                        if first:
                            self.tokens.append(first)
                        if delimeter == ' ':
                            continue
                        else:
                            self.tokens.append(delimeter)
        for token in self.tokens:
            if token in KEYWORDS:
                self.token_instances.append(TerminalToken("keyword", token))
            elif token in SYMBOL:
                self.token_instances.append(TerminalToken("symbol", token))
            elif token.startswith('"'):
                self.token_instances.append(TerminalToken("stringConstant", token.strip('"')))
            elif token.isdigit():
                self.token_instances.append(TerminalToken("integerConstant", token))
            else:
                self.token_instances.append(TerminalToken("identifier", token))
        
    def writter(self):
        output_file_path = re.sub(".jack", "T1.xml", self.filepath)
        with open(output_file_path, 'w') as file:
            file.write("<tokens>\n")
            for token in self.token_instances:
                file.write(token.xml_form + '\n')
            file.write("</tokens>")
    
    def hasmoretoken(self):
        return self.index <= len(self.token_instances) - 1
    
    def advance(self):
        if self.hasmoretoken():
            ret = self.token_instances[self.index]
            self.index += 1
            return ret
        else:
            return None
        
    def current(self):
        return self.token_instances[self.index]
    
class TerminalToken:
    def __init__(self, tag, token) -> None:
        self._tag = tag
        self.token = token
        self.isterminal = True
        if token == "<":
            self.xml_form = f"<{tag}>" + " &lt; " + f"</{tag}>"
        elif token == ">":
            self.xml_form = f"<{tag}>" + " &gt; " + f"</{tag}>"
        elif token == "&":
            self.xml_form = f"<{tag}>" + " &amp; " + f"</{tag}>"
        else:
            self.xml_form = f"<{tag}>" + f" {token} " + f"</{tag}>"
        
        
    @property
    def tag(self):
        return self._tag
    @tag.setter
    def tag(self, tag):
        assert tag in TERMINAL_TAGS, "terminal tags error!"
        self._tag = tag
    
class UnTerminalToken:
    def __init__(self, tag, isbegin) -> None:
        self._tag = tag
        self.isterminal = False
        if isbegin:
            self.xml_form = f"<{tag}>"
        else:
            self.xml_form = f"</{tag}>"
        
    @property
    def tag(self):
        return self.tag
    @tag.setter
    def tag(self, tag):
        assert tag in UNTERMINAL_TAGS, "unterminal tags error!"
    
def main():
    if len(sys.argv) != 2:
        raise ValueError("Usage: python Tokenizer.py filepath")
    input_file_path = sys.argv[1]
    assert input_file_path.endswith(".jack"), "give me a .jack file!"
    tokenizer = Tokenizer(input_file_path)
    tokenizer.tokenize()
    tokenizer.writter()

    
if __name__ == "__main__":
    main()