# Autor: Alejandro Valdes y Evan Juarez
# Archivo que funciona para al analisis sintactico de Frida
# usa la libreria ply
import ply.yacc as yacc

# importar la lista de tokens
from frida_lexer import tokens

# Defino las reglas del lenguaje MyLittleDuck2017
# se definenen como funcciones p_*
# las reglas se escriben de la forma A : a + b
# ejemplo si la funcion se define como p_A
# no es necesario llamar a esa regla con p_A sino con A

def p_programa(p):
	'programa : PROGRAMA ID COLON programa2'
	#Este mensaje solo se imprime si es valido el archivo
	print('Valid MyLittleDuck2017 file')

def p_programa2(p):
    '''programa2 : vars 
    	| bloque'''

def p_vars(p):
	'vars : VAR vars2'

def p_vars2(p):
	'vars2 : ID vars3'
	
def p_vars3(p):
	'''vars3 : COMA vars2 
		| COLON tipo SEMICOLON vars2
		| COLON tipo SEMICOLON 
		| COLON tipo SEMICOLON bloque 
		| vars2 '''
	
def p_tipo(p):
	'''tipo : TYPEINT 
		| TYPEFLOAT'''

def p_bloque(p):
	'bloque : LBRACE bloque2'
	
def p_bloque2(p):
	'''bloque2 : estatuto bloque2 
		| RBRACE'''
	
def p_estatuto(p):
	'''estatuto : asignacion 
		| condicion 
		| escritura'''

def p_asignacion(p):
	'asignacion : ID ASIGN expresion SEMICOLON'

def p_condicion(p):
	'condicion : IF LPARENTHESIS expresion RPARENTHESIS bloque condicion2'

def p_condicion2(p):
	'''condicion2 : SEMICOLON 
		| ELSE bloque SEMICOLON'''

def p_escritura(p):
	'escritura : PRINT LPARENTHESIS escritura2'

def p_escritura2(p):
	'''escritura2 : expresion escritura3 '''

def p_escritura3(p):
	'''escritura3 : POINT escritura2 
		| RPARENTHESIS SEMICOLON'''

def p_expresion(p):
	'''expresion : exp 
		| exp expresion2'''

def p_expresion2(p):
	'''expresion2 : GTHAN expresion 
		| LTHAN expresion 
		| NOTEQUAL expresion'''

def p_exp(p):
	'''exp : termino 
		| termino exp2'''

def p_exp2(p):
	'''exp2 : PLUS exp 
		| MINUS exp'''
	
def p_termino(p):
	'''termino : factor 
		| factor termino2'''

def p_termino2(p):
	'''termino2 : TIMES termino 
		| DIVIDE termino'''

def p_factor(p):
	'''factor : LPARENTHESIS expresion RPARENTHESIS 
		| varcte 
		| PLUS varcte 
		| MINUS varcte'''

def p_varcte(p):
	'''varcte : ID 
		| INT 
		| FLOAT 
		| STRING'''

# parametros

def p_parametros(p):
	'parametros : tipo COLON ID parametros_loop'

def p_parametros_loop(p):
	'''parametros_loop : COMA parametros
		| empty'''

# lienzo

def p_lienzo(p):
	'lienzo : LIENZO bloque_lienzo'

# Bloque

def p_bloque(p):
	'bloque : LBRACE bloque_loop RBRACE'

def p_bloque_loop(p):
	'''bloque_loop : estatuto bloque_loop
		| empty'''

# Bloque rutina

def p_bloque_rutina(p):
	'LBRACE bloque_rutina_opt bloque_rutina_loop bloque_rutina_opt_2 RBRACE'

def p_bloque_rutina_opt(p):
	'''bloque_rutina_opt : vars 
		| empty'''

def p_bloque_rutina_loop(p):
	'''bloque_rutina_loop : estatuto bloque_rutina_loop 
		| empty'''

def p_bloque_rutina_opt_2(p):
	'''bloque_rutina_opt_2 : RETURN logica
		| empty'''

# Bloque lienzo

def p_bloque_lienzo(p):
	'bloque_lienzo : LBRACE bloque_lienzo_loop RBRACE'

def p_bloque_lienzo_loop(p):
	'''bloque_lienzo_loop : estatuto_lienzo bloque_lienzo_loop 
		| empty'''

# ESTATUTO 

def p_estatuto(p):
	'''estatuto : asignacion 
		| condicion 
		| ciclo 
		| impresion 
		| lectura 
		| accion 
		| llamada'''

def p_estatuto_lienzo(p):
	'''estatuto_lienzo : vars 
		| asignacion 
		| condicion 
		| ciclo 
		| impresion 
		| lectura 
		| accion 
		| llamada'''

# ASIGNACION TODO opt_2?

def p_asigncaion(p):
	'asignacion : ID asignacion_opt ASIGN asignacion_opt_2'

def p_asignacion_opt(p):
	'''asignacion_opt : LBRACKET logica RBRACKET
		| empty'''

# CONDICION

def p_condicion(p):
	'condicion : IF condicion_loop condicion_opt'
def p_condicion_loop(p):
	'condicion_loop : LPARENTHESIS logica RPARENTHESIS bloque condicion_loop_opt'
def p_condicion_loop_opt(p):
	'''condicion_loop_opt : ELIF condicion_loop 
		| empty'''
def p_condicion_opt(p):
	'''condicion_opt : ELSE bloque 
		| empty'''
	
# CICLO

def p_ciclo(p):
	'ciclo : WHILE LPARENTHESIS logica RPARENTHESIS bloque'

# Error rule se tiene que agregar
# Nos indica el error y el numero de linea donde esta
# gracias al contador del lexer
def p_error(p):
	if(p):
		print("Syntax error '" + str(p.value) + "' in input line: " + str(p.lineno))
	else:
		print("Syntax error at the end of the file")

# Crea el parser dandole el estado inicial
parser = yacc.yacc(start='programa')

# Pruebas del analizador lexico y gramatico
def readFile(file):
	file_in = open(file, 'r')
	data = file_in.read()
	file_in.close()
	parser.parse(data)

print('\nArchivos Falla:\n')

readFile("test_fail_1.txt")
readFile("test_fail_2.txt")
readFile("test_fail_3.txt")

print('\n#####################')

print('\nArchivos Exito:\n')
readFile("test_1.txt")
readFile("test_2.txt")
readFile("test_3.txt")
print('\n')

