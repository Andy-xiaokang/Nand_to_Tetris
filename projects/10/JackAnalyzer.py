from Tokenizer import Tokenizer, TerminalToken, UnTerminalToken
import re
import sys

UNTERMINAL_TAGS = ["class", "classVarDec", "subroutineDec", "parameterList", "subroutineBody", "varDec", 
                   "statements", "letStatement", "ifStatement", "whileStatement", "doStatement",
                   "returnStatement", "expression", "term", "expressionList"]
CLASS_VAR_DEC_TOKEN = ["static", "field"]
SUBROUTINE_DEC_TOKEN = ["constructor", "function", "method"]
STATEMENT_TOKEN = ["let", "if", "while", "do", "return"]
OP_TOKEN = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
UNOP_TOKEN = ['-', '~']


class CompilationEngine:
    def __init__(self, input_filepath) -> None:
        self.filepath = input_filepath
        self.tokenizer = Tokenizer(input_filepath)
        self.tokenizer.tokenize()
        self.complete_tokens = []

    def add(self, token):
        self.complete_tokens.append(token)
        
    def next(self):
        return self.tokenizer.advance()
    
    def current(self) -> TerminalToken:
        return self.tokenizer.current()
    
    def compileClass(self):
        self.add(UnTerminalToken("class", True))  # <class>
        self.add(self.next())  # terminal token class
        self.add(self.next())  # className
        self.add(self.next())  # {
        while self.current().token in CLASS_VAR_DEC_TOKEN:
            self.compileClassVarDec()
        while self.current().token in SUBROUTINE_DEC_TOKEN:
            self.compileSubroutine()
        self.add(self.next())  # }
        self.add(UnTerminalToken("class", False))  # </class>
    
    def compileClassVarDec(self):
        self.add(UnTerminalToken("classVarDec", True))  # <classVarDec>
        self.add(self.next())  # static|field
        self.add(self.next())  # type
        self.add(self.next())  # varName
        while self.current().token == ',':
            self.add(self.next())  # ,
            self.add(self.next())  # varName
        self.add(self.next())  # ;
        self.add(UnTerminalToken("classVarDec", False))  # </classVarDec>
    
    def compileSubroutine(self):
        self.add(UnTerminalToken("subroutineDec", True))  # <subroutineDec>
        self.add(self.next())  # constructor|function|method
        self.add(self.next())  # void|type
        self.add(self.next())  # subroutineName
        self.add(self.next())  # (
        self.compileParameterList()  # parameterList
        self.add(self.next())  # )
        self.compileSubroutineBody()  # subroutineBody
        self.add(UnTerminalToken("subroutineDec", False))  # </subroutineDec>
    
    def compileParameterList(self):
        self.add(UnTerminalToken("parameterList", True))  # <parameterList>
        if self.current().token != ")":
            self.add(self.next())  # type
            self.add(self.next())  # varName
        while self.current().token == ",":
            self.add(self.next())  # ,
            self.add(self.next())  # type
            self.add(self.next())  # varName
        self.add(UnTerminalToken("parameterList", False))  # </parameterList>
    
    def compileSubroutineBody(self):
        self.add(UnTerminalToken("subroutineBody", True))  # <subroutineBody>
        self.add(self.next())  # {
        while self.current().token == 'var':
            self.compileVarDec()  # varDec*
        self.compileStatements()  # statements
        self.add(self.next())  # }
        self.add(UnTerminalToken("subroutineBody", False))  # </subroutineBody>
    
    def compileVarDec(self):
        self.add(UnTerminalToken("varDec", True))  # <varDec>
        self.add(self.next())  # var
        self.add(self.next())  # type
        self.add(self.next())  # varName
        while self.current().token == ',':
            self.add(self.next())  # ,
            self.add(self.next())  # varName
        self.add(self.next())  # ;
        self.add(UnTerminalToken("varDec", False))  # </varDec>
    
    def compileStatements(self):
        self.add(UnTerminalToken("statements", True))  # <statements>
        while self.current().token in STATEMENT_TOKEN:
            token = self.current().token
            if token == "let":
                self.compileLet()
            elif token == "if":
                self.compileIf()
            elif token == "while":
                self.compileWhile()
            elif token == "do":
                self.compileDo()
            elif token == "return":
                self.compileReturn()
        self.add(UnTerminalToken("statements", False))  # </statements>
    
    def compileLet(self):
        self.add(UnTerminalToken("letStatement", True))  # <letStatement>
        self.add(self.next())  # let
        self.add(self.next())  # varName
        if self.current().token == '[':
            self.add(self.next())  # if [ add [
            self.compileExpression()  # expression
            self.add(self.next())  # ]
        self.add(self.next())  # =
        self.compileExpression() # expression
        self.add(self.next())  # ;
        self.add(UnTerminalToken("letStatement", False))  # </letStatement> 
        
    def compileIf(self):
        self.add(UnTerminalToken("ifStatement", True))  # <ifStatement>
        self.add(self.next())  # if
        self.add(self.next())  # (
        self.compileExpression()  # expression
        self.add(self.next())  # )
        self.add(self.next())  # {
        self.compileStatements()  # statements
        self.add(self.next())  # }
        if self.current().token == 'else':
            self.add(self.next())  # else
            self.add(self.next())  # {
            self.compileStatements()  # statements
            self.add(self.next())  # }
        self.add(UnTerminalToken("ifStatement", False))  # </ifStatement>
    
    def compileWhile(self):
        self.add(UnTerminalToken("whileStatement", True))  # <whileStatement>
        self.add(self.next())  # while
        self.add(self.next())  # (
        self.compileExpression()  # expression
        self.add(self.next())  # )
        self.add(self.next())  # {
        self.compileStatements()  # statements
        self.add(self.next())  # }
        self.add(UnTerminalToken("whileStatement", False))  # </whileStatement>
    
    def compileDo(self):
        self.add(UnTerminalToken("doStatement", True))  # <doStatement>
        self.add(self.next())  # do
        self.add(self.next())  # subroutinename|classname|varname
        if self.current().token == '(':
            self.add(self.next())  # (
            self.compileExpressionList()  # ExpressionList
            self.add(self.next())  # )
        elif self.current().token == '.':
            self.add(self.next())  # .
            self.add(self.next())  # subroutineName
            self.add(self.next())  # (
            self.compileExpressionList()  # ExpressionList
            self.add(self.next())  # )
        self.add(self.next())  # ;
        self.add(UnTerminalToken("doStatement", False))  # </doStatement>
    
    def compileReturn(self):
        self.add(UnTerminalToken("returnStatement", True))  # <returnStatement>
        self.add(self.next())  # return
        if self.current().token != ';':
            self.compileExpression()  # expression
        self.add(self.next())  # ;
        self.add(UnTerminalToken("returnStatement", False))  # </returnStatement>
    
    def compileExpression(self):
        self.add(UnTerminalToken("expression", True))  # <expression>
        self.compileTerm()
        while self.current().token in OP_TOKEN:
            self.add(self.next())  # op
            self.compileTerm()
        self.add(UnTerminalToken("expression", False))  # </expression>
    
    def compileTerm(self):
        self.add(UnTerminalToken("term", True))  # <term>
        if self.current().token == '(':
            self.add(self.next())  # (
            self.compileExpression()  # expression
            self.add(self.next())  # )
        elif self.current().token in UNOP_TOKEN:
            self.add(self.next())  # unaryop
            self.compileTerm()
        else:
            self.add(self.next())  # read next 
            if self.current().token == '[':
                self.add(self.next())  # [
                self.compileExpression()  # expression
                self.add(self.next())  # ]
            elif self.current().token == '(':
                self.add(self.next())  # (
                self.compileExpressionList()  # ExpressionList
                self.add(self.next())  # )
            elif self.current().token == '.':
                self.add(self.next())  # .
                self.add(self.next())  # subroutineName
                self.add(self.next())  # (
                self.compileExpressionList()  # ExpressionList
                self.add(self.next())  # )
        self.add(UnTerminalToken("term", False))  # </term> 
    
    def compileExpressionList(self):
        self.add(UnTerminalToken("expressionList", True))  # <expressionList>
        if self.current().token != ')':
            self.compileExpression()  # expression
            while self.current().token == ',':
                self.add(self.next())  # ,
                self.compileExpression()  # expression*
        self.add(UnTerminalToken("expressionList", False))  # </expressionList>
        
    def writer(self):
        output_filepath = re.sub(".jack", "1.xml", self.filepath) 
        with open(output_filepath, 'w') as file:
            for token_instance in self.complete_tokens:
                file.write(token_instance.xml_form + '\n')
    
def main():
    if len(sys.argv) != 2:
        raise ValueError("Usage: python Tokenizer.py filepath")
    input_file_path = sys.argv[1]
    assert input_file_path.endswith(".jack"), "give me a .jack file!"
    compilation_engine = CompilationEngine(input_file_path)
    compilation_engine.compileClass()
    compilation_engine.writer()
    
if __name__ == "__main__":
    main()