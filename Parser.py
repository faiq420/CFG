DATATYPES = ["num", "string", "bool","fp","char"]
CONST=['int_const','fp_const','str_const','bool_const','char_const']
KEYWORDS = ["func","repeat","until",'when','either','otherwise','this','void','new','main','return','private','public','break','continue','class','try','catch','enum']
BOOLEAN=['True','False']
RETURN_TYPES=["void","num"]
RELATIONAL_OPERATORS = ['==','!=','<=','>=','>','<']
LOGICAL_OPERATORS = ['&&','||']
TEMPVAL = {}
CLASSES=[]
DEFS=["num", "string", "bool","fp","char",'func',"enum","class"]
ACCESS_MODIFIERS=['private','public']
PM = ['+','-']
MD=['*','/']
LOGICAL_OPERATORS = ['&&','||']

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.value_part = None
        self.line_number = 1
        self.class_part=None
        self.next_token
        self.token_index = -1
        self.increase()

    def increase(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.class_part = self.tokens[self.token_index].get("class_part")
            self.value_part = self.tokens[self.token_index].get("value_part")
            self.line_number = self.tokens[self.token_index].get("line#")
            self.next_token = self.tokens[self.token_index+1].get("value_part")
        else:
            self.value_part = None
    
    def raise_error(self, message):
        raise SyntaxError(f"{message} at line {self.line_number}")
    
    def validateVariableName(self):
        if (self.value_part in DATATYPES is not None or self.value_part in KEYWORDS is not None):
            raise NameError("Variable can not be named as Reseserved words.")

    def Start(self):
        if(self.value_part in DEFS):
            self.increase()
            self.defs()
        elif(self.value_part=='void'):
            self.increase()
            if(self.value_part=='main'):
                self.increase()
                self.main_func()
            else:
                self.raise_error(f'Main function is expected instead got {self.value_part}')

    def main_func(self):
        if(self.value_part=='('):
            self.increase()
            self.args()
            if(self.value_part==')'):
                self.increase()
                if(self.value_part=="{"):
                    self.increase()
                    self.MST()
                    self.increase()
                    if(self.value_part=="}"):
                        self.increase()
                        self.defs()
                    else:
                        self.raise_error(f"Expected Closing Brace instead got {self.value_part}")
                else:
                    self.raise_error(f"Expected Opening Brace instead got {self.value_part}")
            else:
                    self.raise_error(f'Expected Closing Bracket )  instead got {self.value_part}')
        else:
            self.raise_error(f'Expected Opening Bracket ( instead got {self.value_part}')

    def defs(self):
        if(self.value_part in DATATYPES):
            self.increase()
            self.decl()
        elif(self.value_part=='func'):
            self.increase()
            self.func_def()
        elif(self.value_part=='class'):
            self.increase()
            self.class_dec()
        elif(self.value=='enum'):
            self.increase()
            self.enum_def()
        else:
            pass

    def args(self):
        if(self.class_part=='Identifier' or self.class_part in CONST):
            self.increase()
            if(self.value_part==','):
                self.increase()
                self.mul_args()
            else:
                pass
        elif(self.next_token==')'):
            self.increase()
            pass
        else:
            self.raise_error(f"Invalid argument passed-> {self.value_part}")
    
    def mul_args(self):
        if(self.class_part=='Identifier' or self.class_part in CONST):
            self.increase()
            if(self.value_part==','):
                self.increase()
                self.mul_args()
            else:
                pass
        elif(self.next_token==')'):
            self.increase()
            pass
        else:
            self.raise_error(f"Invalid argument passed-> {self.value_part}")

    def decl(self):
        if(self.class_part=='Identifier'):
            self.increase()
            self.init()
            self.increase()
            self.mul_decl()
        else:
            self.validateVariableName()
    
    def init(self):
        if(self.value_part=='='):
            self.increase()
            self.S()
            pass
        else:
            self.raise_error(f"Expected =  instead got {self.value_part}")

    def mul_decl(self):
        if(self.value_part==';'):
            self.increase()
            pass
        elif(self.value_part==','):
            self.increase()
            self.decl()
        else:
            self.raise_error(f"Unexpected token {self.value_part}")

    def MST(self):
        if(self.value_part in KEYWORDS or self.class_part=='Identifier'):
            self.SST()
            self.increase()
            self.MST()
        else:
            pass

    def SST(self):
        if(self.value_part=='func'):
            self.fn_def()
            self.increase()
        elif(self.value_part=='when'):
            self.if_else()
            self.increase()
        elif(self.value_part=='until'):
            self.while_st()
            self.increase()
        elif(self.value_part=='repeat'):
            self.for_st()
            self.increase()
        elif(self.class_part=='jump'):
            self.br_cont()
            self.increase()
        elif(self.value_part=='return'):
            self.ret()
            self.increase()
        elif(self.value_part=='class'):
            self.class_dec()
            self.increase()
        elif(self.value_part=='this'):
            self.this_st()
            self.increase()
        elif(self.value_part=='try'):
            self.try_catch()
            self.increase()
        elif(self.value_part=='enum'):
            self.enum_st()
            self.increase()
        elif(self.value_part in ACCESS_MODIFIERS):
            self.attribute_st()
            self.increase()
        elif(self.class_part=="Identifier"):
            self.ids()
            self.increase()
        else:
            pass