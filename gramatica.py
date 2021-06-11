'''
gramatica de JPR
'''
from TS.Exception import Excepcion
reservadas = {
    'var': 'RVAR', 'int': 'RINT', 'double': 'RDOUBLE', 'boolean': 'RBOOL', 'char': 'RCHAR', 'string': 'RSTRING',
    'null': 'RNULL',
    'main': 'RMAIN', 'read': 'RREAD', 'print': 'RPRINT', 'continue': 'RCONTINUE', 'return': 'RRETURN', 'new': 'RNEW',
    'lenght': 'RLENGHT', 'truncate': 'RTRUNCATE', 'round': 'RROUND', 'tipeof': 'RTIPEOF', 'func': 'RFUNC',
    'switch': 'RSWITCH', 'case': 'RCASE', 'default': 'RDEFAULT', 'break': 'RBREAK',
    'toLower': 'RTOLOWER', 'toUpper': 'RTOUPPER',
    'while': 'RWHILE', 'for': 'RFOR',
    'if': 'RIF', 'else': 'RELSE'
}
tokens = [
     'IGUAL', 'DIFERENTE', 'MENOR', 'MAYOR', 'MENIGUAL', 'MAYIGUAL', 'IGUALIGUAL',
     'MAS', 'MENOS', 'MASMAS', 'MENOSMENOS', 'POR', 'DIV', 'MODULO', 'POT',
     'PTCOMA', 'DOSPUNTOS', 'COMA', 'COMILLASIMPLE', 'COMILLADOBLE',
     'DECIMAL', 'ENTERO', 'CADENA', 'BOOL', 'CHAR', 'ID',
     'PARA', 'PARC', 'CORA', 'CORC', 'LLAVEA', 'LLAVEC',
     'COMENTARIO', 'COMENTARIOMULTI',
     'OR', 'AND', 'NOT'
 ] + list(reservadas.values())

# set value of TOKENS
t_IGUAL = r'='
t_DIFERENTE = r'=\!'
t_MENOR = r'<'
t_MAYOR = r'>'
t_MENIGUAL = r'<='
t_MAYIGUAL = r'>='
t_IGUALIGUAL = r'=='
t_MAS = r'\+'
t_MENOS = r'-'
t_MASMAS = r'\+\+'
t_MENOSMENOS = r'--'
t_POR = r'\*'
t_DIV = r'/'
t_MODULO = r'%'
t_POT = r'\*\*'
t_PTCOMA = r';'
t_DOSPUNTOS = r':'
t_COMA = r','
t_COMILLASIMPLE = r'\''
t_COMILLADOBLE = r'\"'
t_PARA = r'\('
t_PARC = r'\)'
t_CORA = r'\['
t_CORC = r'\]'
t_LLAVEA = r'\{'
t_LLAVEC = r'\}'
t_OR = r'\|\|'
t_AND = r'&&'
t_NOT = r'\!'

# Comentario de múltiples líneas #* .. *#
def t_COMENTARIOMULTI(t):
    r'\#\*(.|\n)*?\*\#'
    t.lexer.lineno += t.value.count('\n')
# Comentario simple // ...
def t_COMENTARIO(t):
    r'\#.*\n?'
    t.lexer.lineno += 1
def t_BOOL(t):
    r'(true|false)'
    if t.value == "true":
        t.value = True
    elif t.value == "false":
        t.value = False
    return t
def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t
def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t
def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value.lower(), 'ID')
    return t
def t_CADENA(t):
    r'\"((\\\")|.|\n)*?\"'
    t.value = t.value[1:-1]  # remuevo las comillas
    t.value = t.value.replace('\\n', '\n')
    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace('\\\'', '\'')
    t.value = t.value.replace('\\\"', '\"')
    return t
def t_CHAR(t):
    r'(\'(\\(n|t|\\|\"|\')|.)\')'
    t.value = t.value[1:-1]  # remuevo las comillas
    t.value = t.value.replace('\\n', '\n')
    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace('\\\'', '\'')
    t.value = t.value.replace('\\\"', '\"')
    return t
# Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    errores.append(Excepcion("Lexico","Error léxico." + t.value[0] , t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()



