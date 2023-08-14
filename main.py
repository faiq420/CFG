from Implementation import Parser,tokenize
from tokenizer import Tokenizer

program = open('./FAAM.txt','r').read()
# tokens = tokenize(program)
lexer = Tokenizer(program)
tokens = lexer.tokenize()
parser = Parser(tokens)
result = parser.parse()
 



# Usage example
# num x,num y,num z  = 0;
# bool variable = false;
# fp x = abc;
# string variable = testing;
# num x;
# random variable = testing;
# string % = abc;
# repeat(num i=0;i<=10;i=i+2){
#     string text = "10";
#     repeat(num j=0;j<=10;j=j+2){
#         num random = 10;
#     }   
# }
# until ( x < 9 ) {
#     num random = 5;
# }
# func add(num a){
#     num c = 5;
# }
# func add(num a,num b){
#   num c = 5;
#     repeat(num j=0;j<=10;j=j+2){
#         num random = 10;
#         until ( x <= 9 ) {
#             bool a = true;
#         }
#     } 
# }  