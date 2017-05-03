# try:
#     from Tkinter import *
# except ImportError:
#     from tkinter import *
import tkinter as tk
import quadruples as q
import symbol_table as st
from memory import Memory
import global_vars
import os
import threading
import virtual_machine as vm
from tkinter.filedialog import askopenfilename, asksaveasfile

class FridaGui(tk.Frame):
	"""Clase FridaGui -> tkinter.Frame
	
	Clase que utiliza la máquina virtual, parser y memoria del lenguaje Frida en conjunto 
	con un editor de texto para facilitar el desarrollo de software en este lenguaje.

	La utilización del manejador de geometrías Pack, módulo nativo de TKinter, ayudó en gran parte
	en el desarrollo de esta interfaz al mantener una geometría simple pero limpia.
	"""
	def __init__(self, parent, parser, *args, **kwargs):
		"""Inicializador default de clase FridaGui

		args:
			parent -- instancia de tk.Frame de la cual hereda esta clase
			parser -- objeto parser definido para el lenguaje Frida
		"""

		self.lock = threading.Lock() # Lock que previene una condición de carrera entre esta clase y la máquina virtual

		self.console_index = 1.0

		self.parent = parent

		self.parser = parser

		self.receiving_input = True

		self.filename = '' # Nombre del archivo actual
		self.identations = 0 

		tk.Frame.__init__(self, *args, **kwargs) # Inicialización de frame principal de GUI
		self.top_frame = tk.Frame(self) # Definición de frame superior
		self.bottom_frame = tk.Frame(self) # Definición de frame inferior

		self.top_frame.pack(fill="x")
		self.bottom_frame.pack(fill="x")

		self.text = CustomText(self.top_frame)
		self.vsb = tk.Scrollbar(self.top_frame, command=self.text.yview)
		self.text.configure(yscrollcommand=self.vsb.set)
		self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))

		self.linenumbers = TextLineNumbers(self.top_frame, width=30) # Barra lateral que muestra número de línea para el cuadro de texto
		self.linenumbers.attach(self.text)
		self.linenumbers.pack(side="left", fill="y")

		self.text.pack(side="left", fill="both", expand=True)
		self.vsb.pack(side="left", fill="y")

		self.text.bind("<<Change>>", self._on_change)
		self.text.bind("<Configure>", self._on_change)

		self.canvas = tk.Canvas(self.top_frame, width=700, height=600, bd = 1) # Canvas donde se dibujaran los elementos gráficos del lenguaje
		self.canvas.pack(side="right", expand=True, fill=tk.BOTH)

		self.console = tk.Text(self.bottom_frame) # Consola en donde se hace output de errores y, también, por la cual se recibe input
		self.console.pack(fill="x")
		
		self.menubar = tk.Menu(self.parent)
		self.parent.config(menu=self.menubar)

		# Funciones básicas
		filemenu = tk.Menu(self.menubar, tearoff=0)
		filemenu.add_command(label="Nuevo", command=self.new_file)
		filemenu.add_command(label="Abrir", command=self.open_file)
		filemenu.add_command(label="Ejecutar", command=self.compile_run)
		filemenu.add_command(label="Detener", command=self.stop_task)
		filemenu.add_command(label="Guardar", command=self.file_save)
		filemenu.add_command(label="Guardar como...", command=self.file_save_as)

		filemenu.add_separator()

		filemenu.add_command(label="Salir", command=self.quit_ask)
		self.menubar.add_cascade(label="Archivo", menu=filemenu)

		helpmenu = tk.Menu(self.menubar, tearoff=0)
		helpmenu.add_command(label="About...", command=self.donothing)
		self.menubar.add_cascade(label="Help", menu=helpmenu)

		self.console.bind("<Return>", self.process_input)
		# self.text.bind("<Return>", self.insert_idents)
		# self.text.bind("<Tab>", self.update_idents)
		# self.text.bind("<Backspace>", self.update_idents)
		self.prompt = ">>> "

		self.threads = list()

	# def update_idents(self):
	# 	if tk.SEL_FIRST == '': 

	def new_file(self):
		"""Función que limpia el cuadro de texto y el archivo cargado para comenzar con un nuevo archivo"""
		if not self.filename and self.text.compare("end-1c", "!=", "1.0"):
			self.content_loss_dialog()
		self.text.delete("1.0",tk.END)
		self.filename = ''

	def content_loss_dialog(self):
		"""Función que muestra un diálogo para prevenir la pérdida del trabajo actual si es que éste no está guardado"""
		user_response = tk.messagebox.askyesno(title='Alerta', message='Tu trabajo actual será sobrescrito ¿Deseas guardar tus cambios en un nuevo archivo?', icon=tk.messagebox.WARNING)

		if user_response:
			self.file_save_as()
		else: 
			pass

	def open_file(self):
		"""Función que muestra un diálogo de selección de archivo para poder editar en el editor de texto"""
		if not self.filename and self.text.compare("end-1c", "!=", "1.0"):
			self.content_loss_dialog()
		self.text.delete("1.0",tk.END)
		file_types = [('Frida files', '*.frida'), ('All files', '*')]
		dialog = tk.filedialog.Open(self, filetypes = file_types)
		file = dialog.show()
		self.filename = file

		if file != '':
			text = self.read_file(file)
			self.text.insert(tk.END, text)

	# Las funciones file_save_as y file_save fueron basadas en código encontrado en stack overflow: http://stackoverflow.com/a/19476284
	
	def file_save_as(self):
		"""Abre un diálogo para guardar el contenido que se encuentra en el editor, 
		dentro de un archivo especificado por el usuario

		Función basada en código encontrado en stack overflow: http://stackoverflow.com/a/19476284
		"""
		f = tk.filedialog.asksaveasfile(mode='w', defaultextension=".frida")
		if f is None: # asksaveasfile regresa `None` si el diálogo se cierra con "cancel".
			return

		text_save = str(self.text.get(1.0, tk.END))
		self.filename = f.name # settea el nombre de archivo actual
		f.write(text_save)
		f.close() 

	def file_save(self):
		"""Abre un diálogo para guardar el contenido que se encuentra en el editor, 
		dentro de un archivo especificado por el usuario. En caso de que el archivo 
		ya haya sido guardado anteriormente, esta función sobreescribirá el contenido del archivo.

		Función basada en código encontrado en stack overflow: http://stackoverflow.com/a/19476284
		"""
		if self.filename == '':
			f = tk.filedialog.asksaveasfile(mode='w', defaultextension=".frida")
		else:
			f = open(self.filename, 'w')

		if f is None: # asksaveasfile regresa `None` si diálogo se cierra con "cancel".
		    return
		text_save = str(self.text.get(1.0, tk.END)) 
		f.write(text_save)
		f.close() 

	def read_file(self, filename):
		"""Función que lee el contenido de un archivo con base en el nombre de éste
		
		args: 
			filename -- nombre del archivo que será leído

		return:
			text -- string con los contenidos del archivo
		"""
		f = open(filename, "r")
		text = f.read()
		return text

	def donothing():
		"""Función de prueba que permite continuar con el programa 
		cuando se presionan botones que están bindeados a esta función
		"""
		filewin = tk.Toplevel(self)
		button = tk.Button(filewin, text="Do nothing button")
		button.pack()

	def compile_run(self):
		"""Función que ejecuta el contenido que se encuentra dentro del editor de texto"""
		self.virtual_machine = vm.VirtualMachine()

		self.reset()
		input = self.text.get(1.0,tk.END) # Recupera el contenido del editor de texto
		self.running = True

		# A través de este try-catch esperamos cualquier tipo de error proveniente 
		# de la máquina virtual y, supuestamente, del parser.
		try:
			# Dentro de este bloque se crea un thread que manejará la máquina virtual y permitirá
			# el uso de la consola desde GUI durante la ejecución
			self.parser.parse(input)
			t = threading.Thread(target=self.virtual_machine.run_list, args=(self, self.canvas, q.Quadruple.quadruple_list)) 
			self.threads.append(t)
			t.start()
		except Exception as e: 
			self.print(e)
			pass

	def reset(self):
		"""Función que resetea los valores viejos de ejecuciones 
		pasadas que fueron guardados en recursos compartidos
		"""
		global_vars.init()
		self.virtual_machine.mem = Memory()
		st.SymbolsTable.function_dictionary = {}
		self.canvas.delete("all")
		self.console.delete(1.0,tk.END)
		q.Quadruple.quadruple_list = []

	def print(self, string):
		"""Función para imprimir en consola de GUI
		
		args:
			string -- valor a imprimir
		"""
		self.console.insert(str(self.console_index), str(string) + '\n')
		self.console_index += len(str(string)) + 1

	def _on_change(self, event):
	    self.linenumbers.redraw()

	def insert_prompt(self):
		"""Solución basada en esta respuesta de stack overflow: http://stackoverflow.com/a/17840173
		
		Nos aseguramos que la última línea termine con '\n';
		tkinter garantiza un salto de línea, así que tomamos el caracter
		antes de este salto (end-2c)
		"""
		c = self.console.get("end-2c")
		if c != "\n":
			self.console.insert("end", "\n")
		self.console.insert("end", self.prompt, ("prompt",))

		# esta marca nos permite encontrar el final del prompt, y
		# por lo tanto el comienzo del input de usuario
		self.console.mark_set("end-of-prompt", "end-1c")
		self.console.mark_gravity("end-of-prompt", "left")

		self.receiving_input = True # levanta una bandera que garantizará que process_input lea input 
		self.lock.acquire() # obtiene lock y para el thread de la máquina virtual para ahorrar recursos

	def process_input(self):
		"""Solución basada en esta respuesta de stack overflow: http://stackoverflow.com/a/17840173
		
		Función que procesa input si y solo si se encuentra levantada la bandera 'receiving_input'
		"""

		if self.receiving_input:

			# Inserta un salto de línea y esto overridea el comportamiento defáult de tkinter
			self.console.insert("end", "\n")
			self.input = self.console.get("end-of-prompt", "end-1c")
			self.console.see("end")

			self.receiving_input = False
			self.lock.release() # Suelta el lock para que la máquina virtual continúe su procesamiento

		return "break"

	def quit_ask(self):
		"""Función que muestra el diálogo para guardar el contenido no guardado antes de salir del IDE"""
		if not self.filename and self.text.compare("end-1c", "!=", "1.0"):
			self.content_loss_dialog()
		self.quit()

	def stop_task(self):
		"""Función que detiene la ejecución de la máquina virtual"""
		self.running = False

