from Parser import Parser
from tokenizer import Tokenizer

program = open('./FAAM.txt','r').read()
# tokens = tokenize(program)
# print(program)
lexer = Tokenizer(program)
tokens = lexer.tokenize()
parser = Parser(tokens)
result = parser.Start()
 

