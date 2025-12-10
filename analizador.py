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

            # 1. Resetear lexer
            lexer.lineno = 1
            lexer.lex_errors = []
            lexer.lex_error = False
            
            # 2. Resetear bandera de error del parser
            sql_parser.hubo_error = False 

            # 3. Ejecutar Parser directamente
            # (El parser pedirá los tokens al lexer internamente)
            resultado_ast = sql_parser.parser.parse(data, lexer=lexer)

            # Verificar errores léxicos
            if getattr(lexer, 'lex_error', False):
                print("\n*** ERRORES LÉXICOS DETECTADOS ***")
                for error in lexer.lex_errors:
                    print(error)

            print("\n--- Análisis Finalizado ---\n")

    except FileNotFoundError:
        print(f"*** ERROR ***: No se pudo encontrar el archivo '{ruta_archivo}'.")
    except Exception as e:
        print(f"*** ERROR INESPERADO ***: {e}")

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