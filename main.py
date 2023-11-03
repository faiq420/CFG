from Parser import Parser
from tokenizer import Tokenizer

program = open('./FAAM.txt','r').read()
# tokens = tokenize(program)
lexer = Tokenizer(program)
tokens = lexer.tokenize()
parser = Parser(tokens)
result = parser.Start()
 

# class MyClass {       
#   public num myNum;        
#   public string myString;  

#   MyClass(number,st){
#     this->myNum = number;
#     this->myString = st;
#   }

#   public void random(){
#     string name="ANything";
#   }
# };

# class ChildClass(MyClass){
#   public string OtherString;
# }

# class Animal {
#   publicv oid animalSound() {
#       print("The animal makes a sound");
#     }
# };

# class Pig extends public Animal {
#   public void animalSound() {
#       print("The pig says: wee wee");
#     }
# };

# class Dog extends public Animal {
#   public void animalSound() {
#       print("The dog says: bow wow");
#     }
# };

# main(){
#     ChildClass obj = new ChildClass();
#     obj->random();
#     print(obj->OtherString);
#     print(obj->MyString);

#     Animal myAnimal = new Animal();
#   Pig myPig=new Pig();
#   Dog myDog=new Dog();

#   myAnimal->animalSound();
#   myPig->animalSound();
#   myDog->animalSound();
# }



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

# num x = 5;
# num random = 5;
# when(x<=9 ){
#     string t="Equals";
#}
# either(random<9){
#     string z="Greater than 10";
# }
# either(x<9){
#     string z="Greater than 10";
# }
# otherwise{
#     string y= "Lesser Than or Equal To 10 ";
# }
# when(x<10){
#     string a ="greater than ten" ;
# }