# ─────────────────────────────────────────────
#  main.py  (updated — multi-language transpiler)
#
#  Usage:
#    python main.py                    → default: C → Python
#    python main.py --to cpp           → C → C++
#    python main.py --to java          → C → Java
#    python main.py --to js            → C → JavaScript
#    python main.py --to python        → C → Python  (same as default)
# ─────────────────────────────────────────────

import sys

from lexer.lexer import lexer
from parser.parser import parser
from semantic.analyzer import SemanticAnalyzer, SemanticError
from ir.ir_generator import IRGenerator

# ── all available code generators ──────────────
from codegen.python_generator import PythonCodeGenerator
from codegen.cpp_generator     import CppCodeGenerator
from codegen.java_generator    import JavaCodeGenerator
from codegen.js_generator      import JavaScriptCodeGenerator

# ══════════════════════════════════════════════
#  SAMPLE C SOURCE CODE
#  (change this to test different programs)
# ══════════════════════════════════════════════
source_code = """
int a = 5;
while (a > 0) {
    if (a == 3) {
       break;
    }
    a = a - 1;
}
"""

# ══════════════════════════════════════════════
#  CHOOSE TARGET LANGUAGE
#  Read --to <lang> from command line, default = python
# ══════════════════════════════════════════════
def get_target():
    args = sys.argv[1:]
    if "--to" in args:
        idx = args.index("--to")
        if idx + 1 < len(args):
            return args[idx + 1].lower()
    return "python"   # default

GENERATORS = {
    "python": PythonCodeGenerator,
    "cpp":    CppCodeGenerator,
    "java":   JavaCodeGenerator,
    "js":     JavaScriptCodeGenerator,
}

# ══════════════════════════════════════════════
#  PIPELINE
# ══════════════════════════════════════════════
def main():
    target = get_target()

    if target not in GENERATORS:
        print(f"Unknown target '{target}'. Choices: {list(GENERATORS.keys())}")
        sys.exit(1)

    print(f"Source language : C")
    print(f"Target language : {target}")
    print("─" * 40)

    # ── 1. Lexing + Parsing ──
    ast = parser.parse(source_code)
    if ast is None:
        print("Parsing failed. Exiting.")
        sys.exit(1)
    print("Parsing        ✅")

    # ── 2. Semantic Analysis ──
    semantic = SemanticAnalyzer()
    try:
        semantic.analyze(ast)
        print("Semantic check ✅")
    except SemanticError as e:
        print(f"Semantic error ❌: {e}")
        sys.exit(1)

    # ── 3. IR Generation ──
    ir = IRGenerator().generate(ast)
    print("IR generation  ✅")

    # ── 4. Code Generation ──
    generator = GENERATORS[target]()
    output_code = generator.generate(ir)

    print("Code generation✅")
    print("─" * 40)
    print(f"\nGENERATED {target.upper()} CODE:\n")
    print(output_code)


if __name__ == "__main__":
    main()








# from lexer.lexer import lexer
# from parser.parser import parser
# from semantic.analyzer import SemanticAnalyzer, SemanticError
# from ir.ir_generator import IRGenerator
# from codegen.python_generator import PythonCodeGenerator

# source_code = """
# int a = 5;
# while (a > 0) {
#     if (a == 3) {
#        break;
#     }
#     a = a - 1;
# }
# """

# # source_code = """
# # int a = 5;
# # int b = 3;

# # while (a > b) {
# #     if (a > 4) {
# #         printf(a);
# #     } else {
# #         printf(b);
# #     }
# #     a = a - 1;
# # }
# # """

# # source_code = """
# # int a = 5;
# # if (a > 0) {
# #     int b = 10;
# #     printf(b);
# # }
# # printf(a);
# # """

# # source_code = """
# # if (1) {
# #     int x = 5;
# # }
# # printf(x);
# # """
# # ---- Parsing ----
# ast = parser.parse(source_code)

# if ast is None:
#     print("Parsing failed. Exiting.")
#     exit(1)

# # ---- Semantic Analysis ----
# semantic = SemanticAnalyzer()
# try:
#     semantic.analyze(ast)
#     print("Semantic analysis passed ✅")
# except SemanticError as e:
#     print(f"Semantic error ❌: {e}")
#     exit(1)

# # ---- IR Generation ----
# ir_generator = IRGenerator()
# ir = ir_generator.generate(ast)   # 🔥 THIS LINE WAS MISSING

# # ---- Code Generation ----
# generator = PythonCodeGenerator()
# python_code = generator.generate(ir)

# print("\nGENERATED PYTHON CODE:\n")
# print(python_code)


# # data = """
# # int a = 10;
# # float b = 3.5;
# # if (a > b) {
# #     printf(a);
# # }
# # """

# # lexer.input(data)

# # while True:
# #     tok = lexer.token()
# #     if not tok:
# #         break
# #     print(tok)

# # code = """
# # int a = 10;
# # int b = 5;
# # if (a > b) {
# #     printf(a);
# # }
# # """

# # ast = parser.parse(code)
# # print(ast)

# # // semantic eror analyze

# # code = """
# # a =10;
# # """

# # ast = parser.parse(code)

# # analyzer = SemanticAnalyzer()

# # try:
# #     analyzer.analyze(ast)
# #     print("Semantic analysis passed ✅")
# # except SemanticError as e:
# #     print("Semantic error ❌: Variable 'a' used before declaration", e)

# # // IR genration test
# # ast = parser.parse(code)

# # SemanticAnalyzer().analyze(ast)

# # ir = IRGenerator().generate(ast)

# # from pprint import pprint
# # pprint(ir)