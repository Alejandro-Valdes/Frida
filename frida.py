from frida_parser import parser
import global_vars
from frida_gui import *
import sys

def main(file):
	file_in = open(file, 'r')
	data = file_in.read()
	file_in.close()
	parser.parse(data)


if __name__ == '__main__':
	file = "test/" + sys.argv[1]

	global_vars.init()

	frida_gui = tk.Tk()
	frida_gui.title('Frida IDE')

	FridaGui(frida_gui).pack(side="top", fill="both", expand=True)
	frida_gui.mainloop()

	main(file)
