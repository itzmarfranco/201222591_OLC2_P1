from graphviz import Graph
from graphviz import nohtml
import re

import os

from graphviz import Digraph
import pydotplus

from node import Node
from SymbolTable import Table, Symbol
from Error import Error, ErrorList


# graph = pydotplus.graph_from_dot_data('DIGRAPH{tbl[shape=plaintext\nlabel=<<TABLE><TR><TD colspan=\'4\'>REPORTE GRAMATICAL ASCENDENTE</TD></TR><TR><TD>Gramatica</TD><TD>Acciones</TD><TD>Linea</TD><TD>Comentario</TD></TR><TR><TD>instruccion_asignacion : registro ASIGNACION expresion PUNTOYCOMA</TD><TD>t[0] = (t[1],t[3])</TD><TD>2</TD><TD>Se reconocio una asignacion (\'$t0\', (\'$a0\', \'+\', 8))</TD></TR><TR>\n        <TD>\n        <TABLE ALIGN="LEFT" BORDER="0">\n        <TR><TD>instruccion : instruccion_imprimir</TD></TR>\n        <TR><TD>| instruccion_unset</TD></TR>\n        <TR><TD>| instruccion_asignacion</TD></TR>\n        <TR><TD>| instruccion_control</TD></TR>\n        <TR><TD>| instruccion_goto</TD></TR>\n        <TR><TD>| instruccion_etiqueta</TD></TR>\n        <TR><TD>| instruccion_salir</TD></TR>\n        </TABLE>\n        </TD>\n        <TD>t[0] = t[1]</TD><TD>2</TD><TD>Se reconocio una instruccion del catalogo</TD></TR><TR><TD>instrucciones : instruccion</TD><TD>t[0] = [t[1]]</TD><TD>2</TD><TD>Se reconocio una instrucciones</TD></TR><TR><TD>instruccion_asignacion : registro ASIGNACION expresion PUNTOYCOMA</TD><TD>t[0] = (t[1],t[3])</TD><TD>3</TD><TD>Se reconocio una asignacion (\'$t1\', (42, \'*\', 1))</TD></TR><TR>\n        <TD>\n        <TABLE ALIGN="LEFT" BORDER="0">\n        <TR><TD>instruccion : instruccion_imprimir</TD></TR>\n        <TR><TD>| instruccion_unset</TD></TR>\n        <TR><TD>| instruccion_asignacion</TD></TR>\n        <TR><TD>| instruccion_control</TD></TR>\n        <TR><TD>| instruccion_goto</TD></TR>\n        <TR><TD>| instruccion_etiqueta</TD></TR>\n        <TR><TD>| instruccion_salir</TD></TR>\n        </TABLE>\n        </TD>\n        <TD>t[0] = t[1]</TD><TD>3</TD><TD>Se reconocio una instruccion del catalogo</TD></TR><TR><TD>instrucciones : instrucciones instruccion</TD><TD>t[1].append(t[2]), t[0] = t[1]</TD><TD>2</TD><TD>Lista de instrucciones</TD></TR><TR><TD>instruccion_asignacion : registro ASIGNACION expresion PUNTOYCOMA</TD><TD>t[0] = (t[1],t[3])</TD><TD>4</TD><TD>Se reconocio una asignacion (\'$t2\', \'$t1\')</TD></TR><TR>\n        <TD>\n        <TABLE ALIGN="LEFT" BORDER="0">\n        <TR><TD>instruccion : instruccion_imprimir</TD></TR>\n        <TR><TD>| instruccion_unset</TD></TR>\n        <TR><TD>| instruccion_asignacion</TD></TR>\n        <TR><TD>| instruccion_control</TD></TR>\n        <TR><TD>| instruccion_goto</TD></TR>\n        <TR><TD>| instruccion_etiqueta</TD></TR>\n        <TR><TD>| instruccion_salir</TD></TR>\n        </TABLE>\n        </TD>\n        <TD>t[0] = t[1]</TD><TD>4</TD><TD>Se reconocio una instruccion del catalogo</TD></TR><TR><TD>instrucciones : instrucciones instruccion</TD><TD>t[1].append(t[2]), t[0] = t[1]</TD><TD>2</TD><TD>Lista de instrucciones</TD></TR><TR><TD>instruccion_asignacion : registro ASIGNACION expresion PUNTOYCOMA</TD><TD>t[0] = (t[1],t[3])</TD><TD>5</TD><TD>Se reconocio una asignacion (\'$t3\', \'array\')</TD></TR><TR>\n        <TD>\n        <TABLE ALIGN="LEFT" BORDER="0">\n        <TR><TD>instruccion : instruccion_imprimir</TD></TR>\n        <TR><TD>| instruccion_unset</TD></TR>\n        <TR><TD>| instruccion_asignacion</TD></TR>\n        <TR><TD>| instruccion_control</TD></TR>\n        <TR><TD>| instruccion_goto</TD></TR>\n        <TR><TD>| instruccion_etiqueta</TD></TR>\n        <TR><TD>| instruccion_salir</TD></TR>\n        </TABLE>\n        </TD>\n        <TD>t[0] = t[1]</TD><TD>5</TD><TD>Se reconocio una instruccion del catalogo</TD></TR><TR><TD>instrucciones : instrucciones instruccion</TD><TD>t[1].append(t[2]), t[0] = t[1]</TD><TD>2</TD><TD>Lista de instrucciones</TD></TR><TR><TD>instruccion_imprimir : PRINT PARENTESISIZQ registro PARENTESISDER PUNTOYCOMA</TD><TD>t[0] = t[3]</TD><TD>6</TD><TD>Se reconocio una instruccion de imprimir registro $t0</TD></TR><TR>\n        <TD>\n        <TABLE ALIGN="LEFT" BORDER="0">\n        <TR><TD>instruccion : instruccion_imprimir</TD></TR>\n        <TR><TD>| instruccion_unset</TD></TR>\n        <TR><TD>| instruccion_asignacion</TD></TR>\n        <TR><TD>| instruccion_control</TD></TR>\n        <TR><TD>| instruccion_goto</TD></TR>\n        <TR><TD>| instruccion_etiqueta</TD></TR>\n        <TR><TD>| instruccion_salir</TD></TR>\n        </TABLE>\n        </TD>\n        <TD>t[0] = t[1]</TD><TD>6</TD><TD>Se reconocio una instruccion del catalogo</TD></TR><TR><TD>instrucciones : instrucciones instruccion</TD><TD>t[1].append(t[2]), t[0] = t[1]</TD><TD>2</TD><TD>Lista de instrucciones</TD></TR> <TR><TD>inicio_august : MAIN DOSPUNTOS instruccions</TD><TD>t[0] = t[3]</TD><TD>1</TD><TD>Se reconocio Main</TD></TR></TABLE>>];}')
# #Image(graph.create_png())
# graph.write_pdf('tree.pdf')

