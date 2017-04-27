from frida_parser import parser
import global_vars
from frida_gui import *

if __name__ == "__main__":
	global_vars.init()

	frida_gui = tk.Tk()
	frida_gui.title('Frida IDE')

	FridaGui(frida_gui).pack(side="top", fill="both", expand=True)
	frida_gui.mainloop()
	# readFile("test/test_arrays.frida")