# Definición de la gramática

#Abstract
from Abstract.instruccion import Instruccion
from Instrucciones.Imprimir import Imprimir
from Expresiones.Primitivos import Primitivos
from TS.Tipo import OperadorAritmetico, TIPO
from Expresiones.Aritmetica import Aritmetica

def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_instrucciones_instruccion(t) :
    'instrucciones    : instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]
    
#///////////////////////////////////////INSTRUCCIONES//////////////////////////////////////////////////

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion'
    if t[1] == "":
        t[0] = []
    else:    
        t[0] = [t[1]]

#///////////////////////////////////////INSTRUCCION//////////////////////////////////////////////////

def p_instruccion(t) :
    '''instruccion      : print'''
    t[0] = t[1]

def p_instruccion_error(t):
    'instruccion        : error PTCOMA'
    errores.append(Excepcion("Sintáctico","Error Sintáctico." + str(t[1].value) , t.lineno(1), find_column(input, t.slice[1])))
    t[0] = ""
#///////////////////////////////////////IMPRIMIR//////////////////////////////////////////////////

def p_imprimir(t) :
    'print     : RPRINT PARA expresion PARC fin'
    t[0] = Imprimir(t[3], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////EXPRESION//////////////////////////////////////////////////

def p_expresion_binaria(t):
    '''
    expresion : expresion MAS expresion
            | expresion MENOS expresion
            | expresion POR expresion
			| expresion DIV expresion
			| expresion POT expresion
			| expresion MODULO expresion
    '''
    if t[2] == '+':
        t[0] = Aritmetica(OperadorAritmetico.MAS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':
        t[0] = Aritmetica(OperadorAritmetico.MENOS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*':
        t[0] = Aritmetica(OperadorAritmetico.POR, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '/':
        t[0] = Aritmetica(OperadorAritmetico.DIV, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '**':
        t[0] = Aritmetica(OperadorAritmetico.POT, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '%':
        t[0] = Aritmetica(OperadorAritmetico.MOD, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))

def p_expresion_agrupacion(t):
    'expresion : PARA expresion PARC'
    t[0] = t[2]
def p_expresion_entero(t):
    '''expresion : ENTERO'''
    t[0] = Primitivos(TIPO.ENTERO,t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_decimal(t):
    '''expresion : DECIMAL'''
    t[0] = Primitivos(TIPO.DECIMAL, t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_cadena(t):
    '''expresion : CADENA'''
    t[0] = Primitivos(TIPO.CADENA,t[1], t.lineno(1), find_column(input, t.slice[1]))
def p_expresion_char(t):
    '''expresion : CHAR'''
    t[0] = Primitivos(TIPO.CHARACTER,t[1], t.lineno(1), find_column(input, t.slice[1]))
def p_expresion_bool(t):
    '''expresion : BOOL'''
    t[0] = Primitivos(TIPO.BOOLEANO,t[1], t.lineno(1), find_column(input, t.slice[1]))
# --------------- fin --------------
def p_fin(t):
    '''
    fin : PTCOMA
        | 
    '''

import ply.yacc as yacc
parser = yacc.yacc()

input = ''

def getErrores():
    return errores

def parse(inp) :
    global errores
    global lexer
    global parser
    errores = []
    lexer = lex.lex()
    parser = yacc.yacc()
    global input
    input = inp
    return parser.parse(inp)

#INTERFAZ

f = open("./entrada.txt", "r")
entrada = f.read()

from TS.Arbol import Arbol
from TS.TablaSimbolos import TablaSimbolos

instrucciones = parse(entrada) #ARBOL AST
ast = Arbol(instrucciones)
TSGlobal = TablaSimbolos()
ast.setTSglobal(TSGlobal)
for error in errores:                   #CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
    ast.getExcepciones().append(error)
    ast.updateConsola(error.toString())

for instruccion in ast.getInstrucciones():      # REALIZAR LAS ACCIONES
    value = instruccion.interpretar(ast,TSGlobal)
    if isinstance(value, Excepcion) :
        ast.getExcepciones().append(value)
        ast.updateConsola(value.toString())

print(ast.getConsola())