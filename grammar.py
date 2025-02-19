import ply.yacc as yacc
import sys
from lex import tokens
import re

# Stack para armazenar os números
stack = []

# Stack para auxiliar quando é para fazer WRITE de um NUM ou de uma STRING
dotAuxiliarStack = []

# Dicionário para armazenar as funções
functions = {}

# Dicionário para armazenar as variáveis
variables = {}

def p_Frase(p):
    '''
    Phrase : Phrase Expression
           | Phrase Function
           | Expression
           | Function
    '''
    if len(p) == 3:
        if p[1] is None:
            p[0] = p[2]
        elif p[2] is None:
            p[0] = p[1]
        else:
            p[0] = p[1] + p[2]
    else:
        p[0] = p[1]
    
    if p[0] is not None:
        stack.extend(p[0])

def p_Expression(p):
    '''
    Expression : Command
               | Expression Command
    '''
    if len(p) == 2:
        if isinstance(p[1], list):
            p[0] = p[1]
        elif p[1] is not None:
            p[0] = [p[1]]
    else:
        if isinstance(p[2], list):
            p[0] = p[1] + p[2]
        else:
            p[0] = p[1] + [p[2]]

def p_Function1(p): # Funções Com e Sem Argumentos
    '''
    Function : ':' ID '(' Args DASHDASH Args ')' Expression ';'
    '''
    index = len(functions) + len(variables)
    functions[p[2]] = {
        'args': p[4],     # Armazena o número de argumentos da função
        'nOutput': p[6],  # Armazena o número de outputs da função
        'body': p[8],     # Armazena o corpo da função como uma lista de comandos
        'result': [],
        'index': index,
        'activated': False
    }
    res = functions[p[2]]['result']
    res.append(p[2]+":")
    a = functions[p[2]]['args']
    while a > 0:
        res.append("PUSHFP")
        res.append("LOAD " + str(-a))
        a -= 1
    n = functions[p[2]]['nOutput']
    res.extend(functions[p[2]]['body'])
    while n > 0:
        res.append("STOREG " + str(index))
        n-= 1
    res.append("RETURN")

def p_Function2(p): # Funções com Strings
    '''
    Function : ':' ID Expression ';'
    '''
    functions[p[2]] = {
        'args': 0,     # Armazena o número de argumentos da função
        'nOutput': 0,  # Armazena o número de outputs da função
        'body': p[3],  # Armazena o corpo da função como uma lista de comandos
        'result': [],
        'index': len(functions) + len(variables),
        'activated': False
    }
    index = len(functions) + len(variables)
    res = functions[p[2]]['result']
    res.append(p[2]+":")
    res.extend(functions[p[2]]['body'])
    res.append("RETURN")

def p_Args(p):
    '''
    Args : ID
         | Args ID
         | 
    '''
    if len(p) == 2:
        p[0] = 1
    elif len(p) == 3:
        p[0] = p[1] + 1
    else:
        p[0] = 0

def p_Command1(p):
    '''
    Command : NUM
    '''
    p[0] = "PUSHI " + str(p[1])

def p_Command2(p):
    '''
    Command : Operation
    '''
    p[0] = p[1]

def p_Command3(p):
    '''
    Command : '.' TEXTO
    '''
    p[0] = ['PUSHS '+ p[2], 'WRITES']

def p_Command4(p):
    '''
    Command : '.'
    '''
    if dotAuxiliarStack == []:
        p[0] = 'WRITEI'
    elif dotAuxiliarStack[-1] == 'STRING':
        dotAuxiliarStack.pop()
        p[0] = 'WRITES'
    else:
        p[0] = 'WRITEI'

def p_Command5(p):
    '''
    Command : ID
    '''
    if (p[1] in functions):
        if (functions[p[1]]['args']) > 0 and (functions[p[1]]['nOutput']) > 0:
            p[0] = [
                "PUSHA " + p[1],
                "CALL",
                "POP " + str(functions[p[1]]['args']),
                "PUSHG " + str(functions[p[1]]['index'])
            ]
        elif (functions[p[1]]['args']) > 0 and (functions[p[1]]['nOutput']) == 0:
            p[0] = [
                "PUSHA " + p[1],
                "CALL",
                "POP " + str(functions[p[1]]['args']),
            ]
        else:
            p[0] = ["PUSHA " + p[1], "CALL"]
        functions[p[1]]['activated'] = True

def p_Command6(p):
    '''
    Command : SWAP
    '''
    p[0] = "SWAP"

def p_Command7(p):
    '''
    Command : EMIT
    '''
    p[0] = "WRITECHR"

def p_Command8(p):
    '''
    Command : KEY
    '''
    dotAuxiliarStack.append('STRING')
    p[0] = "READ"

def p_Command9(p):
    '''
    Command : Char
    '''
    p[0] = p[1]

def p_Char(p):
    '''
    Char : CHAR ID
    '''
    p[0] = [
        'PUSHS "' + p[2] + '"',
        'CHRCODE'
    ]

def p_Command10(p):
    '''
    Command : OR
    '''
    p[0] = "OR"

def p_Command11(p):
    '''
    Command : AND
    '''
    p[0] = "AND"

def p_Command12(p):
    '''
    Command : CR
    '''
    p[0] = "WRITELN"

def p_Command13(p):
    '''
    Command : SPACE
    '''
    p[0] = ['PUSHS " "', 'WRITES']
    
def p_Command14(p):
    '''
    Command : 2DUP
    '''

    p[0] = [
        'PUSHSP',
        'LOAD -1',
        'PUSHSP',
        'LOAD -1'
    ]

