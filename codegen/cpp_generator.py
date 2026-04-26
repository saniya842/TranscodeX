# ─────────────────────────────────────────────
#  codegen/cpp_generator.py
#  Generates C++ source code from the IR
#  (same IR that PythonCodeGenerator uses)
# ─────────────────────────────────────────────

class CppCodeGenerator:
    """
    Walks the IR produced by IRGenerator and emits valid C++ code.

    Supported IR node types
    -----------------------
    declare   →  int / float variable declaration
    assign    →  variable assignment
    print     →  std::cout << value << std::endl;
    if        →  if / else block
    while     →  while loop
    break     →  break statement
    continue  →  continue statement
    """

    def __init__(self):
        self.output = []       # list of code lines
        self.indent = 0        # current indentation level

    # ── helpers ───────────────────────────────
    def _pad(self):
        """Return the current indentation string (4 spaces per level)."""
        return "    " * self.indent

    def _line(self, text):
        """Append one indented line to output."""
        self.output.append(self._pad() + text)

    # ── public entry point ────────────────────
    def generate(self, ir):
        """
        ir  : list of IR dicts produced by IRGenerator.generate()
        returns : complete C++ source as a string
        """
        self.output = []
        self.indent = 0

        # Standard C++ header boilerplate
        self._line("#include <iostream>")
        self._line("")
        self._line("int main() {")
        self.indent += 1

        for node in ir:
            self._handle(node)

        self._line("return 0;")
        self.indent -= 1
        self._line("}")

        return "\n".join(self.output)

    # ── node dispatcher ───────────────────────
    def _handle(self, node):
        t = node["type"]
        if   t == "declare":  self._declare(node)
        elif t == "assign":   self._assign(node)
        elif t == "print":    self._print(node)
        elif t == "if":       self._if(node)
        elif t == "while":    self._while(node)
        elif t == "break":    self._line("break;")
        elif t == "continue": self._line("continue;")
        else:
            raise Exception(f"CppGenerator: unsupported IR node '{t}'")

    # ── statement generators ──────────────────
    def _declare(self, node):
        dtype = node.get("datatype", "int")   # 'int' or 'float'
        name  = node["name"]
        val   = self._expr(node["value"])
        self._line(f"{dtype} {name} = {val};")

    def _assign(self, node):
        name = node["name"]
        val  = self._expr(node["value"])
        self._line(f"{name} = {val};")

    def _print(self, node):
        val = self._expr(node["value"])
        self._line(f"std::cout << {val} << std::endl;")

    def _if(self, node):
        cond = self._expr(node["condition"])
        self._line(f"if ({cond}) {{")
        self.indent += 1
        for stmt in node.get("then", []):
            self._handle(stmt)
        self.indent -= 1

        if node.get("else"):
            self._line("} else {")
            self.indent += 1
            for stmt in node["else"]:
                self._handle(stmt)
            self.indent -= 1

        self._line("}")

    def _while(self, node):
        cond = self._expr(node["condition"])
        self._line(f"while ({cond}) {{")
        self.indent += 1
        for stmt in node.get("body", []):
            self._handle(stmt)
        self.indent -= 1
        self._line("}")

    # ── expression generator ──────────────────
    def _expr(self, expr):
        t = expr["type"]

        if t == "number":
            return str(expr["value"])

        if t == "var":
            return expr["name"]

        if t == "binop":
            left  = self._expr(expr["left"])
            right = self._expr(expr["right"])
            op    = expr["op"]
            return f"({left} {op} {right})"

        raise Exception(f"CppGenerator: unknown expression type '{t}'")