from Implementation import Parser,tokenize
from tokenizer import Tokenizer

program = open('./FAAM.txt','r').read()
# tokens = tokenize(program)
lexer = Tokenizer(program)
tokens = lexer.tokenize()
parser = Parser(tokens)
result = parser.parse()
 



# Usage example
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

# num random = 5;
# num sec=6;
# num triple=7;
# until(random<9 & sec!=9 & triple!=5){
#     bool a = True;
# }