from lexer import lexer
from parser import parser
from codegen import CodeGenerator

def compile_code(source_code):
    # Análisis léxico
    lexer.input(source_code)
    # for token in lexer:
    #     print(token)

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
    # Ejemplo de código fuente
    source_code = """
    x = 5;
    y = x + 3;
    if (x < 10) {
        y = y * 2;
    }
    while (y > 0) {
        y = y - 1;
    }
    """
    compile_code(source_code)