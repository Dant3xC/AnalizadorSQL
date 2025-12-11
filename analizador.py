# -*- coding: utf-8 -*-
# analizador.py

import sys
import os
from sql_lexer import lexer
import sql_parser 

def analizar_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            data = archivo.read()
            print(f"\n--- Iniciando análisis de: {ruta_archivo} ---\n")

            # 1. Validación Léxica 
            # Recorremos todos los tokens para asegurar que no haya errores léxicos
            # antes de iniciar el análisis sintáctico.
            lexer.input(data)
            try:
                for tok in lexer:
                    pass 
            except Exception as e:
                if "LexicalError" in str(e):
                    print("\n--- Análisis finalizado ---")
                    return
                else:
                    raise e

            # 2. Resetear lexer para el parser
            lexer.lineno = 1
            
            # 3. Resetear bandera de error del parser
            sql_parser.hubo_error = False 

            # 4. Ejecutar Parser
            resultado_ast = sql_parser.parser.parse(data, lexer=lexer)

            print("\n--- Análisis Finalizado ---\n")

    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{ruta_archivo}'.")
    except Exception as e:
        print(f"Error inesperado: {e}")

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