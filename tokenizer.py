import re

#classes
DATATYPES = ["num", "string", "bool","fp"]
ARRAY=["[","]"]
RELATIONAL_OPERATORS = ['==','!=','<=','>=','<','>']
LOGICAL_OPERATORS = ['&','|']
ASSIGNMENT='='
PM = ['+','-']
MD=['*','/']
IF='when'
ELSE_IF='either'
ELSE='otherwise'
FUNCTION='func'
FOR='repeat'
WHILE='until'
VOID='void'
THIS='this'
NEW='new'
ACCESS_MODIFIERS=['private','public']
MAIN='main'
RETURN='return'


line_Number=1
class Tokenizer:

    def __init__(self, string):
        self.source = string
        self.current = 0
        self.tokens = []
        self.currentChar = self.source[0]
        self.nextChar = self.source[1]
        self.class_part=''
        self.value_part=''
        self.line_number=''

    def increase(self):
        self.current += 1
        if (self.current < len(self.source)):
            self.currentChar = self.source[self.current]
            try:
                self.nextChar = self.source[self.current + 1]
            except:
                self.nextChar = None
        else:
            self.currentChar = None

    def retreat(self):
        self.current -= 1
        if (self.current > 0):
            self.currentChar = self.source[self.current]
            try:
                self.nextChar = self.source[self.current + 1]
            except:
                self.nextChar = None
        else:
            self.currentChar = None

    def checkForSymbols(self,token):
        obj={}
        if(token == '('):
            obj['class_part']="("
            obj['value_part']=token
            obj['line#']=line_Number
            return obj
            
        if(token == '{'):
            obj['class_part']="{"
            obj['value_part']=token
            obj['line#']=line_Number
            return obj
            
        if(token == '}'):
            obj['class_part']="}"
            obj['value_part']=token
            obj['line#']=line_Number
            return obj
            
        if(token == ')'):
            obj['class_part']=")"
            obj['value_part']=token
            obj['line#']=line_Number
            return obj
            
        if(token == ';'):
            obj['class_part']=";"
            obj['value_part']=token
            obj['line#']=line_Number
            return obj
            
        if(token == ','):
            obj['class_part']=","
            obj['value_part']=token
            obj['line#']=line_Number
            return obj
            
        if(token == '.'):
            obj['class_part']="."
            obj['value_part']=token
            obj['line#']=line_Number
            return obj
            

    def tokenize(self):
        global line_Number
        while(self.currentChar != None):
            obj={}
            if(self.currentChar == " "):
                self.increase()
                continue

            if(self.currentChar == '\n'):
                global line_Number
                line_Number +=1
                self.increase()
                continue

                #for comments
            if(self.currentChar=='#'):
                self.increase()
                while(self.currentChar!='#'):
                    self.increase()
                self.increase()


            #check for keywords
            charAtEndOfLiteral={}
            if(re.match(r"[a-zA-Z]$",self.currentChar)):
                keyToken=self.currentChar
                while(re.match(r"[a-zA-Z_][a-zA-Z0-9_]*$",keyToken)):
                    self.increase()
                    keyToken += self.currentChar
                keyToken=keyToken.replace(" ", "")
                if(not re.match(r"[a-zA-Z]$",keyToken[len(keyToken)-1])):
                    charAtEndOfLiteral=self.checkForSymbols(keyToken[len(keyToken)-1])
                    # self.tokens.append(charAtEndOfLiteral)
                    # self.current -=1
                    keyToken = keyToken[:len(keyToken)-1]
                contains_digits = any(char.isdigit() for char in keyToken)
                contains_underscore = '_' in keyToken
                if contains_digits or contains_underscore:
                    obj['class_part']="Identifier"
                    obj['value_part']=keyToken
                    obj['line#']=line_Number
                    self.tokens.append(obj)
                    self.increase()
                    continue
                else:
                    if(keyToken in DATATYPES):
                        obj['class_part']="DataType"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken =="when"):
                        obj['class_part']="If"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken in "either"):
                        obj['class_part']="else_if"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken in "otherwise"):
                        obj['class_part']="else"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken in "func"):
                        obj['class_part']="function"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken in "repeat"):
                        obj['class_part']="for"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken in "until"):
                        obj['class_part']="while"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken in "void"):
                        obj['class_part']="void"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken in "return"):
                        obj['class_part']="return"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    else:
                        obj['class_part']="Identifier"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
            if(charAtEndOfLiteral):
                print(charAtEndOfLiteral)
                self.tokens.append(charAtEndOfLiteralToken)
    
                #to check for string literals
            if (self.currentChar == '"'):
                self.increase()
                stringToken = self.currentChar
                self.increase()
                while (self.currentChar != '"'):
                    stringToken += self.currentChar
                    self.increase()
                # stringToken += self.currentChar
                obj['class_part']="str_const"
                obj['value_part']=stringToken
                obj['line#']=line_Number
                self.tokens.append(obj)
                self.increase()
                continue

                #to check for character literals
            if (self.currentChar == "'"):
                charToken = self.currentChar
                self.increase()
                charToken += self.currentChar
                self.increase()
                charToken += self.currentChar
                self.increase()
                obj['class_part']="char_const"
                obj['value_part']=charToken
                obj['line#']=line_Number
                self.tokens.append(obj)
                self.increase()
                continue
                

                #CHECK FOR NUMBERS

            if(re.match(r"[0-9]$",self.currentChar)):
                numberToken=self.currentChar
                while(re.match(r"[0-9]+$",numberToken)):
                    self.increase()
                    numberToken += self.currentChar
                obj['class_part']="int_const"
                obj['value_part']=numberToken
                obj['line#']=line_Number
                self.tokens.append(obj)#numericalToken[:len(numericalToken)-1]

            if(self.currentChar in '-+' and re.match(r"[0-9]$",self.nextChar)):
                numericalToken = self.currentChar
                self.increase()
                numericalToken += self.currentChar
                while(re.match(r"[-+][0-9]+$",numericalToken)):
                    self.increase()
                    numericalToken += self.currentChar
                if(self.nextChar == '.'):
                    fpToken=numericalToken
                    fpToken+=self.currentChar
                    while(re.match(r"[-+][0-9]+.[0-9]+$",fpToken)):
                        self.increase()
                        fpToken += self.currentChar
                    obj['class_part']="FP_const"
                    obj['value_part']=fpToken
                    obj['line#']=line_Number
                else:
                    obj['class_part']="int_const"
                    obj['value_part']=numericalToken
                    obj['line#']=line_Number
                self.tokens.append(obj)#numericalToken[:len(numericalToken)-1]
                continue
            elif(self.currentChar in '+-' and self.nextChar=="."):
                fpToken=self.currentChar
                self.increase()
                fpToken+=self.currentChar
                while(re.match(r"[-+].[0-9]+$",fpToken)):
                    self.increase()
                    fpToken += self.currentChar
                obj['class_part']="FP_const"
                obj['value_part']=fpToken
                obj['line#']=line_Number
                self.tokens.append(obj)#numericalToken[:len(numericalToken)-1]
                continue
            elif(self.currentChar in "+-"):
                obj['class_part']="PM"
                obj['value_part']=self.currentChar
                obj['line#']=line_Number
                self.tokens.append(obj)
                self.increase()
                continue

                #CHECK FOR SYMBOLS
            # if(self.currentChar in "{(;,.)}"):
            if(self.currentChar == '('):
                obj['class_part']="("
                obj['value_part']=self.currentChar
                obj['line#']=line_Number
                self.tokens.append(obj)
                self.increase()
                continue
            
            if(self.currentChar == '{'):
                obj['class_part']="{"
                obj['value_part']=self.currentChar
                obj['line#']=line_Number
                self.tokens.append(obj)
                self.increase()
                continue
                
            if(self.currentChar == '}'):
                obj['class_part']="}"
                obj['value_part']=self.currentChar
                obj['line#']=line_Number
                self.tokens.append(obj)
                self.increase()
                continue
                
            if(self.currentChar == ')'):
                obj['class_part']=")"
                obj['value_part']=self.currentChar
                obj['line#']=line_Number
                self.tokens.append(obj)
                self.increase()
                continue
                
            if(self.currentChar == ';'):
                obj['class_part']=";"
                obj['value_part']=self.currentChar
                obj['line#']=line_Number
                self.tokens.append(obj)
                self.increase()
                continue
                
            if(self.currentChar == ','):
                obj['class_part']=","
                obj['value_part']=self.currentChar
                obj['line#']=line_Number
                self.tokens.append(obj)
                self.increase()
                continue
                
            if(self.currentChar == '.'):
                obj['class_part']="."
                obj['value_part']=self.currentChar
                obj['line#']=line_Number
                self.tokens.append(obj)
                self.increase()
                continue
                
            if(self.currentChar=='>' or self.currentChar=='<' or self.currentChar=='!'):
                symbolToken=self.currentChar
                if(self.nextChar=="="):
                    self.increase()
                    symbolToken+=self.currentChar
                obj['class_part']="RO"
                obj['value_part']=symbolToken
                obj['line#']=line_Number
                self.tokens.append(obj)
                self.increase()
                continue

            if(self.currentChar=='&' or self.currentChar=='|'):
                symbolToken=self.currentChar
                obj['class_part']="LO"
                obj['value_part']=symbolToken
                obj['line#']=line_Number
                self.tokens.append(obj)
                self.increase()
                continue

            if(self.currentChar=='='):
                obj['class_part']="Assignment"
                obj['value_part']=self.currentChar
                obj['line#']=line_Number
                self.tokens.append(obj)
                self.increase()
                continue

            if(self.currentChar in '*/'):
                obj['class_part']="MD"
                obj['value_part']=self.currentChar
                obj['line#']=line_Number
                self.tokens.append(obj)
                self.increase()
                continue
                            

            self.increase()
        print(self.tokens,len(self.tokens))
        return self.tokens


