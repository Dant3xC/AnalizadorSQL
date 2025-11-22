# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# ANALIZADOR SINTÁCTICO SQL (Proyecto Integrador 2025)
# ------------------------------------------------------------
# Define la gramática para el subconjunto SQL del grupo 7:
# CREATE TABLE / SELECT ... HAVING
# ------------------------------------------------------------

import ply.yacc as yacc
from sql_lexer import tokens, lexer

# --- Precedencia de operadores ---
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQ', 'LT', 'LE', 'GT', 'GE', 'NE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# --- Reglas gramaticales ---

def p_program(p):
    '''program : statements'''
    print("-> Análisis sintáctico finalizado: Programa válido.")
    p[0] = p[1]

def p_statements(p):
    '''statements : statement
                  | statements statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : create_statement SEMI
                 | select_statement SEMI'''
    p[0] = p[1]

# --- CREATE TABLE ---
def p_create_statement(p):
    '''create_statement : CREATE TABLE ID LPAREN column_definitions RPAREN'''
    print(f"Detectada sentencia CREATE TABLE para: {p[3]}")
    p[0] = {'type': 'CREATE_TABLE', 'table': p[3], 'columns': p[5]}

def p_column_definitions(p):
    '''column_definitions : column_definition
                         | column_definitions COMMA column_definition'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_column_definition(p):
    '''column_definition : ID data_type'''
    p[0] = {'column': p[1], 'type': p[2]}

def p_data_type(p):
    '''data_type : INT
                 | CHAR
                 | DECIMAL'''
    p[0] = p[1]

# --- SELECT ---
def p_select_statement(p):
    '''select_statement : SELECT select_list FROM ID
                        | SELECT select_list FROM ID HAVING condition'''
    print(f"Detectada sentencia SELECT para la tabla: {p[4]}")
    if len(p) == 5:
        p[0] = {'type': 'SELECT', 'columns': p[2], 'table': p[4]}
    else:
        p[0] = {'type': 'SELECT_HAVING', 'columns': p[2], 'table': p[4], 'condition': p[6]}

def p_select_list(p):
    '''select_list : ID
                   | function
                   | select_list COMMA ID
                   | select_list COMMA function'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_function(p):
    '''function : SUM LPAREN ID RPAREN
                | COUNT LPAREN ID RPAREN
                | MIN LPAREN ID RPAREN'''
    p[0] = {'function': p[1], 'column': p[3]}

# --- Condiciones y expresiones ---
def p_condition(p):
    '''condition : expression EQ expression
                 | expression LT expression
                 | expression LE expression
                 | expression GT expression
                 | expression GE expression
                 | expression NE expression
                 | condition AND condition
                 | condition OR condition'''
    p[0] = {'op': p[2], 'left': p[1], 'right': p[3]}

def p_expression(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | ID
                  | NUMBER
                  | function'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {'op': p[2], 'left': p[1], 'right': p[3]}

# --- Manejo de errores ---
def p_error(p):
    if p:
        print(f"ERROR DE SINTAXIS: Línea {p.lineno}: Token inesperado '{p.value}' ({p.type})")
    else:
        print("ERROR DE SINTAXIS: Fin de archivo inesperado (EOF).")

# --- Construcción del parser ---
parser = yacc.yacc()

# --- Bloque de prueba ---
if __name__ == "__main__":
    test_data = '''
        CREATE TABLE alumnos (id INT, nombre CHAR, promedio DECIMAL);
        SELECT id, SUM(promedio) FROM alumnos HAVING SUM(promedio) > 6;
    '''
    print("--- Probando sql_parser.py ---")
    result = parser.parse(test_data, lexer=lexer)
    print("\nAST generado:")
    if result:
        for stmt in result:
            print(stmt)
