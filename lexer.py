import ply.lex as lex

# Lista de tokens
tokens = (
    'NUMBER', 'ID',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN',
    'EQUALS', 'SEMICOLON',
    'IF', 'WHILE', 'LBRACE', 'RBRACE',
    'EQ', 'LT', 'GT'
)

# Reglas de expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_SEMICOLON = r';'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_EQ = r'=='
t_LT = r'<'
t_GT = r'>'

# Palabras reservadas
reserved = {
    'if': 'IF',
    'while': 'WHILE'
}

# Regla para identificadores y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Verifica si es palabra reservada
    return t

# Regla para números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Manejo de saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()