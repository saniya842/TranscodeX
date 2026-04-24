import ply.yacc as yacc
from lexer.lexer import tokens
from ast_nodes.nodes import *

# precedence (important for expressions)
precedence = (
    ('left', 'EQ', 'NE'),
    ('left', 'GT', 'LT', 'GE', 'LE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# program → multiple statements
def p_program(p):
    '''program : statements'''
    # return the list of statements directly (not wrapped in another list)
    p[0] = Program(p[1])

# block rules
def p_block(p):
    '''block : LBRACE statements RBRACE'''
    p[0] = p[2]

# statement types
def p_statement(p):
    '''
    statement : declaration
                 | assignment
                 | print_stmt
                 | if_stmt
                 | while_stmt
    '''
    p[0] = p[1]

def p_statements(p):
    '''statements : statements statement
                  | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement_break(p):
    """statement : BREAK SEMICOLON"""
    p[0] = Break()

def p_statement_continue(p):
    '''statement : CONTINUE SEMICOLON'''
    p[0] = Continue()


# int a = 10;
def p_declaration(p):
    'declaration : INT ID ASSIGN expression SEMICOLON'
    p[0] = Declaration(p[1], p[2], p[4])

# a = 5;
def p_assignment(p):
    '''assignment : ID ASSIGN expression SEMICOLON'''
    p[0] = Assignment(p[1], p[3])

# printf(a);
def p_print(p):
    '''print_stmt : PRINTF LPAREN expression RPAREN SEMICOLON'''
    p[0] = Print(p[3])

# if (a > b) { statement }
def p_if(p):
    '''if_stmt : IF LPAREN expression RPAREN block
               | IF LPAREN expression RPAREN block ELSE block'''
    if len(p) == 6:
        p[0] = If(p[3], p[5])
    else:
        p[0] = If(p[3], p[5], p[7])

def p_while(p):
    '''while_stmt : WHILE LPAREN expression RPAREN block'''
    p[0] = While(p[3], p[5])

# expressions
def p_expression_binop(p):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
               | expression GT expression
               | expression LT expression
               | expression GE expression
               | expression LE expression
               | expression EQ expression
               | expression NE expression
    '''
    p[0] = BinaryOp(p[1], p[2], p[3])


def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = Number(p[1])


def p_expression_id(p):
    '''expression : ID'''
    p[0] = Identifier(p[1])

# to handle warnings and eror
def p_error(p):
    if p:
        raise SyntaxError(f"Syntax error at {p.type} ({p.value})")
    else:
        raise SyntaxError("Syntax error at EOF")

parser = yacc.yacc()
