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

# Programa
def p_programa(p):
	'programa : PROGRAMA ID vars_opt'
	#Este mensaje solo se imprime si es valido el archivo
	print('Valid Frida file')

def p_vars_opt(p):
	'''vars_opt : vars 
		| empty'''

def p_rutinas_loop(p):
	'''rutinas_loop : rutinas_loop rutinas 
		| empty '''

# Vars

def p_vars(p):
	'vars : VAR tipo COLON vars_loop'

def p_vars_loop(p):
	'''vars_loop : vars
		| empty
	'''

# Rutinas

def p_rutinas(p):
	'rutinas : RUTINA rutina_opt SEMICOLON ID LPARENTHESIS parametros RPARENTHESIS bloque_rutina rutinas_loop_2'

def p_rutina_opt(p):
	'''rutina_opt : primitivo 
		| figura 
		| VOID'''

def p_rutinas_loop_2(p):
	'''rutinas_loop_2 : rutinas
		| empty '''

# Tipo

def p_tipo(p):
	'tipo : tipo-opt SEMICOLON'

def p_tipo_opt(p):
	'''tipo-opt : tipo-opt-prim 
		| tipo-opt-fig'''

# Tipo Prim

def p_tipo_opt_prim(p):
	'tipo_opt_prim : primitivo ID tipo-opt-prim-2 tipo-opt-prim-loop'

def p_tipo_opt_prim_loop(p):
	'''topo_opt_prin_loop : COMA tipo-opt-prim
		| emtpy'''

def p_tipo_opt_prim_2(p):
	'''tipo_opt_prim_2 : ini_prim 
		| LBRACKET logica RBRACKET tipo-opt-prim-3
		| empty'''

def p_tipo_opt_prim_3(p):
	'''tipo_opt_prim_3 : ini_prim_v 
		| empty '''

# Tipo fig

def p_tipo_opt_fig(p):
	'tipo_opt_fig : figura ID tipo_opt_fig_2'

def p_tipo_opt_fig_loop(p):
	'''tipo_opt_fig_loop : COMA tipo_opt_fig
		| empty'''

def p_tipo_opt_fig_2(p):
	'''tipo_opt_fig_2 : ini_fgra 
		| LBRACKET logica RBRACKET tipo_opt_fig_3 
		| empty '''

def p_tipo_opt_fig_3(p):
	'''tipo_opt_fig_3 : ini_fgra_v 
		| empty'''

# Inicializacion de valores primitivos

def p_ini_prim(p):
	'ini_prim : ASIGN logica'

# Inicializacion de arreglos con valores primarios

def p_ini_prim_v(p):
	'ini_prim_v : ASIGN LBRACE logica ini_prim_v_loop RBRACE'

def p_ini_prim_v_loop(p):
	'''ini_prim_v-loop : COMA logica ini_prim_v_loop 
		| empty'''

# Inicializacion de figuras

def p_ini_fgra(p):
	'ini_fgra : ASIGN fgra_nva'

# Inicitalizacion de arreglos de figuras

def p_ini_fgra_v(p):
	'''ini_fgra_v : COMA logica init_fgras_v_loop
		| emtpy'''

def p_fgra_nva(p):
	'''fgra_nva : nuevo fgra_atr
		| empty'''

def p_fgra_atr(p):
	'''fgra_atr : pincel LPARENTHESIS fgra_atr_end 
		| cuadrado LPARENTHESIS exp COMA fgra_atr_end 
		| circulo LPARENTHESIS exp COMA fgra_atr_end
		| rectangulo LPARENTHESIS exp COMA exp COMA fgra_atr_end
		| triangulo LPARENTHESIS exp COMA exp COMA exp COMA exp COMA fgra_atr_end'''

def p_fgra_atr_end(p):
	'fgra_atr_end : exp COMA exp COMA color RPARENTHESIS'

# Data types

def p_primitivo(p):
	'''primitivo : TYPEINT
		| TYPEDOUBLE
		| TYPEBOOL
		| TYPESTRING'''

def p_figura(p):
	'''figura : PINCEL
		| CUADRDO
		| RECTANGULO
		| CIRCULO
		| TRIANGULO'''

def p_cte(p):
	'''cte : STRING 
		| INT
		| DOUBLE
		| BOOL'''	

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




def p_empty(p):
    'empty :'
    pass

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

#readFile("test_fail_1.txt")
#readFile("test_fail_2.txt")
#readFile("test_fail_3.txt")

#print('\n#####################')

#print('\nArchivos Exito:\n')
readFile("test_1.txt")
#readFile("test_2.txt")
#readFile("test_3.txt")
print('\n')

