import os
#from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

import analizer

class Notepad:

	root = Tk()

	# default window width and height
	width = 700
	height = 600
	textArea = Text(root)
	menuBar = Menu(root)
	menuFile = Menu(menuBar, tearoff=0)
	menuEdit = Menu(menuBar, tearoff=0)
	menuAbout = Menu(menuBar, tearoff=0)
	menuNew = Menu(menuBar, tearoff=0)

	# To add scrollbar
	scrollbar = Scrollbar(textArea)
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
		self.textArea.grid(sticky = N + E + S + W)

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

		self.root.config(menu=self.menuBar)

		self.scrollbar.pack(side=RIGHT,fill=Y)

		# Scrollbar will adjust automatically according to the content
		self.scrollbar.config(command=self.textArea.yview)
		self.textArea.config(yscrollcommand=self.scrollbar.set)


	def quit(self):
		self.root.destroy()
		# exit()

	def showAbout(self):
		showinfo("Augus Interpreter","Kairi Franco 201222591")

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
		showinfo("Augus Interpreter","Interpretando...")

	def run(self):

		# Run main application
		self.root.mainloop()


# Main
notepad = Notepad(width=700,height=600)
notepad.run()
