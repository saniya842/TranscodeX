from ast_nodes.nodes import *

class IRGenerator:
    def generate(self, ast):
        for stmt in ast.statements:
            self.visit(stmt)
        return self.instructions

    def visit(self, node):
        method = f'visit_{type(node).__name__}'
        return getattr(self, method)(node)

    def visit_Declaration(self, node):
        return {
            "type": "declare",
            "datatype": node.var_type,
            "name": node.name,
            "value": self.gen_expr(node.value)
        }

    def visit_Assignment(self, node):
        return {
            "type": "assign",
            "name": node.name,
            "value": self.gen_expr(node.value)
        }

    def visit_Print(self, node):
        return {
            "type": "print",
            "value": self.gen_expr(node.value)
        }

    def visit_If(self, node):
        return {
            "type": "if",
            "condition": self.gen_expr(node.condition),
            "then": [self.visit(s) for s in node.then_body],
            "else": [self.visit(s) for s in node.else_body] if node.else_body else None
        }
    
    def visit_While(self, node):
        return {
            "type": "while",
            "condition": self.gen_expr(node.condition),
            "body": [self.visit(s) for s in node.body]
       }

    def visit_Break(self, node):
        return {"type": "break"}

    def visit_Continue(self, node):
        return {"type": "continue"}

    def visit_BinaryOp(self, node):
        return {
            "type": "binop",
            "op": node.op,
            "left": self.gen_expr(node.left),
            "right": self.gen_expr(node.right)
        }

    def visit_Number(self, node):
        return {
            "type": "number",
            "value": node.value
        }

    def visit_Identifier(self, node):
        return {
            "type": "var",
            "name": node.name
        }

    def gen_expr(self, expr):
        from ast_nodes.nodes import Number, Identifier, BinaryOp

        # accept raw numeric literals too (defensive)
        if isinstance(expr, (int, float)):
            return {"type": "number", "value": expr}

        if isinstance(expr, Number):
            return {"type": "number", "value": expr.value}

        if isinstance(expr, Identifier):
            return {"type": "var", "name": expr.name}

        if isinstance(expr, BinaryOp):
            return {
                "type": "binop",
                "op": expr.op,
                "left": self.gen_expr(expr.left),
                "right": self.gen_expr(expr.right)
            }

        raise Exception(f"Unsupported expression node: {expr}")
