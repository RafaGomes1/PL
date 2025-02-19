import ply.lex as lex
import re

literals = ['(', ')', ':', ';', '.']

tokens = [
    '2DUP',
    'NUM',
    'ADD',
    'DASHDASH',
    'SUB',
    'MUL',
    'DIV',
    'MOD',
    'SWAP',
    'EMIT',
    'KEY',
    'CHAR',
    'OR',
    'AND',
    'CR',
    'SPACES',
    'SPACE',
    'DROP',
    'DEPTH',
    'DUP',
    'CONDITION',
    'IF',
    'THEN',
    'ELSE',
    'VARIABLE',
    'STORE',
    'FETCH',
    'LOOP',
    'DO',
    'BEGIN',
    "TEXTO",
    'ID'
]

def t_2DUP(t):
    r'2[dD][uU][pP]'
    return t

def t_ADD(t):
    r'\+'
    return t

def t_DASHDASH(t):
    r'\-\-'
    return t

def t_SUB(t):
    r'\-'
    return t

def t_MUL(t):
    r'\*'
    return t

def t_DIV(t):
    r'\/'
    return t

def t_MOD(t):
    r'\%'
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_SWAP(t):
    r'[sS][wW][aA][pP]'
    return t

def t_EMIT(t):
    r'[eE][mM][iI][tT]'
    return t

def t_KEY(t):
    r'[kK][eE][yY]'
    return t

def t_CHAR(t):
    r'[cC][hH][aA][rR]'
    return t

def t_OR(t):
    r'[oO][rR]'
    return t

def t_AND(t):
    r'[aA][nN][dD]'
    return t

def t_CR(t):
    r'[cC][rR]'
    return t

def t_SPACES(t):
    r'[sS][pP][aA][cC][eE][sS]'
    return t

def t_SPACE(t):
    r'[sS][pP][aA][cC][eE]'
    return t

def t_DROP(t):
    r'[dD][rR][oO][pP]'
    return t

def t_DEPTH(t):
    r'[dD][eE][pP][tT][hH]'
    return t

def t_DUP(t):
    r'[dD][uU][pP]'
    return t

def t_CONDITION(t):
    r'(=)|(<=)|(>=)|<|>'
    return t

def t_IF(t):
    r'[iI][fF]'
    return t

def t_THEN(t):
    r'[tT][hH][eE][nN]'
    return t

def t_ELSE(t):
    r'[eE][lL][sS][eE]'
    return t

def t_VARIABLE(t):
    r'[vV][aA][rR][iI][aA][bB][lL][eE]'
    return t

def t_STORE(t):
    r'\!'
    return t

def t_FETCH(t):
    r'\@'
    return t

def t_LOOP(t):
    r'[lL][oO][oO][pP]'
    return t

def t_DO(t):
    r'[dD][oO]'
    return t

def t_BEGIN(t):
    r'[bB][eE][gG][iI][nN]'
    return t

def t_TEXTO(t):
    r'"([^"]*)"'
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z\-0-9]*'
    return t

t_ignore = ' \n\t'

def t_error(t):
    print(f"Caracter Ilegal : {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()
