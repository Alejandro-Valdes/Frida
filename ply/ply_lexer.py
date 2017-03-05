# Jesus Alejandro Valdes Valdes
# A00999044
# importar ply.lex
import ply.lex as lex

# Lista con los nombres de los tokens
# Esta lista sera utilizada por el parser
tokens = [
   'ASIGN',
   'LTHAN',
   'GTHAN',
   'NOTEQUAL',
   'COLON',
   'SEMICOLON',
   'LBRACE',
   'RBRACE',
   'LPARENTHESIS',
   'RPARENTHESIS',
   'POINT',
   'COMA',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'INT',
   'STRING',
   'FLOAT',
   'ID'
]

# Lista de palabras reservadas, siguen siendo tokens
# se identifican como reeservadas para que no se confundan con IDs
reserved = {
  'program' : 'PROGRAMA',
  'var' : 'VAR',
  'print' : 'PRINT',
  'if' : 'IF',
  'else' : 'ELSE',
  'int' : 'TYPEINT',
  'float' : 'TYPEFLOAT'
}

# agrego los valores de las palabras reservadas a la lista de Tokens
tokens += reserved.values()

# Expresiones regulares 'simples'
# simplesn ya que no necesitan de ninguna operacion adicional
# deben de llevar el t_ al inico
t_ASIGN = r'='
t_LTHAN = r'<'
t_GTHAN = r'>'
t_NOTEQUAL = r'<>'
t_COLON = r':'
t_SEMICOLON = r';'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_LPARENTHESIS = r'\('
t_RPARENTHESIS = r'\)'
t_POINT = r'\.'
t_COMA = r'\,'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_INT = r'[\+,-]?\d+'
t_FLOAT = r'[+,-]?[0-9]+\.[0-9]+((E|e)[+,-]?[0-9]+)?'
t_STRING = r'(\'.*\' | \".*\")'
t_ignore = ' \t'

# funciones que atraparan tokens que necesiten funcionalidad extra

# token id revisa que no este en palabras reservadas
# si si esta regresa el valor del token reservado
def t_ID(t):
    r'[a-z](_?[a-zA-Z0-9])*'
    if t.value in reserved:
      if(t.value == 'program'):
        t.lexer.lineno = 0
      t.type = reserved[t.value]
      return t
    t.value = str(t.value)
    return t

# Token que agrega cada nueva linea a un contador
# Util para buscar errores
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling tiene que estar en el lexer de PLY
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Crea el lexer 
lexer = lex.lex()