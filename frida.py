from frida_parser import parser
from virtual_machine import *
from frida_gui import *
import sys

def main(file):
	file_in = open(file, 'r')
	data = file_in.read()
	file_in.close()
	parser.parse(data)

if __name__ == '__main__':
	# file = "test/" + sys.argv[1]

	virtual_machine = VirtualMachine()

	frida_gui = tk.Tk()
	frida_gui.title('Frida IDE')

	FridaGui(frida_gui, parser, virtual_machine).pack(side="top", fill="both", expand=True)
	frida_gui.mainloop()
	# main(file)
