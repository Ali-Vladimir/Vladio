Compilador Nuevo
Este es un compilador sencillo implementado en Python utilizando la librería PLY (Python Lex-Yacc). Soporta un lenguaje simple con las siguientes características:

Expresiones aritméticas (+, -, *, /).
Asignación de variables.
Estructuras de control if y while.
Generación de código intermedio en forma de instrucciones de tres direcciones.

Estructura del proyecto

lexer.py: Define el analizador léxico.
parser.py: Define el analizador sintáctico y construye el AST.
codegen.py: Genera código intermedio a partir del AST.
main.py: Punto de entrada para ejecutar el compilador.
README.md: Este archivo.

Instalación

Instala Python 3.6 o superior.
Instala la librería PLY:pip install ply


Clona este repositorio y navega a la carpeta compilador_nuevo.

Uso

Modifica el código fuente en main.py (variable source_code) o pásalo como entrada.
Ejecuta el compilador:python main.py


El programa mostrará el código intermedio generado.

Ejemplo de código soportado
x = 5;
y = x + 3;
if (x < 10) {
    y = y * 2;
}
while (y > 0) {
    y = y - 1;
}

Contribuciones
Si deseas contribuir, por favor revisa el código y envía un pull request con tus mejoras.
Licencia
MIT
