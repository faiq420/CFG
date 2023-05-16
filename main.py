from Variable_implementation import Parser,tokenize

# Usage example
program = open('./FAAM.txt','r').read()
# program = 'num x,num y,num z  = 0;'
# program = 'bool variable = false;'
# program = 'fp x = abc;'
# program = 'string variable = testing;'
# program = 'num x;'
# program = 'random variable = testing;'
# program = 'string % = abc;'
tokens = tokenize(program)
parser = Parser(tokens)
result = parser.parse()
 