import struct
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TABLA_SIMBOLOS_PATH = os.path.join(BASE_DIR, "tabla_simbolos.dat")
RECORD_FORMAT = "30s20sI"  # Identificador, tipo, índice de siguiente (para colisiones)
RECORD_SIZE = struct.calcsize(RECORD_FORMAT)

# Función hash FNV-1a
def fnv1a_hash(token):
    FNV_PRIME = 16777619
    FNV_OFFSET = 2166136261
    hash_value = FNV_OFFSET
    for char in str(token).encode('utf-8'):
        hash_value = (hash_value ^ char) * FNV_PRIME
        hash_value &= 0xFFFFFFFF  # Limitar a 32 bits
    return hash_value % 1000  # Limitar el índice a 1000 posiciones

def init_tabla_simbolos_file():
    """Crea o limpia el archivo de la Tabla de Símbolos."""
    with open(TABLA_SIMBOLOS_PATH, "wb") as f:
        f.write(b'\x00' * RECORD_SIZE * 1000)  # Inicializar 1000 posiciones

def add_symbol(identifier, token_type):
    """Agrega un símbolo a la tabla de símbolos usando hash."""
    identifier = str(identifier).strip()
    index = fnv1a_hash(identifier)
    
    with open(TABLA_SIMBOLOS_PATH, "rb+") as f:
        f.seek(index * RECORD_SIZE)
        record_bytes = f.read(RECORD_SIZE)
        
        # Si la posición está vacía
        if record_bytes == b'\x00' * RECORD_SIZE:
            rec_id_bytes = identifier.encode('utf-8').ljust(30, b' ')[:30]
            token_type_bytes = token_type.encode('utf-8').ljust(20, b' ')[:20]
            f.seek(index * RECORD_SIZE)
            f.write(struct.pack(RECORD_FORMAT, rec_id_bytes, token_type_bytes, 0))
            return
        
        # Manejo de colisiones con encadenamiento
        while True:
            rec_id, rec_type, next_index = struct.unpack(RECORD_FORMAT, record_bytes)
            rec_id = rec_id.decode('utf-8').strip()
            if rec_id == identifier:
                return  # Símbolo ya existe
            if next_index == 0:
                # Encontrar nueva posición para colisión
                new_index = fnv1a_hash(identifier + str(index)) % 1000
                while True:
                    f.seek(new_index * RECORD_SIZE)
                    record_bytes = f.read(RECORD_SIZE)
                    if record_bytes == b'\x00' * RECORD_SIZE:
                        break
                    new_index = (new_index + 1) % 1000
                # Actualizar el índice de la posición actual
                f.seek(index * RECORD_SIZE)
                f.write(struct.pack(RECORD_FORMAT, rec_id.encode('utf-8').ljust(30, b' ')[:30], 
                                   rec_type.decode('utf-8').ljust(20, b' ')[:20], new_index))
                # Escribir el nuevo símbolo
                f.seek(new_index * RECORD_SIZE)
                f.write(struct.pack(RECORD_FORMAT, identifier.encode('utf-8').ljust(30, b' ')[:30], 
                                   token_type.encode('utf-8').ljust(20, b' ')[:20], 0))
                return
            index = next_index
            f.seek(index * RECORD_SIZE)
            record_bytes = f.read(RECORD_SIZE)

def load_tabla_simbolos():
    """Carga la tabla de símbolos desde el archivo binario."""
    symbols = []
    try:
        with open(TABLA_SIMBOLOS_PATH, "rb") as f:
            for index in range(1000):
                f.seek(index * RECORD_SIZE)
                record_bytes = f.read(RECORD_SIZE)
                if record_bytes == b'\x00' * RECORD_SIZE:
                    continue
                rec_id, rec_type, _ = struct.unpack(RECORD_FORMAT, record_bytes)
                rec_id = rec_id.decode('utf-8').strip()
                rec_type = rec_type.decode('utf-8').strip()
                if rec_id:
                    symbols.append((rec_id, rec_type))
    except FileNotFoundError:
        pass
    return symbols