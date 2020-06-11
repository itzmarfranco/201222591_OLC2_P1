import ply.lex as lex
import ply.yacc as yacc
import sys

from graphviz import Digraph
import pydotplus
from node import Node
from SymbolTable import Table, Symbol
from Error import Error, ErrorList


dot = Digraph(comment='The Round Table')

dot.node('A', 'King Arthur' + 'TEST', shape='box')
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')
dot.edges(['AB'])
dot.edge('B', 'L', constraint='false')
graph = pydotplus.graph_from_dot_data(dot.source)
#Image(graph.create_png())
graph.write_png('tree.png')

a = Node('1', 'Nodo1', [])

ts = Table({})



def run(tree):
    if type(tree) == tuple:
        for node in tree:
            if(type(node) == tuple):
                if node[0] == '=':
                    print('Asignando ', node[1], ' -> ', node[2])
                    return None
                elif node[0] == '+':
                    return run(tree[1]) + run(tree[2])
            else:
                if node == 'main':
                    return run(tree[1])
            return run(node)

sym = Symbol('$VAR', 'int', 0, 1)
ts.add(sym)
ts.print()

lexicalErrors = ErrorList([])
syntacticErrors = ErrorList([])
semanticErrors = ErrorList([])

def run2(tree):
    #print('ARBOL = ', tree)
    if type(tree) == tuple:
        for node in tree:
            if type(node) == tuple:
                run2(node)
            else:
                if node == '=':
                    if run2(tree[2]) != None:
                        print('ASSIGNING ', tree[1], ' -> ', run2(tree[2]))
                    else:
                        error = Error('Cannot assign none value', 0,0)
                        semanticErrors.add(error)
                    #store in symbol table
                elif node == '+':
                    if type(tree[1]) == str and (type(tree[2] == int) or type(tree[2] == float)):
                        error = Error('Cannot add string and number', 0,0)
                        semanticErrors.add(error)
                        return
                    elif type(tree[2]) == str and (type(tree[1] == int) or type(tree[1] == float)):
                        error = Error('Cannot add string and number', 0,0)
                        semanticErrors.add(error)
                        return
                    else:
                        return run2(tree[1]) + run2(tree[2])
                elif node == '-':
                    if type(tree[1]) == str and (type(tree[2] == int) or type(tree[2] == float)):
                        error = Error('Cannot substract string and number', 0,0)
                        semanticErrors.add(error)
                        return
                    elif type(tree[2]) == str and (type(tree[1] == int) or type(tree[1] == float)):
                        error = Error('Cannot substract string and number', 0,0)
                        semanticErrors.add(error)
                        return
                    else:
                        return run2(tree[1]) - run2(tree[2])
                elif node == '*':
                    if type(tree[1]) == str and (type(tree[2] == int) or type(tree[2] == float)):
                        error = Error('Cannot multiply string and number', 0,0)
                        semanticErrors.add(error)
                        return
                    elif type(tree[2]) == str and (type(tree[1] == int) or type(tree[1] == float)):
                        error = Error('Cannot multiply string and number', 0,0)
                        semanticErrors.add(error)
                        return
                    else:
                        return run2(tree[1]) * run2(tree[2])
                elif node == '/':
                    if type(tree[1]) == str and (type(tree[2] == int) or type(tree[2] == float)):
                        error = Error('Cannot divide string and number', 0,0)
                        semanticErrors.add(error)
                        return
                    elif type(tree[2]) == str and (type(tree[1] == int) or type(tree[1] == float)):
                        error = Error('Cannot divide string and number', 0,0)
                        semanticErrors.add(error)
                        return
                    else:
                        return run2(tree[1]) - run2(tree[2])
                elif node == '%':
                    if type(tree[1]) == str and (type(tree[2] == int) or type(tree[2] == float)):
                        error = Error('Cannot get remainder from string and number', 0,0)
                        semanticErrors.add(error)
                        return
                    elif type(tree[2]) == str and (type(tree[1] == int) or type(tree[1] == float)):
                        error = Error('Cannot get remainder from string and number', 0,0)
                        semanticErrors.add(error)
                        return
                    else:
                        return run2(tree[1]) - run2(tree[2])
                elif node == 'if':
                    print('IF',  run2(tree[1]), tree[2])
                    #call 'search' function to locate tag and execute from there
                elif node == '<':
                    return run2(tree[1]) < run2(tree[2])
                elif node == '>':
                    return run2(tree[1]) > run2(tree[2])
                elif node == '<=':
                    return run2(tree[1]) <= run2(tree[2])
                elif node == '>=':
                    return run2(tree[1]) >= run2(tree[2])
                elif node == '==':
                    return run2(tree[1]) == run2(tree[2])
                elif node == '!=':
                    return run2(tree[1]) != run2(tree[2])
                elif node == '&&':
                    return run2(tree[1]) and run2(tree[2])
                elif node == '||':
                    return run2(tree[1]) or run2(tree[2])
                elif node == '!':
                    return not run2(tree[1])
                elif node == 'xor':
                    print(tree[1], '&', tree[2])
                    return run2(tree[1]) != run2(tree[2])
                elif node == '&':
                    return run2(tree[1]) and run2(tree[2])
                elif node == '|':
                    return run2(tree[1]) or run2(tree[2])
                elif node == '~':
                    return not run2(tree[1])
                elif node == '^':
                    return run2(tree[1]) != run2(tree[2])
                elif node == '<<':
                    return run2(tree[1]) << run2(tree[2])
                elif node == '>>':
                    return run2(tree[1]) >> run2(tree[2])
                elif node == 'print':
                    return print('PRINTING', run2(tree[1]))
                elif node == 'unset':
                    return print('DELETING', run2(tree[1]))
                elif node == 'exit':
                    return print('EXITING')
                elif node == 'goto':
                    return print('JUMPING TO', tree[1])
                elif node == 'tag':
                    return print('ADDING TAG', tree[1])
                elif node == 'array':
                    return print('CREATING ARRAY', tree[1])                                        
                elif node == 'read':
                    return print('READING TO', tree[1])                                        
                else:
                    return tree
    else:
        return tree


