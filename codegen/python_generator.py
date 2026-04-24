class PythonCodeGenerator:
    def __init__(self):
        self.output = []
        self.indent = 0

    def append_line(self, line):
        self.output.append("    " * self.indent + line)

    def generate(self, ir):
        for node in ir:
            self.handle_node(node)
        return "\n".join(self.output)

    def handle_node(self, node):
        node_type = node["type"]

        if node_type == "declare":
            self.gen_declaration(node)
        elif node_type == "assign":
            self.gen_assignment(node)
        elif node_type == "print":
            self.gen_print(node)
        elif node_type == "if":
            self.handle_if(node)
        elif node_type == "while":
            self.handle_while(node)
        elif node["type"] == "break":
            self.emit(indent + "break")
        elif node["type"] == "continue":
            self.emit(indent + "continue")
        else:
            raise Exception(f"Unsupported IR node: {node_type}")
        
    def handle_if(self, node):
        # condition is an expression dict; convert to Python source
        condition = self.gen_expr(node['condition'])
        self.append_line(f"if {condition}:")
        self.indent += 1
        for stmt in node.get('then', []):
            self.handle_node(stmt)
        self.indent -= 1

        if node.get('else'):
            self.append_line("else:")
            self.indent += 1
            for stmt in node['else']:
                self.handle_node(stmt)
            self.indent -= 1

    def handle_while(self, node):
        condition = self.gen_expr(node['condition'])
        self.append_line(f"while {condition}:")
        self.indent += 1
        for stmt in node.get('body', []):
            self.handle_node(stmt)
        self.indent -= 1

     
    def gen_declaration(self, node):
        if node.get("value") is not None:
            self.append_line(f'{node["name"]} = {self.gen_expr(node["value"])}')
        else:
            self.append_line(f'{node["name"]} = None')

    def gen_assignment(self, node):
        self.append_line(f'{node["name"]} = {self.gen_expr(node["value"])}')

    def gen_print(self, node):
        self.append_line(f'print({self.gen_expr(node["value"])})')

    def gen_if(self, node):
        condition = self.gen_expr(node["condition"])
        self.append_line(f'if {condition}:')
        self.indent += 1
        for stmt in node["body"]:
            self.handle_node(stmt)
        self.indent -= 1

    def gen_expr(self, expr):
        t = expr["type"]

        if t == "number":
            return str(expr["value"])

        if t == "var":
            return expr["name"]

        if t == "binop":
            left = self.gen_expr(expr["left"])
            right = self.gen_expr(expr["right"])
            return f"({left} {expr['op']} {right})"
        
        # if isinstance(node, Number):
        #    return str(node.value)
        # if isinstance(node, Identifier):
        #    return node.name
        # if isinstance(node, BinaryOp):
        #    return f"{self.gen_expr(node.left)} {node.op} {self.gen_expr(node.right)}"

        raise Exception(f"Unknown expression type: {t}")
