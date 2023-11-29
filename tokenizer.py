import re

#classes
DATATYPES = ["num", "string", "bool","fp","char"]
ARRAY=["[","]"]
BOOLEAN=["True","False"]
RELATIONAL_OPERATORS = ['==','!=','<=','>=','<','>']
LOGICAL_OPERATORS = ['&&','||']
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
        global line_Number

        charAtEndOfLiteral={}

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
            obj['class_part']="ref"
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
                # global line_Number
                line_Number +=1
                self.increase()
                continue

                #for comments
            if(self.currentChar=='/'and self.nextChar=="*"):
                self.increase()
                self.increase()
                while(self.currentChar!='*' and self.nextChar!='/'):
                    # global line_Number
                    if(self.currentChar == '\n'):
                        line_Number+=1
                        self.increase()
                        continue
                    self.increase()
                self.increase()
                self.increase()
                continue
            
            if(self.currentChar=='#'):
                while(not self.currentChar=='\n'):
                    if(self.currentChar==None):
                        break
                    self.increase()
                self.increase()
                continue

            if(self.currentChar=='-' and self.nextChar=='>'):
                refToken=self.currentChar
                self.increase()
                refToken+=self.currentChar
                self.increase()
                obj['class_part']="ref"
                obj['value_part']=refToken
                obj['line#']=line_Number
                self.tokens.append(obj)
                self.increase()
                continue

            #check for keywords
            
            if(re.match(r"[a-zA-Z]$",self.currentChar)):
                keyToken=self.currentChar
                while(re.match(r"[a-zA-Z_][a-zA-Z0-9_]*$",keyToken)):
                    self.increase()
                    keyToken += self.currentChar
                keyToken=keyToken.replace(" ", "")
                if(not re.match(r"[a-zA-Z]$",keyToken[len(keyToken)-1])):
                    # if(keyToken[len(keyToken)-1] == '-' and not self.nextChar=='>'):
                        charAtEndOfLiteral=self.checkForSymbols(keyToken[len(keyToken)-1])             
                        keyToken = keyToken[:len(keyToken)-1]
                        self.current -=1
                    # else:
                    #     if(keyToken[len(keyToken)-1]=='-' and self.nextChar=='>'):
                    #         keyToken = keyToken[:len(keyToken)-1]
                    #         refToken=keyToken[len(keyToken)-1]
                    #         self.increase()
                    #         refToken+=self.currentChar
                    #         self.increase()
                    #         obj['class_part']="ref"
                    #         obj['value_part']=refToken
                    #         obj['line#']=line_Number
                    #         self.tokens.append(obj)
                    #         self.current -=1
                    #         self.increase()
                contains_digits = any(char.isdigit() for char in keyToken)
                contains_underscore = '_' in keyToken
                if contains_digits or contains_underscore:
                    obj['class_part']="Identifier"
                    obj['value_part']=keyToken
                    obj['line#']=line_Number
                    self.tokens.append(obj)
                    self.increase()
                    continue
                    if(charAtEndOfLiteral):
                        self.tokens.append(charAtEndOfLiteral)
                else:
                    if(keyToken in DATATYPES):
                        obj['class_part']="DataType"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken =="break" or keyToken=="continue"):
                        obj['class_part']="jump"
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
                    elif(keyToken == "either"):
                        obj['class_part']="else_if"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken == "otherwise"):
                        obj['class_part']="else"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken == "func"):
                        obj['class_part']="function"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken == "repeat"):
                        obj['class_part']="for"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken == "until"):
                        obj['class_part']="while"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken == "void"):
                        obj['class_part']="void"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken == "return"):
                        obj['class_part']="return"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken == "main"):
                        obj['class_part']="main"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken == "new"):
                        obj['class_part']="new"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken == "this"):
                        obj['class_part']="this"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken == "class"):
                        obj['class_part']="class"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken == "extends"):
                        obj['class_part']="extends"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken == "struct"):
                        obj['class_part']="struct"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken in ACCESS_MODIFIERS):
                        obj['class_part']="Access_Modifier"
                        obj['value_part']=keyToken
                        obj['line#']=line_Number
                        self.tokens.append(obj)
                        self.increase()
                        continue
                    elif(keyToken in BOOLEAN):
                        obj['class_part']="bool_const"
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
                        self.tokens.append(charAtEndOfLiteral)    
            # if(charAtEndOfLiteral):
            #     print(charAtEndOfLiteral)
            #     self.tokens.append(charAtEndOfLiteral)
    
                #to check for string literals
            if (self.currentChar == '"'):
                stringToken = self.currentChar
                self.increase()
                while (self.currentChar != '"'):
                    stringToken += self.currentChar
                    self.increase()
                stringToken += self.currentChar
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
                if(self.nextChar == '\\'):
                    print(self.currentChar)
                    charToken += self.currentChar
                    self.increase()    
                    print(self.currentChar)
                charToken += self.currentChar
                self.increase()
                if(self.nextChar != "'"):
                    print(len(charToken),'sa')
                    obj['class_part']="invalid_token"
                    obj['value_part']=charToken
                    obj['line#']=line_Number
                    self.tokens.append(obj)
                    self.increase()
                    continue
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
                numericalToken = self.currentChar
                self.increase()
                numericalToken += self.currentChar
                while(re.match(r"[0-9]+$",numericalToken)):
                    self.increase()
                    numericalToken += self.currentChar
                numericalToken=numericalToken.replace(" ", "")                
                if(not re.match(r"[0-9]$",numericalToken[len(numericalToken)-1]) and numericalToken[len(numericalToken)-1]!='.'):                    
                    charAtEndOfLiteral=self.checkForSymbols(numericalToken[len(numericalToken)-1])
                    numericalToken = numericalToken[:len(numericalToken)-1]
                    self.current -=1

                if(numericalToken[len(numericalToken)-1] == '.'):
                    self.increase()
                    fpToken=numericalToken
                    fpToken+=self.currentChar
                    while(re.match(r"[0-9]+.[0-9]+$",fpToken)):
                        self.increase()
                        fpToken += self.currentChar
                    fpToken=fpToken.replace(" ", "")                
                    if(not re.match(r"[0-9]$",fpToken[len(fpToken)-1])):                    
                        charAtEndOfLiteral=self.checkForSymbols(fpToken[len(fpToken)-1])
                        fpToken = fpToken[:len(fpToken)-1]
                        self.current -=1
                    obj['class_part']="FP_const"
                    obj['value_part']=fpToken
                    obj['line#']=line_Number
                else:
                    obj['class_part']="int_const"
                    obj['value_part']=numericalToken
                    obj['line#']=line_Number
                self.tokens.append(obj)
                self.increase()
                continue
                

            if(self.currentChar in '-+' and re.match(r"[0-9]$",self.nextChar)):
                numericalToken = self.currentChar
                self.increase()
                numericalToken += self.currentChar
                while(re.match(r"[-+][0-9]+$",numericalToken)):
                    self.increase()
                    numericalToken += self.currentChar
                numericalToken=numericalToken.replace(" ", "")                
                if(not re.match(r"[0-9]$",numericalToken[len(numericalToken)-1]) and numericalToken[len(numericalToken)-1]!='.'):                    
                    charAtEndOfLiteral=self.checkForSymbols(numericalToken[len(numericalToken)-1])
                    numericalToken = numericalToken[:len(numericalToken)-1]
                    self.current -=1

                if(numericalToken[len(numericalToken)-1] == '.'):
                    self.increase()
                    fpToken=numericalToken
                    fpToken+=self.currentChar
                    while(re.match(r"[-+][0-9]+.[0-9]+$",fpToken)):
                        self.increase()
                        fpToken += self.currentChar
                    fpToken=fpToken.replace(" ", "")                
                    if(not re.match(r"[0-9]$",fpToken[len(fpToken)-1])):                    
                        charAtEndOfLiteral=self.checkForSymbols(fpToken[len(fpToken)-1])
                        fpToken = fpToken[:len(fpToken)-1]
                        self.current -=1
                    obj['class_part']="FP_const"
                    obj['value_part']=fpToken
                    obj['line#']=line_Number
                else:
                    obj['class_part']="int_const"
                    obj['value_part']=numericalToken
                    obj['line#']=line_Number
                self.tokens.append(obj)
                self.increase()
                continue

            elif(self.currentChar == '.' and re.match(r"[0-9]$",self.nextChar)):
                fpToken=self.currentChar
                self.increase()
                fpToken+=self.currentChar
                while(re.match(r".[0-9]+$",fpToken)):
                    self.increase()
                    fpToken += self.currentChar
                if(not re.match(r"[0-9]$",fpToken[len(fpToken)-1])):
                    obj['class_part']="invalid_token"
                    obj['value_part']=fpToken
                    obj['line#']=line_Number
                    self.tokens.append(obj)
                    self.increase()
                    continue
                else:
                    obj['class_part']="FP_const"
                    obj['value_part']=fpToken
                    obj['line#']=line_Number
                    self.tokens.append(obj)
                    self.increase()
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
                self.tokens.append(obj)
                self.increase()
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
                self.increase()
                if(self.currentChar==symbolToken):
                    symbolToken+=self.currentChar
                obj['class_part']="LO"
                obj['value_part']=symbolToken
                obj['line#']=line_Number
                self.tokens.append(obj)
                self.increase()
                continue

            if(self.currentChar=='='):
                symbolToken=self.currentChar
                if(self.nextChar=="="):
                    self.increase()
                    symbolToken+=self.currentChar
                    obj['class_part']="RO"
                    obj['value_part']=symbolToken
                    obj['line#']=line_Number
                else:
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
        # print(self.tokens,len(self.tokens))
        return self.tokens


