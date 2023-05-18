# Lexer/tokenizer implementation
import re as reg



def tokenize(program):
    tokens = reg.findall(
        r'true|false|[a-zA-Z_][a-zA-Z0-9_]*|[a-zA-Z]+|[0-9]+|[+-]*?[0-9]+.[0-9]+|<=|>=|==|!=|".*"|;|\S', program)
    print(tokens)
    return tokens

# Parser implementation

DATATYPES = ["num", "string", "bool","fp"]
OPERATORS = ['==','!=','<=','>=']

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.token_index = -1
        self.increase()

    def increase(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    def parse(self):
        while (self.current_token):
            if (self.current_token in DATATYPES):
                self.declaration()
            elif (self.current_token == 'repeat'):
                self.increase()
                self.parseRepeatLoop()
            elif (self.current_token == 'until'):
                self.increase()
                self.parseUntilLoop()
            elif (self.current_token == 'func'):
                self.increase()
                self.parseFunction()
            elif self.current_token=='}':
                break  
            else:
                raise SyntaxError(f"Invalid DataType {self.current_token}")

    def parseFunction(self):
        Terminate = False
        while (not Terminate):
            newToken = self.current_token
            if(reg.match(r'[a-zA-Z]+',newToken)):
                self.increase()
                if self.current_token == "(":
                    self.increase()
                    self.checkFuncParameters()
                    self.increase()
                    if (self.current_token == '{'):
                        self.increase()
                        self.body() 
                        self.increase()
                        Terminate=True
                    else:
                        raise SyntaxError("Unexpected identifier. Expected '{' ")
                else:
                    raise SyntaxError(f"Invalid Identifier Expected '(' but given '{self.current_token}'")
            else:
                raise SyntaxError("Invalid Function Name")

    def checkFuncParameters(self):
        Terminate = False
        while self.current_token!=')':
            if self.current_token in DATATYPES:
                self.increase()
                newToken =  self.current_token
                if(reg.match(r'[a-zA-Z]+',newToken)):
                    self.increase()
                    if self.current_token == ')':
                        Terminate = True
                    elif (self.current_token == ","):
                        self.increase()
                        continue
                else:
                    raise SyntaxError("Invalid Parameter")
            else:
                raise SyntaxError("Invalid Datatype")
        print("VALID FUNCTION")

    def parseUntilLoop(self):
        Terminate = False
        while (not Terminate):
            if self.current_token == "(":
                self.increase()
                self.checkUntilCondition()          
                if (self.current_token == '{'):
                    self.increase()
                    self.body() 
                    self.increase()
                    Terminate=True
                else:
                    raise SyntaxError("Unexpected identifier. Expected '{' ")
            else:
                raise SyntaxError(f"Invalid Identifier Expected '(' but given '{self.current_token}'")
        print("VALID UNTIL LOOP")
                

    def parseRepeatLoop(self):
        Terminate = False
        while (not Terminate):
            if self.current_token == "(":
                self.increase()
                self.checkLoopInitialization()
                self.increase()
                self.checkRepeatCondition()
                newToken = self.checkINCDEC()
                if (reg.match(r'[a-zA-Z]=[a-zA-Z][+-][0-9][)]$', newToken)):
                    if (self.current_token == '{'):
                        self.increase()
                        self.body() 
                        self.increase()
                        Terminate=True
                    else:
                        raise SyntaxError("Unexpected identifier  Expected '{' ")
                else:
                    raise SyntaxError("Unexpected identifier")
            else:
                raise SyntaxError(f"Invalid Identifier Expected '(' but given '{self.current_token}'")
        print("VALID REPEAT LOOP")

    def body(self):
        while (self.current_token != '}'):
            self.parse()

    def checkLoopInitialization(self):
        if(self.current_token == "num"):
            local = self.current_token
            self.increase()
            local += self.current_token
            self.increase()
            local += self.current_token
            self.increase()
            local += self.current_token
            self.increase()
            local += self.current_token
            if(reg.match(r"num\s*[a-zA-Z]=[0-9]+;",local) is None):
                raise SyntaxError("Invalid Identifier")
        else:
            raise SyntaxError("Invalid Identifier")

    def checkRepeatCondition(self):
        cond = self.current_token
        self.increase()
        if(self.current_token in OPERATORS):
            cond += self.current_token
            self.increase()
        else:
            raise SyntaxError()
        cond += self.current_token
        self.increase()
        cond += self.current_token
        self.increase()
        if(reg.match(r"[a-zA-Z]+<|>|<=|>=|==|!=[0-9]+;$",cond) is None):
            raise SyntaxError("Invalid Condition")
        
    def checkINCDEC(self):
        NewToken = self.current_token
        self.increase()
        NewToken += self.current_token
        self.increase()
        NewToken += self.current_token
        self.increase()
        NewToken += self.current_token
        self.increase()
        NewToken += self.current_token
        self.increase()
        NewToken += self.current_token
        self.increase()
        return NewToken

    def checkUntilCondition(self):
        cond = self.current_token
        self.increase()
        if(self.current_token in OPERATORS):
            cond += self.current_token
            self.increase()
        else:
            raise SyntaxError()
        cond += self.current_token
        self.increase()
        cond += self.current_token
        self.increase()
        if(reg.match(r"[a-zA-Z]+<|>|<=|>=|==|!=[0-9]+[)]$",cond) is None):
            raise SyntaxError("Wrong Condition")

    def declaration(self):
        Type = None
        re = False
        if(self.current_token in DATATYPES and not re):
            Type = self.current_token
        Terminate = False
        while (not Terminate):
            if(self.current_token in DATATYPES):
                if(re and self.current_token != Type):
                    raise SyntaxError("Mismatched Data types")
                self.increase()
                if reg.match(r"[a-zA-Z_][a-zA-Z0-9_]*", self.current_token) is not None:
                    self.increase()
                    # if(Type != 'repeat' and self.tokens[len(self.tokens)-1] != ';'):
                    #     raise SyntaxError("Termination not detected")
                    if(self.current_token == ';'):
                            Terminate = True
                            self.increase()
                    elif self.current_token == ',':
                        self.increase()
                        re = True
                        continue
                    elif self.current_token == '=':
                        self.increase()
                        if (Type == "bool"):
                            if(reg.match(r'true|false',self.current_token) is None):
                                raise ValueError(f"Invalid value for type {Type}")
                        if (Type == "num"):
                            if(reg.match(r'[0-9]+',self.current_token) is None):
                                raise ValueError(f"Invalid value for type {Type}")
                        if (Type == "fp"):
                            if(reg.match(r'[+-]*?[0-9]+.[0-9]+',self.current_token) is None):
                                raise ValueError(f"Invalid value for type {Type}")
                        if (Type == "string"):
                            if(reg.match(r'".*"',self.current_token) is None):
                                raise ValueError(f"Invalid value for type {Type}")
                        self.increase()
                        if(self.current_token == ';'):
                            Terminate = True
                            self.increase()
                    else:
                        raise SyntaxError("Invalid Identifier")
                else:
                    raise SyntaxError("Variable naming violation")
        print("VALID")