def analizador(entrada):
    
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
        'STRING' # hello

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

    def t_COMMENT(t):
        r'\#.*'
        pass

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

    def find_column(input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1
        
    # Skip the current token and output 'Illegal characters' using the special Ply t_error function.
    def t_error(t):
        print("Illegal characters!")
        t.lexer.skip(1)

    # Build the lexer
    log = []
    from .ply import lex as lex
    lexer = lex.lex()

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

        tree = p[0]
        #run(tree)
        print(tree)
        log.append('<tr><td>start : MAIN COLON body</td><td>p[0] = p[1]</td><td>'+ str(p.lineno(0)) +'</td><td>Etiqueta main</td></tr>')

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
        log.append('<tr><td>body : INSTRUCCION body</td><td>p[0] = (p[1], p[2]</td><td>'+ str(p.lineno(0)) +'</td><td>Instrucciones del cuerpo del programa</td></tr>')

    def p_body_e(p):
        '''
        body : empty
        '''
        p[0] = None
        log.append('<tr><td>body : empty</td><td>p[0] = None</td><td>'+ str(p.lineno(0)) +'</td><td>Produccion vacia</td></tr>')

    def p_goto(p):
        '''
        goto : GOTO NAME SEMICOLON
        '''
        p[0] = ('goto', p[2])
        log.append('<tr><td>goto : GOTO NAME ;</td><td>p[0] = (goto, p[2])</td><td>'+ str(p.lineno(0)) +'</td><td>Instruccion GOTO</td></tr>')

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
        log.append('<tr><td>unset : UNSET ( VAR ) ;</td><td>p[0] = (unset, p[3])</td><td>'+ str(p.lineno(0)) +'</td><td>Instruccion unset</td></tr>')

    def p_print_1(p):
        '''
        print : PRINT L_PAR TVAR R_PAR SEMICOLON
            | PRINT L_PAR AVAR R_PAR SEMICOLON
            | PRINT L_PAR VVAR R_PAR SEMICOLON
            | PRINT L_PAR SVAR R_PAR SEMICOLON
            | PRINT L_PAR SPVAR R_PAR SEMICOLON
            | PRINT L_PAR RAVAR R_PAR SEMICOLON
        '''
        p[0] = ('print', p[3])
        log.append('<tr><td>print : PRINT ( VAR ) ;</td><td>p[0] = (print, p[3])</td><td>'+ str(p.lineno(0)) +'</td><td>Instruccion print</td></tr>')

    def p_print_2(p):
        '''
        print : PRINT L_PAR TVAR L_BRACKET arithmetic R_BRACKET R_PAR SEMICOLON
            | PRINT L_PAR AVAR L_BRACKET arithmetic R_BRACKET R_PAR SEMICOLON
            | PRINT L_PAR VVAR L_BRACKET arithmetic R_BRACKET R_PAR SEMICOLON
            | PRINT L_PAR SVAR L_BRACKET arithmetic R_BRACKET R_PAR SEMICOLON
            | PRINT L_PAR SPVAR L_BRACKET arithmetic R_BRACKET R_PAR SEMICOLON
            | PRINT L_PAR RAVAR L_BRACKET arithmetic R_BRACKET R_PAR SEMICOLON
        '''
        var = str(p[3]) + '[' + str(p[5]) + ']'
        p[0] = ('print_array', var)
        log.append('<tr><td>print : print ( VAR [ OP ] )</td><td>p[0] = (print_array, VAR[OP])</td><td>'+ str(p.lineno(0)) +'</td><td>Instruccion imprimir arreglos</td></tr>')

    def p_exit(p):
        '''
        exit : EXIT SEMICOLON
        '''
        p[0] = p[1]
        log.append('<tr><td>exit : EXIT ;</td><td>p[0] = p[1]</td><td>'+ str(p.lineno(0)) +'</td><td>Instruccion exit</td></tr>')

    def p_tag(p):
        '''
        tag : NAME COLON
        '''
        p[0] = ('tag', p[1])
        log.append('<tr><td>tag : NAME :</td><td>p[0] = (tag, p[1])</td><td>'+ str(p.lineno(0)) +'</td><td>Declaracion de etiqueta</td></tr>')

    def p_if(p):
        '''
        if : IF L_PAR condition R_PAR GOTO NAME SEMICOLON
        '''
        p[0] = ('if',  p[3], p[6])
        log.append('<tr><td>if : IF ( condition ) GOTO NAME ;</td><td>p[0] = (if, p[3], p[6])</td><td>'+ str(p.lineno(0)) +'</td><td>Condicional if</td></tr>')

    def p_condition_1(p):
        '''
        condition : condition AND condition
            | condition OR condition
        '''
        p[0] = (p[2], p[1], p[3])
        log.append('<tr><td>condition : condition '+str(p[2])+' condition</td><td>p[0] = (p[2], p[1], p[3])</td><td>'+ str(p.lineno(0)) +'</td><td>Operaciones condicionales AND OR</td></tr>')

    def p_condition_2(p):
        '''
        condition : NOT condition
        '''
        p[0] = (p[1], p[2])
        log.append('<tr><td>condition : NOT condition</td><td>p[0] = (p[1], p[2])</td><td>'+ str(p.lineno(0)) +'</td><td>Operacion condicional NOT</td></tr>')

    def p_condition_3(p):
        '''
        condition : relational
        '''
        p[0] = p[1]
        log.append('<tr><td>condition : relational</td><td>p[0] = p[1]</td><td>'+ str(p.lineno(0)) +'</td><td>Operaciones relacionales</td></tr>')

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
        log.append('<tr><td>relational : arithmetic '+str(p[2])+'</td><td>p[0] = p[1]</td><td>'+ str(p.lineno(0)) +'</td><td>Operacion relacional '+str(p[2])+'</td></tr>')

    def p_relational_2(p):
        '''
        relational : arithmetic
        '''
        p[0] = p[1]
        log.append('<tr><td>relational : arithmetic</td><td>p[0] = p[1]</td><td>'+ str(p.lineno(0)) +'</td><td>Operaciones aritmeticas</td></tr>')

    def p_arithmetic_1(p):
        '''
        arithmetic : arithmetic PLUS arithmetic
            | arithmetic MINUS arithmetic
            | arithmetic MULTIPLY arithmetic
            | arithmetic DIVIDE arithmetic
            | arithmetic REMAINDER arithmetic
        '''
        p[0] = (p[2], p[1], p[3])
        log.append('<tr><td>arithmetic : arithmetic '+str(p[2])+' aritmetic</td><td>p[0] = (p[2], p[1], p[3])</td><td>'+ str(p.lineno(0)) +'</td><td>Operacion aritmetica'+str(p[2])+'</td></tr>')

    def p_arithmetic_2(p):
        '''
        arithmetic : INTEGER
            | DECIMAL
            | STRING
            | var
            | array_access
        '''
        p[0] = p[1]
        log.append('<tr><td>arithmetic : INT | FLOAT | STRING | VAR</td><td>p[0] = p[1]</td><td>'+ str(p.lineno(0)) +'</td><td>Operando</td></tr>')

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
        log.append('<tr><td>var : TVAR | AVAR | VVAR | SVAR | RAVAR | SPVAR</td><td>p[0] = p[1]</td><td>'+ str(p.lineno(0)) +'</td><td>Variables generadas</td></tr>')

    def p_array_access(p):
        '''
        array_access : 
        '''
        p[0] = ()

    def p_assign_1(p):
        '''
        assign : TVAR ASSIGN condition SEMICOLON
            | AVAR ASSIGN condition SEMICOLON
            | VVAR ASSIGN condition SEMICOLON
            | SVAR ASSIGN condition SEMICOLON
        '''
        p[0] = ('=', p[1], p[3])
        log.append('<tr><td>assign : VAR ASSIGN condition ;</td><td>p[0] = (=, p[1], p[3])</td><td>'+ str(p.lineno(0)) +'</td><td>Asignacion de valor a variable</td></tr>')

    def p_assign_2(p):
        '''
        assign : TVAR ASSIGN conversion SEMICOLON
            | AVAR ASSIGN conversion SEMICOLON
            | VVAR ASSIGN conversion SEMICOLON
            | SVAR ASSIGN conversion SEMICOLON
        '''
        p[0] = ('=', p[1], p[3])
        log.append('<tr><td>assign : VAR ASSIGN conversion ;</td><td>p[0] = (=, p[1], p[3])</td><td>'+ str(p.lineno(0)) +'</td><td>Asignacion de conversion a variable</td></tr>')

    def p_assign_3(p):
        '''
        assign : TVAR ASSIGN READ L_PAR R_PAR SEMICOLON
            | AVAR ASSIGN READ L_PAR R_PAR SEMICOLON
            | VVAR ASSIGN READ L_PAR R_PAR SEMICOLON
            | SVAR ASSIGN READ L_PAR R_PAR SEMICOLON
        '''
        p[0] = ('read', p[1])
        log.append('<tr><td>assign : VAR ASSIGN READ () ;</td><td>p[0] = (=, p[1], p[3])</td><td>'+ str(p.lineno(0)) +'</td><td>Asignacion de valor a variable</td></tr>')

    def p_assign_4(p):
        '''
        assign : TVAR ASSIGN bitwise SEMICOLON
            | AVAR ASSIGN bitwise SEMICOLON
            | VVAR ASSIGN bitwise SEMICOLON
            | SVAR ASSIGN bitwise SEMICOLON
        '''
        p[0] = ('=', p[1], p[3])
        log.append('<tr><td>assign : VAR ASSIGN bitwise ;</td><td>p[0] = (=, p[1], p[3])</td><td>'+ str(p.lineno(0)) +'</td><td>Asignacion de valor a variable</td></tr>')

    def p_assign_5(p):
        '''
        assign : TVAR L_BRACKET arithmetic R_BRACKET ASSIGN condition SEMICOLON
            | AVAR L_BRACKET arithmetic R_BRACKET ASSIGN condition SEMICOLON
            | VVAR L_BRACKET arithmetic R_BRACKET ASSIGN condition SEMICOLON
            | SVAR L_BRACKET arithmetic R_BRACKET ASSIGN condition SEMICOLON
            | SPVAR L_BRACKET arithmetic R_BRACKET ASSIGN condition SEMICOLON
            | RAVAR L_BRACKET arithmetic R_BRACKET ASSIGN condition SEMICOLON
        '''
        p[0] = ('=', 'array_a', p[1], p[3], p[6])
        log.append('<tr><td>assign : VAR [ OP ] ASSIGN condition ;</td><td>p[0] = (=, array_assign, p[1], p[3], p[6])</td><td>'+ str(p.lineno(0)) +'</td><td>Asignacion de valor a variable de arreglo</td></tr>')

    def p_bitwise_1(p):
        '''
        bitwise : var AND_B var
            | var OR_B var
            | var XOR_B var
            | var SHIFT_L var
            | var SHIFT_R var
        '''
        p[0] = (p[2], p[1], p[3])
        log.append('<tr><td>bitwise : VAR AND VAR | VAR OR VAR | VAR XOR VAR | VAR SHIFT VAR</td><td>p[0] = (p[2], p[1], p[3])</td><td>'+ str(p.lineno(0)) +'</td><td>Operaciones bit a bit</td></tr>')

    def p_bitwise_2(p):
        '''
        bitwise : NOT_B TVAR
            | NOT_B AVAR
            | NOT_B VVAR
            | NOT_B SVAR
        '''
        p[0] = (p[1], p[2])
        log.append('<tr><td>bitwise : NOT VAR</td><td>p[0] = (p[1], p[2])</td><td>'+ str(p.lineno(0)) +'</td><td>Operaciones bit a bit</td></tr>')

    def p_conversion(p):
        '''
        conversion : L_PAR type R_PAR var
        '''
        p[0] = ('convert', p[2], p[4])
        log.append('<tr><td>conversion : ( type ) VAR</td><td>p[0] = (convert, p[2], p[4])</td><td>'+ str(p.lineno(0)) +'</td><td>Conversion de tipos</td></tr>')

    def p_type(p):
        '''
        type : INT
            | FLOAT
            | CHAR
        '''
        p[0] = p[1]
        log.append('<tr><td>type : INT | FLOAT | CHAR</td><td>p[0] = p[1]</td><td>'+ str(p.lineno(0)) +'</td><td>Generacion de tipos de variables</td></tr>')

    def p_declaration_1(p):
        '''
        declaration : var
        '''
        p[0] = ('declaration', p[1])
        log.append('<tr><td>declaration : var</td><td>p[0] = (declaration, p[1])</td><td>'+ str(p.lineno(0)) +'</td><td>Declaracion de variables</td></tr>')

    def p_declaration_2(p):
        '''
        declaration : TVAR ASSIGN ARRAY L_PAR R_PAR SEMICOLON
            | AVAR ASSIGN ARRAY L_PAR R_PAR SEMICOLON
            | VVAR ASSIGN ARRAY L_PAR R_PAR SEMICOLON
            | SVAR ASSIGN ARRAY L_PAR R_PAR SEMICOLON
            | SPVAR ASSIGN ARRAY L_PAR R_PAR SEMICOLON
            | RAVAR ASSIGN ARRAY L_PAR R_PAR SEMICOLON
        '''
        p[0] = ('array', p[1])
        log.append('<tr><td>declaration : VAR = array ( ) ;</td><td>p[0] = (array, p[1])</td><td>'+ str(p.lineno(0)) +'</td><td>Declaracion de arreglos</td></tr>')

    def p_declaration_3(p):
        '''
        declaration : TVAR L_BRACKET arithmetic R_BRACKET SEMICOLON
            | AVAR L_BRACKET arithmetic R_BRACKET SEMICOLON
            | VVAR L_BRACKET arithmetic R_BRACKET SEMICOLON
            | SVAR L_BRACKET arithmetic R_BRACKET SEMICOLON
            | SPVAR L_BRACKET arithmetic R_BRACKET SEMICOLON
            | RAVAR L_BRACKET arithmetic R_BRACKET SEMICOLON
        '''
        p[0] = ('array_d', p[1], p[3])
        log.append('<tr><td>declaration: VAR [ OP ] ;</td><td>p[0] = (array_d, p[1], p[3])</td><td>'+ str(p.lineno(0)) +'</td><td>Declaracion de variable de arreglo</td></tr>')

    #Empty production
    def p_empty(p):
        '''
        empty :
        '''
        p[0] = None
        log.append('<tr><td>empty : </td><td>p[0] = None</td><td>'+ str(p.lineno(0)) +'</td><td>Produccion vacia</td></tr>')

    # def p_error(p):
    #     print("Syntax error found in ", p.type,': \'', p.value, '\'')

    def p_error(t):
        #print(t)
        print("Error sintactico: " + str(t.value) + " , tipo: " + str(t.type))
        print("Linea: " + str(t.lineno) + " ,Columna: " + str(t.lexpos))

        #historial.append("<TR><TD>instruccion_goto : GOTO ETIQUETA PUNTOYCOMA</TD><TD>t[0] = t[2]</TD><TD>"+str(t.lineno(2))+f"</TD><TD>Se reconocio una instruccion goto {t[0]}</TD></TR>")
    
    ts = Table([])

    lexicalErrors = ErrorList([])
    syntacticErrors = ErrorList([])
    semanticErrors = ErrorList([])
    #  lineal AST
    tree = None

    def run(tree):
        if type(tree) == tuple:
            for node in tree:
                if type(node) == tuple:
                    run(node)
                else:
                    if node == '=':
                        if tree[1] == 'array_a':
                            if ts.isSymbolInTable(tree[2]) and ts.get(tree[2]).length == 2:
                                if run(tree[4]) != None:
                                    print('ASSIGNING ARRAY ', tree[2],'[',run(tree[3]), '] -> ', run(tree[4]))
                                    #p[0] = ('=', 'array_a', p[1], p[3], p[6])
                                    varType = ''
                                    if isinstance(run(tree[4]), str):
                                        varType = 'str'
                                    elif isinstance(run(tree[4]), int):
                                        varType = 'int'
                                    elif isinstance(run(tree[4]), float):
                                        varType = 'flt'

                                    id = str(tree[2]) + '[' + str(run(tree[3])) + ']'
                                    sym = Symbol(id, varType, run(tree[4]), 1, ())
                                    ts.add(sym)
                                    print('TS')
                                    ts.print()
                                    return
                                else:
                                    error = Error('Cannot assign none value', 0,0)
                                    semanticErrors.add(error)
                                    return
                            else:
                                error = Error('Array \''+str(tree[2])+'\' not declared', 0,0)
                                semanticErrors.add(error)
                        else:
                            if run(tree[2]) != None:
                                print('ASSIGNING ', tree[1], ' -> ', run(tree[2]))
                                varType = ''
                                if isinstance(run(tree[2]), str):
                                    varType = 'str'
                                elif isinstance(run(tree[2]), int):
                                    varType = 'int'
                                elif isinstance(run(tree[2]), float):
                                    varType = 'flt'

                                sym = Symbol(tree[1], varType, run(tree[2]), 1, ())
                                ts.add(sym)
                                print('TS')
                                ts.print()
                                return
                            else:
                                error = Error('Cannot assign none value', 0,0)
                                semanticErrors.add(error)
                                return
                        #store in symbol table
                    elif node == '+':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('Cannot operate \'+\' none value', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[2]), str) and (isinstance(run(tree[1]), int) or isinstance(run(tree[1]), float)):
                            error = Error('Cannot add string and number', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) and (isinstance(run(tree[2]), int) or isinstance(run(tree[2]), float)):
                            error = Error('Cannot add number and string', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) + run(tree[2])
                    elif node == '-':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('Cannot operate \'-\' none value', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) or isinstance(run(tree[2]), str):
                            error = Error('Cannot substract string and number', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) - run(tree[2])
                    elif node == '*':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('Cannot operate \'*\' none value', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) or isinstance(run(tree[2]), str):
                            error = Error('Cannot multiply string and number', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) * run(tree[2])
                    elif node == '/':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('Cannot operate \'*\' none value', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) or isinstance(run(tree[2]), str):
                            error = Error('Cannot divide string and number', 0,0)
                            semanticErrors.add(error)
                            return
                        elif run(tree[2]) == 0:
                            error = Error('Cannot divide by 0', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) / run(tree[2])
                    elif node == '%':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('Cannot operate \'/\' none value', 0,0)
                            semanticErrors.add(error)
                            return
                        if isinstance(run(tree[1]), str) or isinstance(run(tree[2]), str):
                            error = Error('Cannot divide string and number', 0,0)
                            semanticErrors.add(error)
                            return
                        elif run(tree[2]) == 0:
                            error = Error('Cannot get remainder from zero division', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) % run(tree[2])
                    elif node == 'if':
                        print('IF',  run(tree[1]), tree[2])
                        #call 'search' function to locate tag and execute from there
                    elif node == '<':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('Cannot compare \'<\' none value', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) and (isinstance(run(tree[2]), int) or isinstance(run(tree[2]), float)):
                            error = Error('Cannot compare \'<\' string and number', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[2]), str) and (isinstance(run(tree[1]), int) or isinstance(run(tree[1]), float)):
                            error = Error('Cannot compare \'<\' string and number', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) < run(tree[2])
                    elif node == '>':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('Cannot compare \'>\' none value', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) and (isinstance(run(tree[2]), int) or isinstance(run(tree[2]), float)):
                            error = Error('Cannot compare \'>\' string and number', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[2]), str) and (isinstance(run(tree[1]), int) or isinstance(run(tree[1]), float)):
                            error = Error('Cannot compare \'>\' string and number', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) > run(tree[2])
                    elif node == '<=':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('Cannot compare \'<=\' none value', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) and (isinstance(run(tree[2]), int) or isinstance(run(tree[2]), float)):
                            error = Error('Cannot compare \'<=\' string and number', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[2]), str) and (isinstance(run(tree[1]), int) or isinstance(run(tree[1]), float)):
                            error = Error('Cannot compare \'<=\' string and number', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) <= run(tree[2])
                    elif node == '>=':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('Cannot compare \'>=\' none value', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) and (isinstance(run(tree[2]), int) or isinstance(run(tree[2]), float)):
                            error = Error('Cannot compare \'>=\' string and number', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[2]), str) and (isinstance(run(tree[1]), int) or isinstance(run(tree[1]), float)):
                            error = Error('Cannot compare \'>=\' string and number', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) >= run(tree[2])
                    elif node == '==':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('Cannot compare \'==\' none value', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) and (isinstance(run(tree[2]), int) or isinstance(run(tree[2]), float)):
                            error = Error('Cannot compare \'==\' string and number', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[2]), str) and (isinstance(run(tree[1]), int) or isinstance(run(tree[1]), float)):
                            error = Error('Cannot compare \'==\' string and number', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) == run(tree[2])
                    elif node == '!=':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('Cannot compare \'!=\' none value', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) and (isinstance(run(tree[2]), int) or isinstance(run(tree[2]), float)):
                            error = Error('Cannot compare \'!=\' string and number', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[2]), str) and (isinstance(run(tree[1]), int) or isinstance(run(tree[1]), float)):
                            error = Error('Cannot compare \'!=\' string and number', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) != run(tree[2])
                    elif node == '&&':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('Cannot compare \'&&\' none value', 0,0)
                            semanticErrors.add(error)
                            return
                        elif run(tree[1]) not in (0,1) or run(tree[2]) not in (0,1):
                            error = Error('Cannot compare \'&&\' non-boolean values', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) and run(tree[2])
                    elif node == '||':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('Cannot compare \'||\' none value', 0,0)
                            semanticErrors.add(error)
                            return
                        elif run(tree[1]) not in (0,1) or run(tree[2]) not in (0,1):
                            error = Error('Cannot compare \'||\' non-boolean values', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) or run(tree[2])
                    elif node == '!':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('Cannot compare \'<\' none value', 0,0)
                            semanticErrors.add(error)
                            return
                        elif run(tree[1]) not in (0,1):
                            error = Error('Cannot compare \'!\' non-boolean values', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return not run(tree[1])
                    elif node == 'xor':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('Cannot compare \'xor\' none value', 0,0)
                            semanticErrors.add(error)
                            return
                        elif run(tree[1]) not in (0,1) or run(tree[2]) not in (0,1):
                            error = Error('Cannot compare \'xor\' non-boolean values', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) != run(tree[2])
                    elif node == '&':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('Cannot compare \'&\' none value', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) or isinstance(run(tree[2]), str) or isinstance(run(tree[1]), float) or isinstance(run(tree[2]), float):
                            error = Error('Cannot compare \'&\' string or float', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) & run(tree[2])
                    elif node == '|':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('Cannot compare \'|\' none value', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) or isinstance(run(tree[2]), str) or isinstance(run(tree[1]), float) or isinstance(run(tree[2]), float):
                            error = Error('Cannot compare \'|\' string or float', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) | run(tree[2])
                    elif node == '~':
                        if run(tree[1]) == None:
                            error = Error('Cannot compare \'~\' none value', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) or isinstance(run(tree[1]), float):
                            error = Error('Cannot operate \'~\' string or float', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return ~(run(tree[1]))
                    elif node == '^':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('Cannot compare \'^\' none value', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) or isinstance(run(tree[2]), str) or isinstance(run(tree[1]), float) or isinstance(run(tree[2]), float):
                            error = Error('Cannot compare \'^\' string or float', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) ^ run(tree[2])
                    elif node == '<<':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('Cannot use none value when shifting', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) or isinstance(run(tree[2]), str) or isinstance(run(tree[1]), float) or isinstance(run(tree[2]), float):
                            error = Error('Cannot use \'<<\' operator with string or float', 0,0)
                            semanticErrors.add(error)
                            if run(tree[2]) < 0:
                                error = Error('Cannot shift negative steps', 0,0)
                                semanticErrors.add(error)
                                return
                        else:
                            return run(tree[1]) << run(tree[2])
                    elif node == '>>':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('Cannot use none value when shifting', 0,0)
                            semanticErrors.add(error)
                            return
                        if isinstance(run(tree[1]), str) or isinstance(run(tree[2]), str) or isinstance(run(tree[1]), float) or isinstance(run(tree[2]), float):
                            error = Error('Cannot use \'>>\' operator with string or float', 0,0)
                            semanticErrors.add(error)
                            if run(tree[2]) < 0:
                                error = Error('Cannot shift negative steps', 0,0)
                                semanticErrors.add(error)
                                return
                            else:
                                return run(tree[1]) >> run(tree[2])
                    elif node == 'print':
                        # buscar en tabla de simbolos el valor de run(tree[1])
                        return print('PRINTING', run(tree[1]))
                    elif node == 'print_array':
                        # buscar en tabla de simbolos el valor de run(tree[1])
                        return print('PRINTING ARRAY', run(tree[1]))
                    elif node == 'unset':
                        # buscar en la tabla de símbolos la variable, eliminar el registro
                        return print('DELETING', run(tree[1]))
                    elif node == 'exit':
                        # fin de la ejecución
                        return print('EXITING')
                    elif node == 'goto':
                        # buscar la etiqueta en la tabla de simbolos o en el arbol, recorrer desde ese punto el arbol
                        return print('JUMPING TO', tree[1])
                    elif node == 'tag':
                        # guardar la etiqueta como variable en la tabla de simbolos
                        return print('ADDING TAG', tree[1])
                    elif node == 'array':
                        # guardar variable como arreglo en la tabla de simbolos
                        sym = Symbol(tree[1], 'array', None, 2, ())
                        ts.add(sym)
                        ts.print()
                        return print('CREATING ARRAY', tree[1])                                        
                    elif node == 'read':
                        # capturar entrada escrita en la terminal
                        # guardar en la tabla de simbolos
                        return print('READING TO', tree[1])                                        
                    else:
                        #print('returning tree 1:::', tree)
                        #return tree
                        pass
        else:
            if isinstance(tree, str):
                if tree[0] == '$':
                    # seach in TS
                    if ts.isSymbolInTable(tree):
                        print('return value', ts.get(tree).value)
                        return ts.get(tree).value
                    else:
                        errorStr = 'Variable \''+ str(tree) + '\' not defined'
                        error = Error(errorStr, 0,0)
                        semanticErrors.add(error)
                        return None
                else:
                    # Will return string
                    return tree
            else:
                # will return number
                return tree


    

    from .ply import yacc as yacc
    parser = yacc.yacc()

    resultado = parser.parse(entrada,tracking=True)

    dotData = 'DIGRAPH{tbl[shape=plaintext\nlabel=<<TABLE><TR><TD colspan=\'4\'>Reporte gramatical</TD></TR>'
    dotData = dotData + '<TR><TD>Produccion</TD><TD>Acciones</TD><TD>Línea</TD><TD>Descripción</TD></TR>'
    for x in reversed(log):
        dotData = dotData + x
    dotData = dotData + '</TABLE>>];}'

    
    #dot.node(name ='Tabla_Reporte', label= historial_string)
    #dot.view()
    graph = pydotplus.graph_from_dot_data(dotData)
    #Image(graph.create_png())
    graph.write_png('reporte_gramatical.png')
    return resultado