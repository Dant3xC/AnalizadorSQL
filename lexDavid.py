#DECLARACION DE TOKENS, DEFINICION DE TOKENS, REGLAS ESPECIALES, CREACION DEL ANALIZADOR LEXICO
import ply.lex as lex # se instala con 

# --- 1. Definición de tokens ---
tokens = [
    'ID', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQ', 'LT', 'GE',
    'LPAREN', 'RPAREN', 'COMMA',
]
# --- 2. Palabras reservadas ---
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
    'or': 'OR',
}
# Se añaden las palabras reservadas a la lista principal de tokens
tokens += list(reserved.values())

# --- 3. Definición de expresiones regulares para tokens simples ---
# Se usan "raw strings" (r'...') y se escapan los metacaracteres
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_EQ     = r'='
t_LT     = r'<'
t_GE     = r'>='
t_LPAREN = r'\(' 
t_RPAREN = r'\)' 
t_COMMA  = r','

t_ignore = ' \t'

# --- 4. Definición de reglas con funciones ---

# Regla para ID y Palabras Reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Convierte a minúsculas y busca en el diccionario de reservadas
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

# Regla para Números
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    return t

# Regla para Strings
def t_STRING(t):
    r'\'[^\']*\''
    return t

# Regla para Comentarios
def t_COMMENT(t):
    r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/'
    pass  # ignora comentarios

# Regla para manejar saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regla para manejar errores
def t_error(t):
    print(f"Error léxico en línea {t.lineno}: carácter inesperado '{t.value[0]}'")
    t.lexer.skip(1)

# --- 5. Construcción del Analizador Léxico ---
lexer = lex.lex()

# --- 6. Bloque de prueba ---
if __name__ == "__main__":
    data = '''
    /* Ejemplo de consulta SQL */
    SELECT name, age FROM users WHERE age >= 18 AND status = 'active';
    CREATE TABLE orders (id INT, amount DECIMAL);
    '''
    lexer.lineno = 1
    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

#Para el informe realizar una tabla de tokens con descripcion y expresion regular