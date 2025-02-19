import ply.lex as lex
import re

literals = ['(', ')', ':', ';', ',']

tokens = [
    'NUM',
    'ADD',
    'SUB',
    'MUL',
    'DIV',
    'MOD',
    'DOT',
    'CONDITION',
    'NOT',
    'DUP',
    'POP',
    'SWAP',
    'NEGATE',
    'DEPTH',
    'EMPTY'
]

def t_ADD(t):
    r'\+'
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
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

def t_DOT(t):
    r'\.'
    return t

def t_CONDITION(t):
    r'(=)|(<=)|(>=)|<|>'
    return t

def t_NOT(t):
    r'[nN][oO][tT]'
    return t

def t_DUP(t):
    r'[dD][uU][pP]'
    return t

def t_POP(t):
    r'[pP][oO][pP]'
    return t

def t_SWAP(t):
    r'[sS][wW][aA][pP]'
    return t

def t_NEGATE(t):
    r'[nN][eE][gG][aA][tT][eE]'
    return t

def t_DEPTH(t):
    r'[dD][eE][pP][tT][hH]'
    return t

def t_EMPTY(t):
    r'[eE][mM][pP][tT][yY]'
    return t

t_ignore = ' \n\t'

def t_error(t):
    print(f"Caracter Ilegal : {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()