class CustomText(tk.Text):
	"""Clase CustomText -> tkinter.Text

	Clase con listeners escritos en Tcl (Tkinter está escrito sobre el lenguaje/librería Tcl/Tk) 
	para llamar la acción <<Change>> y con ello ejecutar un cambio en TextLineNumbers.
	Utilizado para el mejoramiento de la interfaz del IDE

	Código obtenido de stack overflow: http://stackoverflow.com/a/16375233
	"""
	def __init__(self, *args, **kwargs):
		"""Inicializador default"""
		tk.Text.__init__(self, *args, **kwargs)

		# Creación de función listener en Tcl
		self.tk.eval('''
			proc widget_proxy {widget widget_command args} {

				# call the real tk widget command with the real args
				set result [uplevel [linsert $args 0 $widget_command]]

				# generate the event for certain types of commands
				if {([lindex $args 0] in {insert replace delete}) ||
					([lrange $args 0 2] == {mark set insert}) || 
					([lrange $args 0 1] == {xview moveto}) ||
					([lrange $args 0 1] == {xview scroll}) ||
					([lrange $args 0 1] == {yview moveto}) ||
					([lrange $args 0 1] == {yview scroll})} {

					event generate  $widget <<Change>> -when tail
				}

				# return the result from the real widget command
				return $result
			}
			''')
		self.tk.eval('''
			rename {widget} _{widget}
			interp alias {{}} ::{widget} {{}} widget_proxy {widget} _{widget}
		'''.format(widget=str(self)))

