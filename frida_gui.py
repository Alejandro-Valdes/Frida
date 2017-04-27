# try:
#     from Tkinter import *
# except ImportError:
#     from tkinter import *
import tkinter as tk

class FridaGui(tk.Frame):
	def __init__(self, parent, *args, **kwargs):

		self.parent = parent

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

		self.canvas = tk.Canvas(self.top_frame, width = 750, height = 600, bd = 1, relief = tk.GROOVE)
		self.canvas.pack(side="right", fill="y")

		self.user_entry = tk.Text(self.bottom_frame)
		self.user_entry.pack(fill="x")

		# read_btn = tk.Button(self, state=tk.DISABLED, text='Lee', padx=15)
		# read_btn.grid(row=3, column=2, sticky='WENS')

		# run_btn = tk.Button(self, text = 'Frida Pinta')
		# run_btn.grid(row = 2, column=2, sticky='WENS')

		# output_lbl = tk.Label(self, text = 'Output:')
		# output_lbl.grid(row = 3, column = 4, sticky = 'WNS')

		# output_area = tk.Text(self, width = 20, height= 6, bd = 1, relief = tk.GROOVE, state = tk.DISABLED)
		# output_area.grid(row=5, column = 4, sticky = 'WENS', pady=(0,20), padx=(0,5))
		
		self.menubar = tk.Menu(self.parent)
		self.parent.config(menu=self.menubar)

		filemenu = tk.Menu(self.menubar, tearoff=0)
		filemenu.add_command(label="New", command=self.NewFile)
		filemenu.add_command(label="Open", command=self.donothing)
		filemenu.add_command(label="Save", command=self.donothing)
		filemenu.add_command(label="Save as...", command=self.donothing)
		filemenu.add_command(label="Close", command=self.donothing)

		filemenu.add_separator()

		filemenu.add_command(label="Exit", command=self.quit)
		self.menubar.add_cascade(label="File", menu=filemenu)
		editmenu = tk.Menu(self.menubar, tearoff=0)
		editmenu.add_command(label="Undo", command=self.donothing)

		editmenu.add_separator()

		editmenu.add_command(label="Cut", command=self.donothing)
		editmenu.add_command(label="Copy", command=self.donothing)
		editmenu.add_command(label="Paste", command=self.donothing)
		editmenu.add_command(label="Delete", command=self.donothing)
		editmenu.add_command(label="Select All", command=self.donothing)

		self.menubar.add_cascade(label="Edit", menu=editmenu)
		helpmenu = tk.Menu(self.menubar, tearoff=0)
		helpmenu.add_command(label="Help Index", command=self.donothing)
		helpmenu.add_command(label="About...", command=self.donothing)
		self.menubar.add_cascade(label="Help", menu=helpmenu)

		# self.mainloop()

		# frida_lbl = Label(self, text = '-FRIDA-')
		# frida_lbl.grid(row = 0, column=1, sticky='WENS')
		# save_btn.grid(row = 0, column = 0, sticky='WENS', padx=15, pady=10)
		# open_btn.grid(row = 0, column = 2, sticky='WENS')


	def NewFile():
		text_area.delete("1.0",END)


	def donothing():
	   filewin = tk.Toplevel(self)
	   button = tk.Button(filewin, text="Do nothing button")
	   button.pack()

	def _on_change(self, event):
	    self.linenumbers.redraw()

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