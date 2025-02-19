import ply.yacc as yacc
import sys
from extra_lex import tokens
import re

# Stack para armazenar os números
stack = []

def p_Expression(p):
    '''
    Expression : Command
               | Expression Command
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_Command1(p):
    """
    Command : NUM
               | "(" SUB NUM ")"
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = -p[3]
    stack.append(p[0])
    print("Push:", p[0])
    print("Stack:", stack)

def p_Command2(p):
    '''
    Command : Operation
    '''
    stack.append(p[1])
    print("Stack:", stack)
    p[0] = p[1]

def p_Command3(p):
    '''
    Command : DOT
    '''
    print("Topo da Stack:", stack[-1])
    p[0] = p[1]

def p_Command4(p):
    '''
    Command : CONDITION
    '''
    if len(stack) < 2:
        print(f"ERROR! Condition {p[1]} Number of arguments is not enough!")
        parser.success = False
    else:
        operand2 = stack.pop()
        operand1 = stack.pop()
        bool = 0
        if p[1] == '=':
            if operand1 == operand2:
                bool = 1
        elif p[1] == '<=':
            if operand1 <= operand2:
                bool = 1
        elif p[1] == '>=':
            if operand1 >= operand2:
                bool = 1
        elif p[1] == '<':
            if operand1 < operand2:
                bool = 1
        elif p[1] == '>':
            if operand1 > operand2:
                bool = 1
        print("Condition:", p[1])
        stack.append(bool)
        print("Stack:", stack)
        p[0] = p[1]

def p_Commmand5(p):
    '''
    Command : NOT
    '''
    if len(stack) < 1:
        print(f"ERROR! Condition {p[1]} Number of arguments is not enough!")
        parser.success = False
    else:
        stack.pop()
        stack.append(0)
        print("Command:", p[1])
        print("Stack:", stack)
        p[0] = p[1]

def p_Command6(p):
    '''
    Command : DUP
    '''
    if len(stack) < 1:
        print(f"ERROR! Condition {p[1]} Number of arguments is not enough!")
        parser.success = False
    else:
        d = stack.pop()
        stack.append(d)
        stack.append(d)
        print("Command:", p[1])
        print("Stack:", stack)
        p[0] = p[1]

def p_Command7(p):
    '''
    Command : POP
    '''
    if len(stack) < 1:
        print(f"ERROR! Condition {p[1]} Number of arguments is not enough!")
        parser.success = False
    else:
        stack.pop()
        print("Command:", p[1])
        print("Stack:", stack)
        p[0] = p[1]

def p_Command8(p):
    '''
    Command : SWAP
    '''
    if len(stack) < 2:
        print(f"ERROR! Condition {p[1]} Number of arguments is not enough!")
        parser.success = False
    else:
        p1 = stack.pop()
        p2 = stack.pop()
        stack.append(p1)
        stack.append(p2)
        print("Command:", p[1])
        print("Stack:", stack)
        p[0] = p[1]

def p_Command9(p):
    '''
    Command : NEGATE
    '''
    if len(stack) < 1:
        print(f"ERROR! Condition {p[1]} Number of arguments is not enough!")
        parser.success = False
    else:
        x = stack.pop()
        stack.append(-1*x)
        print("Command:", p[1])
        print("Stack:", stack)
        p[0] = p[1]

def p_Command10(p):
    '''
    Command : DEPTH
    '''
    print("Tamanho da Stack:", len(stack))
    p[0] = p[1]

def p_Command11(p):
    '''
    Command : EMPTY
    '''
    global stack
    stack = []
    print("Command:", p[1])
    print("Stack:", stack)
    p[0] = p[1]

def p_Operation1(p):
    '''
    Operation : ADD
    '''
    print("Operation:", p[1])
    if len(stack) < 2:
        print(f"ERROR! Condition {p[1]} Number of arguments is not enough!")
        parser.success = False
    else:
        operand2 = stack.pop()
        operand1 = stack.pop()
        p[0] = operand1 + operand2

def p_Operation2(p):
    '''
    Operation : SUB
    '''
    print("Operation:", p[1])
    if len(stack) < 2:
        print(f"ERROR! Condition {p[1]} Number of arguments is not enough!")
        parser.success = False
    else:
        operand2 = stack.pop()
        operand1 = stack.pop()
        p[0] = operand1 - operand2

def p_Operation3(p):
    '''
    Operation : MUL
    '''
    print("Operation:", p[1])
    if len(stack) < 2:
        print(f"ERROR! Condition {p[1]} Number of arguments is not enough!")
        parser.success = False
    else:
        operand2 = stack.pop()
        operand1 = stack.pop()
        p[0] = operand1 * operand2

def p_Operation4(p):
    '''
    Operation : DIV
    '''
    print("Operation:", p[1])
    if len(stack) < 2:
        print(f"ERROR! Condition {p[1]} Number of arguments is not enough!")
        parser.success = False
    else:
        operand2 = stack.pop()
        operand1 = stack.pop()
        p[0] = operand1 / operand2

def p_Operation5(p):
    '''
    Operation : MOD
    '''
    print("Operation:", p[1])
    if len(stack) < 2:
        print(f"ERROR! Condition {p[1]} Number of arguments is not enough!")
        parser.success = False
    else:
        operand2 = stack.pop()
        operand1 = stack.pop()
        p[0] = operand1 % operand2

def p_error(p):
    print("Erro sintático! Reescreva a frase.")
    parser.success = False

# Criar o parser
parser = yacc.yacc()
parser.success = True

# Ler a entrada
source = ""
for line in sys.stdin:
    source += line

# Fazer o parsing e avaliar a expressão
result = parser.parse(source)
if parser.success:
    print("Parsing terminou com sucesso!")