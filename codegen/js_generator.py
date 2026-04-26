# ─────────────────────────────────────────────
#  codegen/js_generator.py
#  Generates JavaScript source code from the IR
# ─────────────────────────────────────────────

class JavaScriptCodeGenerator:
    """
    Walks the IR produced by IRGenerator and emits valid JavaScript.

    JavaScript-specific decisions
    ------------------------------
    • Variables declared with  let  (block-scoped, just like C locals)
    • printf  →  console.log(...)
    • No type annotations (JS is dynamically typed)
    • All code is wrapped in an IIFE for clean scoping
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
        returns : complete JavaScript source as a string
        """
        self.output = []
        self.indent = 0

        # Wrap in an immediately-invoked function so let-scoping is clean
        self._line("(function() {")
        self.indent += 1

        for node in ir:
            self._handle(node)

        self.indent -= 1
        self._line("})();")

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
            raise Exception(f"JSGenerator: unsupported IR node '{t}'")

    # ── statement generators ──────────────────
    def _declare(self, node):
        name = node["name"]
        val  = self._expr(node["value"])
        self._line(f"let {name} = {val};")

    def _assign(self, node):
        name = node["name"]
        val  = self._expr(node["value"])
        self._line(f"{name} = {val};")

    def _print(self, node):
        val = self._expr(node["value"])
        self._line(f"console.log({val});")

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

        raise Exception(f"JSGenerator: unknown expression type '{t}'")