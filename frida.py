from frida_parser import parser
from frida_gui import *
import sys

# Script principal de la aplicación que ejecuta la GUI con el parser

def main(file):
	file_in = open(file, 'r')
	data = file_in.read()
	file_in.close()
	parser.parse(data)

if __name__ == '__main__':
	# Método anterior de compilación/ejecución
	# file = "test/" + sys.argv[1]

	root = tk.Tk()
	root.title('Frida IDE')

	root.state('zoomed')

	FridaGui(root, parser).pack(side="top", fill="both", expand=True)
	root.mainloop()
	# main(file)
