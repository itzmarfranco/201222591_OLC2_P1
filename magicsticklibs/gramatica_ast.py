from graphviz import Graph
import re

i = 0
def inc():
    global i
    i = i+1
    return i

def analizador_ast(entrada):
    
    #crear arbol AST

    #Graficar AST

    
    #analizador lexico


    tokens_operaciones = {
        'MAS',              # +
        'MENOS',            # -
        'MULTIPLICACION',   # *
        'DIVISION',         # /
        'MODULAR',          # %
        'NOT',              # not
        'AND',              # and
        'OR',               # or
        'NOTBIT',           # notbit
        'ANDBIT',           # andbit
        'ORBIT',            # orbit
        'XORBIT',           # xorbit
        'SHIFTIZQ',         # <<
        'SHIFTDER',         # >>
        'IGUALCOMPARACION', # ==
        'NOIGUAL',          # !=
        'MENOROIGUAL',      # <=
        'MAYOROIGUAL',      # >=
        'MENOR',            # <
        'MAYOR',            # >
        'ASIGNACION',       # =
    }

    palabras_reservadas = {
        'main' : 'MAIN',
        'if' : 'IF',
        'goto' : 'GOTO',
        'unset' : 'UNSET',
        'print' : 'PRINT',
        'read' : 'READ',
        'exit' : 'EXIT',
        'int' : 'INT',
        'float' : 'FLOAT',
        'char' : 'CHAR',
        'array' : 'ARRAY',
        'xor' : 'XOR',
        'abs' : 'ABS',
    }

    tokens = [
        'TEMPORAL',
        'PARAMETRO',
        'DEVUELTO',
        'DERETORNO',
        'PILA',
        'PUNTERO',          # 
        'PUNTOYCOMA',       # ;
        'DOSPUNTOS',        # :
        'PARENTESISIZQ',    # (
        'PARENTESISDER',    # )
        'CORCHETEIZQ',      # [
        'CORCHETEDER',      # ]
        'DECIMAL',          # numb.numb
        'ENTERO',           # numb
        'CADENADOBLE',      # ""
        'CADENASIMPLE',     # ''
        'SALTODELINEA',     # \n
        'ETIQUETA'          # id
    ] + list(tokens_operaciones) + list(palabras_reservadas.values())
    
    #Expresiones reguales para tokens

    t_TEMPORAL          = r'\$t\d+'
    t_PARAMETRO         = r'\$a\d+'
    t_DEVUELTO          = r'\$v\d+'
    t_DERETORNO         = r'\$ra'
    t_PILA              = r'\$s\d+'
    t_PUNTERO           = r'\$sp'
    t_PUNTOYCOMA        = r';'
    t_DOSPUNTOS         = r':'
    t_PARENTESISIZQ     = r'\('
    t_PARENTESISDER     = r'\)'
    t_CORCHETEIZQ       = r'\['
    t_CORCHETEDER       = r'\]'
    t_MAS               = r'\+'
    t_MENOS             = r'-'
    t_MULTIPLICACION    = r'\*'
    t_DIVISION          = r'/'
    t_MODULAR           = r'%'
    t_NOT               = r'!'
    t_AND               = r'&&'
    t_OR                = r'\|\|'
    t_NOTBIT            = r'~'
    t_ANDBIT            = r'&'
    t_ORBIT             = r'\|'
    t_XORBIT            = r'\^'
    t_SHIFTIZQ          = r'<<'
    t_SHIFTDER          = r'>>'
    t_IGUALCOMPARACION  = r'=='
    t_NOIGUAL          = r'!='
    t_MENOROIGUAL       = r'<='
    t_MAYOROIGUAL       = r'>='
    t_MENOR             = r'<'
    t_MAYOR             = r'>'
    t_ASIGNACION        = r'='

    # Definicion de numeros: Decimal y enteros

    def t_DECIMAL(t):
        r'\d+\.\d+'
        try:
            t.value = float(t.value)
        except ValueError:
            print("Float value too large %d", t.value)
            t.value = 0
        return t

    def t_ENTERO(t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %d", t.value)
            t.value = 0
        return t
    
    # Definicion de Etiqueta o id: Saltos y etiquetas
    
    def t_ETIQUETA(t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = palabras_reservadas.get(t.value.lower(),'ETIQUETA')
        return t
    
    # Definicion de Cadenas: Dobles y simples

    def t_CADENADOBLE(t):
        r'\".*?\"'
        t.value = t.value[1:-1] # quitar comillas dobles
        return t 

    def t_CADENASIMPLE(t):
        r'\'.*?\''
        t.value = t.value[1:-1] # quitar comillas simples
        return t 

    # Definicion de comentarios

    def t_COMENTARIO_SIMPLE(t):
        r'\#.*\n'
        t.lexer.lineno += 1

    # Definicion de saltos de linea

    def t_newline(t):
        r'\n+'
        #t.lineno += len(t.value) 
        t.lexer.lineno += t.value.count("\n")  

    def t_SALTOLINEA(t):
        r'\"\n\"'
        #t.value = t.value[1:-1] # remuevo las comillas dobles
        return t

    # Definicion de Caracteres ignorados
    t_ignore = " \t"

    # Manejo de Errores

    def t_error(t):
        #print ("Error Lexico: '%s'" % t.value[0])
        t.lexer.skip(1)

    # Analizador lexico Construccion

    from .ply import lex as lex
    lexer = lex.lex()

    lex.input(entrada)

    # Graficar AST
    #while 1:
    #    tok = lex.token()
    #    if not tok: break
    #    print(tok)

    #-------------------------------------------------------------------------
    #-------------------------------------------------------------------------
    #-------------------------------------------------------------------------

    #Asociacion de operadores y precedencia

    #Definicion de gramatica

    historial = []
    # Agregar tabla de simbolos Lexico-sintactico 

    def p_main(t):
        'inicio_august : MAIN DOSPUNTOS instrucciones' 
        t[0] = t[3]

        # Armando AST Graficar ------------------------------------------
        id = inc()
        t[0] = id
        dot.node(str(id), str('InicioAugust'))
        dot.edge(str(id),str(t[1]))
        dot.edge(str(id), str(t[3]))
        #----------------------------------------------------------------

    def p_instrucciones(t):
        'instrucciones : instrucciones instruccion' 
        #t[1].append(t[2])
        #t[0] = t[1]

        # Armando AST Graficar ------------------------------------------
        id = inc()
        t[0] = id
        dot.node(str(id), str('instrucciones'))
        dot.edge(str(id),str(t[1]))
        dot.edge(str(id),str(t[2]))
        #----------------------------------------------------------------
    
    def p_instrucciones_ultima_intruccion(t):
        'instrucciones : instruccion' 
        #t[0] = [t[1]]
        # Armando AST Graficar ------------------------------------------
        id = inc()
        t[0] = id
        dot.node(str(id), str('instrucciones'))
        dot.edge(str(id),str(t[1]))
        #----------------------------------------------------------------

    def p_instruccion(t):
        '''instruccion : instruccion_imprimir
                        | instruccion_unset
                        | instruccion_asignacion
                        | instruccion_control
                        | instruccion_goto
                        | instruccion_etiqueta
                        | instruccion_salir'''        
        t[0] = t[1]

        # Armando AST Graficar ------------------------------------------
        #id = inc()
        #t[0] = id
        #dot.node(str(id), str('instruccion'))
        #dot.edge(str(id),str(t[1]))
        #----------------------------------------------------------------

    
    def p_instruccion_imprimir(t):
        '''instruccion_imprimir : PRINT PARENTESISIZQ registro PARENTESISDER PUNTOYCOMA
                       | PRINT PARENTESISIZQ registro arreglos PARENTESISDER PUNTOYCOMA'''
        if t[4]==')':
            t[0] = t[3]
            # Armando AST Graficar ------------------------------------------
            id = inc()
            t[0] = id
            dot.node(str(id), str('instruccion_imprimir'))
            id = inc()
            dot.node(str(id), str('print(' + str(t[3]) + ')'))
            dot.edge(str(id-1), str(id))
            #----------------------------------------------------------------

        else:
            t[0] = (t[3], t[4])

    def p_instruccion_unset(t):
        'instruccion_unset : UNSET PARENTESISIZQ registro PARENTESISDER PUNTOYCOMA'
        t[0] = t[3]

    def p_instruccion_asignacion(t):
        'instruccion_asignacion : registro ASIGNACION expresion PUNTOYCOMA'
        t[0] = (t[1],t[3])

        # Armando AST Graficar ------------------------------------------
        id = inc()
        t[0] = id
        dot.node(str(id), str('instruccion_asignacion'))
        
        id = inc()
        dot.node(str(id), str(t[1]) + "=" + str(t[3]))
        dot.edge(str(id-1), str(id))
        #----------------------------------------------------------------

    def p_instruccion_asignacion_arreglo(t):
        'instruccion_asignacion : registro arreglos ASIGNACION expresion PUNTOYCOMA'
        t[0] = (t[1], t[2], t[4])
    
    def p_arreglos(t):
        'arreglos : arreglos arreglo'
        t[0].append(t[2])
        t[0] = t[1]
    
    def p_arreglos_arreglo(t):
        'arreglos : arreglo'
        t[0] = [t[1]]
    
    def p_arreglo(t):
        '''arreglo : CORCHETEIZQ ENTERO CORCHETEDER
                   | CORCHETEIZQ CADENADOBLE CORCHETEDER
                   | CORCHETEIZQ CADENASIMPLE CORCHETEDER'''
        t[0] = t[2]

    def p_expresion(t):
        '''expresion : instruccion_aritmetica
                     | instruccion_logica
                     | instruccion_relacional
                     | instruccion_bit
                     | READ PARENTESISIZQ PARENTESISDER
                     | ARRAY PARENTESISIZQ PARENTESISDER
                     | casteo'''
        t[0] = t[1]

        # Armando AST Graficar ------------------------------------------
        #id = inc()
        #t[0] = id
        #dot.node(str(id), str('expresion'))
        #dot.edge(str(id), str(t[1]))
        #----------------------------------------------------------------
    
    def p_instruccion_aritmetica_binaria(t):
        '''instruccion_aritmetica : instruccion_aritmetica MAS instruccion_aritmetica
                        | instruccion_aritmetica MENOS instruccion_aritmetica
                        | instruccion_aritmetica MULTIPLICACION instruccion_aritmetica
                        | instruccion_aritmetica DIVISION instruccion_aritmetica
                        | instruccion_aritmetica MODULAR instruccion_aritmetica'''        
        if t[2] == '+':
            #t[0] = (t[1],'+',t[3])
            t[0] = str(t[1]) + '+' + str(t[3])

        elif t[2] == '-':
            #t[0] = (t[1],'-',t[3])
            t[0] = str(t[1]) + '-' + str(t[3])

        elif t[2] == '*':
            #t[0] = (t[1], '*', t[3]) 
            t[0] = str(t[1]) + '*' + str(t[3])

        elif t[2] == '/':
            #t[0] = (t[1], '/', t[3]) 
            t[0] = str(t[1]) + '/' + str(t[3])

        elif t[2] == '%':
            #t[0] = (t[1], '%', t[3]) 
            t[0] = str(t[1]) + '%' + str(t[3])
    
    def p_instruccion_aritmetica_unaria(t):
        'instruccion_aritmetica : MENOS instruccion_aritmetica'
        t[0] = t[2]

    def p_instruccion_aritmetica_absoluta(t):
        'instruccion_aritmetica : ABS PARENTESISIZQ instruccion_aritmetica PARENTESISDER'
        t[0] = t[3]

    def p_instruccion_aritmetica_elemento_operando(t):
        'instruccion_aritmetica : elemento_operando'
        t[0] = t[1]

        # Armando AST Graficar ------------------------------------------
        #id = inc()
        #t[0] = id
        #dot.node(str(id), str('instruccion_aritmetica'))
        #dot.edge(str(id), str(t[1]))
        #----------------------------------------------------------------

    def p_elemento_operando(t):
        '''elemento_operando : ENTERO
                             | DECIMAL
                             | registro
                             | CADENADOBLE
                             | CADENASIMPLE'''
        t[0] = t[1]

    def p_instruccion_logica_binaria(t):
        '''instruccion_logica : elemento_operando AND elemento_operando
                              | elemento_operando OR elemento_operando
                              | elemento_operando XOR elemento_operando'''
        if t[2] == '&&':
            t[0] = (t[1], 'and', t[3]) 

        elif t[2] == '||':
            t[0] = (t[1], 'or', t[3]) 

        elif t[2] == 'xor':
            t[0] = (t[1], 'xor', t[3]) 

    def p_instruccion_logica_unaria(t):
        'instruccion_logica : NOT elemento_operando'
        t[0] = t[2]

    def p_instruccion_relacional(t):
        '''instruccion_relacional : elemento_operando IGUALCOMPARACION elemento_operando
                                  | elemento_operando NOIGUAL elemento_operando
                                  | elemento_operando MENOROIGUAL elemento_operando
                                  | elemento_operando MAYOROIGUAL elemento_operando
                                  | elemento_operando MENOR elemento_operando
                                  | elemento_operando MAYOR elemento_operando
                                  | elemento_operando ASIGNACION elemento_operando'''
        if t[2] == '==':
            #t[0] = (t[1], '==', t[3]) 
            t[0] = str(t[1]) + '==' + str(t[3])
        elif t[2] == '!=':
            #t[0] = (t[1], '!=', t[3])
            t[0] = str(t[1]) + '!=' + str(t[3])
        elif t[2] == '>=':
            #t[0] = (t[1], '>=', t[3]) 
            t[0] = str(t[1]) + '>=' + str(t[3])
        elif t[2] == '<=':
            #t[0] = (t[1], '<=', t[3]) 
            t[0] = str(t[1]) + '<=' + str(t[3])
        elif t[2] == '>':
            #t[0] = (t[1], '>', t[3]) 
            t[0] = str(t[1]) + '>' + str(t[3])
        elif t[2] == '<':
            #t[0] = (t[1], '<', t[3])
            t[0] = str(t[1]) + '<' + str(t[3])

    def p_instruccion_bit_binario(t):
        '''instruccion_bit : elemento_operando ANDBIT elemento_operando
	                | elemento_operando ORBIT elemento_operando
	                | elemento_operando XORBIT elemento_operando
	                | elemento_operando SHIFTIZQ elemento_operando
	                | elemento_operando SHIFTDER elemento_operando'''

        if t[2] == '&':
            t[0] = (t[1], '&', t[3]) 
        elif t[2] == '|':
            t[0] = (t[1], '|', t[3]) 
        elif t[2] == '^':
            t[0] = (t[1], '^', t[3]) 
        elif t[2] == '<<':
            t[0] = (t[1], '<<', t[3]) 
        elif t[2] == '>>':
            t[0] = (t[1], '>>', t[3])        
    
    def p_instruccion_bit_unaria(t):
        'instruccion_bit :	NOTBIT elemento_operando'
        t[0] = t[2]
   
    def p_casteo(t):
        'casteo : PARENTESISIZQ tipo PARENTESISDER registro'
        t[0] = (t[2], t[4]) 
    
    def p_tipo(t):
        '''tipo : INT
                | FLOAT
                | CHAR'''
        t[0] = t[1] 
    
    def p_registro(t):
        '''registro : TEMPORAL
                    | PARAMETRO
                    | DEVUELTO
                    | DERETORNO'''
        t[0] = t[1]

    def p_instruccion_control(t):
        'instruccion_control : IF PARENTESISIZQ expresion PARENTESISDER instruccion_goto'    
        t[0] = (t[3], t[5])

        # Armando AST Graficar ------------------------------------------
        id = inc()
        t[0] = id
        dot.node(str(id), str('instruccion_control'))

        id = inc()
        dot.node(str(id), 'condicion: ' + str(t[3]))
        dot.edge(str(id-1), str(id))
        dot.edge(str(id-1), str(t[5]))
        #----------------------------------------------------------------

    def p_instruccion_goto(t):
        'instruccion_goto : GOTO ETIQUETA PUNTOYCOMA'
        t[0] = t[2]
        # Armando AST Graficar ------------------------------------------
        id = inc()
        t[0] = id
        dot.node(str(id), str('instruccion_goto'))

        id = inc()
        dot.node(str(id), 'goto ' + str(t[2]))
        dot.edge(str(id-1),str(id))
        #dot.edge(str(id), 'goto ' + str(t[2]))
        #----------------------------------------------------------------
    
    def p_etiqueta(t):
        'instruccion_etiqueta : ETIQUETA DOSPUNTOS'
        t[0] = t[1]
        # Armando AST Graficar ------------------------------------------
        id = inc()
        t[0] = id
        dot.node(str(id), str('instruccion_etiqueta'))
        
        id = inc()
        dot.node(str(id), str('etiqueta ') + str(t[1]))
        dot.edge(str(id-1), str(id))
        #----------------------------------------------------------------

    def p_instruccion_salir(t):
        'instruccion_salir : EXIT PUNTOYCOMA'
        t[0] = t[1]
        # Armando AST Graficar ------------------------------------------
        id = inc()
        t[0] = id
        dot.node(str(id), str('instruccion_salir'))
        dot.edge(str(id), str(t[1]))
        #----------------------------------------------------------------

    def p_error(t):
        print("-")
        #print("Error sintáctico en '%s'" %t.value)

    from .ply import yacc as yacc
    parser = yacc.yacc()

    # Caracteristicas de Grafo
    dot = Graph()
    dot.attr(splines = 'false', rankdir="TBLR")
    dot.node_attr.update(shape= 'rect')
    dot.edge_attr.update(color= 'red', arrowhead = 'normal', arrowtail ="dot")
    # dot.view()

    resultado = parser.parse(entrada)
    return resultado