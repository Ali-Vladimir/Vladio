from lexer import lexer
from parser import parser
from codegen import CodeGenerator
from interfazgrafica import add_symbol

def compile_code(source_code):
    # Análisis léxico
    lexer.input(source_code)
    for token in lexer:
        if token.type in ('IDENTIFICADOR', 'NUMERO'):
            add_symbol(str(token.value), token.type)

    # Análisis sintáctico
    ast = parser.parse(source_code, lexer=lexer)
    if not ast:
        print("Error: No se pudo generar el AST")
        return

    # Generación de código
    codegen = CodeGenerator()
    codegen.generate(ast)
    print("Código intermedio generado:")
    print(codegen.get_code())

if __name__ == "__main__":
    with open("texto_ejemplo.txt", "r", encoding="utf-8") as f:
        source_code = f.read()
    compile_code(source_code)