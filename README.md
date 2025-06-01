Compilador Nuevo
Este es un compilador implementado en Python utilizando la librería PLY (Python Lex-Yacc) para un lenguaje definido en gramatica.txt. Incluye una interfaz gráfica basada en tkinter y cumple con los requisitos de la práctica especificados en cambios.txt.
Características

Lenguaje soportado: Soporta declaraciones (var), asignaciones, decisiones (PreguntaExistencial), ciclos (Mientras, Cuatro, DoMientras), manejo de errores (intenta/AgarraElError), y selección múltiple (switch).
Interfaz gráfica: Permite escribir código, cargar archivos, resaltar sintaxis, compilar, y mostrar errores y la tabla de símbolos.
Tabla de símbolos: Almacenada en un archivo binario de acceso aleatorio (tabla_simbolos.dat).
Análisis léxico y sintáctico: Implementado con PLY, incluyendo AFD para identificadores y números.
Generación de código: Produce código intermedio en forma de instrucciones de tres direcciones.

Estructura del proyecto

lexer.py: Analizador léxico con PLY.
parser.py: Analizador sintáctico con PLY.
codegen.py: Generador de código intermedio.
interfazgrafica.py: Interfaz gráfica con tkinter.
main.py: Punto de entrada para pruebas sin GUI.
tabla_contenidos.json: Definición de tokens y palabras reservadas.
tabla_simbolos.dat: Archivo binario para la tabla de símbolos.
README.md: Este archivo.

Instalación

Instala Python 3.6 o superior.
Instala la librería PLY:pip install ply


Clona este repositorio y navega a la carpeta compilador_nuevo.

Uso

Ejecuta la interfaz gráfica:python interfazgrafica.py


O prueba el compilador sin GUI:python main.py


Usa el menú "Archivo" para cargar un archivo de texto (como texto_ejemplo.txt).
Escribe o edita código en el área de texto, que resaltará la sintaxis en tiempo real.
Presiona "Compilar" para tokenizar, analizar sintácticamente, y generar código intermedio.
Presiona "Ver Tabla de Símbolos" para mostrar los identificadores y números almacenados.

Ejemplo de código soportado
inicio
    var _edad : ChicoEntero;
    var _nombre : string;
    var _esMayor : VerdaderoOFalso;
    _nombre = "Juan";
    _edad = 20;
    PreguntaExistencial [_edad >= 18] ¿
        _esMayor = verdad;
    ? PuesSiNo ¿
        _esMayor = fake;
    ?
    Mientras [_edad < 25] ¿
        _edad = _edad + 1;
    ?
fin

AFD para identificadores y números

Identificadores: Deben comenzar con _ seguido de letras (a-z, A-Z) y opcionalmente números. Regla: _[a-zA-Z][a-zA-Z0-9]*.
Números: Enteros o decimales. Regla: \d+(\.\d+)?.

Contribuciones
Por favor, revisa el código y envía un pull request con tus mejoras.
Licencia
MIT
