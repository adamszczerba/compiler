import ply.lex as lex
import sys

reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'for' : 'FOR',
    'while' : 'WHILE',
    'break' : 'BREAK',
    'continue' : 'CONTINUE',
    'return' : 'RETURN',
    'eye' : 'EYE',
    'zeros' : 'ZEROS',
    'ones' : 'ONES',
    'print' : 'PRINT'
}

tokens = ['DOT_PLUS',
          'DOT_MINUS',
          'DOT_TIMES',
          'DOT_DIVIDE',

          'ASSIGN',
          'ADD_ASSIGN',
          'SUB_ASSIGN',
          'MULTIPLIES_ASSIGN',
          'DIVIDES_ASSIGN',

          'LESS',
          'GREATER',
          'LESS_EQUAL',
          'GREATER_EQUAL',
          'INEQUAL',
          'EQUAL',

          'ID',
          'INT_NUM',
          'FLOATING_POINT_NUM',
          'STRING',
          'COMMENT'] + list(reserved.values())


t_DOT_PLUS = r'\.\+'
t_DOT_MINUS = r'\.\-'
t_DOT_TIMES = r'\.\*'
t_DOT_DIVIDE = r'\./'

t_ASSIGN = r'='
t_ADD_ASSIGN = r'\+='
t_SUB_ASSIGN = r'\-='
t_MULTIPLIES_ASSIGN = r'\*='
t_DIVIDES_ASSIGN = r'/='

t_LESS = r'<'
t_GREATER = r'>'
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_INEQUAL = r'!='
t_EQUAL = r'=='


literals = ['+', '-', '*', '/', '(', ')',
            '[', ']', '{', '}', ':', '\'', ',', ';']

t_ignore = '  \t'


def t_COMMENT(t):
    r'\#.*'
    pass

def t_STRING(t):
    r'\"[^\"]*\"'
    return t

def t_FLOATING_POINT_NUM(t):
    r'( ([0-9]+\.[0-9]*[E][0-9]+) | (\.[0-9]*[E][0-9]+) | ([0-9]+\.[0-9]*) | (\.[0-9]+) )'
    t.value = float(t.value)
    return t

def t_INT_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value, 'ID')
    return t

# counting columns and lines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Compute column.
 #     input is the input text string
 #     token is a token instance
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

def t_error(t):
    print("line %d: illegal character '%s'" %(t.lineno, t.value[0]) )
    t.lexer.skip(1)

lexer = lex.lex()

