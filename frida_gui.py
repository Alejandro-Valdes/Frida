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
	def __init__(self, parent, parser, *args, **kwargs):

		self.lock = threading.Lock()

		self.console_index = 1.0

		self.parent = parent

		self.parser = parser

		self.receiving_input = True

		self.filename = ''
		self.identations = 0

		tk.Frame.__init__(self, *args, **kwargs)
		self.top_frame = tk.Frame(self)
		self.bottom_frame = tk.Frame(self)

		self.top_frame.pack(fill="x")
		self.bottom_frame.pack(fill="x")

		self.text = CustomText(self.top_frame)
		self.vsb = tk.Scrollbar(self.top_frame, command=self.text.yview)
		self.text.configure(yscrollcommand=self.vsb.set)
		self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
		self.linenumbers = TextLineNumbers(self.top_frame, width=30)
		self.linenumbers.attach(self.text)

		self.linenumbers.pack(side="left", fill="y")
		self.text.pack(side="left", fill="both", expand=True)
		self.vsb.pack(side="left", fill="y")

		self.text.bind("<<Change>>", self._on_change)
		self.text.bind("<Configure>", self._on_change)

		self.canvas = tk.Canvas(self.top_frame, width=700, height=600, bd = 1)
		self.canvas.pack(side="right", expand=True, fill=tk.BOTH)

		self.console = tk.Text(self.bottom_frame)
		self.console.pack(fill="x")
		
		self.menubar = tk.Menu(self.parent)
		self.parent.config(menu=self.menubar)

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
		if not self.filename and self.text.compare("end-1c", "!=", "1.0"):
			self.content_loss_dialog()
		self.text.delete("1.0",tk.END)
		self.filename = ''

	def content_loss_dialog(self):
		user_response = tk.messagebox.askyesno(title='Alerta', message='Tu trabajo actual será sobrescrito ¿Deseas guardar tus cambios en un nuevo archivo?', icon=tk.messagebox.WARNING)

		if user_response:
			self.file_save_as()
		else: 
			pass

	def open_file(self):
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

	def file_save_as(self):
		f = tk.filedialog.asksaveasfile(mode='w', defaultextension=".frida")
		if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
			return

		text_save = str(self.text.get(1.0, tk.END)) # starts from `1.0`, not `0.0`
		self.filename = f.name # Set current filename
		f.write(text_save)
		f.close() # `()` was missing.

	def file_save(self):
		if self.filename == '':
			f = tk.filedialog.asksaveasfile(mode='w', defaultextension=".frida")
		else:
			f = open(self.filename, 'w')

		if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
		    return
		text_save = str(self.text.get(1.0, tk.END)) # starts from `1.0`, not `0.0`
		f.write(text_save)
		f.close() # `()` was missing.

	def read_file(self, filename):

	    f = open(filename, "r")
	    text = f.read()
	    return text

	def donothing():
	   filewin = tk.Toplevel(self)
	   button = tk.Button(filewin, text="Do nothing button")
	   button.pack()

	def compile_run(self):
		self.virtual_machine = vm.VirtualMachine()

		self.reset()
		input = self.text.get(1.0,tk.END)
		self.running = True

		try:
			self.parser.parse(input)
			t = threading.Thread(target=self.virtual_machine.run_list, args=(self, self.canvas, q.Quadruple.quadruple_list))
			self.threads.append(t)
			t.start()
		except Exception as e: 
			self.print(e)
			pass

	def reset(self):
		global_vars.init()
		self.virtual_machine.mem = Memory()
		st.SymbolsTable.function_dictionary = {}
		self.canvas.delete("all")
		self.console.delete(1.0,tk.END)
		q.Quadruple.quadruple_list = []

	def print(self, string):
		self.console.insert(str(self.console_index), str(string) + '\n')
		self.console_index += len(str(string)) + 1

	def _on_change(self, event):
	    self.linenumbers.redraw()

	def insert_prompt(self):
	    # make sure the last line ends with a newline; remember that
	    # tkinter guarantees a trailing newline, so we get the
	    # character before this trailing newline ('end-1c' gets the
	    # trailing newline, 'end-2c' gets the char before that)
	    c = self.console.get("end-2c")
	    if c != "\n":
	        self.console.insert("end", "\n")
	    self.console.insert("end", self.prompt, ("prompt",))

	    # this mark lets us find the end of the prompt, and thus
	    # the beggining of the user input
	    self.console.mark_set("end-of-prompt", "end-1c")
	    self.console.mark_gravity("end-of-prompt", "left")

	    self.receiving_input = True
	    self.lock.acquire()

	def process_input(self, event=None):
		if self.receiving_input:

			# if there is an event, it happened before the class binding,
			# thus before the newline actually got inserted; we'll
			# do that here, then skip the class binding.
			self.console.insert("end", "\n")
			self.input = self.console.get("end-of-prompt", "end-1c")
			self.console.see("end")

			# this prevents the class binding from firing, since we 
			# inserted the newline in this method

			self.receiving_input = False
			self.lock.release()

		return "break"

	def quit_ask(self):
		if not self.filename and self.text.compare("end-1c", "!=", "1.0"):
			self.content_loss_dialog()
		self.quit()

	def stop_task(self):
		self.running = False

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

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
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)
	
if __name__ == "__main__":
    root = tk.Tk()
    FridaGui(root).pack(side="top", fill="both", expand=True)
    root.mainloop()