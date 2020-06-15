import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

def open_file():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete(1.0, tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"Simple Text Editor - {filepath}")

def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_edit.get(1.0, tk.END)
        output_file.write(text)
    window.title(f"Simple Text Editor - {filepath}")

window = tk.Tk()
window.title("Simple Text Editor")
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

txt_edit = tk.Text(window)
fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_open = tk.Button(fr_buttons, text="Open", command=open_file)
btn_save = tk.Button(fr_buttons, text="Save As...", command=save_file)

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

window.mainloop()

##############################################

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

[('$t0', (...)), ('$t1', (...)), ('$t2', '$t1'), ('$t3', 'array'), '$t0']


'DIGRAPH{
tbl
[
label=<
<TABLE><TR><TD colspan=\'4\'>REPORTE GRAMATICAL ASCENDENTE</TD></TR><TR><TD>Gramatica</TD><TD>Acciones</TD><TD>Linea</TD><TD>Comentario</TD></TR><TR><TD>instruccion_asignacion : registro ASIGNACION expresion PUNTOYCOMA</TD><TD>t[0] = (t[1],t[3])</TD><TD>2</TD><TD>Se reconocio una asignacion (\'$t0\', (\'$a0\', \'+\', 8))</TD></TR><TR>\n        <TD>\n        <TABLE ALIGN="LEFT" BORDER="0">\n        <TR><TD>instruccion : instruccion_imprimir</TD></TR>\n        <TR><TD>| instruccion_unset</TD></TR>\n        <TR><TD>| instruccion_asignacion</TD></TR>\n        <TR><TD>| instruccion_control</TD></TR>\n        <TR><TD>| instruccion_goto</TD></TR>\n        <TR><TD>| instruccion_etiqueta</TD></TR>\n        <TR><TD>| instruccion_salir</TD></TR>\n        </TABLE>\n        </TD>\n        <TD>t[0] = t[1]</TD><TD>2</TD><TD>Se reconocio una instruccion del catalogo</TD></TR><TR><TD>instrucciones : instruccion</TD><TD>t[0] = [t[1]]</TD><TD>2</TD><TD>Se reconocio una instrucciones</TD></TR><TR><TD>instruccion_asignacion : registro ASIGNACION expresion PUNTOYCOMA</TD><TD>t[0] = (t[1],t[3])</TD><TD>3</TD><TD>Se reconocio una asignacion (\'$t1\', (42, \'*\', 1))</TD></TR><TR>\n        <TD>\n        <TABLE ALIGN="LEFT" BORDER="0">\n        <TR><TD>instruccion : instruccion_imprimir</TD></TR>\n        <TR><TD>| instruccion_unset</TD></TR>\n        <TR><TD>| instruccion_asignacion</TD></TR>\n        <TR><TD>| instruccion_control</TD></TR>\n        <TR><TD>| instruccion_goto</TD></TR>\n        <TR><TD>| instruccion_etiqueta</TD></TR>\n        <TR><TD>| instruccion_salir</TD></TR>\n        </TABLE>\n        </TD>\n        <TD>t[0] = t[1]</TD><TD>3</TD><TD>Se reconocio una instruccion del catalogo</TD></TR><TR><TD>instrucciones : instrucciones instruccion</TD><TD>t[1].append(t[2]), t[0] = t[1]</TD><TD>2</TD><TD>Lista de instrucciones</TD></TR><TR><TD>instruccion_asignacion : registro ASIGNACION expresion PUNTOYCOMA</TD><TD>t[0] = (t[1],t[3])</TD><TD>4</TD><TD>Se reconocio una asignacion (\'$t2\', \'$t1\')</TD></TR><TR>\n        <TD>\n        <TABLE ALIGN="LEFT" BORDER="0">\n        <TR><TD>instruccion : instruccion_imprimir</TD></TR>\n        <TR><TD>| instruccion_unset</TD></TR>\n        <TR><TD>| instruccion_asignacion</TD></TR>\n        <TR><TD>| instruccion_control</TD></TR>\n        <TR><TD>| instruccion_goto</TD></TR>\n        <TR><TD>| instruccion_etiqueta</TD></TR>\n        <TR><TD>| instruccion_salir</TD></TR>\n        </TABLE>\n        </TD>\n        <TD>t[0] = t[1]</TD><TD>4</TD><TD>Se reconocio una instruccion del catalogo</TD></TR><TR><TD>instrucciones : instrucciones instruccion</TD><TD>t[1].append(t[2]), t[0] = t[1]</TD><TD>2</TD><TD>Lista de instrucciones</TD></TR><TR><TD>instruccion_asignacion : registro ASIGNACION expresion PUNTOYCOMA</TD><TD>t[0] = (t[1],t[3])</TD><TD>5</TD><TD>Se reconocio una asignacion (\'$t3\', \'array\')</TD></TR><TR>\n        <TD>\n        <TABLE ALIGN="LEFT" BORDER="0">\n        <TR><TD>instruccion : instruccion_imprimir</TD></TR>\n        <TR><TD>| instruccion_unset</TD></TR>\n        <TR><TD>| instruccion_asignacion</TD></TR>\n        <TR><TD>| instruccion_control</TD></TR>\n        <TR><TD>| instruccion_goto</TD></TR>\n        <TR><TD>| instruccion_etiqueta</TD></TR>\n        <TR><TD>| instruccion_salir</TD></TR>\n        </TABLE>\n        </TD>\n        <TD>t[0] = t[1]</TD><TD>5</TD><TD>Se reconocio una instruccion del catalogo</TD></TR><TR><TD>instrucciones : instrucciones instruccion</TD><TD>t[1].append(t[2]), t[0] = t[1]</TD><TD>2</TD><TD>Lista de instrucciones</TD></TR><TR><TD>instruccion_imprimir : PRINT PARENTESISIZQ registro PARENTESISDER PUNTOYCOMA</TD><TD>t[0] = t[3]</TD><TD>6</TD><TD>Se reconocio una instruccion de imprimir registro $t0</TD></TR><TR>\n        <TD>\n        <TABLE ALIGN="LEFT" BORDER="0">\n        <TR><TD>instruccion : instruccion_imprimir</TD></TR>\n        <TR><TD>| instruccion_unset</TD></TR>\n        <TR><TD>| instruccion_asignacion</TD></TR>\n        <TR><TD>| instruccion_control</TD></TR>\n        <TR><TD>| instruccion_goto</TD></TR>\n        <TR><TD>| instruccion_etiqueta</TD></TR>\n        <TR><TD>| instruccion_salir</TD></TR>\n        </TABLE>\n        </TD>\n        <TD>t[0] = t[1]</TD><TD>6</TD><TD>Se reconocio una instruccion del catalogo</TD></TR><TR><TD>instrucciones : instrucciones instruccion</TD><TD>t[1].append(t[2]), t[0] = t[1]</TD><TD>2</TD><TD>Lista de instrucciones</TD></TR> <TR><TD>inicio_august : MAIN DOSPUNTOS instruccions</TD><TD>t[0] = t[3]</TD><TD>1</TD><TD>Se reconocio Main</TD></TR></TABLE>>];}'