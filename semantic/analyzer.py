from ast_nodes.nodes import *

class SemanticError(Exception):
    pass


class SemanticAnalyzer:
    def __init__(self):
        self.scopes = []
        self.loop_depth = 0

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()


    def analyze(self, program):
        self.enter_scope()  # Global scope
        for stmt in program.statements:
            self.visit(stmt)
        self.exit_scope()

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f"No visit method for {type(node).__name__}")

    # int a = 10;
    def visit_Declaration(self, node):
        current_scope = self.scopes[-1]

        if node.name in current_scope:
            raise SemanticError(f"Variable '{node.name}' redeclared")

        value_type = self.visit(node.value)
        if value_type != node.var_type:
            raise SemanticError(f"Type mismatch in declaration of '{node.name}'")
        current_scope[node.name] = node.var_type
        return node.var_type

    # a = 5;
    def visit_Assignment(self, node):
        for scope in reversed(self.scopes):
            if node.name in scope:
                value_type = self.visit(node.value)
                if value_type != scope[node.name]:
                    raise SemanticError(f"Type mismatch in assignment to '{node.name}'")
                return
        raise SemanticError(f"Variable '{node.name}' used before declaration")

    # printf(a)
    def visit_Print(self, node):
        self.visit(node.value)

    # if (...)
    def visit_If(self, node):
        self.visit(node.condition)
        # cond_type = self.visit(node.condition)
        # if cond_type != 'bool':
        #     raise SemanticError("IF condition must be boolean")

        self.enter_scope()
        for stmt in node.then_body:
            self.visit(stmt)
        self.exit_scope()

        if node.else_body:
            self.enter_scope()
            for stmt in node.else_body:
                self.visit(stmt)
            self.exit_scope()
        # self.visit(node.condition)
        # self.visit(node.body)

    # while (...)
    def visit_While(self, node):
        self.loop_depth += 1
        self.visit(node.condition)
        # cond_type = self.visit(node.condition)
        # if cond_type != 'bool':
        #     raise SemanticError("WHILE condition must be boolean")
        self.enter_scope()

        for stmt in node.body:
            self.visit(stmt)
        
        self.exit_scope()
        self.loop_depth -= 1
    
    # break
    def visit_Break(self, node):
        if self.loop_depth == 0:
            raise SemanticError("BREAK statement not within a loop")
    # continue
    def visit_Continue(self, node):
        if self.loop_depth == 0:
            raise SemanticError("CONTINUE statement not within a loop")

    # a + b
    def visit_BinaryOp(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type != right_type:
            raise SemanticError("Type mismatch in expression")
        # comparison returns boolean
        if node.op in ('>', '<', '>=', '<=', '==', '!='):
           return 'bool'
        return left_type

    def visit_Number(self, node):
        if isinstance(node.value, int):
            return 'int'
        return 'float'

    def visit_Identifier(self, node):
        for scope in reversed(self.scopes):
            if node.name in scope:
                return scope[node.name]
        raise SemanticError(f"Variable '{node.name}' used before declaration")
