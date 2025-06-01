import pickle
import os

# Configuración
TABLE_SIZE = 100
RECORD_SIZE = 1024  # Aumentar tamaño para manejar listas más grandes
SYMBOLS_FILE = "tabla_simbolos.dat"

# Función hash FNV-1
def hash_token(token):
    hash_value = 2166136261  # FNV offset basis
    for char in str(token):
        hash_value = (hash_value * 16777619) ^ ord(char)  # FNV prime
    return hash_value % TABLE_SIZE

# Inicializar el archivo de tabla de símbolos
def init_tabla_simbolos_file():
    with open(SYMBOLS_FILE, "wb") as f:
        for _ in range(TABLE_SIZE):
            pickle.dump([], f)  # Cada posición es una lista vacía
            # Rellenar con ceros hasta RECORD_SIZE
            f.write(b'\x00' * (RECORD_SIZE - f.tell() % RECORD_SIZE))

# Agregar un símbolo a la tabla
def add_symbol(value, token_type):
    position = hash_token(value)
    symbols = []
    
    # Leer la lista existente en la posición
    try:
        with open(SYMBOLS_FILE, "r+b") as f:
            f.seek(position * RECORD_SIZE)
            try:
                symbols = pickle.load(f)
            except (EOFError, pickle.UnpicklingError):
                symbols = []
            
            # Verificar si el símbolo ya existe
            for sym in symbols:
                if sym[0] == value and sym[1] == token_type:
                    return
            
            # Agregar nuevo símbolo
            symbols.append((value, token_type))
            
            # Reescribir la lista en la posición
            f.seek(position * RECORD_SIZE)
            pickle.dump(symbols, f)
    except FileNotFoundError:
        init_tabla_simbolos_file()
        add_symbol(value, token_type)  # Reintentar

# Cargar todos los símbolos
def load_tabla_simbolos():
    symbols = []
    if not os.path.exists(SYMBOLS_FILE):
        init_tabla_simbolos_file()
        return symbols
    
    with open(SYMBOLS_FILE, "rb") as f:
        for i in range(TABLE_SIZE):
            try:
                f.seek(i * RECORD_SIZE)
                bucket = pickle.load(f)
                if isinstance(bucket, list):
                    symbols.extend(bucket)
            except (EOFError, pickle.UnpicklingError):
                continue
    return symbols