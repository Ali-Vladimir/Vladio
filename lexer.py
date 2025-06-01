import ply.lex as lex
import json
import os

# Cargar definiciones de tokens desde tabla_contenidos.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "tabla_contenidos.json")
with open(JSON_PATH, "r", encoding="utf-8") as archivo:
    tabla_simbolos_json = json.load(archivo)

# Extraer palabras reservadas y operadores
palabras_reservadas = {item["token"]: item["token"].upper() for item in tabla_simbolos_json["palabras_reservadas"]}
operadores = set(
    tabla_simbolos_json["operadores_aritmeticos"] +
    tabla_simbolos_json["operadores_asignacion"] +
    tabla_simbolos_json["operadores_comparacion"] +
    tabla_simbolos_json["operadores_logicos"]
)
simbolos_puntuacion = set(tabla_simbolos_json["simbolos_puntuacion"])

# Lista de tokens
tokens = list(palabras_reservadas.values()) + [
    'IDENTIFICADOR', 'NUMERO', 'CADENA',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQUALS', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE',
    'AND', 'OR', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE',
    'COLON', 'SEMICOLON', 'COMMA'
]

# Reglas de expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_EQ = r'=='
t_NE = r'!='
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_AND = r'&&'
t_OR = r'\|\|'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\¿'
t_RBRACE = r'\?'
t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','

# Ignorar espacios, tabulaciones y saltos de línea
t_ignore = r'[ \t\n]+'

# Ignorar comentarios
def t_COMENTARIO(t):
    r'//.*|/\*[\s\S]*?\*/'
    pass

# AFD para números (enteros y decimales)
def t_NUMERO(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# AFD para cadenas
def t_CADENA(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]  # Quitar comillas
    return t

# AFD para identificadores y palabras reservadas
def t_IDENTIFICADOR(t):
    r'_[a-zA-Z][a-zA-Z0-9]*'
    t.type = palabras_reservadas.get(t.value, 'IDENTIFICADOR')
    return t

# Manejo de errores
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()