DATATYPES = ["num", "string", "bool","fp","char"]
KEYWORDS = ["func","repeat","until",'when','either','otherwise','this','void','new','main','return','private','public']
BOOLEAN=[True,False]
RETURN_TYPES=["void","num"]
OPERATORS = ['==','!=','<=','>=','>','<']
LOGICAL_OPERATORS = ['&&','||']
TEMPVAL = {}
CLASSES=[]
DEFS=["num", "string", "bool","fp","char",'func',"enum","class"]
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
            self.increase()
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
            self.decl()
        elif(self.value_part=='func'):
            self.func_def()
        elif(self.value_part=='class'):
            self.class_dec()
        elif(self.value=='enum'):
            self.enum_def()
        else:
            pass
    
    def decl(self):

    
    # def MST(self):