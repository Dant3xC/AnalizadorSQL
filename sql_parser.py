# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# ANALIZADOR SINTACTICO 
# ------------------------------------------------------------
# Define la gramática para el subconjunto SQL del grupo 7:
# CREATE TABLE / SELECT ... HAVING
# ------------------------------------------------------------

import ply.yacc as yacc
from sql_lexer import tokens, lexer

# Variable global para controlar si hubo errores
hubo_error = False


# --- Reglas gramaticales ---

def p_program(p):
    '''program : statements'''
    global hubo_error
    
    # Verificar errores sintácticos (hubo_error) Y TAMBIÉN léxicos
    errores_lexicos = getattr(lexer, 'lex_error', False)
    
    if not hubo_error and not errores_lexicos:
        print("-> Análisis sintáctico finalizado: Programa válido.")
    
    p[0] = p[1]

def p_statements(p):
    '''statements : sentencia
                  | statements sentencia'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''sentencia : sentencia_create SEMI
                 | sentencia_select SEMI'''
    p[0] = p[1]

# --- CREATE TABLE ---
def p_create_statement(p):
    '''sentencia_create : CREATE TABLE ID LPAREN lista_columnas RPAREN'''
    p[0] = {'type': 'CREATE_TABLE', 'table': p[3], 'columns': p[5]}

def p_column_definitions(p):
    '''lista_columnas : definicion_columna 
                         | lista_columnas COMMA definicion_columna'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_column_definition(p):
    '''definicion_columna : ID tipo_dato'''
    p[0] = {'column': p[1], 'type': p[2]}

def p_data_type(p):
    '''tipo_dato : INT
                 | CHAR
                 | DECIMAL'''
    p[0] = p[1]

# --- SELECT ---
def p_select_statement(p):
    '''sentencia_select : SELECT lista_seleccion FROM ID
                        | SELECT lista_seleccion FROM ID  HAVING condition'''
    if len(p) == 5:
        p[0] = {'type': 'SELECT', 'columns': p[2], 'table': p[4]}
    else:
        p[0] = {'type': 'SELECT_HAVING', 'columns': p[2], 'table': p[4], 'condition': p[6]}

def p_select_list(p):
    '''lista_seleccion : ID
                        | function
                        | lista_seleccion COMMA ID
                        | lista_seleccion COMMA function'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_function(p):
    '''function : SUM LPAREN ID RPAREN
                | COUNT LPAREN ID RPAREN
                | MIN LPAREN ID RPAREN'''
    p[0] = {'function': p[1], 'column': p[3]}

# --- CONDICIONES (Lógica Jerárquica para Precedencia OR < AND por jerarquía) ---
# Nivel más bajo: OR
def p_condition(p):
    '''condition : condition_term
                 | condition OR condition_term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {'op': 'OR', 'left': p[1], 'right': p[3]}

# Nivel medio: AND
def p_condition_term(p):
    '''condition_term : condition_factor
                      | condition_term AND condition_factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {'op': 'AND', 'left': p[1], 'right': p[3]}

# Nivel alto: Comparaciones
def p_condition_factor(p):
    '''condition_factor : expression EQ expression
                        | expression LT expression
                        | expression LE expression
                        | expression GT expression
                        | expression GE expression
                        | expression NE expression'''
    p[0] = {'op': p[2], 'left': p[1], 'right': p[3]}

# --- EXPRESIONES ARITMÉTICAS (Jerarquía: Suma < Prod < Factor) ---

# Nivel 1: Suma y Resta
def p_expression(p):
    '''expression : term
                  | expression PLUS term
                  | expression MINUS term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {'op': p[2], 'left': p[1], 'right': p[3]}

# Nivel 2: Multiplicación y División
def p_term(p):
    '''term : factor
            | term TIMES factor
            | term DIVIDE factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {'op': p[2], 'left': p[1], 'right': p[3]}

# Nivel 3: Factores (Números, IDs, Paréntesis, Funciones)
def p_factor(p):
    '''factor : ID
              | NUMBER
              | function
              | LPAREN expression RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        # Es paréntesis: ( expression )
        p[0] = p[2]

# --- Manejo de errores ---
def p_error(p):
    global hubo_error
    hubo_error = True  # se marca el error
    if p:
        print(f"Error de sintaxis en línea {p.lineno}: Token inesperado '{p.value}' ({p.type})")
    else:
        print("Error de sintaxis: Fin de archivo inesperado (EOF).")

# --- Construcción del parser ---
parser = yacc.yacc()