import re
from expressionValidation import build_expression_tree_with_types

DATATYPES = ["num", "string", "bool", "fp", "char"]
CONST = ["int_const", "FP_const", "str_const", "bool_const", "char_const"]
KEYWORDS = [
    "func",
    "repeat",
    "until",
    "when",
    "either",
    "otherwise",
    "this",
    "void",
    "new",
    "main",
    "return",
    "private",
    "public",
    "break",
    "continue",
    "class",
    "try",
    "catch",
    "enum",
]
BOOLEAN = ["True", "False"]
RETURN_TYPES = ["void", "num", "bool", "string"]
RELATIONAL_OPERATORS = ["==", "!=", "<=", ">=", ">", "<"]
LOGICAL_OPERATORS = ["&&", "||"]
DEFS = ["num", "string", "bool", "fp", "char", "func", "enum", "class"]
ACCESS_MODIFIERS = ["private", "public"]
PM = ["+", "-"]
MD = ["*", "/"]
LOGICAL_OPERATORS = ["&&", "||"]
CONST_EQUIVALENT_DT = {
    "int_const": "num",
    "FP_const": "fp",
    "str_const": "string",
    "bool_const": "bool",
    "char_const": "char",
}


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.value_part = self.tokens[0].get("value_part") if (len(tokens)) else None
        self.line_number = 1
        self.class_part = self.tokens[0].get("class_part") if (len(tokens)) else None
        self.token_index = 0
        self.next_token = (
            self.tokens[self.token_index + 1].get("value_part")
            if (len(tokens))
            else None
        )
        self.SymbolTable = []
        self.MemberTable = []
        self.DefinitionTable = []
        self.ScopeNumber = 0
        self.Scope = []
        self.TestScope = []
        self.Type = None
        self.Name = None
        self.AccessModifier = None
        self.TypeModifier = None
        self.CR = None
        self.PL = []
        self.ScopeId = 0
        self.currentClass = None
        self.CCR = None
        self.classConstructor = None
        self.currentEnum = None
        self.childRef = None
        self.parentRef = None
        self.referenceFunction = None
        self.isArray = False
        self.expression = []
        self.funcReturnType = None
        self.members = []
        self.isSealed = False

    def increase(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.class_part = self.tokens[self.token_index].get("class_part")
            self.value_part = self.tokens[self.token_index].get("value_part")
            self.line_number = self.tokens[self.token_index].get("line#")
            if self.token_index < len(self.tokens) - 2:
                self.next_token = self.tokens[self.token_index + 1].get("value_part")
            else:
                self.next_token = None
        else:
            self.value_part = None

    def decrease(self):
        self.token_index -= 1
        if self.token_index < len(self.tokens):
            self.class_part = self.tokens[self.token_index].get("class_part")
            self.value_part = self.tokens[self.token_index].get("value_part")
            self.line_number = self.tokens[self.token_index].get("line#")
            if self.token_index < len(self.tokens) - 2:
                self.next_token = self.tokens[self.token_index + 1].get("value_part")
            else:
                self.next_token = None
        else:
            self.value_part = None

    def raise_error(self, message):
        raise SyntaxError(f"{message} at line {self.line_number}")

    def validateVariableName(self):
        if (
            self.value_part in DATATYPES is not None
            or self.value_part in KEYWORDS is not None
        ):
            raise NameError("Variable can not be named as Reseserved words")

    def openingBracketErr(self):
        self.raise_error(f"Expected ( but instead got {self.value_part}")

    def closingBracketErr(self):
        self.raise_error(f"Expected ) but instead got {self.value_part}")

    def openingBraceErr(self):
        self.raise_error(f"Expected opening brace but instead got {self.value_part}")

    def closingBraceErr(self):
        self.raise_error(f"Expected closing brace but instead got {self.value_part}")

    def invalidArgumentErr(self):
        self.raise_error(f"Invalid argument passed-> {self.value_part}")

    def DataTypeErr(self):
        self.raise_error(f"Expected DATATYPE but instead got {self.value_part}")

    def SemiColonErr(self):
        self.raise_error(f"Expected semicolon but instead got {self.value_part}")

    def colonErr(self):
        self.raise_error(f"Expected colon but instead got {self.value_part}")

    def commaErr(self):
        self.raise_error(f"Expected comma but instead got {self.value_part}")

    def AssignmentOpError(self):
        self.raise_error(f"Expected Assignment Operator instead got {self.value_part}")

    def invalid_token(self):
        self.raise_error(f"Invalid token -> {self.value_part}")

    def indexationError(self, b):
        self.raise_error(f"Expected {b} instead got {self.value_part}")

    def RedeclarationError(self, message):
        self.raise_error(message)

    def invalidClassConstructor(self, message):
        self.raise_error(message)

    def accessModiferRequirement(self):
        self.raise_error(f"Expected Access Modifier for function")

    def invalidModifier(self):
        self.raise_error(f"Unexpected Access Modifier {self.value_part} for function")

    def invalidMemberAccess(self):
        self.raise_error(f"{self.value_part} is not a member of {self.currentClass}")

    def invalidAssignment(self):
        self.raise_error(f"Invalid Assignment")

    def mainFunctionMissing(self):
        raise SyntaxError(f"Main Function is not present")

    def unAssignedParameter(self, n):
        self.raise_error(f"Parameter {n} is not declared")

    def TypeMismatch(self):
        self.raise_error(
            f"Type of {self.value_part} does not match the type of variable {self.Name}"
        )

    def voidReturnTypeError(self):
        self.raise_error(
            f"Function {self.Name} is void hence can not return expression"
        )

    def undeclaredVariable(self):
        self.raise_error(f"Undeclared variable {self.value_part}")

    def invalidReference(self):
        self.raise_error(
            f"{self.parentRef} cannot be used to make objects of {self.childRef}"
        )

    def compatibility_check(self, typeone, typetwo, operator):
        if typeone == "num" and typetwo == "num":
            return "num"
        elif typeone == "string" and typetwo == "char" and operator == "+":
            return "string"
        elif typeone == "string" and typetwo == "string" and operator == "+":
            return "string"
        elif typeone == "char" and typetwo == "char" and operator == "+":
            return "string"
        elif typeone == typetwo and operator == "relational":
            return "bool"
        else:
            self.raise_error(f"Type Error between {typeone} and {typetwo}")

    def Start(self):
        if self.value_part in DEFS:
            self.defs()
        if self.value_part == "void":
            self.increase()
            if self.value_part == "main":
                self.increase()
                self.main_func()
            else:
                self.raise_error(
                    f"Main function is expected instead got {self.value_part}"
                )
        else:
            self.mainFunctionMissing()
        print(self.Scope, "\nScope Table")
        print(self.DefinitionTable, "\nDefinition Table")
        print(self.MemberTable, "\nMember Table")
        print(self.TestScope, "\nWhole Scope Table through out")

    def main_func(self):
        print("ENTERED MAIN FUNCTION")
        self.Type = "void"
        self.Name = "main"
        self.ScopeNumber += 1
        # self.ScopeId+=1
        if self.value_part == "(":
            self.increase()
            self.args()
            if self.value_part == ")":
                self.insertST(self.Name, self.Type, self.ScopeNumber - 1)

                self.increase()
                if self.value_part == "{":
                    self.increase()
                    self.MST()
                    if self.value_part == "}":
                        self.increase()
                        self.RemoveFromScope()
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
        if self.value_part in DATATYPES:
            self.decl()
            self.defs()
        elif self.value_part == "func":
            self.fn_def()
            self.defs()
        elif self.value_part == "class" or self.value_part == "sealed":
            self.class_dec()
            self.defs()
        elif self.value_part == "enum":
            self.increase()
            self.enum_st()
            self.defs()
        else:
            pass

    def args(self):
        if self.class_part == "Identifier":
            print(self.value_part, 217)
            ST = self.lookupST(self.value_part)
            print(ST, 218)
            if ST != False:
                # self.expression.append(ST["Type"])
                if "->" not in self.Type:
                    self.Type = self.Type + "->" + ST["Type"]
                else:
                    self.Type = self.Type + "," + ST["Type"]
            else:
                self.unAssignedParameter(self.value_part)
            self.increase()
            if self.value_part == ",":
                self.increase()
                self.mul_args()
            else:
                pass
        elif self.class_part in CONST:
            CT = CONST_EQUIVALENT_DT[self.class_part]
            # self.expression.append(CT)
            if "->" not in self.Type:
                self.Type = self.Type + "->" + CT
            else:
                self.Type = self.Type + "," + CT
            self.increase()
            if self.value_part == ",":
                self.increase()
                self.mul_args()
            else:
                pass
        elif self.value_part == ")":
            # self.increase()
            self.Type = None
            pass
        else:
            # self.raise_error(f"Invalid argument passed-> {self.value_part}")
            pass

    def mul_args(self):
        if self.class_part == "Identifier" or self.class_part in CONST:
            self.args()
        elif self.next_token == ")":
            self.increase()
            pass
        else:
            self.raise_error(f"Invalid argument passed-> {self.value_part}")

    def params(self):
        if self.value_part in DATATYPES or self.class_part == "Identifier":
            if "->" not in self.Type:
                self.Type = self.Type + "->" + self.value_part
            else:
                self.Type = self.Type + "," + self.value_part
            CurrentParamType = self.value_part
            self.increase()
            if self.class_part == "Identifier":
                CurrentParamName = self.value_part
                self.insertST(CurrentParamName, CurrentParamType, self.ScopeNumber)
                self.increase()
                self.mul_params()
            else:
                self.validateVariableName()
        else:
            pass

    def mul_params(self):
        if self.value_part == ",":
            self.increase()
            self.params()
        else:
            pass

    def searchParents(self):
        if self.class_part == "Identifier":
            self.PL.append(self.value_part)
            self.increase()
            self.mul_searchParents()
        else:
            pass

    def mul_searchParents(self):
        if self.value_part == ",":
            self.increase()
            self.searchParents()
        else:
            pass

    def decl(self):
        if self.value_part in DATATYPES:
            self.Type = self.value_part
            self.increase()
            if self.class_part == "Identifier":
                self.Name = self.value_part
                self.insertST(self.Name, self.Type, self.ScopeNumber)
                self.increase()
                if self.value_part == ",":
                    self.ID_ext()
                if self.value_part == "[":
                    self.increase()
                    if self.value_part == "]":
                        self.isArray = True
                        self.increase()
                    else:
                        self.indexationError("]")
                elif self.value_part != "=":
                    self.invalid_token()
                self.init()
                self.isArray = False
                self.mul_decl()
            else:
                self.validateVariableName()
        else:
            self.invalidArgumentErr()

    def ID_ext(self):
        if self.value_part == ",":
            self.increase()
            if self.class_part == "Identifier":
                self.Name = self.value_part
                self.insertST(self.Name, self.Type, self.ScopeNumber)
                self.increase()
                self.ID_ext()
        else:
            pass

    def init(self):
        if self.value_part == "=":
            self.increase()
            self.expression = []
            self.S()
            # print(self.expression,371)
            assignment_type = ""
            if len(self.expression) != 0:
                assignment_type = build_expression_tree_with_types(self.expression)
                self.expression = []
            else:
                assignment_type = self.funcReturnType
            if self.isArray == True:
                pass
            else:
                self.compatibility_check(
                    self.Type.split("->")[0], assignment_type, "relational"
                )

        else:
            self.AssignmentOpError()

    def mul_decl(self):
        if self.value_part not in ";,":
            self.decrease()
        if self.value_part == ";":
            self.increase()
        elif self.value_part == ",":
            self.increase()
            if self.class_part == "Identifier":
                self.Name = self.value_part
                self.insertST(self.Name, self.Type, self.ScopeNumber)
                self.increase()
                if self.value_part == ",":
                    self.ID_ext()
                if self.value_part != "=":
                    self.invalid_token()
                self.init()
                self.isArray = False
                self.mul_decl()
        else:
            self.raise_error(f"Unexpected token {self.value_part}")

    def body(self):
        self.MST()

    def classBody(self):
        self.CMST()

    def MST(self):
        if (
            self.value_part in KEYWORDS
            or self.value_part in DATATYPES
            or self.class_part == "Identifier"
        ):
            self.SST()
            self.MST()
        else:
            pass

    def CMST(self):
        if (
            self.value_part in KEYWORDS
            or self.value_part in DATATYPES
            or self.class_part == "Identifier"
        ):
            self.CST()
            self.CMST()
        else:
            pass

    def SST(self):
        if self.value_part == "func":
            self.fn_def()
        elif self.value_part == "when":
            self.if_else()
        elif self.value_part == "until":
            self.while_st()
        elif self.value_part == "repeat":
            self.for_st()
        elif self.class_part == "jump":
            self.br_cont()
        elif self.value_part == "return":
            self.ret()
        elif self.value_part == "this":
            self.this_st()
        elif self.value_part == "try":
            self.try_catch()
        elif self.value_part == "enum":
            self.enum_st()
        elif self.value_part in ACCESS_MODIFIERS:
            self.invalid_token()
        elif self.class_part == "Identifier":
            self.ids()
        elif self.value_part == "class":
            self.invalid_token()
        elif self.value_part in DATATYPES:
            self.decl()
        else:
            pass

    def CST(self):
        if self.value_part == "func":
            self.fn_def()
        elif self.value_part == "when":
            self.if_else()
        elif self.value_part == "until":
            self.while_st()
        elif self.value_part == "repeat":
            self.for_st()
        elif self.class_part == "jump":
            self.br_cont()
        elif self.value_part == "return":
            self.ret()
        elif self.value_part == "this":
            self.this_st()
        elif self.value_part == "try":
            self.try_catch()
        elif self.value_part == "enum":
            self.enum_st()
        elif self.value_part in ACCESS_MODIFIERS:
            self.attribute_st()
        elif self.class_part == "Identifier":
            self.ids()
        elif self.value_part in DATATYPES:
            self.decl()
        else:
            pass

    def this_st(self):
        self.increase()
        if self.value_part == ".":
            self.increase()
            self.this_st_ext()
            if self.value_part == ";":
                self.increase()
                print("VALID THIS STATEMENT")
        else:
            self.invalid_token()

    def this_st_ext(self):
        self.Name = self.value_part
        if self.next_token == "=":
            if self.class_part == "Identifier":
                RMT = self.lookupMT(self.value_part)
                if len(RMT) != 0:
                    self.increase()
                    if self.value_part == "=":
                        self.increase()
                        self.expression = []
                        self.S()
                        assignment_type = build_expression_tree_with_types(
                            self.expression
                        )
                        self.compatibility_check(
                            RMT[0]["Type"], assignment_type, "relational"
                        )
                        self.expression = []
                        self.this_st_ext()
                    else:
                        self.AssignmentOpError()
                else:
                    self.invalidMemberAccess()
            else:
                self.invalidArgumentErr()
        elif self.value_part == ";":
            pass
        elif self.next_token == "(":
            self.referenceFunction = self.value_part
            self.CCR = self.currentClass
            self.increase()
            self.increase()
            self.fn_call()
            self.dot()
            # self.this_st_ext()
            self.CCR = None

    def if_else(self):
        self.increase()
        self.ScopeNumber += 1
        if self.value_part == "(":
            self.increase()
            self.expression = []
            self.S()
            assignment_type = build_expression_tree_with_types(self.expression)
            self.compatibility_check("bool", assignment_type, "relational")
            self.expression = []
            if self.value_part == ")":
                self.increase()
                if self.value_part == "{":
                    self.increase()
                    if self.currentClass is None:
                        self.body()
                    else:
                        self.classBody()
                    if self.value_part == "}":
                        self.increase()
                        self.RemoveFromScope()
                        print("VALID IF CONDITION")
                        if self.value_part == "either":
                            self.increase()
                            self.either()
                        if self.value_part == "otherwise":
                            self.increase()
                            self.otherwise()
                        else:
                            print("VALID IF CONDITION")
                            pass
                    else:
                        self.closingBraceErr()
            else:
                self.closingBracketErr()
        else:
            self.openingBracketErr()

    def either(self):
        self.ScopeNumber += 1
        if self.value_part == "(":
            self.increase()
            self.expression = []
            self.S()
            assignment_type = build_expression_tree_with_types(self.expression)
            self.compatibility_check("bool", assignment_type, "relational")
            self.expression = []
            if self.value_part == ")":
                self.increase()
                if self.value_part == "{":
                    self.increase()
                    if self.currentClass is None:
                        self.body()
                    else:
                        self.classBody()
                    if self.value_part == "}":
                        self.increase()
                        self.RemoveFromScope()
                        print("VALID ELSE IF CONDITION")
                        if self.value_part == "either":
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
        self.ScopeNumber += 1
        if self.value_part == "{":
            self.increase()
            if self.currentClass is None:
                self.body()
            else:
                self.classBody()
            if self.value_part == "}":
                self.increase()
                self.RemoveFromScope()
            else:
                self.closingBraceErr()
        else:
            self.openingBraceErr()

    def attribute_st(self):
        self.AccessModifier = self.value_part
        self.increase()
        if self.value_part in DATATYPES:
            self.Type = self.value_part
            self.increase()
            if self.class_part == "Identifier":
                self.Name = self.value_part
                self.insertMT(
                    self.Name, self.Type, self.AccessModifier, self.currentClass
                )
                self.increase()
                if self.value_part == "=":
                    self.increase()
                    self.S()
                    if self.value_part == ";":
                        self.increase()
                    else:
                        self.SemiColonErr()
                else:
                    self.AssignmentOpError()
            else:
                self.invalid_token()
        else:
            self.DataTypeErr()

    def while_st(self):
        self.increase()
        self.ScopeNumber += 1
        if self.value_part == "(":
            self.increase()
            self.expression = []
            self.S()
            assignment_type = build_expression_tree_with_types(self.expression)
            self.compatibility_check("bool", assignment_type, "relational")
            self.expression = []
            if self.value_part == ")":
                self.increase()
                if self.value_part == "{":
                    self.increase()
                    if self.currentClass is None:
                        self.body()
                    else:
                        self.classBody()
                    if self.value_part == "}":
                        self.increase()
                        self.RemoveFromScope()
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
        self.Type = self.value_part
        self.classConstructor = self.value_part
        if self.next_token == "=" or self.next_token == ".":
            ST = self.lookupST(self.value_part)
            if ST:
                self.Type = ST["Type"]
        self.increase()
        self.identifier()

    def att_access(self):
        if self.value_part == ".":
            RDT = self.lookupDT(self.Type)
            if len(RDT) != 0:
                members = self.fetchMembers(self.Type)
                self.increase()
                type = None
                for member in members:
                    if (member["Name"]) == self.value_part:
                        if member["AM"] != "private":
                            type = member["Type"]
                        else:
                            self.raise_error(f"Private Member cannot be accessed")
                if type == None:
                    self.invalidAssignment()
                else:
                    self.Type = type
                    self.increase()
            else:
                self.invalidAssignment()
        else:
            pass

    def inc_dec(self):
        if self.class_part == "Identifier":
            self.increase()
            if self.value_part == "=":
                self.increase()
                self.S()
                print("VALID INCREMENT/DECREMENT")
            else:
                self.AssignmentOpError()
        else:
            self.invalidArgumentErr()

    def for_st(self):
        self.increase()
        self.ScopeNumber += 1
        if self.value_part == "(":
            self.increase()
            if self.value_part == "num":
                self.decl()
                self.S()
                if self.value_part == ";":
                    self.increase()
                    self.inc_dec()
                    if self.value_part == ")":
                        self.increase()
                        if self.value_part == "{":
                            self.increase()
                            if self.currentClass is None:
                                self.body()
                            else:
                                self.classBody()
                            if self.value_part == "}":
                                self.increase()
                                self.RemoveFromScope()
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
        if self.value_part != ";":
            if self.Type != None and self.Type.split("->")[0] == "void":
                self.voidReturnTypeError()
            else:
                self.expression = []
                self.S()
                if len(self.expression) != 0:
                    assignment_type = build_expression_tree_with_types(self.expression)
                    # self.compatibility_check(
                    #     self.funcReturnType.split("->")[0], assignment_type, "relational"
                    # )
                    self.expression = []
            if self.value_part == ";":
                self.increase()
                print("VALID RETURN STATEMENT")
            else:
                self.SemiColonErr()
        else:
            self.increase()
            print("VALID RETURN STATEMENT")

    def br_cont(self):
        self.increase()
        if self.value_part == ";":
            self.increase()
            print("VALID JUMP STATEMENT")
        else:
            self.SemiColonErr()

    def try_catch(self):
        self.increase()
        self.ScopeNumber += 1
        if self.value_part == "{":
            self.increase()
            if self.currentClass is None:
                self.body()
            else:
                self.classBody()
            if self.value_part == "}":
                self.increase()
                self.RemoveFromScope()
                if self.value_part == "catch":
                    self.increase()
                    self.ScopeNumber += 1
                    if self.value_part == "(":
                        self.increase()
                        if self.class_part == "DataType":
                            self.Type = self.value_part
                            self.increase()
                            if self.class_part == "Identifier":
                                self.Name = self.value_part
                                self.increase()
                                if self.value_part == ")":
                                    self.insertST(
                                        self.Name, self.Type, self.ScopeNumber
                                    )
                                    self.increase()
                                    if self.value_part == "{":
                                        self.increase()
                                        if self.currentClass is None:
                                            self.body()
                                        else:
                                            self.classBody()
                                        if self.value_part == "}":
                                            self.RemoveFromScope()
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
                            self.DataTypeErr()
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
        if self.value_part == "virtual":
            self.increase()
        if self.value_part in ACCESS_MODIFIERS and self.currentClass is not None:
            self.AccessModifier = self.value_part
            self.increase()
        elif self.currentClass is not None and self.class_part != "Access_Modifier":
            self.accessModiferRequirement()
        if self.value_part in ACCESS_MODIFIERS and self.currentClass is None:
            self.invalidModifier()
        if self.value_part in RETURN_TYPES:
            self.funcReturnType = self.value_part
            self.increase()
            if self.class_part == "Identifier":
                self.Name = self.value_part
                self.increase()
                self.ScopeId += 1
                self.ScopeNumber += 1
                if self.value_part == "(":
                    self.increase()
                    self.params()
                    if self.value_part == ")":
                        if self.currentClass is None:
                            self.insertST(self.Name, self.Type, self.ScopeNumber - 1)
                            # self.Type=None
                        else:
                            self.insertMT(
                                self.Name,
                                self.Type,
                                self.AccessModifier,
                                self.currentClass,
                            )
                            self.Type = None
                        self.increase()
                        if self.value_part == "{":
                            self.increase()
                            if self.currentClass is None:
                                self.body()
                            else:
                                self.classBody()
                            if self.value_part == "}":
                                self.RemoveFromScope()
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
        if self.class_part == "Identifier":
            self.currentEnum = self.value_part
            self.insertDT(self.currentEnum, "enum", "-", "-", "-")
            self.increase()
            if self.value_part == "=":
                self.increase()
                if self.value_part == "{":
                    self.key_st()
                    if self.value_part == "}":
                        self.increase()
                        self.currentEnum = None
                        print("VALID ENUMERATION")
                    else:
                        self.closingBraceErr()
                else:
                    self.openingBraceErr()
            else:
                self.AssignmentOpError()
        else:
            self.validateVariableName()

    def key_st(self):
        self.increase()
        if self.class_part == "Identifier":
            self.insertMT(self.value_part, "-", "-", self.currentEnum)
            self.increase()
            if self.value_part == ",":
                self.key_st()
            else:
                pass

    def mul_key_st(self):
        if self.value_part == ",":
            self.key_st()
        else:
            pass

    def class_dec(self):
        if self.value_part == "sealed":
            self.isSealed = True
            self.increase()
        self.increase()
        self.ScopeNumber += 1
        if self.value_part in ACCESS_MODIFIERS:
            self.AccessModifier = self.value_part
            self.Type = "class"
            self.increase()
            self.classList()
            classModifier = "sealed" if self.isSealed == True else "-"
            self.insertDT(
                self.Name, self.Type, self.AccessModifier, classModifier, self.PL
            )
            self.PL = []
            if self.value_part == "{":
                self.increase()
                self.classBody()
                if self.value_part == "}":
                    self.increase()
                    self.RemoveFromScope()
                    self.currentClass = None
                    print("VALID CLASS DECLARATION")
                else:
                    self.closingBraceErr()
            else:
                self.openingBraceErr()
        else:
            self.invalid_token()

    def classList(self):
        # self.increase()
        if self.class_part == "Identifier":
            self.Name = self.value_part
            self.currentClass = self.value_part
            self.classDiv()
        else:
            self.validateVariableName()

    def classDiv(self):
        self.increase()
        if self.value_part == "(":
            self.inh()
        elif self.value_part == ":":
            self.increase()
            if self.value_part in ACCESS_MODIFIERS:
                self.increase()
                if self.class_part == "Identifier":
                    self.increase()
                    pass
                else:
                    self.validateVariableName()
        else:
            self.invalid_token()

    def inh(self):
        self.increase()
        if self.value_part == ")":
            self.increase()

        elif self.class_part == "Identifier":
            # self.increase()
            self.searchParents()
            if self.value_part == ")":
                self.increase()
            else:
                self.closingBracketErr()

    def identifier(self):
        if self.value_part == "=" or self.value_part == ".":
            self.assign_st()
        elif self.value_part == "(":
            self.bracket_exp()
        elif self.class_part == "Identifier":
            self.enum_obj_dec()
        else:
            self.indexationError()

    def assign_st(self):
        if self.value_part == ".":
            self.att_access()
        if self.value_part == "=":
            self.increase()
            self.expression = []
            self.S()
            assignment_type = build_expression_tree_with_types(self.expression)
            self.expression = []
            self.compatibility_check(
                self.Type.split("->")[0], assignment_type, "relational"
            )
            if self.value_part == ";":
                self.increase()
                pass
            else:
                self.SemiColonErr()
        else:
            self.AssignmentOpError()

    def bracket_exp(self):
        self.increase()
        flag = self.token_index
        flagVariable = self.tokens[flag].get("value_part")
        while flagVariable != ")":
            flag += 1
            flagVariable = self.tokens[flag].get("value_part")
        if self.tokens[flag + 1].get("value_part") == "{":
            self.ScopeNumber += 1
            # self.increase()
            self.constructor_def()
        else:
            # self.increase()
            self.fn_call()

    def constructor_def(self):
        if self.currentClass == self.classConstructor:
            self.params()
            if self.value_part == ")":
                self.insertMT(self.currentClass, self.Type, "public", self.currentClass)
                self.increase()
                if self.value_part == "{":
                    self.increase()
                    self.classBody()
                    if self.value_part == "}":
                        self.increase()
                        self.RemoveFromScope()
                        print("VALID CONSTRUCTOR")
                    else:
                        self.closingBraceErr()
                else:
                    self.openingBraceErr()
            else:
                self.closingBracketErr()
        else:
            self.invalidClassConstructor(
                f"Invalid constructor {self.classConstructor} for class {self.currentClass}"
            )

    def enum_obj_dec(self):
        self.childRef = self.classConstructor
        if self.class_part == "Identifier":
            self.Name = self.value_part
            self.increase()
            if self.value_part == "=":
                self.increase()
                self.enum_obj_dec_ext()

            else:
                self.AssignmentOpError()
        else:
            self.validateVariableName()

    def enum_obj_dec_ext(self):
        if self.value_part == "new":
            self.increase()
            if self.class_part == "Identifier":
                self.parentRef = self.value_part
                self.increase()
                if self.value_part == "(":
                    self.increase()
                    if self.value_part == ")":
                        RDT = self.lookupDT(self.childRef)
                        if len(RDT) != 0:
                            if self.childRef == self.parentRef:
                                self.insertST(
                                    self.Name, self.childRef, self.ScopeNumber
                                )
                            elif self.parentRef in RDT[0]["Parent"]:
                                self.insertST(
                                    self.Name, self.childRef, self.ScopeNumber
                                )
                            else:
                                self.invalidReference()
                        self.increase()
                        if self.value_part == ";":
                            print("OBJECT CREATED")
                            self.increase()
                        else:
                            self.SemiColonErr()
                    else:
                        self.closingBracketErr()
                else:
                    self.openingBracketErr()
                # else:
                #     self.validateVariableName()
        elif self.class_part == "Identifier":
            members = self.fetchMembers(self.childRef)
            valid = False
            for member in members:
                if member["Name"] == self.value_part:
                    self.increase()
                    self.insertST(self.Name, self.childRef, self.ScopeNumber)
                    valid = True
            if valid == False and self.value_part != ";":
                self.invalidAssignment()
            else:
                self.increase()
                print("ENUM ASSIGNED")
        else:
            self.invalid_token()

    def fn_call(self):
        self.args()
        if self.value_part == ")":
            if self.currentClass is None:
                ST = self.lookupFuncST(self.referenceFunction, self.Type)
                if ST is not False:
                    self.funcReturnType = ST["Type"].split("->")[0]
                    # self.increase()
                else:
                    self.invalidAssignment()
            elif self.currentClass is not None:
                RMT = self.LookupFuncMT(
                    self.referenceFunction, self.Type, self.currentClass
                )
                if len(RMT) == 0:
                    self.invalidAssignment()
                else:
                    self.funcReturnType = RMT[0]["Type"].split("->")[0]
                    # self.increase()
            # self.increase()

            else:
                self.SemiColonErr()
        else:
            self.closingBracketErr()

    def array(self):
        if self.value_part == "[":
            self.increase()
            self.array_element()
            if self.value_part == "]":
                self.increase()
            else:
                self.indexationError("]")
        else:
            self.indexationError("[")

    def array_element(self):
        if self.value_part == "[":
            self.array_list()
        elif self.class_part in CONST or self.class_part == "Identifier":
            self.element_list()
        else:
            pass

    def array_list(self):
        self.array()
        self.mul_array_list()

    def element_list(self):
        self.element_list_body()
        self.mul_element_list()

    def element_list_body(self):
        if self.class_part in CONST:
            if self.Type == CONST_EQUIVALENT_DT[self.class_part]:
                self.increase()
            else:
                self.TypeMismatch()
        elif self.class_part == "Identifier":
            ST = self.lookupST(self.value_part)
            # print(ST)
            if self.Type == ST["Type"]:
                self.increase()
            else:
                self.TypeMismatch()
        # else:
        #     pass

    def mul_element_list(self):
        if self.value_part == ",":
            self.increase()
            self.element_list()
        else:
            pass

    def mul_array_list(self):
        if self.value_part == ",":
            self.increase()
            self.array_list()

    def S(self):
        if (
            self.value_part == "("
            or self.value_part == "!"
            or self.class_part in CONST
            or self.class_part == "Identifier"
            or self.value_part == "this"
            or self.value_part == "["
        ):
            self.AE()
            self.OE1()
            print("VALID EXPRRESSION")
        else:
            self.invalidArgumentErr()

    def OE1(self):
        if self.value_part == "||":
            self.expression.append(self.value_part)
            self.increase()
            self.AE()
            self.OE1()
        else:
            pass

    def AE(self):
        self.RE()
        self.AE1()

    def AE1(self):
        if self.value_part == "&&":
            self.expression.append(self.value_part)
            self.increase()
            self.RE()
            self.AE1()
        else:
            pass

    def RE(self):
        self.E()
        self.RE1()

    def RE1(self):
        if self.class_part == "RO":
            self.expression.append(self.value_part)
            self.increase()
            self.E()
            self.RE1()
        else:
            pass

    def E(self):
        self.T()
        self.E1()

    def E1(self):
        if self.class_part == "PM":
            self.expression.append(self.value_part)
            self.increase()
            self.T()
            self.E1()
        else:
            pass

    def T(self):
        self.F()
        self.T1()

    def T1(self):
        if self.class_part == "MD":
            self.expression.append(self.value_part)
            self.increase()
            self.F()
            self.T1()
        else:
            pass

    def F(self):
        if self.class_part == "Identifier":
            # self.increase()
            # print(self.value_part,1083)
            self.dot()
        elif self.class_part in CONST:
            self.expression.append(self.value_part)
            self.increase()
            # if(self.Type==CONST_EQUIVALENT_DT[self.class_part]):
            #     self.increase()
            # else:
            #     self.TypeMismatch()
            # print(self.value_part,1099)
        elif self.value_part == "(":
            self.expression.append(self.value_part)
            self.increase()
            self.S()
            if self.value_part == ")":
                self.expression.append(self.value_part)
                self.increase()
        elif self.value_part == "!":
            self.expression.append(self.value_part)
            self.increase()
            self.F()
        elif self.value_part == "this":
            self.this_st()
        elif self.value_part == "[":
            self.array()
        else:
            self.invalidArgumentErr()

    def dot(self):
        self.referenceFunction = self.value_part
        ST = self.lookupST(self.value_part)
        if ST != False:
            TypeEquivalency = ST["Type"]
            if TypeEquivalency == "num":
                self.expression.append("0")
            elif TypeEquivalency == "fp":
                self.expression.append("0.0")
            elif TypeEquivalency == "bool":
                self.expression.append("True")
            elif TypeEquivalency == "char":
                self.expression.append(self.value_part)
            elif TypeEquivalency == "string":
                self.expression.append(self.value_part)
        # elif(self.next_token not in ".([" and self.value_part!=";"):
        #     print(self.next_token,1361)
        #     self.undeclaredVariable()
        if self.next_token == ".":
            self.increase()
            self.increase()
            if self.class_part == "Identifier":
                self.increase()
                self.dot()
            else:
                self.invalid_token()
        elif self.next_token == "(":
            self.increase()
            self.increase()
            self.new_bracket()
        elif self.next_token == "[":
            self.increase()
            self.increase()
            self.S()
            if self.value_part == "]":
                print("760")
                self.increase()
                if self.value_part == "[":
                    self.Dim()
                    if self.value_part == ".":
                        self.dot()
                    else:
                        pass
            else:
                self.indexationError("]")
        else:
            self.increase()
            if re.match(r"[a-zA-Z]$", self.value_part):
                self.dot()
            # if(self.currentClass is None):
            #     if("->" in self.Type):
            #         ST=self.lookupFuncST(self.referenceFunction,self.Type)
            #         print(ST,1130)
            #         if(ST is not False):
            #             self.increase()
            #         else:
            #             self.invalidAssignment()
            #     else:
            #         ST=self.lookupST(self.value_part)
            #         if(ST is not False):
            #             self.increase()
            #         else:
            #             self.invalidAssignment()
            # elif(self.currentClass is not None):
            #         RMT=self.LookupFuncMT(self.referenceFunction,self.Type,self.currentClass)
            #         if(len(RMT)==0):
            #             self.invalidAssignment()

    def new_bracket(self):
        if self.class_part == "DataType":
            self.params()
            self.dot()
        else:
            self.fn_call()
            self.dot()

    def Dim(self):
        print("called")
        if self.value_part == "[":
            self.increase()
            self.S()
            if self.value_part == "]":
                self.increase()
                self.Dim()
            else:
                self.indexationError("]")
        else:
            pass

    def insertST(self, n, t, s):
        currentScopeObjs = list(filter(lambda x: x["ScopeId"] == s, self.Scope))
        checkByName = list(filter(lambda y: y["Name"] == n and y["Type"]==t, currentScopeObjs))
        if len(checkByName) == 0:
            obj = {
                "Name": n,
                "Type": t,
                "ScopeId": s,
                "ParentScopeId": s - 1 if ((s - 1) > -1) else None,
            }
            self.Scope.append(obj)
            self.TestScope.append(obj)
        else:
            self.RedeclarationError(f"Variable {n} already exists in scope {s}")

    def RemoveFromScope(self):
        filteredScopeTb = list(
            filter(lambda x: x["ScopeId"] != self.ScopeNumber, self.Scope)
        )
        self.ScopeNumber -= 1
        self.Scope = filteredScopeTb

    def insertDT(self, n, t, a, c, p):
        DT = self.lookupDT(n)
        if len(DT) == 0:
            if len(p) == 0:
                obj = {"Name": n, "Type": t, "AM": a, "CM": c, "Parent": p}
                self.DefinitionTable.append(obj)
            else:
                exists = True
                if p != "-":
                    for parent in p:
                        PDT = self.lookupDT(parent)
                        if len(PDT) == 0:
                            exists = False
                            self.RedeclarationError(
                                f"Parent Class({parent}) for class {n} doesn't exist"
                            )
                        elif PDT[0]["AM"] == "private" or PDT[0]["CM"] == "sealed":
                            exists = False
                            self.raise_error(
                                f"Private Class ({parent}) can not be inherited"
                            )
                if exists == True:
                    obj = {"Name": n, "Type": t, "AM": a, "CM": c, "Parent": p}
                    self.DefinitionTable.append(obj)
        else:
            self.RedeclarationError(f"Class/Enum of name {n} already exists")

    def lookupDT(self, n):
        check = list(filter(lambda x: x["Name"] == n, self.DefinitionTable))
        return check

    def insertMT(self, n, t, a, r):
        DT = self.lookupMT(n)
        if len(DT) == 0 or DT[0]["Type"] != t:
            if len(r) == 0:
                obj = {"Name": n, "Type": t, "AM": a, "Reference": r}
                self.MemberTable.append(obj)
            else:
                exists = True
                typeOfParent = None
                if isinstance(r, list):
                    typeOfParent = "array"
                elif isinstance(r, str):
                    typeOfParent = "string"
                if typeOfParent == "array":
                    for parent in r:
                        PDT = self.lookupDT(parent)
                        if len(PDT) == 0:
                            exists = False
                            self.RedeclarationError(
                                f"Parent ({parent}) for {n} doesn't exist."
                            )
                elif typeOfParent == "string":
                    PDT = self.lookupDT(r)
                    if len(PDT) == 0:
                        exists = False
                        self.RedeclarationError(
                            f"Parent ({parent}) for {n} doesn't exist."
                        )
                if exists == True:
                    obj = {"Name": n, "Type": t, "AM": a, "Reference": r}
                    self.MemberTable.append(obj)
        else:
            self.RedeclarationError(f"Member of name {n} already exists")

    def lookupMT(self, n):
        check = list(filter(lambda x: x["Name"] == n, self.MemberTable))
        return check

    def lookupST(self, current):
        scopeLimit = self.ScopeNumber
        ST = None
        while scopeLimit is not None:
            ST = list(filter(lambda x: x["ScopeId"] == scopeLimit, self.Scope))
            if len(ST) != 0:
                for name in ST:
                    if name["Name"] == current and "->" not in name["Type"]:
                        return name
            scopeLimit = scopeLimit - 1 if (scopeLimit >= 0) else None
        return False

    def lookupFuncST(self, current, pl):
        scopeLimit = self.ScopeNumber
        ST = None
        while scopeLimit is not None:
            ST = list(filter(lambda x: x["ScopeId"] == scopeLimit, self.Scope))
            if len(ST) != 0:
                for name in ST:
                    if "->" in name["Type"]:
                        if (
                            name["Name"] == current
                            and name["Type"].split("->")[1] == pl.split("->")[1]
                        ):
                            return name
            scopeLimit = scopeLimit - 1 if (scopeLimit >= 0) else None
        return False

    def LookupFuncMT(self, n, pl, r):
        check = list(filter(lambda x: x["Name"] == n, self.MemberTable))
        checkByParent = list(filter(lambda x: x["Reference"] == r, check))
        checkByParams = list(
            filter(lambda y: y["Type"].split("->") == pl.split("->"), checkByParent)
        )
        return checkByParams

    def fetchMembers(self, p):
        checkByParent = list(filter(lambda x: x["Reference"] == p, self.MemberTable))
        return checkByParent
