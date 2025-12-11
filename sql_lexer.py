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
    'having': 'HAVING',
    'create': 'CREATE',
    'table': 'TABLE',
    'int': 'INT',
    'char': 'CHAR',
    'decimal': 'DECIMAL',
    'sum': 'SUM',
    'count': 'COUNT',
    'min': 'MIN',
    'and': 'AND',
    'or': 'OR'
}

# --- Tokens ---
tokens = [
    'ID', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQ', 'LT', 'LE', 'GT', 'GE', 'NE',
    'LPAREN', 'RPAREN', 'COMMA', 'SEMI'
] + list(reserved.values())

# --- RegEx simples ---
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
    pass  # ignora comentarios

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    # Imprimir error y detener inmediatamente
    print(f"Error léxico en línea {t.lineno}: carácter inesperado '{t.value[0]}'")
    raise Exception("LexicalError")

# Construcción del lexer
lexer = lex.lex()

# Bloque de prueba 
if __name__ == "__main__":
    data = '''
    /* Ejemplo */
    CREATE TABLE orders (id INT, amount DECIMAL);
    SELECT name FROM users WHERE age >= 18;
    '''
    lexer.input(data)
    for tok in lexer:
        print(tok)
    if getattr(lexer, 'lex_error', False):
        print("Errores léxicos encontrados:")
        for e in lexer.lex_errors:
            print(e)
