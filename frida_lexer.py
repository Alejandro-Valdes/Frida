#Autor: Alejandro Valdes y Evan Juarez
#Archivo que funcionra para al analisis lexico de Frida
#usa la libreria ply

import ply.lex as lex

#lista con los nombres de tokens a utilizar por el analizador sintaxico

tokens = [
	'ASSIGN',
	'GTHAN',
	'LTHAN',
	'GETHAN',
	'LETHAN',
	'EQUAL',
	'NOTEQUAL',
	'COLON',
	'SEMICOLON',
	'LBRACE',
	'RBRACE',
	'LPARENTHESIS',
   	'RPARENTHESIS',
   	'LBRACKET',
   	'RBRACKET',
   	'POINT',
   	'COMA',
   	'PLUS',
   	'MINUS',
   	'TIMES',
   	'DIVIDE',
   	'INT',
   	'DOUBLE',
   	'STRING',
   	'COMMENT',
   	'CTEFUNCION',
   	'ID'
]

#lista con las palabras reservadas para Frida

reserved = {
	'programa' : 'PROGRAMA',
	'variable' : 'VAR',
	'lienzo' : 'MAIN',
	'si' : 'IF',
	'sino' : 'ELSE',
	'sino_pero' : 'ELIF',
	'y' : 'AND',
	'o' : 'OR',
	'mientras' : 'WHILE',
	'rutina' : 'RUTINA',
	'imprimir' : 'PRINT',
	'leer' : 'READ',
	'entero' : 'TYPEINT',
	'decimal' : 'TYPEDOUBLE',
	'bool' : 'TYPEBOOL',
	'cadena' : 'TYPESTRING',
	'pincel' : 'PINCEL',
	'cuadrado' : 'CUAD',
	'rectangulo' : 'RECT',
	'circulo' : 'CIRC',
	'triangulo' : 'TRIANG',
	'nuevo' : 'NUEVO',
	'void' : 'VOID',
	'regresa' : 'RETURN',
	'mover' : 'MOVEA',
	'gira' : 'ROTATE',
	'crece' : 'GROW',
	'grosor' : 'THICK',
	'elimina' : 'REMOVE',
	'borrar' : 'REMOVEFIG',
	'relleno' : 'FILL', 
	'color' : 'COLOR',
	'desplazar' : 'DISPLACE',
	'pinta' : 'PAINT',
	'arco' : 'ARC',
	'verdadero' : 'TRUE',
	'falso' : 'FALSE'
}

#la lista de valores de las palabras reservadas se agregan a la lista de tokens.
tokens += reserved.values()

#Expresiones regulares simples,
#no necesitan operaciones adicionales.
#necesitan la t_

t_ASSIGN = r'='
t_GTHAN = r'<'
t_LTHAN = r'>'
t_GETHAN = r'>='
t_LETHAN = r'<='
t_EQUAL = r'=='
t_NOTEQUAL = r'!='
t_COLON = r':'
t_SEMICOLON = r';'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPARENTHESIS = r'\('
t_RPARENTHESIS = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_POINT = r'\.'
t_COMA = r'\,'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_INT = r'-?(\d+)'
t_DOUBLE = r'-?(\d+(\.\d+))'
t_TRUE = r'verdadero'
t_FALSE = r'falso'
t_STRING = r'("[^".]*")|(\'[^\'.]*\')'

t_ignore_COMMENT = r'\/\*(\*(?!\/)|[^*])*\*\/'

t_CTEFUNCION = r'\"(([x]|[0-9]+(.[0-9]+)?))+([+\-*/^]([xX]|([0-9]+(.[0-9]+)?)+))+\"'
t_ignore = ' \t'

#Funciones para tokens que necesitan funcionalidad extra

#TODO checar si faltan funciones

# token id revisa que no este en palabras reservadas
# si si esta regresa el valor del token reservado
def t_ID(t):
    r'[a-z](_?[a-zA-Z0-9])*'
    if t.value in reserved:
      if(t.value == 'programa'):
        t.lexer.lineno = 1
      t.type = reserved[t.value]
      return t
    t.value = str(t.value)
    return t

# Token que agrega cada nueva linea a un contador
# Util para buscar errores
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#Manejador de errores 
def t_error(t):
	print("Caracter ilegal '%s'" % t.value[0])
	print (t.lexer.lineno)
	t.lexer.skip(1)

#crea el lexer
lexer = lex.lex();