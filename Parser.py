DATATYPES = ["num", "string", "bool", "fp", "char"]
CONST = ['int_const', 'FP_const', 'str_const', 'bool_const', 'char_const']
KEYWORDS = ["func", "repeat", "until", 'when', 'either', 'otherwise', 'this', 'void', 'new',
            'main', 'return', 'private', 'public', 'break', 'continue', 'class', 'try', 'catch', 'enum']
BOOLEAN = ['True', 'False']
RETURN_TYPES = ["void", "num","bool","string"]
RELATIONAL_OPERATORS = ['==', '!=', '<=', '>=', '>', '<']
LOGICAL_OPERATORS = ['&&', '||']
DEFS = ["num", "string", "bool", "fp", "char", 'func', "enum", "class"]
ACCESS_MODIFIERS = ['private', 'public']
PM = ['+', '-']
MD = ['*', '/']
LOGICAL_OPERATORS = ['&&', '||']
TEMPVAL = {}
CLASSES = []


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.value_part = self.tokens[0].get("value_part") if(len(tokens)) else None
        self.line_number = 1
        self.class_part = self.tokens[0].get("class_part") if(len(tokens)) else None
        self.token_index = 0
        self.next_token=self.tokens[self.token_index+1].get("value_part") if(len(tokens)) else None

    def increase(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.class_part = self.tokens[self.token_index].get("class_part")
            self.value_part = self.tokens[self.token_index].get("value_part")
            self.line_number = self.tokens[self.token_index].get("line#")
            if self.token_index < len(self.tokens)-2:

                self.next_token = self.tokens[self.token_index+1].get("value_part")
            else:
                self.next_token= None
        else:
            self.value_part = None

    def raise_error(self, message):
        raise SyntaxError(f"{message} at line {self.line_number}")

    def validateVariableName(self):
        if (self.value_part in DATATYPES is not None or self.value_part in KEYWORDS is not None):
            raise NameError("Variable can not be named as Reseserved words")

    def openingBracketErr(self):
        self.raise_error(f"Expected ( but instead got {self.value_part}")

    def closingBracketErr(self):
        self.raise_error(f"Expected ) but instead got {self.value_part}")

    def openingBraceErr(self):
        self.raise_error(
            f"Expected opening brace but instead got {self.value_part}")

    def closingBraceErr(self):
        self.raise_error(
            f"Expected closing brace but instead got {self.value_part}")

    def invalidArgumentErr(self):
        self.raise_error(f"Invalid argument passed-> {self.value_part}")

    def DataTypeErr(self):
        self.raise_error(
            f"Expected DATATYPE but instead got {self.value_part}"
        )

    def SemiColonErr(self):
        self.raise_error(
            f"Expected semicolon but instead got {self.value_part}"
        )

    def colonErr(self):
        self.raise_error(
            f"Expected colon but instead got {self.value_part}"
        )

    def commaErr(self):
        self.raise_error(
            f"Expected comma but instead got {self.value_part}"
        )

    def EqualsToErr(self):
        self.raise_error(
            f"Expected Assignment Operator instead got {self.value_part}")

    def invalid_token(self):
        self.raise_error(f"Invalid token -> {self.value_part}")

    def indexationError(self,b):
        self.raise_error(f"Expected {b} instead got {self.value_part}")

    def Start(self):
        if (self.value_part in DEFS):
            self.defs()
        if (self.value_part == 'void'):
            self.increase()
            if (self.value_part == 'main'):
                self.increase()
                self.main_func()
            else:
                self.raise_error(
                    f'Main function is expected instead got {self.value_part}')

    def main_func(self):
        if (self.value_part == '('):
            self.increase()
            self.args()
            if (self.value_part == ')'):
                self.increase()
                if (self.value_part == "{"):
                    self.increase()
                    self.MST()
                    if (self.value_part == "}"):
                        self.increase()
                        print("COMPLETED MAIN FUNCTION")
                        self.defs()
                    else:
                        self.closingBraceErr()
                else:
                    self.openingBraceErr()
            else:
                self.closingBracketErr()
        else:
            self.openingBracketErr()

    def defs(self):
        if (self.value_part in DATATYPES):
            self.decl()
            self.defs()
        elif (self.value_part == 'func'):
            # self.increase()
            self.fn_def()
            self.defs()
        elif (self.value_part == 'class'):
            self.increase()
            self.class_dec()
            self.defs()
        elif (self.value_part == 'enum'):
            self.increase()
            self.enum_def()
            self.defs()
        else:
            pass

    def args(self):
        if (self.class_part == 'Identifier' or self.class_part in CONST):
            self.increase()
            if (self.value_part == ','):
                self.increase()
                self.mul_args()
            else:
                pass
        elif (self.value_part == ')'):
            # self.increase()
            pass
        else:
            # self.raise_error(f"Invalid argument passed-> {self.value_part}")
            pass

    def mul_args(self):
        if (self.class_part == 'Identifier' or self.class_part in CONST):
            self.increase()
            if (self.value_part == ','):
                self.increase()
                self.mul_args()
            else:
                pass
        elif (self.next_token == ')'):
            self.increase()
            pass
        else:
            self.raise_error(f"Invalid argument passed-> {self.value_part}")

    def params(self):
        if (self.value_part in DATATYPES):
            self.increase()
            if (self.class_part == "Identifier"):
                self.increase()
                self.mul_params()
            else:
                self.validateVariableName()
        else:
            pass

    def mul_params(self):
        if (self.value_part == ','):
            self.increase()
            self.params()
        else:
            pass

    def decl(self):
        if (self.value_part in DATATYPES):
            self.increase()
            if (self.class_part == 'Identifier'):
                self.increase()
                self.init()
                self.mul_decl()
            else:
                self.validateVariableName()
        else:
            self.invalidArgumentErr()

    def init(self):
        if (self.value_part == '='):
            self.increase()
            self.S()
        else:
            self.EqualsToErr()

    def mul_decl(self):
        if (self.value_part == ';'):
            self.increase()            
        elif (self.value_part == ','):
            self.increase()
            self.decl()
        else:
            self.raise_error(f"Unexpected token {self.value_part}")

    def body(self):
        self.MST()

    def MST(self):
        if (self.value_part in KEYWORDS or self.value_part in DATATYPES):
            self.SST()
            self.MST()
        else:
            pass

    def SST(self):
        if (self.value_part == 'func'):
            self.fn_def()
        elif (self.value_part == 'when'):
            self.if_else()
        elif (self.value_part == 'until'):
            self.while_st()
        elif (self.value_part == 'repeat'):
            self.for_st()
        elif (self.class_part == 'jump'):
            self.br_cont()
        elif (self.value_part == 'return'):
            self.ret()
        elif (self.value_part == 'class'):
            self.class_dec()
        elif (self.value_part == 'this'):
            self.this_st()
        elif (self.value_part == 'try'):
            self.try_catch()
        elif (self.value_part == 'enum'):
            self.enum_st()
        elif (self.value_part in ACCESS_MODIFIERS):
            self.attribute_st()
        elif (self.class_part == "Identifier"):
            self.ids()
        elif (self.value_part in DATATYPES):
            self.decl()
        else:
            pass

    def this_st(self):
        self.increase()
        if(self.value_part=='.'):
            self.increase()
            if(self.class_part=="Identifier"):
                self.increase()
                if(self.value_part=='='):
                    self.increase()
                    self.S()
                    if(self.value_part==";"):
                        self.increase()
                        print("VALID THIS STATEMENT")
                else:
                    self.EqualsToErr()
            else:
                self.invalidArgumentErr()
        else:
            self.invalid_token()

    def if_else(self):
        self.increase()
        if (self.value_part == '('):
            self.increase()
            self.S()
            if (self.value_part == ')'):
                self.increase()
                if (self.value_part == '{'):
                    self.increase()
                    self.body()
                    if (self.value_part == '}'):
                        self.increase()
                        print("VALID IF CONDITION")
                        if (self.value_part == 'either'):
                            self.increase()
                            self.either()
                        if (self.value_part == 'otherwise'):
                            self.increase()
                            self.otherwise()
                        else:
                            print('VALID IF CONDITION')
                            pass
                    else:
                        self.closingBraceErr()
            else:
                self.closingBracketErr()
        else:
            self.openingBracketErr()

    def either(self):
        if (self.value_part == '('):
            self.increase()
            self.S()
            if (self.value_part == ')'):
                self.increase()
                if (self.value_part == '{'):
                    self.increase()
                    self.body()
                    if (self.value_part == '}'):
                        self.increase()
                        print("VALID ELSE IF CONDITION")
                        if (self.value_part == "either"):
                            self.increase()
                            self.either()
                    else:
                        self.closingBraceErr()
                else:
                    self.openingBraceErr()
            else:
                self.closingBracketErr()
        else:
            self.openingBracketErr()

    def otherwise(self):
        if (self.value_part == '{'):
            self.increase()
            self.body()
            if (self.value_part == '}'):
                self.increase()
                pass
            else:
                self.closingBraceErr()
        else:
            self.openingBraceErr()

    def while_st(self):
        self.increase()
        if (self.value_part == '('):
            self.increase()
            self.S()
            if (self.value_part == ')'):
                self.increase()
                if (self.value_part == '{'):
                    self.increase()
                    self.body()
                    if (self.value_part == '}'):
                        self.increase()
                        print("VALID WHILE LOOP")
                    else:
                        self.closingBraceErr()
                else:
                    self.openingBraceErr()
            else:
                self.closingBracketErr()

        else:
            self.openingBracketErr()

    def ids(self):
        self.increase()
        self.identifier()

    def inc_dec(self):
        if(self.class_part=="Identifier"):
            self.increase()
            if(self.value_part=="="):
                self.increase()
                self.S()
                print(self.value_part)
                print("VALID INCREMENT/DECREMENT")
            else:
                self.EqualsToErr()
        else:
            self.invalidArgumentErr()

    def for_st(self):
        self.increase()
        if (self.value_part == '('):
            self.increase()
            if (self.value_part == 'num'):
                self.decl()
                self.S()
                if (self.value_part == ';'):
                    self.increase()
                    self.inc_dec()
                    if (self.value_part == ')'):
                        self.increase()
                        if (self.value_part == '{'):
                            self.increase()
                            self.body()
                            if (self.value_part == '}'):
                                self.increase()
                                print("VALID FOR LOOP")
                                pass
                            else:
                                self.closingBraceErr()
                        else:
                            self.openingBraceErr()
                    else:
                        self.closingBracketErr()
                else:
                    self.SemiColonErr()
            else:
                self.DataTypeErr()
        else:
            self.openingBracketErr()

    def ret(self):
        self.increase()
        if(self.value_part!=";"):
            self.S()
            if (self.value_part == ';'):
                self.increase()
                print("VALID RETURN STATEMENT")
            else:
                self.SemiColonErr()
        else:
            self.increase()
            print("VALID RETURN STATEMENT")

    def br_cont(self):
        self.increase()
        if (self.value_part == ';'):
            self.increase()
            print("VALID JUMP STATEMENT")
        else:
            self.SemiColonErr()

    def try_catch(self):
        self.increase()
        if (self.value_part == '{'):
            self.increase()
            self.body()
            if (self.value_part == '}'):
                self.increase()
                if (self.value_part == "catch"):
                    self.increase()
                    if (self.value_part == '('):
                        self.increase()
                        if (self.class_part == "Identifier"):
                            self.increase()
                            if (self.value_part == ')'):
                                self.increase()
                                if (self.value_part == '{'):
                                    self.increase()
                                    self.body()
                                    if (self.value_part == '}'):
                                        self.increase()
                                        print("VALID TRY CATCH")
                                        # pass
                                    else:
                                        self.closingBraceErr()
                                else:
                                    self.openingBraceErr()
                            else:
                                self.closingBracketErr()
                        else:
                            self.raise_error(f"Expected Identifier")
                    else:
                        self.openingBracketErr()
                else:
                    self.raise_error(f"Expected catch statement")
            else:
                self.closingBraceErr()
        else:
            self.openingBraceErr()

    def fn_def(self):
        self.increase()
        if (self.value_part == "virtual"):
            self.increase()
        if (self.value_part in RETURN_TYPES):
            self.increase()
            if (self.class_part == "Identifier"):
                self.increase()
                if (self.value_part == '('):
                    self.increase()
                    self.params()
                    if (self.value_part == ')'):
                        self.increase()
                        if (self.value_part == '{'):
                            self.increase()
                            self.body()
                            if (self.value_part == '}'):
                                self.increase()
                                print("VALID FUNCTION")
                            else:
                                self.closingBraceErr()
                        else:
                            self.openingBraceErr()
                    else:
                        self.closingBracketErr()
                else:
                    self.openingBracketErr()
            else:
                self.validateVariableName()

        else:
            self.raise_error("Function return type expected.")

    def enum_st(self):
        self.increase()
        if (self.class_part == "Identifier"):
            self.increase()
            if (self.value_part == '='):
                self.increase()
                if (self.value_part == '{'):
                    self.key_st()
                    if (self.value_part == '}'):
                        self.increase()
                        print("VALID ENUMERATION")
                    else:
                        self.closingBraceErr()
                else:
                    self.openingBraceErr()
            else:
                self.EqualsToErr()
        else:
            self.validateVariableName()

    def key_st(self):
        self.increase()
        if (self.class_part == "Identifier"):
            self.increase()
            if (self.value_part == '='):
                self.increase()
                self.S()
                # self.increase()
                if (self.value_part == ','):
                    self.key_st()
                else:
                    pass
            else:
                self.EqualsToErr()
        else:
            self.validateVariableName()

    def mul_key_st(self):
        if(self.value_part==','):
            self.key_st()
        else:
            pass

    def class_dec(self):
        self.increase()
        self.classList()
        if (self.value_part == '{'):
            self.increase()
            self.body()
            if (self.value_part == '}'):
                self.increase()
                pass
            else:
                self.closingBraceErr()
        else:
            self.openingBraceErr()

    def classList(self):
        self.increase()
        if (self.class_part == "Identifier"):
            self.classDiv()
        else:
            self.validateVariableName()

    def classDiv(self):
        self.increase()
        if (self.value_part == '('):
            self.inh()
        elif (self.value_part == ':'):
            if (self.value_part in ACCESS_MODIFIERS):
                self.increase()
                if (self.class_part == "Identifier"):
                    self.increase()
                    pass
                else:
                    self.validateVariableName()
        else:
            self.invalid_token()

    def inh(self):
        self.increase()
        if (self.value_part == ')'):
            self.increase()
            pass
        elif (self.class_part == 'Identifier'):
            self.increase()
            self.args()
            if (self.value_part == ')'):
                self.increase()
                pass
            else:
                self.closingBracketErr()
        else:
            self.colonErr()

        self.increase()
        if (self.class_part == "Identifier"):
            self.increase()
            self.identifier()
        else:
            self.validateVariableName()

    def identifier(self):
        if(self.value_part=="="):
            self.assign_st()
        elif(self.value_part=="("):
            self.bracket_exp()
        elif(self.class_part=="Identifier"):
            self.obj_dec()
        else:
            self.indexationError()

    def assign_st(self):
        self.increase()
        if (self.value_part == '='):
            self.increase()
            self.S()
            if (self.value_part == ';'):
                self.increase()
                pass
            else:
                self.SemiColonErr()
        else:
            self.EqualsToErr()

    def bracket_exp(self):
        self.increase()
        self.constructor_def()
        self.fn_call()

    def constructor_def(self):
        if(self.class_part=="DataType"):
            self.params()
            self.increase()
            if(self.value_part=="{"):
                self.increase()
                self.body()
                if(self.value_part=="}"):
                    self.increase()
                    print("VALID PARAMETERIZED CONSTRUCTOR DEFINITION")
                else:
                    self.closingBraceErr()
            else:
                self.openingBraceErr()
        else:
            self.fn_call()

    def obj_dec(self):
        self.increase()
        if (self.class_part == "Identifier"):
            self.increase()
            if (self.value_part == '='):
                self.increase()
                if (self.value_part in KEYWORDS):
                    if (self.class_part == "Identifier"):
                        self.increase()
                        if (self.value_part == '('):
                            self.increase()
                            if (self.value_part == ')'):
                                self.increase()
                                if (self.value_part == ';'):
                                    self.increase()
                                    pass
                                else:
                                    self.SemiColonErr()
                            else:
                                self.closingBracketErr()
                        else:
                            self.openingBracketErr()
                    else:
                        self.validateVariableName()
                else:
                    self.invalid_token()
            else:
                self.EqualsToErr()
        else:
            self.validateVariableName()

    def fn_call(self):
        self.args()
        if (self.value_part == ')'):
            self.increase()
            if (self.value_part == ';'):
                pass
            else:
                self.SemiColonErr()
        else:
            self.closingBracketErr()
            
    def S(self):
        if self.value_part=='(' or self.value_part=='!' or self.class_part in CONST or self.class_part=='Identifier':
            self.AE()
            self.OE1()
            
            print("VALID EXPRRESSION")
        else:
            self.invalidArgumentErr()

    def OE1(self):
        if(self.value_part=='||'):
            self.increase()
            self.AE()
            self.OE1()
        else:
            pass

    def AE(self):
        self.RE()
        self.AE1()
        
    def AE1(self):
        if self.value_part=="&&":
            self.increase()
            self.RE()
            self.AE1()
        else:
            pass

    def RE(self):
        self.E()
        self.RE1()

    def RE1(self):
        if(self.class_part == "RO"):
            self.increase()
            self.E()
            self.RE1()
        else:
            pass

    def E(self):
        self.T()
        self.E1()
    
    def E1(self):
        if(self.class_part=="PM"):
            self.increase()
            self.T()
            self.E1()
        else:
            pass

    def T(self):
        self.F()
        self.T1()

    def T1(self):
        if(self.class_part=="MD"):
            self.increase()
            self.F()
            self.T1()
        else:
            pass

    def F(self):
        if self.class_part=='Identifier':
            self.increase()
            self.dot()
        elif self.class_part in CONST:
            self.increase()
        elif self.value_part=='(':
            self.increase()
            self.S()
        elif self.value_part=='!':
            self.increase()
            self.F()
        else:
            self.invalidArgumentErr()
   
    def dot(self):
        if self.value_part==".":
            self.increase()
            if self.class_part=='Identifier':
                self.increase()
                self.dot()
            else:
                self.invalid_token()
        elif self.value_part=="(":
            self.increase()
            self.new_bracket()
        elif self.value_part=="[":
            self.increase()
            self.S()
            if(self.value_part=="]"):
                print("760")
                self.increase()
                if(self.value_part=="["):
                    self.Dim()
                    if(self.value_part=="."):
                        self.dot()
                    else:
                        pass
            else:
                self.indexationError("]")
        else:
            pass

    def new_bracket(self):
        if(self.class_part=="DataType"):
            self.params()
            self.dot()
        else:
            self.fn_call()
            self.dot()

    def Dim(self):
        print("called")
        if (self.value_part=="["):
            self.increase()
            self.S()
            if(self.value_part=="]"):
                self.increase()
                self.Dim()
            else:
                self.indexationError("]")
        # elif(self.next_token!="."):
        #     self.indexationError("[")
        else:
            pass
