import ply.lex as lex


class Scanner:
    reserved = {
        'if': 'IF',
        'else': 'ELSE',
        'for': 'FOR',
        'while': 'WHILE',
        'break': 'BREAK',
        'continue': 'CONTINUE',
        'return': 'RETURN',
        'eye': 'EYE',
        'zeros': 'ZEROS',
        'ones': 'ONES',
        'print': 'PRINT'
    }

    tokens = ['ASSIGN',
              'ADD_ASSIGN',
              'SUB_ASSIGN',
              'MULTIPLIES_ASSIGN',
              'DIVIDES_ASSIGN',

              'EQUAL',
              'INEQUAL',

              'LESS',
              'GREATER',
              'LESS_EQUAL',
              'GREATER_EQUAL',

              'PLUS',
              'MINUS',
              'DOT_PLUS',
              'DOT_MINUS',

              'TIMES',
              'DIVIDE',
              'DOT_TIMES',
              'DOT_DIVIDE',

              'APOSTROPHE',

              'COLON',

              'LPAREN',
              'RPAREN',
              'LSQUARE_BRACKET',
              'RSQUARE_BRACKET',
              'LCURLY_BRACKET',
              'RCURLY_BRACKET',
              'COMA',

              'SEMICOLON',

              'ID',
              'INT_NUM',
              'FLOATING_POINT_NUM',
              'STRING'] + list(reserved.values())

    t_ASSIGN = r'='
    t_ADD_ASSIGN = r'\+='
    t_SUB_ASSIGN = r'\-='
    t_MULTIPLIES_ASSIGN = r'\*='
    t_DIVIDES_ASSIGN = r'\/='

    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_DOT_PLUS = r'\.\+'
    t_DOT_MINUS = r'\.\-'

    t_TIMES = r'\*'
    t_DIVIDE = r'\/'
    t_DOT_TIMES = r'\.\*'
    t_DOT_DIVIDE = r'\./'

    t_LESS = r'<'
    t_GREATER = r'>'
    t_LESS_EQUAL = r'<='
    t_GREATER_EQUAL = r'>='
    t_INEQUAL = r'!='
    t_EQUAL = r'=='

    t_APOSTROPHE = '\''

    t_COLON = r'\:'

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LSQUARE_BRACKET = r'\['
    t_RSQUARE_BRACKET = r'\]'
    t_LCURLY_BRACKET = r'\{'
    t_RCURLY_BRACKET = r'\}'
    t_COMA = r','

    t_SEMICOLON = r';'

    # literals = ['+', '-', '*', '/', '(', ')',
    #             '[', ']', '{', '}', ':', '\'', ',', ';']

    t_ignore = '  \t'

    t_ignore_COMMENT = r'\#.*'

    def t_STRING(self, t):
        r'\"[^\"]*\"'
        return t

    def t_FLOATING_POINT_NUM(self, t):
        r'[-+]?(?:\d*\.\d+|\d+\.\d*)(?:[eE][-+]?\d+)?'
        t.value = float(t.value)
        return t

    def t_INT_NUM(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_ID(self, t):
        r'[a-zA-Z_]\w*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    # counting columns and lines
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Compute column.
    #     input is the input text string
    #     token is a token instance
    def find_column(self, input_text, token):
        line_start = input_text.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    def t_error(self, t):
        print("%d: illegal character '%s'" % (t.lineno, t.value[0]))
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, input_text):
        self.lexer.input(input_text)

    def token(self):
        return self.lexer.token()

    def get_data(self):
        return self.lexer.lexdata
