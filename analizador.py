# -*- coding: utf-8 -*-
import sys
from sql_lexer import lexer
from sql_parser import parser

def analizar_archivo(ruta_archivo):
    """
    Lee un archivo, lo analiza léxica y sintácticamente.
    """
    try:
        with open(ruta_archivo, 'r') as archivo:
            data = archivo.read()
            print(f"--- Iniciando análisis de: {ruta_archivo} ---")
            
            # Pasamos el lexer al parser
            # lexer.input(data) # No es necesario si pasas el lexer a parse()
            
            # Llamamos al parser. 
            # El lexer se pasa como argumento para que el parser 
            # le pida los tokens uno por uno.
            resultado_ast = parser.parse(data, lexer=lexer)
            
            if resultado_ast:
                print("\n--- Resultado del Árbol Sintáctico (AST) ---")
                for sentencia in resultado_ast:
                    print(sentencia)
            
            print("---------------------------------------------")

    except FileNotFoundError:
        print(f"*** ERROR ***: No se pudo encontrar el archivo '{ruta_adchivo}'.")
    except Exception as e:
        print(f"*** ERROR INESPERADO ***: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # sys.argv[0] es el nombre del script (analizador.py)
        # sys.argv[1] es el primer argumento (el archivo a probar)
        nombre_archivo = sys.argv[1]
        analizar_archivo(nombre_archivo)
    else:
        print("Error: Por favor, proporciona la ruta a un archivo .sql como argumento.")
        print("Ejemplo: python analizador.py casos_prueba/prueba_ok.sql")