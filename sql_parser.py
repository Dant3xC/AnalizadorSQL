# -*- coding: utf-8 -*-
# sql_parser.py

import ply.yacc as yacc
from sql_lexer import tokens, lexer

# Variable global para controlar si hubo errores
hubo_error = False

# --- ELIMINADA LA TUPLA PRECEDENCE (Requisito del profesor) ---
# La precedencia ahora se define por la jerarquía de las reglas gramaticales.

# --- Reglas gramaticales ---

def p_program(p):
    '''program : statements'''
    global hubo_error
    # Solo imprimimos "Válido" si NO hubo ningún error durante el análisis
    if not hubo_error:
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
    # Se eliminó el print intermedio para limpiar la salida como pidió el docente
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

# --- CONDICIONES (Lógica Jerárquica para Precedencia OR < AND) ---
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
    hubo_error = True  # ¡MARCAMOS EL ERROR!
    if p:
        print(f"*** ERROR DE SINTAXIS *** Línea {p.lineno}: Token inesperado '{p.value}' ({p.type})")
    else:
        print("*** ERROR DE SINTAXIS *** Fin de archivo inesperado (EOF).")

# --- Construcción del parser ---
parser = yacc.yacc()