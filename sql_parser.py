# -*- coding: utf-8 -*-
import ply.yacc as yacc

# Importamos AMBOS, los tokens y la instancia del lexer
from sql_lexer import tokens, lexer 

# --- Definición de la Precedencia de Operadores ---
# De MENOR a MAYOR precedencia.
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQ', 'LT', 'GE'),  # No asociativos
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# --- Definición de la Gramática (Reglas de Producción) ---

def p_program(p):
    '''program : statements'''
    print("-> Análisis Sintáctico Finalizado: Programa VÁLIDO.")
    p[0] = p[1]

def p_statements(p):
    '''statements : statement
                  | statements statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]] # Añade la nueva sentencia a la lista

def p_statement(p):
    '''statement : create_statement
                 | select_statement'''
    # Una sentencia puede ser CREATE o SELECT
    p[0] = p[1]

# --- Reglas para CREATE TABLE (¡Esta es la que faltaba!) ---

def p_create_statement(p):
    '''create_statement : CREATE TABLE ID '(' column_definitions ')' '''
    print(f"Detectada sentencia CREATE TABLE para: {p[3]}")
    # Creamos un nodo para el AST (Árbol de Sintaxis Abstracta)
    p[0] = ('CREATE_TABLE', p[3], p[5]) 

def p_column_definitions(p):
    '''column_definitions : column_definition
                         | column_definitions ',' column_definition'''
    if len(p) == 2:
        p[0] = [p[1]]  # Una lista con la primera columna
    else:
        p[0] = p[1] + [p[3]] # Añade la nueva columna a la lista

def p_column_definition(p):
    '''column_definition : ID data_type'''
    p[0] = ('COLUMN', p[1], p[2]) # (nombre_columna, tipo_dato)

def p_data_type(p):
    '''data_type : INT
                 | CHAR
                 | DECIMAL'''
    p[0] = p[1]  # El valor del nodo es el token mismo

# --- Reglas para SELECT (¡Esta también faltaba!) ---

def p_select_statement(p):
    '''select_statement : SELECT select_list FROM ID
                        | SELECT select_list FROM ID HAVING condition'''
    print(f"Detectada sentencia SELECT para la tabla: {p[4]}")
    if len(p) == 5:
        p[0] = ('SELECT', p[2], p[4]) # (SELECT, lista_cols, tabla)
    else:
        p[0] = ('SELECT_HAVING', p[2], p[4], p[6]) # (SELECT, lista_cols, tabla, condicion_having)

def p_select_list(p):
    '''select_list : ID
                   | function
                   | select_list ',' ID
                   | select_list ',' function'''
    if len(p) == 2:
        p[0] = [p[1]] # Lista inicial (ID o funcion)
    else:
        p[0] = p[1] + [p[3]] # Añadir a la lista

# --- Reglas para Funciones y Condiciones ---

def p_function(p):
    '''function : SUM '(' ID ')'
                | COUNT '(' ID ')'
                | MIN '(' ID ')' '''
    p[0] = ('FUNCTION', p[1], p[3]) # (FUNCTION, 'SUM', 'col_name')

def p_condition(p):
    '''condition : expression EQ expression
                 | expression LT expression
                 | expression GE expression
                 | condition AND condition
                 | condition OR condition'''
    # p[1] es la expr izq, p[2] el operador, p[3] la expr der
    p[0] = (p[2], p[1], p[3]) # (operador, izq, der)

def p_expression(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | ID
                  | NUMBER
                  | function'''
    if len(p) == 2:
        p[0] = p[1]  # Es un terminal (ID, NUMBER) o una función
    else:
        p[0] = (p[2], p[1], p[3]) # (operador, izq, der)

# --- Manejo de Errores Sintácticos ---
def p_error(p):
    if p:
        print(f"*** ERROR DE SINTAXIS ***")
        print(f"  Línea {p.lineno}: Token inesperado '{p.value}' (Tipo: {p.type})")
        # Detener el parser
        parser.errok()
    else:
        print("*** ERROR DE SINTAXIS ***")
        print("  Fin de archivo inesperado (EOF).")

# --- Construir el Parser ---
# Esta línea DEBE estar al final y en el ámbito global
parser = yacc.yacc()

# --- Bloque de prueba (opcional, para probar este archivo solo) ---
if __name__ == "__main__":
    
    test_data = '''
        CREATE TABLE prueba (id INT);
        SELECT id FROM prueba HAVING id > 10;
    '''
    print("--- Probando sql_parser.py directamente ---")
    result = parser.parse(test_data, lexer=lexer)
    print("--- Fin de la prueba ---")
    if result:
        print("\nResultado AST:")
        for stmt in result:
            print(stmt)