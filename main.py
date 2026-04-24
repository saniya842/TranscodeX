from lexer.lexer import lexer
from parser.parser import parser
from semantic.analyzer import SemanticAnalyzer, SemanticError
from ir.ir_generator import IRGenerator
from codegen.python_generator import PythonCodeGenerator

source_code = """
int a = 5;
while (a > 0) {
    if (a == 3) {
       break;
    }
    a = a - 1;
}
"""

# source_code = """
# int a = 5;
# int b = 3;

# while (a > b) {
#     if (a > 4) {
#         printf(a);
#     } else {
#         printf(b);
#     }
#     a = a - 1;
# }
# """

# source_code = """
# int a = 5;
# if (a > 0) {
#     int b = 10;
#     printf(b);
# }
# printf(a);
# """

# source_code = """
# if (1) {
#     int x = 5;
# }
# printf(x);
# """
# ---- Parsing ----
ast = parser.parse(source_code)

if ast is None:
    print("Parsing failed. Exiting.")
    exit(1)

# ---- Semantic Analysis ----
semantic = SemanticAnalyzer()
try:
    semantic.analyze(ast)
    print("Semantic analysis passed ✅")
except SemanticError as e:
    print(f"Semantic error ❌: {e}")
    exit(1)

# ---- IR Generation ----
ir_generator = IRGenerator()
ir = ir_generator.generate(ast)   # 🔥 THIS LINE WAS MISSING

# ---- Code Generation ----
generator = PythonCodeGenerator()
python_code = generator.generate(ir)

print("\nGENERATED PYTHON CODE:\n")
print(python_code)


# data = """
# int a = 10;
# float b = 3.5;
# if (a > b) {
#     printf(a);
# }
# """

# lexer.input(data)

# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     print(tok)

# code = """
# int a = 10;
# int b = 5;
# if (a > b) {
#     printf(a);
# }
# """

# ast = parser.parse(code)
# print(ast)

# // semantic eror analyze

# code = """
# a =10;
# """

# ast = parser.parse(code)

# analyzer = SemanticAnalyzer()

# try:
#     analyzer.analyze(ast)
#     print("Semantic analysis passed ✅")
# except SemanticError as e:
#     print("Semantic error ❌: Variable 'a' used before declaration", e)

# // IR genration test
# ast = parser.parse(code)

# SemanticAnalyzer().analyze(ast)

# ir = IRGenerator().generate(ast)

# from pprint import pprint
# pprint(ir)