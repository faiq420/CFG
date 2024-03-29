# Lexer/tokenizer implementation
import re as reg



def tokenize(program):
    tokens = reg.findall(
        r'true|false|[a-zA-Z_][a-zA-Z0-9_]*|[a-zA-Z]+|[0-9]+|[+-?][0-9]+.[0-9]+|<=|>=|==|!=|".*"|;|\S', program)
    print(tokens,len(tokens))
    return tokens

# Parser implementation
DATATYPES = ["num", "string", "bool","fp"]
KEYWORDS = ["func","repeat","until",'when','either','otherwise','this','void','new','main','return','private','public']
BOOLEAN=[True,False]
RETURN_TYPES=["void","num"]
OPERATORS = ['==','!=','<=','>=','>','<']
LOGICAL_OPERATORS = ['&','|']
TEMPVAL = {}
CLASSES=[]

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        # self.next_token;
        self.token_index = -1
        self.line_number = 1
        self.increase()

    def increase(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index].get("value_part")
            self.line_number = self.tokens[self.token_index].get("line#")
            # self.next_token = self.tokens[self.token_index+1].get("value_part")
        else:
            self.current_token = None

    def conditionValue(self):
        self.validateVariableName()
        if TEMPVAL[self.current_token] is None:
            raise SyntaxWarning("Variable not assigned a value!")
        else:
            return TEMPVAL[self.current_token]
        
    def raise_error(self, message):
        raise SyntaxError(f"{message} at line {self.line_number}")

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
            elif (self.current_token == 'when'):
                self.increase()
                self.parseConditions()
            elif self.current_token == 'class':
                self.increase()
                self.parseClass()
            elif self.current_token == 'return':
                self.increase();
                self.parseReturnSt()
            elif self.current_token=='}':
                break  
            else:
                self.raise_error(f"Invalid DataType {self.current_token}")

    def parseReturnSt(self):
        self.increase()
        while(self.current_token!=';'):
            self.increase()
        self.increase()
        print("VALID RETURN STATEMENT")

    def parseClass(self):
        # Parse class definition
        class_name = self.current_token
        self.increase()
        curr_tok=self.current_token
        self.increase()
        curr_tok+=self.current_token
        self.increase()
        if self.current_token == '{':
            self.increase()
            self.body()
            if self.current_token == '}':
                self.increase()
            else:
                self.raise_error("Expected '}'")
        else:
            self.raise_error("Expected '{'")
        print("VALID CLASS PARSING")

    def parseConditions(self):
        Terminate = False
        while (not Terminate):
            if self.current_token == "(":
                self.increase()
                self.checkConditions()          
                if (self.current_token == '{'):
                    self.increase()
                    self.body() 
                    self.increase()
                    while(self.current_token == 'either'):
                        self.increase()
                        self.parseEitherCondition()
                    if(self.current_token == 'otherwise'):
                        self.increase()
                        self.parseOtherwiseCondition()
                    Terminate=True
                else:
                    self.raise_error("Unexpected identifier. Expected '{' ")
            else:
                self.raise_error(f"Invalid Identifier Expected '(' but given '{self.current_token}'")
        print("VALID WHEN CONDITION")

    def parseOtherwiseCondition(self):
        Terminate = False
        while (not Terminate):
            if (self.current_token == '{'):
                    self.increase()
                    self.body() 
                    self.increase()
                    Terminate=True
            else:
                self.raise_error("Unexpected identifier. Expected '{' ")
        print("VALID OTHERWISE CONDITION")

    def parseEitherCondition(self):
        Terminate = False
        while (not Terminate):
            if self.current_token == "(":
                # self.conditionValue()
                self.increase()
                self.checkConditions()          
                if (self.current_token == '{'):
                    self.increase()
                    self.body() 
                    self.increase()
                    Terminate=True
                else:
                    self.raise_error("Unexpected identifier. Expected '{' ")
            else:
                self.raise_error(f"Invalid Identifier Expected '(' but given '{self.current_token}'")
        print("VALID EITHER CONDITION")

    def parseFunction(self):
        Terminate = False
        while (not Terminate):
            newToken = self.current_token
            if(reg.match(r'[a-zA-Z]+',newToken)):
                # self.increase()
                if self.current_token =='void' or self.current_token in DATATYPES:
                    self.increase()
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
                        self.raise_error("Unexpected identifier. Expected '{' ")
                else:
                    self.raise_error(f"Invalid Identifier Expected '(' but given '{self.current_token}'")
            else:
                self.raise_error("Invalid Function Name")
        print("VALID FUNCTION")

    def checkFuncParameters(self):
        Terminate = False
        while self.current_token!=')':
            if self.current_token in DATATYPES:
                self.increase()
                newToken =  self.current_token
                self.validateVariableName()
                if(reg.match(r'[a-zA-Z]+',newToken)):
                    self.increase()
                    if self.current_token == ')':
                        Terminate = True
                    elif (self.current_token == ","):
                        self.increase()
                        continue
                else:
                    self.raise_error("Invalid Parameter")
            else:
                self.raise_error("Invalid Datatype")

    def parseUntilLoop(self):
        Terminate = False
        while (not Terminate):
            if self.current_token == "(":
                # self.conditionValue()
                self.increase()
                self.checkConditions()          
                if (self.current_token == '{'):
                    self.increase()
                    self.body() 
                    self.increase()
                    Terminate=True
                else:
                    self.raise_error("Unexpected identifier. Expected '{' ")
            else:
                self.raise_error(f"Invalid Identifier Expected '(' but given '{self.current_token}'")
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
                        self.raise_error("Unexpected identifier  Expected '{' ")
                else:
                    self.raise_error("Unexpected identifier")
            else:
                self.raise_error(f"Invalid Identifier Expected '(' but given '{self.current_token}'")
        print("VALID REPEAT LOOP")

    def body(self):
        while (self.current_token != '}'):
            self.parse()

    def validateVariableName(self):
        if (self.current_token in DATATYPES is not None or self.current_token in KEYWORDS is not None):
            raise NameError("Variable can not be named as Reseserved words.")

    def checkLoopInitialization(self):
        if(self.current_token == "num"):
            local = self.current_token
            self.increase()
            local += self.current_token
            self.validateVariableName()
            self.increase()
            local += self.current_token
            self.increase()
            local += self.current_token
            self.increase()
            local += self.current_token
            if(reg.match(r"num\s*[a-zA-Z]=[0-9]+;",local) is None):
                self.raise_error("Invalid Identifier")
        else:
            self.raise_error("Invalid Identifier")

    def checkRepeatCondition(self):
        cond = self.current_token
        self.increase()
        if(self.current_token in OPERATORS):
            cond += self.current_token
            self.increase()
        else:
            self.raise_error()
        cond += self.current_token
        self.increase()
        cond += self.current_token
        self.increase()
        if(reg.match(r"[a-zA-Z]+<|>|<=|>=|==|!=[0-9]+;$",cond) is None):
            self.raise_error("Invalid Condition")
        
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

    def checkMultiConditions(self):
        condition=self.current_token
        self.increase()
        condition+=self.current_token
        self.conditionValue()
        self.increase()
        if(self.current_token in OPERATORS):
            condition += self.current_token
            self.increase()
        else:
            self.raise_error()
        condition += self.current_token
        self.increase()    
        print(condition)

    def checkConditions(self):
        if(self.current_token != "True" and self.current_token != 1 and self.current_token != "not"):
            cond = self.current_token
            self.conditionValue()
            self.increase()
            if(self.current_token in OPERATORS):
                cond += self.current_token
                self.increase()
            else:
                self.raise_error()
            cond += self.current_token
            self.increase()
            while(self.current_token in LOGICAL_OPERATORS is not None):
                self.checkMultiConditions()
            cond += self.current_token
            self.increase()
            if(reg.match(r"[a-zA-Z]+<|>|<=|>=|==|!=[0-9]+[)]$",cond) is None):
                self.raise_error("Wrong Condition")

        elif(self.current_token == "True" or self.current_token == 1):
            cond = self.current_token
            self.increase()
            cond += self.current_token
            self.increase()

        elif(self.current_token == "not"):
            cond = self.current_token
            self.increase()
            cond += self.current_token
            self.increase()
            cond += self.current_token
            self.increase()


    def declaration(self):
        Type = None
        re = False
        key = None
        if(self.current_token in DATATYPES and not re):
            Type = self.current_token
        Terminate = False
        while (not Terminate):
            if(self.current_token in DATATYPES):
                if(re and self.current_token != Type):
                    self.raise_error("Mismatched Data types")
                self.increase()
                if Type == 'num':
                    key = self.current_token
                    temp = {key:None}
                    TEMPVAL.update(temp) 
                if reg.match(r"[a-zA-Z_][a-zA-Z0-9_]*", self.current_token) is not None:
                    self.validateVariableName()
                    self.increase()
                    # if(Type != 'repeat' and self.tokens[len(self.tokens)-1] != ';'):
                    #     self.raise_error("Termination not detected")
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
                            if(reg.match(r'True|False',self.current_token) is None):
                                raise ValueError(f"Invalid value for type {Type}")
                        if (Type == "num"):
                            if(reg.match(r'[0-9]+',self.current_token) is None):
                                raise ValueError(f"Invalid value for type {Type}")
                            else:
                                TEMPVAL[key]=self.current_token
                        if (Type == "fp"):
                            if(reg.match(r'^[-+]?\d+(\.\d+)?([eE][-+]?\d+)?$',self.current_token) is None):
                                raise ValueError(f"Invalid value for type {Type}")
                        if (Type == "string"):
                            if(reg.match(r'".*"',self.current_token) is None):
                                raise ValueError(f"Invalid value for type {Type}")
                        self.increase()
                        if(self.current_token == ';'):
                            Terminate = True
                            self.increase()
                    else:
                        self.raise_error("Invalid Identifier")
                else:
                    self.raise_error("Variable naming violation")
        print("VALID")

# fp c=+077777.88;
# fp a=78.9;
# num x,num y,num z  = 0;
# #fp x = abc;#
# num x;
# #string % = abc;#
# string text = "10";
# func add(num a,num b){
#   num c = 5;
#     repeat(num j = 0 ; j <= 10 ;j=j + 2){
#         num random = 0;
#         fp algebra =-5.5;
#         until ( random <= 9 ) {
#             bool a = True;
#         }
#     } 
# }