ss = '''
    main:
    $a55 = 0+9+9*5;
    if(56*0 < 7) goto labelA;
    
    '''

#Reserved words

reserved = {
    'if': 'IF',
    'unset': 'UNSET',
    'read': 'READ',
    'goto': 'GOTO',
    'print': 'PRINT',
    'main': 'MAIN',
    'exit': 'EXIT',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'abs': 'ABS',
    'xor': 'XOR',
    'array' : 'ARRAY'
}
# Create a list to hold all of the token names
tokens = [
    'TVAR', # $t0...$tn
    'AVAR', # $a0...$an
    'VVAR', # $v0...$vn
    'RAVAR', # $ra
    'SVAR', # $s0...$sn
    'SPVAR', # $sp
    'COLON', # :
    'COMMA', # ,
    'SEMICOLON', # ;
    'L_PAR', # (
    'R_PAR', # )
    'ASSIGN', # =
    'COMMENT', # #comment
    'NAME', # tags

    'PLUS', # +
    'MINUS', # -
    'MULTIPLY', # *
    'DIVIDE', # /
    'REMAINDER', # %

    'NOT', # !
    'AND', # &&
    'OR', # ||

    'NOT_B', # ~
    'AND_B', # &
    'OR_B', # |

    'XOR_B', # ^
    'SHIFT_L', # <<
    'SHIFT_R', # >>

    'EQUAL', # ==
    'NOT_EQUAL', # !=
    'GREATER', # >
    'LESS', # <
    'GREATER_EQUAL', # >=
    'LESS_EQUAL', # <=

    
    'L_BRACKET', # [
    'R_BRACKET', # ]
    'QUOTE_1', # '
    'QUOTE_2', # "

    'INTEGER', # 1 2 3...
    'DECIMAL', # 1.54...
    'STRING', # hello

    'NEWLINE' # \n
] + list(reserved.values())

# Use regular expressions to define what each token is
t_RAVAR = r'$ra'
t_SPVAR = r'$sp'
t_COLON = r'\:'
t_COMMA = r'\,'
t_SEMICOLON = r'\;'
t_L_PAR = r'\('
t_R_PAR = r'\)'
t_ASSIGN = r'\='


t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_REMAINDER = r'\%'

t_NOT = r'\!'
t_AND = r'\&\&'
t_OR = r'\|\|'
t_NOT_B = r'\~'
t_AND_B = r'\&'
t_OR_B = r'\|'
t_XOR_B = r'\^'
t_SHIFT_L = r'\<\<'
t_SHIFT_R = r'\>\>'

t_EQUAL = r'\='
t_NOT_EQUAL = r'\!\='
t_GREATER = r'\>'
t_LESS = r'\<'
t_GREATER_EQUAL = r'\>\='
t_LESS_EQUAL = r'\<\='

