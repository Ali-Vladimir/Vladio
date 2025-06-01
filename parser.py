import ply.yacc as yacc
from lexer import tokens

# Estructura para el AST
class Node:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.children = children if children is not None else []
        self.value = value

# Reglas de precedencia
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'EQUALS'),
    ('nonassoc', 'LBRACKET', 'RBRACKET'),
    ('nonassoc', 'PREGUNTAEXISTENCIAL', 'MIENTRAS', 'CUATRO')
)

# Reglas de la gramática
def p_programa(p):
    '''programa : INICIO cuerpo FIN'''
    p[0] = Node('programa', [p[2]])

def p_cuerpo(p):
    '''cuerpo : declaraciones
              | instrucciones
              | cuerpo declaraciones
              | cuerpo instrucciones'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('cuerpo', p[1].children + [p[2]])

def p_declaraciones(p):
    '''declaraciones : declaracion
                     | declaraciones declaracion'''
    if len(p) == 2:
        p[0] = Node('declaraciones', [p[1]])
    else:
        p[0] = Node('declaraciones', p[1].children + [p[2]])

def p_declaracion(p):
    '''declaracion : VAR IDENTIFICADOR COLON tipo SEMICOLON'''
    p[0] = Node('declaracion', [Node('identificador', value=p[2]), p[4]])

def p_tipo(p):
    '''tipo : CHICOENTERO
            | FLOTANTE
            | DOBLE
            | VERDADEROOFALSO
            | STRING
            | LETRA'''
    p[0] = Node('tipo', value=p[1])

def p_instrucciones(p):
    '''instrucciones : instruccion
                     | instrucciones instruccion'''
    if len(p) == 2:
        p[0] = Node('instrucciones', [p[1]])
    else:
        p[0] = Node('instrucciones', p[1].children + [p[2]])

def p_instruccion(p):
    '''instruccion : asignacion
                   | decision
                   | ciclo
                   | para
                   | do_mientras
                   | tratamiento_error
                   | seleccion_multiple
                   | llamada_funcion
                   | bloque'''
    p[0] = p[1]

def p_asignacion(p):
    '''asignacion : IDENTIFICADOR EQUALS expresion SEMICOLON'''
    p[0] = Node('asignacion', [Node('identificador', value=p[1]), p[3]])

def p_decision(p):
    '''decision : PREGUNTAEXISTENCIAL LBRACKET expresion RBRACKET bloque PUESSINO bloque'''
    p[0] = Node('decision', [p[3], p[5], p[7]])

def p_decision_solo_if(p):
    '''decision : PREGUNTAEXISTENCIAL LBRACKET expresion RBRACKET bloque'''
    p[0] = Node('decision', [p[3], p[5]])

def p_ciclo(p):
    '''ciclo : MIENTRAS LBRACKET expresion RBRACKET bloque'''
    p[0] = Node('ciclo', [p[3], p[5]])

def p_para(p):
    '''para : CUATRO LBRACKET asignacion expresion SEMICOLON asignacion RBRACKET bloque'''
    p[0] = Node('para', [p[3], p[4], p[6], p[8]])

def p_do_mientras(p):
    '''do_mientras : DOMIENTRAS bloque MIENTRAS_POST LBRACKET expresion RBRACKET SEMICOLON'''
    p[0] = Node('do_mientras', [p[2], p[5]])

def p_tratamiento_error(p):
    '''tratamiento_error : INTENTA bloque AGARRAELERROR LBRACKET IDENTIFICADOR RBRACKET bloque'''
    p[0] = Node('tratamiento_error', [p[2], Node('identificador', value=p[5]), p[7]])

def p_seleccion_multiple(p):
    '''seleccion_multiple : SWITCH LBRACKET expresion RBRACKET LBRACE casos defecto RBRACE'''
    p[0] = Node('seleccion_multiple', [p[3], p[6], p[7]])

def p_casos(p):
    '''casos : caso
             | casos caso'''
    if len(p) == 2:
        p[0] = Node('casos', [p[1]])
    else:
        p[0] = Node('casos', p[1].children + [p[2]])

def p_caso(p):
    '''caso : OPCION valor COLON bloque'''
    p[0] = Node('caso', [p[2], p[4]])

def p_defecto(p):
    '''defecto : DEFAULT COLON bloque'''
    p[0] = Node('defecto', [p[3]])

def p_llamada_funcion(p):
    '''llamada_funcion : PRINT LBRACKET lista_expresiones RBRACKET SEMICOLON'''
    p[0] = Node('llamada_funcion', [Node('identificador', value='_imprimir'), p[3]])

def p_lista_expresiones(p):
    '''lista_expresiones : expresion
                         | lista_expresiones COMMA expresion
                         | '''
    if len(p) == 1:
        p[0] = Node('lista_expresiones', [])
    elif len(p) == 2:
        p[0] = Node('lista_expresiones', [p[1]])
    else:
        p[0] = Node('lista_expresiones', p[1].children + [p[3]])

def p_bloque(p):
    '''bloque : LBRACE instrucciones RBRACE
              | LBRACE RBRACE'''
    if len(p) == 3:
        p[0] = Node('bloque', [])
    else:
        p[0] = Node('bloque', [p[2]])

def p_expresion(p):
    '''expresion : expresion_logica'''
    p[0] = p[1]

def p_expresion_logica(p):
    '''expresion_logica : expresion_relacional
                        | expresion_logica AND expresion_relacional
                        | expresion_logica OR expresion_relacional'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('logica', [p[1], p[3]], p[2])

def p_expresion_relacional(p):
    '''expresion_relacional : expresion_aritmetica
                            | expresion_aritmetica EQ expresion_aritmetica
                            | expresion_aritmetica NE expresion_aritmetica
                            | expresion_aritmetica LT expresion_aritmetica
                            | expresion_aritmetica LE expresion_aritmetica
                            | expresion_aritmetica GT expresion_aritmetica
                            | expresion_aritmetica GE expresion_aritmetica'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('relacional', [p[1], p[3]], p[2])

def p_expresion_aritmetica(p):
    '''expresion_aritmetica : termino
                            | expresion_aritmetica PLUS termino
                            | expresion_aritmetica MINUS termino'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('aritmetica', [p[1], p[3]], p[2])

def p_termino(p):
    '''termino : factor
               | termino TIMES factor
               | termino DIVIDE factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('termino', [p[1], p[3]], p[2])

def p_factor(p):
    '''factor : LBRACKET expresion RBRACKET
              | valor
              | IDENTIFICADOR'''
    if len(p) == 4:
        p[0] = p[2]
    elif p[1] == 'IDENTIFICADOR':
        p[0] = Node('identificador', value=p[1])
    else:
        p[0] = p[1]

def p_valor(p):
    '''valor : NUMERO
             | VERDAD
             | FAKE
             | CADENA'''
    p[0] = Node('valor', value=p[1])

def p_error(p):
    if p:
        print(f"Error de sintaxis en la línea {p.lineno}: token inesperado '{p.value}'")
    else:
        print("Error de sintaxis: EOF inesperado")

# Construir el parser
parser = yacc.yacc()