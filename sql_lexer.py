#DECLARACION DE TOKENS, DEFINICION DE TOKENS, REGLAS ESPECIALES, CREACION DEL ANALIZADOR LEXICO

import ply.lex as lex # se instala con

# Definición de tokens

tokens = [
    'ID', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQ', 'LT', 'GE',
    'AND', 'OR',
]

# Palabras reservadas

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
}

tokens += list(reserved.values())

# Definición de expresiones regulares para tokens simples

t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_EQ     = r'='
t_LT     = r'<'
t_GE     = r'>='
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

    print(f"Error léxico en línea {t.lineno}: carácter inesperado '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()



if __name__ == "__main__":

    data = '''
    /* Ejemplo de consulta SQL */
    SElECT name, age FROM users WHERE age >= 18 AND status = 'active';
    CREATE TABLE orders (id INT, amount DECIMAL);
    '''
    lexer.lineno = 1
    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)