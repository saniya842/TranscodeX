class Node:
    pass
class Break:
    pass
class Continue:
    pass

class Program(Node):
    def __init__(self, statements):
        self.statements = statements


class Declaration(Node):
    def __init__(self, data_type, name, value):
        self.var_type = data_type
        self.name = name
        self.value = value


class Assignment(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Print(Node):
    def __init__(self, value):
        self.value = value


class If(Node):
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body

class While(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


#   expression nodes

class BinaryOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Number(Node):
    def __init__(self, value):
        self.value = value


class Identifier(Node):
    def __init__(self, name):
        self.name = name