t_L_BRACKET = r'\['
t_R_BRACKET = r'\]'
t_QUOTE_1 = r'\''
t_QUOTE_2 = r'\"'

t_NEWLINE = r'\n'

# Ply's special t_ignore variable allows us to define characters the lexer will ignore.
# We're ignoring spaces.
t_ignore = r' \t'

# More complicated tokens, such as tokens that are more than 1 character in length
# are defined using functions.
# A float is 1 or more numbers followed by a dot (.) followed by 1 or more numbers again.
def t_TVAR(t):
    r'\$(T|t)((0)|[1-9]*)'
    return t

def t_AVAR(t):
    r'\$(A|a)((0)|[1-9]*)'
    return t

def t_VVAR(t):
    r'\$(V|v)((0)|[1-9]*)'
    return t    

def t_SVAR(t):
    r'\$(S|s)((0)|[1-9]*)'
    return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# An int is 1 or more numbers.
def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'(\' | \").*?(\' | \")'
    t.value = t.value[1:-1]
    return t 

# A NAME is a variable name. A variable can be 1 or more characters in length.
# The first character must be in the ranges a-z A-Z or be an underscore.
# Any character following the first character can be a-z A-Z 0-9 or an underscore.
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    #r'\?'
    #t.type = 'NAME'
    t.type = reserved.get(t.value, 'NAME')
    return t

