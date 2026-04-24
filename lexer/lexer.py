try:
    import ply.lex as lex
except ModuleNotFoundError:
    raise ModuleNotFoundError("Missing dependency 'ply'. Install it with: pip install ply")

# 2️⃣ Reserved keywords
reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'printf': 'PRINTF'
}

# 1️⃣ List of token names
tokens = [
    'ID',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'ASSIGN',
    'EQ',
    'NE',
    'LT',
    'GT',
    'LE',
    'GE',
    'SEMICOLON',
    'COMMA',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
] + list(reserved.values())

# 3️⃣ Regular expressions for tokens
t_PLUS       = r'\+'
t_MINUS      = r'-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'
t_EQ         = r'=='
t_ASSIGN     = r'='
t_NE         = r'!='
t_LE         = r'<='
t_GE         = r'>='
t_LT         = r'<'
t_GT         = r'>'
t_SEMICOLON  = r';'
t_COMMA      = r','
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_LBRACE     = r'\{'
t_RBRACE     = r'\}'

# 4️⃣ Ignore spaces & tabs
t_ignore = ' \t'

# 5️⃣ Number (int + float)
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# 6️⃣ Identifier or keyword
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# 7️⃣ Newlines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# 8️⃣ Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

# 9️⃣ Build lexer
lexer = lex.lex()