def p_Command15(p):
    '''
    Command : SPACES
    '''

    if 'SPACES' not in functions:
        result = [
            'SPACES:',
            'PUSHFP',
            'LOAD -2',
            'PUSHI 0',
            'SUP',
            'jz ENDSPACES',
            'PUSHFP',
            'LOAD -2',
            'PUSHI 1',
            'SUB',
            'STOREL -2',
            'PUSHFP',
            'LOAD -1',
            'PUSHS " "',
            'CONCAT',
            'STOREL -1',
            'JUMP SPACES',
            'ENDSPACES:',
            'RETURN'
        ]

        functions['SPACES'] = {
            'args': 0,
            'nOutput': 0,
            'body': "",
            'result': result,
            'index': len(functions) + len(variables),
            'activated': True
        }

    p[0] = [
        'PUSHS ""',
        'PUSHA SPACES',
        'CALL',
        'WRITES',
        'POP 1'
    ]

def p_Command16(p):
    '''
    Command : DROP
    '''
    p[0] = "POP 1"

def p_Command17(p):
    '''
    Command : DEPTH
    '''
    if 'DEPTH' not in functions:
        index = len(functions) + len(variables)
        result = [
            'DEPTH:',
            'PUSHG ' + str(index),
            'PUSHI 1',
            'ADD',
            'STOREG ' + str(index),
            'PUSHFP',
            'LOAD 0',
            'PUSHGP',
            'PUSHG ' + str(index),
            'LOADN',
            'EQUAL',
            'JZ DEPTH',
            'PUSHG ' + str(index),
            'MAX FUNCTIONS - 1',
            'SUB',
            'STOREG ' + str(index),
            'RETURN'
        ]
        functions['DEPTH'] = {
            'args': 0,
            'nOutput': 1,
            'body': "",
            'result': result,
            'index': index,
            'activated': True
        }

        p[0] = [
            'PUSHA DEPTH',
            'CALL',
            'PUSHG ' + str(index)
        ]

def p_Command18(p):
    '''
    Command : DUP
    '''
    p[0] = 'DUP 1'

def p_Command19(p):
    '''
    Command : Variables
    '''
    p[0] = p[1]

def p_Command20(p):
    '''
    Command : Conditional
    '''
    p[0] = p[1]

def p_Command21(p):
    '''
    Command : Cycle
    '''
    p[0] = p[1]

def p_Conditional1(p):
    '''
    Conditional : Condition IF Expression ELSE Expression THEN
    '''
    aux = []
    aux.append(p[1])
    aux.append('jz ELSE')
    aux.extend(p[3])
    aux.append('JUMP THEN')
    aux.append('ELSE:')
    aux.extend(p[5])
    aux.append('THEN:')
    p[0] = aux

def p_Conditional2(p):
    '''
    Conditional : Condition IF Expression THEN
    '''
    aux = []
    aux.append(p[1])
    aux.append('jz THEN')
    aux.extend(p[3])
    aux.append('THEN:')
    p[0] = aux

def p_Condtion(p):
    '''
    Condition : CONDITION
    '''
    if p[1] == '=':
        p[0] = "EQUAL"
    elif p[1] == '<=':
        p[0] = "INFEQ"
    elif p[1] == '>=':
        p[0] = "SUPEQ"
    elif p[1] == '<':
        p[0] = "INF"
    elif p[1] == '>':
        p[0] = "SUP"

def p_Variables1(p):
    '''
    Variables : VARIABLE ID
    '''
    variables[p[2]] = {
        'index': len(functions) + len(variables) 
    }
    p[0] = []
    
def p_Variables2(p):
    '''
    Variables : ID FETCH
    '''
    p[0] = 'PUSHG ' + str(variables[p[1]]['index'])

def p_Variables3(p):
    '''
    Variables : ID STORE
    '''
    p[0] = 'STOREG ' + str(variables[p[1]]['index'])

def p_Cycle(p):
    '''
    Cycle : BEGIN Expression DO Expression LOOP
    '''
    aux = []
    aux.extend(p[2])
    aux.extend(['ALLOC 2', 'SWAP', 'STORE 0', 'PUSHST 0', 'SWAP', 'STORE 1', 'CYCLE:'])
    aux.extend(p[4])
    aux.extend(['PUSHST 0', 'LOAD 0', 'PUSHI 1', 'ADD','DUP 1', 'PUSHST 0', 'SWAP', 'STORE 0', 'PUSHST 0', 'LOAD 1',
                'EQUAL', 'JZ  REPEAT', 'JUMP ENDCYCLE', 'REPEAT:', 'JUMP CYCLE', 'ENDCYCLE:'])
    p[0] = aux

def p_Operation1(p):
    '''
    Operation : ADD
    '''
    p[0] = "ADD"

def p_Operation2(p):
    '''
    Operation : SUB
    '''
    p[0] = "SUB"

def p_Operation3(p):
    '''
    Operation : MUL
    '''
    p[0] = "MUL"

def p_Operation4(p):
    '''
    Operation : DIV
    '''
    p[0] = "DIV"

def p_Operation5(p):
    '''
    Operation : MOD
    '''
    p[0] = "MOD"

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
    if stack != []:
        stack.insert(0, "START")
        stack.append("STOP")

    for f in reversed(functions):
        if functions[f]['nOutput'] != 0 and functions[f]['activated'] == True:
            if f == 'DEPTH':
                indice = functions[f]['result'].index('MAX FUNCTIONS - 1')
                print("INDICE: " + str(indice))
                functions[f]['result'][indice] = 'PUSHI ' + str(len(functions) + len(variables) - 1)
            else:
                stack.insert(0,"PUSHI 0")

    for a in reversed(variables):
            stack.insert(0,"PUSHI " + str(variables[a]['index']))

    for f in functions:
        stack.extend(functions[f]['result'])

    print("Parsing terminou com sucesso!")
    print("----------------------------------------")
    print("COMMANDS:")
    for i in stack:
        print(i)