class TextLineNumbers(tk.Canvas):
	"""Clase TextLineNumbers

	Canvas con un widget de texto que cambia cada vez que se 

	Código obtenido de stack overflow: http://stackoverflow.com/a/16375233
	"""
	def __init__(self, *args, **kwargs):
		"""Inicializador por default
		
		Crea una instancia de Canvas, padre de esta clase
		"""
		tk.Canvas.__init__(self, *args, **kwargs)
		self.textwidget = None

	def attach(self, text_widget):
		"""Función utilizada para manejar un text widget desde esta clase
	
		args: 
			text_widget -- objeto de text que tendrá la clase TextLineNumbers adjunta 
		"""
		self.textwidget = text_widget

	def redraw(self, *args):
		"""Función que redibuja las líneas cada vez que se llama a este método"""
		self.delete("all")

		i = self.textwidget.index("@0,0")
		while True :
			dline= self.textwidget.dlineinfo(i)
			if dline is None: break # si no hay una nueva línea, no es necesario dibujar
			y = dline[1]
			linenum = str(i).split(".")[0]
			self.create_text(2,y,anchor="nw", text=linenum) # insertar número a canvas
			i = self.textwidget.index("%s+1line" % i)
	
if __name__ == "__main__":
	root = tk.Tk()
	FridaGui(root).pack(side="top", fill="both", expand=True)
	root.mainloop()