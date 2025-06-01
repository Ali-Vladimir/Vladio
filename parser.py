import ply.yacc as yacc
from lexer import tokens

# Estructura para el AST
class Node:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.children = children if children is not None else []
        self.value = value

# Reglas de la gramática
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'EQ', 'LT', 'GT')
)

def p_program(p):
    '''program : statements'''
    p[0] = Node('program', [p[1]])

def p_statements(p):
    '''statements : statement
                  | statements statement'''
    if len(p) == 2:
        p[0] = Node('statements', [p[1]])
    else:
        p[0] = Node('statements', p[1].children + [p[2]])

def p_statement(p):
    '''statement : assignment
                 | if_stmt
                 | while_stmt'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : ID EQUALS expression SEMICOLON'''
    p[0] = Node('assign', [Node('id', value=p[1]), p[3]])

def p_if_stmt(p):
    '''if_stmt : IF LPAREN expression RPAREN LBRACE statements RBRACE'''
    p[0] = Node('if', [p[3], p[6]])

def p_while_stmt(p):
    '''while_stmt : WHILE LPAREN expression RPAREN LBRACE statements RBRACE'''
    p[0] = Node('while', [p[3], p[6]])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EQ expression
                  | expression LT expression
                  | expression GT expression'''
    p[0] = Node('binop', [p[1], p[3]], p[2])

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = Node('number', value=p[1])

def p_expression_id(p):
    '''expression : ID'''
    p[0] = Node('id', value=p[1])

def p_expression_paren(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_error(p):
    if p:
        print(f"Error de sintaxis en la línea {p.lineno}: token inesperado '{p.value}'")
    else:
        print("Error de sintaxis: EOF inesperado")

# Construir el parser
parser = yacc.yacc()