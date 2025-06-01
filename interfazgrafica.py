import os
import json
import tkinter as tk
from tkinter import scrolledtext, filedialog
from lexer import lexer, palabras_reservadas
from parser import parser
from codegen import CodeGenerator
from symbol_table import init_tabla_simbolos_file, add_symbol, load_tabla_simbolos

# Rutas base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TABLA_SIMBOLOS_PATH = os.path.join(BASE_DIR, "tabla_simbolos.dat")

# Inicializar tabla de símbolos
init_tabla_simbolos_file()

# Resaltado de sintaxis
def resaltar_sintaxis(event=None):
    txt_codigo.tag_remove("reservada", "1.0", tk.END)
    txt_codigo.tag_remove("identificador", "1.0", tk.END)
    txt_codigo.tag_remove("numero", "1.0", tk.END)
    txt_codigo.tag_remove("cadena", "1.0", tk.END)
    txt_codigo.tag_remove("operador", "1.0", tk.END)
    txt_codigo.tag_remove("simbolo", "1.0", tk.END)
    txt_codigo.tag_remove("error", "1.0", tk.END)

    codigo = txt_codigo.get("1.0", tk.END)
    lexer.input(codigo)
    try:
        for token in lexer:
            if token is None:
                continue
            start = f"1.0 + {token.lexpos} chars"
            end = f"1.0 + {token.lexpos + len(str(token.value))} chars"
            if token.type in palabras_reservadas.values():
                txt_codigo.tag_add("reservada", start, end)
            elif token.type == 'IDENTIFICADOR':
                txt_codigo.tag_add("identificador", start, end)
            elif token.type == 'NUMERO':
                txt_codigo.tag_add("numero", start, end)
            elif token.type == 'CADENA':
                txt_codigo.tag_add("cadena", start, end)
            elif token.type in ('PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE', 'AND', 'OR'):
                txt_codigo.tag_add("operador", start, end)
            elif token.type in ('COLON', 'SEMICOLON', 'COMMA', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE'):
                txt_codigo.tag_add("simbolo", start, end)
    except Exception as e:
        print(f"Error en resaltado de sintaxis: {e}")

# Función de compilación
def compilar(text_widget):
    txt_errores.config(state="normal")
    txt_errores.delete("1.0", tk.END)

    codigo = text_widget.get("1.0", tk.END)
    lexer.input(codigo)
    tokens = []
    errores = set()

    # Tokenización y manejo de tabla de símbolos
    try:
        for token in lexer:
            if token is None:
                continue
            tokens.append((token.value, token.type))
            if token.type in ('IDENTIFICADOR', 'NUMERO'):
                add_symbol(str(token.value), token.type)
    except Exception as e:
        errores.add(f"Error léxico: {e}")

    # Análisis sintáctico
    try:
        lexer.input(codigo)  # Reiniciar lexer para el parser
        ast = parser.parse(codigo, lexer=lexer)
        if ast:
            codegen = CodeGenerator()
            codegen.generate(ast)
            txt_errores.insert(tk.END, "Compilación exitosa:\n")
            txt_errores.insert(tk.END, codegen.get_code() + "\n")
        else:
            errores.add("Error: No se pudo generar el AST")
    except Exception as e:
        errores.add(f"Error de sintaxis: {str(e)}")

    if errores:
        txt_errores.insert(tk.END, "Errores encontrados:\n")
        for error in sorted(errores):
            txt_errores.insert(tk.END, error + "\n")
    else:
        txt_errores.insert(tk.END, "No se encontraron errores.\n")

    txt_errores.config(state="disabled")

# Cargar archivo
def cargar_archivo(text_widget):
    file_path = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    if file_path:
        with open(file_path, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, contenido)
        resaltar_sintaxis()

# Mostrar tabla de símbolos
def mostrar_tabla_simbolos():
    symbols = load_tabla_simbolos()
    ventana = tk.Toplevel(root)
    ventana.title("Tabla de Símbolos")
    txt_tabla = scrolledtext.ScrolledText(ventana, width=50, height=20, font=("Consolas", 12))
    txt_tabla.pack(padx=5, pady=5)
    if symbols:
        for ident, tipo in symbols:
            txt_tabla.insert(tk.END, f"{ident} - {tipo}\n")
    else:
        txt_tabla.insert(tk.END, "La tabla de símbolos está vacía.")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("VLAD.io")
root.geometry("900x700")
root.configure(bg="#2e2e2e")

# Fuentes y colores
fuente_general = ("Segoe UI", 11)
color_fondo = "#2e2e2e"
color_texto = "#ffffff"
color_boton = "#444"
color_boton_hover = "#666"
color_input_bg = "#1e1e1e"

def estilo_boton(btn):
    btn.configure(
        bg=color_boton,
        fg="white",
        activebackground=color_boton_hover,
        relief="flat",
        font=fuente_general,
        padx=10,
        pady=5,
        cursor="hand2"
    )

# Menú superior
menu_bar = tk.Menu(root, bg=color_boton, fg="white", activebackground=color_boton_hover, font=fuente_general)
file_menu = tk.Menu(menu_bar, tearoff=0, bg=color_boton, fg="white", activebackground=color_boton_hover, font=fuente_general)
file_menu.add_command(label="Cargar archivo", command=lambda: cargar_archivo(txt_codigo))
menu_bar.add_cascade(label="Archivo", menu=file_menu)
root.config(menu=menu_bar)

# Label
lbl_codigo = tk.Label(root, text="Código:", font=fuente_general, bg=color_fondo, fg=color_texto)
lbl_codigo.pack(padx=5, pady=(10, 2))

# Código fuente
txt_codigo = scrolledtext.ScrolledText(root, width=100, height=20, font=("Consolas", 12), bg=color_input_bg, fg=color_texto, insertbackground="white")
txt_codigo.pack(padx=10, pady=5)
txt_codigo.tag_configure("reservada", foreground="#569CD6")  # Azul
txt_codigo.tag_configure("identificador", foreground="#9CDCFE")  # Celeste
txt_codigo.tag_configure("numero", foreground="#B5CEA8")  # Verde
txt_codigo.tag_configure("cadena", foreground="#CE9178")  # Naranja
txt_codigo.tag_configure("operador", foreground="#D16969")  # Rojo
txt_codigo.tag_configure("simbolo", foreground="#C586C0")  # Violeta
txt_codigo.tag_configure("error", foreground="#FF0000")  # Rojo brillante
txt_codigo.bind("<KeyRelease>", resaltar_sintaxis)

# Botones
frame_botones = tk.Frame(root, bg=color_fondo)
frame_botones.pack(pady=10)

btn_compilar = tk.Button(frame_botones, text="Compilar", command=lambda: compilar(txt_codigo))
btn_ver_tabla = tk.Button(frame_botones, text="Ver Tabla de Símbolos", command=mostrar_tabla_simbolos)

estilo_boton(btn_compilar)
estilo_boton(btn_ver_tabla)

btn_compilar.grid(row=0, column=0, padx=10)
btn_ver_tabla.grid(row=0, column=1, padx=10)

# Errores
lbl_errores = tk.Label(root, text="Errores:", font=fuente_general, bg=color_fondo, fg=color_texto)
lbl_errores.pack(padx=5, pady=(10, 2))

txt_errores = scrolledtext.ScrolledText(root, width=100, height=10, font=("Consolas", 12), bg=color_input_bg, fg="#ff4c4c", insertbackground="white", state="disabled")
txt_errores.pack(padx=10, pady=5)

root.mainloop()