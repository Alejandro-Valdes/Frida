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

	root = tk.Tk()
	root.title('Frida IDE')

	FridaGui(root, parser, virtual_machine).pack(side="top", fill="both", expand=True)
	root.mainloop()
	# main(file)
