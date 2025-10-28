# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# ANALIZADOR LÉXICO SQL
# ------------------------------------------------------------
# Define los tokens, palabras reservadas y reglas para
# construir el analizador léxico con PLY.
# ------------------------------------------------------------

import ply.lex as lex

# --- Palabras reservadas ---
reserved = {
    'select': 'SELECT',
    'from': 'FROM',
    'where': 'WHERE',
    'having': 'HAVING',
    'create': 'CREATE',
    'table': 'TABLE',
    'int': 'INT',
    'char': 'CHAR',
    'decimal': 'DECIMAL',
    'sum': 'SUM',
    'count': 'COUNT',
    'min': 'MIN'
}

# --- Tokens ---
tokens = [
    'ID', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQ', 'LT', 'LE', 'GT', 'GE', 'NE',
    'AND', 'OR',
    'LPAREN', 'RPAREN', 'COMMA', 'SEMI'
] + list(reserved.values())

# --- Expresiones regulares para tokens simples ---
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_EQ     = r'='
t_LT     = r'<'
t_LE     = r'<='
t_GT     = r'>'
t_GE     = r'>='
t_NE     = r'!='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA  = r','
t_SEMI   = r';'
t_ignore = ' \t'

# --- Reglas de tokens con acciones ---
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    return t

def t_STRING(t):
    r'\'[^\']*\''
    return t

def t_COMMENT(t):
    r'/\*([^*]|\*+[^*/])*\*+/'
    pass  # Ignorar comentarios

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Error léxico en línea {t.lineno}: carácter inesperado '{t.value[0]}'")
    t.lexer.skip(1)

# --- Construcción del analizador léxico ---
lexer = lex.lex()

# --- Bloque de prueba ---
if __name__ == "__main__":
    data = '''
    /* Ejemplo de consulta SQL */
    SELECT name, age FROM users WHERE age >= 18 AND status = 'active';
    CREATE TABLE orders (id INT, amount DECIMAL);
    '''
    lexer.input(data)

    for tok in lexer:
        print(tok)
