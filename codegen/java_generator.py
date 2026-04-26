# ─────────────────────────────────────────────
#  codegen/java_generator.py
#  Generates Java source code from the IR
# ─────────────────────────────────────────────

class JavaCodeGenerator:
    """
    Walks the IR produced by IRGenerator and emits valid Java code.

    Java-specific decisions
    -----------------------
    • All code is wrapped in a class Main with a main() method
    • printf  →  System.out.println(...)
    • int     →  int
    • float   →  double   (Java's preferred floating-point type)
    """

    def __init__(self):
        self.output = []
        self.indent = 0

    # ── helpers ───────────────────────────────
    def _pad(self):
        return "    " * self.indent

    def _line(self, text):
        self.output.append(self._pad() + text)

    # ── public entry point ────────────────────
    def generate(self, ir):
        """
        ir      : list of IR dicts from IRGenerator
        returns : complete Java source as a string
        """
        self.output = []
        self.indent = 0

        # Java class + main method wrapper
        self._line("public class Main {")
        self.indent += 1
        self._line("public static void main(String[] args) {")
        self.indent += 1

        for node in ir:
            self._handle(node)

        self.indent -= 1
        self._line("}")          # end main
        self.indent -= 1
        self._line("}")          # end class

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
            raise Exception(f"JavaGenerator: unsupported IR node '{t}'")

    # ── statement generators ──────────────────
    def _declare(self, node):
        raw_type = node.get("datatype", "int")
        # Map C types → Java types
        java_type = "double" if raw_type == "float" else "int"
        name = node["name"]
        val  = self._expr(node["value"])
        self._line(f"{java_type} {name} = {val};")

    def _assign(self, node):
        name = node["name"]
        val  = self._expr(node["value"])
        self._line(f"{name} = {val};")

    def _print(self, node):
        val = self._expr(node["value"])
        self._line(f"System.out.println({val});")

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

        raise Exception(f"JavaGenerator: unknown expression type '{t}'")