#  SQL Parser - Proyecto Integrador 

¡Bienvenido al repositorio del Analizador Léxico y Sintáctico para un subconjunto de SQL! Este proyecto fue desarrollado como parte del curso de Compiladores y muestra cómo utilizar herramientas como `PLY` para construir un analizador robusto y funcional.


## Descripción General

Este proyecto consiste en un analizador léxico y sintáctico para un lenguaje SQL simplificado. El analizador es capaz de procesar sentencias `CREATE TABLE` y `SELECT ... HAVING`, validando la estructura léxica y sintáctica del código de entrada. Al finalizar, genera un Árbol Sintáctico Abstracto (AST) que representa la estructura jerárquica del código analizado.

El objetivo principal es demostrar los conceptos clave del proceso de compilación, incluyendo:
- Análisis Léxico: Reconocimiento de "palabras" o `tokens`.
- Análisis Sintáctico: Verificación de la estructura gramatical del código.
- Manejo de Errores: Identificación y reporte de errores léxicos y sintácticos.



## Tecnología Utilizada

- Python: El lenguaje de programación principal.
- PLY (Python Lex-Yacc): Una librería fundamental en Python para construir analizadores léxicos y sintácticos. `PLY` se inspira en las herramientas clásicas `Lex` y `Yacc` del ecosistema C, pero con la flexibilidad y simplicidad de Python.



## Cómo Iniciar y Ejecutar el Analizador

### 1. Prerrequisitos

Tener Python 3 instalado. Además de la librería `PLY`. Para instalarla se utiliza el siguiente comando:

pip install ply


### 2. Ejecutar el Analizador

El programa principal es `analizador.py` y se ejecuta desde la línea de comandos, abriendo un menu simple que muestra todos los archivos de prueba disponibles en la carpeta `casos_prueba/` pudiendo agregar mas archivos de prueba en la misma y ejecutarlos desde el menu tanto .sql y .txt

python analizador.py


## Resultados Esperados

Dentro de la carpeta `casos_prueba/` encontrarás tres archivos para demostrar el comportamiento del analizador.

### 1. Caso Exitoso (`prueba_ok.sql`)

Al analizar un archivo con sintaxis correcta, el programa imprimirá el Árbol Sintáctico Abstracto (AST) resultante.


Salida Esperada:
```
--- Iniciando análisis de: casos_prueba/prueba_ok.sql ---

Detectada sentencia CREATE TABLE para: alumnos
Detectada sentencia SELECT para la tabla: alumnos
-> Análisis sintáctico finalizado: Programa válido.

--- Árbol Sintáctico Abstracto (AST) ---
{'type': 'CREATE_TABLE', 'table': 'alumnos', 'columns': [{'column': 'id', 'type': 'INT'}, {'column': 'nombre', 'type': 'CHAR'}, {'column': 'promedio', 'type': 'DECIMAL'}]}
{'type': 'SELECT_HAVING', 'columns': ['id', {'function': 'SUM', 'column': 'promedio'}], 'table': 'alumnos', 'condition': {'op': '>', 'left': {'function': 'SUM', 'column': 'promedio'}, 'right': '6'}}

--- Análisis Finalizado ---
```

### 2. Error Léxico (`prueba_error_lexico.sql`)

Este archivo contiene un carácter inválido (`@`). El analizador léxico lo detectará y detendrá el proceso antes de llegar al análisis sintáctico.


Salida Esperada:
```
--- Iniciando análisis de: casos_prueba/prueba_error_lexico.sql ---

Se detectaron errores léxicos. No se ejecutará el análisis sintáctico.
Error léxico en línea 2: carácter inesperado '@'

--- Análisis finalizado (con errores léxicos) ---
```

### 3. Error Sintáctico (`prueba_error_sintaxis.sql`)

Este archivo tiene una sintaxis incorrecta (falta un paréntesis). El analizador léxico no encontrará problemas, pero el analizador sintáctico fallará y reportará el error.


Salida Esperada:
```
--- Iniciando análisis de: casos_prueba/prueba_error_sintaxis.sql ---

ERROR DE SINTAXIS: Línea 2: Token inesperado ';' (SEMI)

--- Análisis Finalizado ---
```

---


