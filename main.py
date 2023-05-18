from Implementation import Parser,tokenize

# Usage example
program = open('./FAAM.txt','r').read()
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
tokens = tokenize(program)
parser = Parser(tokens)
result = parser.parse()
 