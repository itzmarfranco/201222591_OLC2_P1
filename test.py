import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

import ply.lex as lex
import ply.yacc as yacc
import sys

from graphviz import Digraph
import pydotplus
from node import Node
from SymbolTable import Table, Symbol
from Error import Error, ErrorList


class Notepad:
    root = Tk()

    # default window width and height
    width = 700
    height = 600
    textArea = Text(root, background='white', foreground='black', height=10,insertbackground='black', insertwidth=4)
    console = Text(root, background='black', foreground='green', height=10, insertbackground='green', insertwidth=8)
    menuBar = Menu(root)
    menuFile = Menu(menuBar, tearoff=0)
    menuEdit = Menu(menuBar, tearoff=0)
    menuAbout = Menu(menuBar, tearoff=0)
    menuNew = Menu(menuBar, tearoff=0)
    menuReport = Menu(menuBar, tearoff=0)
        

    # To add scrollbar
    scrollbar = Scrollbar(textArea)
    scrollbar2 = Scrollbar(console)

    currentFile = None

    def __init__(self,**kwargs):

        # Set icon
        try:
                self.root.wm_iconbitmap("arrow.ico")
        except:
                pass

        # Set window size (the default is 300x300)

        try:
            self.width = kwargs['width']
        except KeyError:
            pass

        try:
            self.height = kwargs['height']
        except KeyError:
            pass

        # Set the window text
        self.root.title("Sin título - Augus Interpreter")
        
        # set black background to console


        # Center the window
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()

        # For left-alling
        left = (screenWidth / 2) - (self.width / 2)

        # For right-allign
        top = (screenHeight / 2) - (self.height /2)

        # For top and bottom
        self.root.geometry('%dx%d+%d+%d' % (self.width,
                                            self.height,
                                            left, top))

        # To make the textarea auto resizable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Add controls (widget)
        self.textArea.grid(row=0, column=0,sticky = N + E + S + W)
        self.console.grid(row=1, column=0,sticky = N + E + S + W)

        self.console.insert('1.0', '>>')

        # To open new file
        self.menuFile.add_command(label="Nuevo", command=self.newFile)

        # To open a already existing file
        self.menuFile.add_command(label="Abrir", command=self.openFile)

        # To save current file
        self.menuFile.add_command(label="Guardar", command=self.saveFile)

        # To save as new current file
        self.menuFile.add_command(label="Guardar como", command=self.saveFileAs)

        # To create a line in the dialog
        self.menuFile.add_separator()
        
        self.menuFile.add_command(label="Salir", command=self.quit)

        self.menuBar.add_cascade(label="Archivo", menu=self.menuFile)

        # To give a feature of cut
        self.menuEdit.add_command(label="Cortar", command=self.cut)

        # to give a feature of copy
        self.menuEdit.add_command(label="Copiar", command=self.copy)

        # To give a feature of paste
        self.menuEdit.add_command(label="Pegar", command=self.paste)

        # To give a feature of editing
        self.menuBar.add_cascade(label="Editar", menu=self.menuEdit)

        # Nuevas funcionalidades notepad
        self.menuNew.add_command(label="Interpretar", command=self.analyze)
        
        self.menuBar.add_cascade(label="Analizar", menu=self.menuNew)

        # To create a feature of description of the notepad
        self.menuAbout.add_command(label="Acerca de", command=self.showAbout)
        self.menuBar.add_cascade(label="Informacion", menu=self.menuAbout)

        # Reports
        self.menuReport.add_command(label="Semantic errors", command=self.showSemanticReport)
        self.menuBar.add_cascade(label="Reports", menu=self.menuReport)

        self.root.config(menu=self.menuBar)

        self.scrollbar.pack(side=RIGHT,fill=Y)

        self.scrollbar2.pack(side=RIGHT,fill=Y)

        # Scrollbar will adjust automatically according to the content
        self.scrollbar.config(command=self.textArea.yview)
        self.textArea.config(yscrollcommand=self.scrollbar.set)

        self.scrollbar2.config(command=self.console.yview)
        self.console.config(yscrollcommand=self.scrollbar2.set)


    def quit(self):
        self.root.destroy()
        # exit()

    def showAbout(self):
        showinfo("Augus Interpreter","Kairi Franco 201222591")

    def showSemanticReport(self):
        semanticErrors.print()

    def openFile(self):

        self.currentFile = askopenfilename(defaultextension=".txt", filetypes=[("All Files","*.*"), ("Text Documents","*.txt")])

        if self.currentFile == "":

            # no file to open
            self.currentFile = None
        else:

            # Try to open the file
            # set the window title
            self.root.title(os.path.basename(self.currentFile) + " - Augus Interpreter")
            self.textArea.delete(1.0,END)

            file = open(self.currentFile,"r")

            self.textArea.insert(1.0,file.read())

            file.close()


    def newFile(self):
        self.root.title("Sin Titulo - Augus Interpreter")
        self.currentFile = None
        self.textArea.delete(1.0,END)

    def saveFile(self):

        if self.currentFile == None:
            # Save as new file
            self.currentFile = asksaveasfilename(initialfile='Untitled.txt',
                                            defaultextension=".txt",
                                            filetypes=[("All Files","*.*"),
                                                ("Text Documents","*.txt")])

            if self.currentFile == "":
                self.currentFile = None
            else:

                # Try to save the file
                file = open(self.currentFile,"w")
                file.write(self.textArea.get(1.0,END))
                file.close()

                # Change the window title
                self.root.title(os.path.basename(self.currentFile) + " - Augus Interpreter")


        else:
            file = open(self.currentFile,"w")
            file.write(self.textArea.get(1.0,END))
            file.close()

    def saveFileAs(self):

            # Save as new file
            self.currentFile = asksaveasfilename(initialfile='Untitled.txt',
                                            defaultextension=".txt",
                                            filetypes=[("All Files","*.*"),
                                                ("Text Documents","*.txt")])

            if self.currentFile == "":
                self.currentFile = None
            else:

                # Try to save the file
                file = open(self.currentFile,"w")
                file.write(self.textArea.get(1.0,END))
                file.close()

                # Change the window title
                self.root.title(os.path.basename(self.currentFile) + " - Augus Interpreter")


    def cut(self):
        self.textArea.event_generate("<<Cut>>")

    def copy(self):
        self.textArea.event_generate("<<Copy>>")

    def paste(self):
        self.textArea.event_generate("<<Paste>>")

    def analyze(self):
        #showinfo("Augus Interpreter","Interpretando...")
        # lexicalErrors.clear()
        # syntacticErrors.clear()
        # semanticErrors.clear()
        lexer = lex.lex()
        lexer.input(self.textArea.get(1.0,END))
        parser = yacc.yacc()
        parser.parse(self.textArea.get(1.0,END))
        
        

    def run(self):
        # Run main application
        self.root.mainloop()

##############################################################################
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
#lexer = lex.lex()
#lexer.input('main:')

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
    run(tree)

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
        | array_access
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
        | SPVAR ASSIGN ARRAY L_PAR R_PAR SEMICOLON
        | RAVAR ASSIGN ARRAY L_PAR R_PAR SEMICOLON
    '''
    p[0] = ('array', p[1])

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

#Empty production
def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

# def p_error(p):
#     print("Syntax error found in ", p.type,': \'', p.value, '\'')

def p_error(p):
    print('Syntactic error found', p)
    # get formatted representation of stack
    # stack_state_str = ' '.join([symbol.type for symbol in parser.symstack][1:])

    # print('Syntax error in input! Parser State:{} {} . {}'
    #       .format(parser.state,
    #               stack_state_str,
    #               p))
##############################################################################

# Main
notepad = Notepad(width=700,height=600)
notepad.run()