def t_newLine(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
# Skip the current token and output 'Illegal characters' using the special Ply t_error function.
def t_error(t):
    print("Illegal characters!")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
lexer.input(ss)

# Ensure our parser understands the correct order of operations.
# The precedence variable is a special Ply variable.
precedence = (
    ('left', 'OR_B'),
    ('left', 'AND_B'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')

)


# Define our grammar. We allow expressions, var_assign's and empty's.
def p_start(p):
    '''
    start : MAIN COLON body
    '''
    p[0] = (p[3])
    print(p[0])
    root = p[0]
    print('####################')
    run2(root)
    print('####################')
    semanticErrors.print()


def p_body(p):
    '''
    body : goto body
        | unset body
        | print body
        | exit body
        | tag body
        | if body
        | assign body
        | declaration body
    '''    
    p[0] = (p[1], p[2])

def p_body_e(p):
    '''
    body : empty
    '''
    p[0] = None

def p_goto(p):
    '''
    goto : GOTO NAME SEMICOLON
    '''
    p[0] = ('goto', p[2])

def p_unset(p):
    '''
    unset : UNSET L_PAR TVAR R_PAR SEMICOLON
        | UNSET L_PAR AVAR R_PAR SEMICOLON
        | UNSET L_PAR VVAR R_PAR SEMICOLON
        | UNSET L_PAR SVAR R_PAR SEMICOLON
        | UNSET L_PAR SPVAR R_PAR SEMICOLON
        | UNSET L_PAR RAVAR R_PAR SEMICOLON
    '''
    p[0] = ('unset', p[3])

def p_print(p):
    '''
    print : PRINT L_PAR TVAR R_PAR SEMICOLON
        | PRINT L_PAR AVAR R_PAR SEMICOLON
        | PRINT L_PAR VVAR R_PAR SEMICOLON
        | PRINT L_PAR SVAR R_PAR SEMICOLON
        | PRINT L_PAR SPVAR R_PAR SEMICOLON
        | PRINT L_PAR RAVAR R_PAR SEMICOLON
    '''
    p[0] = ('print', p[3])

def p_exit(p):
    '''
    exit : EXIT SEMICOLON
    '''
    p[0] = p[1]    

def p_tag(p):
    '''
    tag : NAME COLON
    '''
    p[0] = ('tag', p[1])

def p_if(p):
    '''
    if : IF L_PAR condition R_PAR GOTO NAME SEMICOLON
    '''
    p[0] = ('if',  p[3], p[6])

def p_condition_1(p):
    '''
    condition : condition AND condition
        | condition OR condition
    '''
    p[0] = (p[2], p[1], p[3])

def p_condition_2(p):
    '''
    condition : NOT condition
    '''
    p[0] = (p[1], p[2])

def p_condition_3(p):
    '''
    condition : relational
    '''
    p[0] = p[1]

def p_relational_1(p):
    '''
    relational : arithmetic EQUAL arithmetic
        | arithmetic NOT_EQUAL arithmetic
        | arithmetic GREATER arithmetic
        | arithmetic LESS arithmetic
        | arithmetic GREATER_EQUAL arithmetic
        | arithmetic LESS_EQUAL arithmetic
    '''
    p[0] = (p[2], p[1], p[3])

def p_relational_2(p):
    '''
    relational : arithmetic
    '''
    p[0] = p[1]

def p_arithmetic_1(p):
    '''
    arithmetic : arithmetic PLUS arithmetic
        | arithmetic MINUS arithmetic
        | arithmetic MULTIPLY arithmetic
        | arithmetic DIVIDE arithmetic
        | arithmetic REMAINDER arithmetic
    '''
    p[0] = (p[2], p[1], p[3])

def p_arithmetic_2(p):
    '''
    arithmetic : INTEGER
        | DECIMAL
        | STRING
        | var
    '''
    p[0] = p[1]

def p_var(p):
    '''
    var : TVAR
        | AVAR
        | VVAR
        | SVAR
        | RAVAR
        | SPVAR
    '''
    p[0] = p[1]

def p_assign_1(p):
    '''
    assign : TVAR ASSIGN arithmetic SEMICOLON
        | AVAR ASSIGN arithmetic SEMICOLON
        | VVAR ASSIGN arithmetic SEMICOLON
        | SVAR ASSIGN arithmetic SEMICOLON
    '''
    p[0] = ('=', p[1], p[3])
    #print(p[0])

def p_assign_2(p):
    '''
    assign : TVAR ASSIGN conversion SEMICOLON
        | AVAR ASSIGN conversion SEMICOLON
        | VVAR ASSIGN conversion SEMICOLON
        | SVAR ASSIGN conversion SEMICOLON
    '''
    p[0] = ('=', p[1], p[3])

def p_assign_3(p):
    '''
    assign : TVAR ASSIGN READ L_PAR R_PAR SEMICOLON
        | AVAR ASSIGN READ L_PAR R_PAR SEMICOLON
        | VVAR ASSIGN READ L_PAR R_PAR SEMICOLON
        | SVAR ASSIGN READ L_PAR R_PAR SEMICOLON
    '''
    p[0] = ('read', p[1])


def p_assign_4(p):
    '''
    assign : TVAR ASSIGN bitwise SEMICOLON
        | AVAR ASSIGN bitwise SEMICOLON
        | VVAR ASSIGN bitwise SEMICOLON
        | SVAR ASSIGN bitwise SEMICOLON
    '''
    p[0] = ('=', p[1], p[3])

def p_bitwise_1(p):
    '''
    bitwise : var AND_B var
        | var OR_B var
        | var XOR_B var
        | var SHIFT_L var
        | var SHIFT_R var
    '''
    p[0] = (p[2], p[1], p[3])

def p_bitwise_2(p):
    '''
    bitwise : NOT_B TVAR
        | NOT_B AVAR
        | NOT_B VVAR
        | NOT_B SVAR
    '''
    p[0] = (p[1], p[2])

def p_conversion(p):
    '''
    conversion : L_PAR type R_PAR var
    '''
    p[0] = ('convert', p[2], p[4])

def p_type(p):
    '''
    type : INT
        | FLOAT
        | CHAR
    '''
    p[0] = p[1]

def p_declaration_1(p):
    '''
    declaration : var
    '''
    p[0] = ('declaration', p[1])


def p_declaration_2(p):
    '''
    declaration : TVAR ASSIGN ARRAY L_PAR R_PAR SEMICOLON
        | AVAR ASSIGN ARRAY L_PAR R_PAR SEMICOLON
        | VVAR ASSIGN ARRAY L_PAR R_PAR SEMICOLON
        | SVAR ASSIGN ARRAY L_PAR R_PAR SEMICOLON
    '''
    p[0] = ('array', p[1])

#Empty production
def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

# def p_error(p):
#     print("Syntax error found in ", p.type,': \'', p.value, '\'')

def p_error(p):

    # get formatted representation of stack
    stack_state_str = ' '.join([symbol.type for symbol in parser.symstack][1:])

    print('Syntax error in input! Parser State:{} {} . {}'
          .format(parser.state,
                  stack_state_str,
                  p))


# Build the parser
parser = yacc.yacc()



# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     #print(tok)

# while True:
#     try:
#         s = input()
#     except EOFError:
#         break
#     parser.parse(s)
parser.parse(ss)
