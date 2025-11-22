# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# PROGRAMA PRINCIPAL: ANALIZADOR SQL
# ------------------------------------------------------------
# Lee un archivo .sql, realiza el análisis léxico y sintáctico
# e imprime el árbol de sintaxis abstracta (AST).
# ------------------------------------------------------------
import sys
import os
from sql_lexer import lexer
from sql_parser import parser

def analizar_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            data = archivo.read()
            print(f"\n--- Iniciando análisis de: {ruta_archivo} ---\n")

            # --- RESET del lexer antes de usarlo ---
            lexer.lineno = 1
            lexer.lex_errors = []
            lexer.lex_error = False

            # --- PRE-ESCANEO LÉXICO: detecta errores léxicos ANTES de parsear ---
            lexer.input(data)
            for _ in lexer:
                # iterar consume tokens y ejecuta t_error si corresponde
                pass

            if getattr(lexer, 'lex_error', False):
                print("Se detectaron errores léxicos. No se ejecutará el análisis sintáctico.")
                for e in lexer.lex_errors:
                    print(e)
                print("\n--- Análisis finalizado (con errores léxicos) ---\n")
                return

            # --- Si no hay errores léxicos, ejecutar el parser ---
            resultado_ast = parser.parse(data, lexer=lexer)

            if resultado_ast:
                print("\n--- Árbol Sintáctico Abstracto (AST) ---")
                for sentencia in resultado_ast:
                    print(sentencia)

            print("\n--- Análisis Finalizado ---\n")

    except FileNotFoundError:
        print(f"ERROR: No se pudo encontrar el archivo '{ruta_archivo}'.")
    except Exception as e:
        print(f"ERROR INESPERADO: {e}")

def mostrar_menu():
    carpeta_casos = 'casos_prueba'
    while True:
        print("\n--- MENÚ DE CASOS DE PRUEBA ---")
        try:
            archivos = [f for f in os.listdir(carpeta_casos) if f.endswith('.sql') or f.endswith('.txt')]
        except FileNotFoundError:
            print(f"Error: No se encontró la carpeta '{carpeta_casos}'.")
            return

        if not archivos:
            print("No hay archivos de prueba disponibles.")
            return

        for i, archivo in enumerate(archivos, 1):
            print(f"{i}. {archivo}")
        print("0. Salir")

        opcion = input("\nSeleccione un archivo (número): ")

        if opcion == '0':
            print("Saliendo...")
            break

        try:
            indice = int(opcion) - 1
            if 0 <= indice < len(archivos):
                archivo_seleccionado = os.path.join(carpeta_casos, archivos[indice])
                analizar_archivo(archivo_seleccionado)
                input("\nPresione Enter para continuar...")
            else:
                print("Opción inválida.")
        except ValueError:
            print("Por favor, ingrese un número válido.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        analizar_archivo(sys.argv[1])
    else:
        mostrar_menu()
