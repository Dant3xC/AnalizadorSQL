# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# PROGRAMA PRINCIPAL: ANALIZADOR SQL
# ------------------------------------------------------------
# Lee un archivo .sql, realiza el análisis léxico y sintáctico
# e imprime el árbol de sintaxis abstracta (AST).
# ------------------------------------------------------------

import sys
from sql_lexer import lexer
from sql_parser import parser

def analizar_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            data = archivo.read()
            print(f"\n--- Iniciando análisis de: {ruta_archivo} ---\n")

            resultado_ast = parser.parse(data, lexer=lexer)
            
            if resultado_ast:
                print("\n--- Árbol Sintáctico Abstracto (AST) ---")
                for sentencia in resultado_ast:
                    print(sentencia)
            print("\n--- Análisis Finalizado ---\n")

    except FileNotFoundError:
        print(f"*** ERROR ***: No se pudo encontrar el archivo '{ruta_archivo}'.")
    except Exception as e:
        print(f"*** ERROR INESPERADO ***: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analizar_archivo(sys.argv[1])
    else:
        print("Uso: python analizador.py <archivo.sql>")
        print("Ejemplo: python analizador.py casos_prueba/prueba1.sql")
